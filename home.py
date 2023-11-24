import streamlit as st
import random
import time
import plotly.express as px
import pandas as pd
from llm_helper import model

st.title("Child development consultants :frog:")


################################### FUNCTION GENERATE RESPONSE ###################################
def generate_response(prompt):
    # Initial Prompt for system, assitant, user
    system_prompt = "You are a child development doctor. Your goal is to score child developmental milestones by standard"
    ai_prompt = prompt_dict[st.session_state.question_order]['question']
    user_prompt = prompt


    #"I spent the afternoon with Sarah, a 6-year-old who loves building with LEGO bricks. We decided to collaborate on constructing a miniature city, discussing our ideas and making joint decisions about the design. It was fascinating to see her creativity at work, and our shared attention to detail made the activity more enjoyable."

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Using model
            #callback, score = llm.model(system_prompt, ai_prompt, user_prompt)
            callback = f"""
            Tokens Used: {st.session_state.question_order} \nPrompt Tokens: {st.session_state.llm_is_processing} \nCompletion Tokens: 22 \nSuccessful Requests: 1 \nTotal Cost (USD): $0.004064
            """
            score = """
            content="I'm sorry, I didn't understand your response. Could you please provide more information or clarify your answer?"
            """

            #time.sleep(1.1)

            # Store (log + score)
            st.session_state.open_ai_call_back.append(callback)
            st.session_state.open_ai_score.append(score)

            # Unlock session for assitant to talk
            st.session_state.llm_is_processing = False





    # To slow down for better gui
    time.sleep(0.5)

    # Rerun for asking next question
    st.rerun()




################################### INITIAL LLM ###################################
llm = model()

# Get list of dict data
prompt_dict = llm.prompt_data



################################### INITIAL session_state ###################################
# Initialize question order
if "question_order" not in st.session_state:
    st.session_state.question_order = 0

# Choose prompt example to be prefix of user input
if st.session_state.question_order < 30:
    llm.cut_data_fit_input_limit(0,30)
else:
    llm.cut_data_fit_input_limit(30,75)

# Initial wait for llm processing
if "llm_is_processing" not in st.session_state:
    st.session_state.llm_is_processing = False

# Initial log
if "open_ai_call_back" not in st.session_state:
    st.session_state.open_ai_call_back = []
    
# Initial score
if "open_ai_score" not in st.session_state:
    st.session_state.open_ai_score = []

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


################################### CHAT SECTION ###################################

########## DISPLAY
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

########## USER CHAT
# Accept user input
if prompt := st.chat_input("Please answer the question above"): # User semi-trasparent input
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Lock session for llm processing
    st.session_state.llm_is_processing = True

########## ASSITANT CHAT (Ask question)
# Avoid assitant talk before llm process
if not st.session_state.llm_is_processing:
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Max of quesiton_order is 75
        if st.session_state.question_order < len(prompt_dict):
            assistant_response = prompt_dict[st.session_state.question_order]['question']
        else:
            assistant_response = "It's the end of consulation!!"

        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response) 
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # question_order +1 (next question)
    st.session_state.question_order += 5



################################### GENERATE RESPONSE ###################################
# Avoid llm input null string
if st.session_state.llm_is_processing or st.session_state.question_order >= len(prompt_dict):
    generate_response(prompt)





################################### PROGRESS BAR ###################################
quesiton_progress_bar = st.progress(0, text='run')

display_loading_text_numerator = int(st.session_state.question_order/5)
display_loading_text_denominator = int(len(prompt_dict)/5)
display_loading_bar = float(display_loading_text_numerator/display_loading_text_denominator)

quesiton_progress_bar.progress(display_loading_bar, text=f'{display_loading_text_numerator}/{display_loading_text_denominator}')






################################### SIDE BAR ###################################


# with st.sidebar:
#     st.caption('Last Updated on March 13th, 2023')

#     col1, col2, col3 = st.columns(3)
#     col1.metric("Cognitive", "83 %", "1.2 %")
#     col2.metric("Social", "58 %", "-8%")
#     col3.metric("Emotional", "93%", "4%")


#     df = pd.DataFrame(dict(
#         r=[1, 5, 2, 2, 3],
#         theta=['cognitive','physical','emotional',
#             'social', 'mind']))
#     fig = px.line_polar(df, r='r', theta='theta', line_close=True)
#     st.plotly_chart(fig, use_container_width=True)
