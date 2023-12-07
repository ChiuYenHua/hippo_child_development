import pandas as pd
from langchain.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
import streamlit as st

class model():
    def __init__(self, csv_path='child_development_standard.csv', openai_api_key=st.secrets["open_ai_key"]):
        self.prompt_data = self.read_csv_to_llm_input(csv_path)
        self.cutted_prompt_data = ''
        self.openai_api_key=openai_api_key

    # Read csv + Convert into llm input
    def read_csv_to_llm_input(self, csv_path):
        # Read csv
        df = pd.read_csv(csv_path)

        # Remove 'Example: ' in example
        df['Example'] = df['Example'].apply(lambda x: x[9:])

        # Rename columns
        df = df.rename({'table': 'type', 'Question': 'question', 'Score': 'score', 'Example': 'answer', 'Evaluation': 'evaluation'},
                            axis='columns')

        # Create list of dict from dataframe
        prompt_example_all = df.to_dict('records')

        return prompt_example_all
    
    # Cut data to fit GPT3.5 input limit
    def cut_data_fit_input_limit(self, first_cutted_index, second_cutted_index):
        self.cutted_prompt_data = self.prompt_data[first_cutted_index:second_cutted_index]

    # Model:
    # system_prompt -> prompt for system to briefly illustrate the goal
    # ai_prompt     -> prompt for every question asked by ai
    # user_prompt   -> prompt for user input
    def model_for_score(self, system_prompt, ai_prompt, user_prompt):
        # This is a prompt template used to format each individual example.
        example_prompt = ChatPromptTemplate.from_messages(
            [
                ('ai', 'question_type: {type}, evaluation_standard: {evaluation} ,question: {question}'),
                ('human', '{answer}'),
                ('ai', 'Score for this answer will be: {score}') ,
            ]
        )

        print(f'exapmle_prompt: {example_prompt}')
        print(f'examples: {self.cutted_prompt_data}')

        few_shot_prompt = FewShotChatMessagePromptTemplate(
            example_prompt=example_prompt,
            examples=self.cutted_prompt_data,
        )

        # Make final prompt and use it for model
        final_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                few_shot_prompt,
                ("ai", ai_prompt),
                ("human", "{input}"),
            ]
        )

        # Model
        chain = final_prompt | ChatOpenAI(openai_api_key=self.openai_api_key, 
                                        model_name="gpt-3.5-turbo",
                                        temperature=0)

        ## Record history
        open_ai_callback = ''
        open_ai_score = 0

        ## Tracking token usage
        with get_openai_callback() as cb:
            open_ai_score = chain.invoke({"input": user_prompt})
            open_ai_callback = cb

        return open_ai_callback, open_ai_score
    
    def model_for_chat(self, system_prompt, messages):
        # Prompt must include all chat history
        chat_history = []
        chat_history.append(("system", system_prompt))

        # Put all chat history in prompt
        for every_chat in messages:
            if every_chat['role'] == 'assistant':
                chat_history.append(("ai", every_chat['content']))
            else:
                chat_history.append((every_chat['content']))

        chat_template = ChatPromptTemplate.from_messages(chat_history)

        # Model
        chain = chat_template | ChatOpenAI(openai_api_key=st.secrets["open_ai_key"], 
                                        model_name="gpt-3.5-turbo",
                                        temperature=1)

        ## Tracking token usage
        with get_openai_callback() as cb:
            open_ai_response = chain.invoke({"input": '123'})
            open_ai_callback = cb

        return open_ai_callback, str(open_ai_response)[9:-1]


