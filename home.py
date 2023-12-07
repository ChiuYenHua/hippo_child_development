import streamlit as st
import time
from llm_helper import model
import pandas as pd
import plotly.express as px
import json
import random



################################### FUNCTION GENERATE RESPONSE ###################################
def generate_response(prompt):
    # Initial Prompt for system, assitant, user
    system_prompt = "You are a child development doctor. Your goal is to help parents figure out child developmental milestones. Be humorous. Don't response more than 3 sentences. Talk like chat with friends!!"
    ai_prompt = prompt_dict[st.session_state.question_order]['question']
    user_prompt = prompt

    #"I spent the afternoon with Sarah, a 6-year-old who loves building with LEGO bricks. We decided to collaborate on constructing a miniature city, discussing our ideas and making joint decisions about the design. It was fascinating to see her creativity at work, and our shared attention to detail made the activity more enjoyable."

    # Using model
    #callback, score = llm.model_for_score(system_prompt, ai_prompt, user_prompt)
    callback, response = llm.model_for_chat(system_prompt, st.session_state.messages)

    # Store (log + score)
    st.session_state.open_ai_call_back.append(callback)
    st.session_state.open_ai_response.append(response)

    return response

def generate_score():
    # Initial Prompt for system, assitant, user
    system_prompt = "You are a child development doctor. Your goal is to give a score from 1 to 5 by user's sentence"
    ai_prompt = prompt_dict[st.session_state.question_order]['question']

    # Avoid user no input
    try:
        user_prompt = st.session_state.messages[1]['content']

        #"I spent the afternoon with Sarah, a 6-year-old who loves building with LEGO bricks. We decided to collaborate on constructing a miniature city, discussing our ideas and making joint decisions about the design. It was fascinating to see her creativity at work, and our shared attention to detail made the activity more enjoyable."

        # Using model
        _, score = llm.model_for_score(system_prompt, ai_prompt, user_prompt)
        score = int(str(score).split(' ')[-1][:-1])

        return score

    except:
        return 0




################################### INITIAL LLM ###################################
llm = model()

# Get list of dict data
prompt_dict = llm.prompt_data

# Compliment sentences
compliment_sentence = ["Your child's curiosity reflects your nurturing",
                        'Kudos on raising an empathetic individual',
                        "Your focus on learning shines through your child's knowledge",
                        'Their resilience speaks volumes about your parenting',
                        'Your support has built their self-confidence',
                        "You've fostered a positive self-image admirably",
                        'Values you instilled shine in their integrity',
                        'Your nurturing has developed their emotional intelligence',
                        'Social adeptness is a credit to your guidance',
                        'Your encouragement fuels their creativity',
                        'Work ethic and determination reflect your values',
                        'Independence at home bred responsibility',
                        'Effective communication stems from your openness',
                        'Your encouragement sparked their curiosity',
                        'Stability at home nurtures their emotional security',
                        'Respect for others mirrors your teachings',
                        'Balanced discipline yields a respectful individual',
                        'Generosity and kindness stem from your example',
                        'Responsibility is a reflection of your guidance',
                        'Active involvement shaped their well-being.']

icon = ['🎉', '😍', '🔥', '🤖', '🚨']


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
if "user_chat_time" not in st.session_state:
    st.session_state.user_chat_time = True

# Initial log
if "open_ai_call_back" not in st.session_state:
    st.session_state.open_ai_call_back = []
    
# Initial response
if "open_ai_response" not in st.session_state:
    st.session_state.open_ai_response = []

# Initial score
if "open_ai_score" not in st.session_state:
    st.session_state.open_ai_score = []

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize for one question chat room
if "is_chatting" not in st.session_state:
    st.session_state.is_chatting = False

# Initialize for Consulation or Result
if "in_consulation" not in st.session_state:
    st.session_state.in_consulation = True


############################ CONFIG ###################################
# Set page config
st.set_page_config(
        page_title="Child Development",
        page_icon="log.png",
        layout="centered",
    )

# Title
if st.session_state.in_consulation == True:
    col1,col2=st.columns([8,1])
    with col1:
        st.title("Child development consultants")
    with col2:
        st.image('logo.png',width=100)
else:
    col1,col2=st.columns([6,1])
    with col1:
        st.title("Child development report")
    with col2:
        st.image('logo.png',width=100)

# Consulatino or Show results
if st.session_state.in_consulation:
    ################################### CHAT SECTION ###################################
    if not st.session_state.is_chatting:
        # If here, then user wants next question, and keep chat until the next question
        st.session_state.is_chatting = True

        ########## ASSITANT CHAT (Ask question)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            assistant_response = prompt_dict[st.session_state.question_order]['question']

            # Simulate stream of response with milliseconds delay
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response) 
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Reload again
        st.rerun()

    ########## DISPLAY
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    ########## USER CHAT
    # Accept user input
    if st.session_state.user_chat_time:
        prompt = st.chat_input("Please answer the question above")
        if prompt:
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Turn for assitant to talk
            st.session_state.user_chat_time = False

    ########## ASSITANT GENERATE RESPONSE (Keep respond user)
    #Avoid assitant talk before llm process
    if not st.session_state.user_chat_time:
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                message_placeholder = st.empty()
                full_response = ""
                
                # Generate response
                assistant_response = generate_response(prompt)

                # Simulate stream of response with milliseconds delay
                for chunk in assistant_response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response) 

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Turn for user to chat
        st.session_state.user_chat_time = True

        
    # Next question button or end button
    if st.session_state.question_order == len(prompt_dict)-5:
        if st.button('End consulation !!!'):
            st.balloons()
            time.sleep(1.8)

            # Turn to show results mode
            st.session_state.in_consulation = False

            # Store chat history
            with open(f'chat_history/chat_history_No.{int(st.session_state.question_order/5)}.json', 'w') as file:
                json.dump(st.session_state.messages, file)

            # Score prompt on single question
            st.session_state.open_ai_score.append({'no': st.session_state.question_order/5, 'score': generate_score()})

            # Rerun
            st.rerun()
    else:
        if st.button('Next question'):
            # Store chat history
            with open(f'chat_history/chat_history_No.{int(st.session_state.question_order/5)}.json', 'w') as file:
                json.dump(st.session_state.messages, file)

            # Score prompt on single question
            st.session_state.open_ai_score.append({'no': st.session_state.question_order/5, 'score': generate_score()})
                
            # Reset message chat history
            st.session_state.messages = []

            # Change is_chatting = False
            st.session_state.is_chatting = False

            # Question_order +1 (next question)
            st.session_state.question_order += 5

            # Compliment user, by sent notfication
            st.toast(random.choice(compliment_sentence))
            time.sleep(.5)
            st.toast(random.choice(compliment_sentence), icon=random.choice(icon))
            time.sleep(1.5)

            # Rerun
            st.rerun()

    ################################### PROGRESS BAR ###################################
    quesiton_progress_bar = st.progress(0, text='run')

    display_loading_text_numerator = int(st.session_state.question_order/5)+1
    display_loading_text_denominator = int(len(prompt_dict)/5)
    display_loading_bar = float(display_loading_text_numerator/display_loading_text_denominator)

    quesiton_progress_bar.progress(display_loading_bar, text=f'{display_loading_text_numerator}/{display_loading_text_denominator}')

else:
    # Config font size
    st.markdown("""
                <style>
                .detail_score_of_question {
                    font-size:18px !important;
                }

                .type_score_of_question {
                    font-size:20px !important;
                }

                p {
                    font-size:16px !important;
                }
                </style>
                """, unsafe_allow_html=True)

    ############################ Deal Score ###########################
    score_every_question = []
    for index, i in enumerate(st.session_state.open_ai_score):
        if index==i['no']:
            score_every_question.append(i['score'])
        else:
            score_every_question.append(0)

    ############################ SHOW TOTAL SCORE ############################
    # Show total score
    with st.container():
        st.header(f'Score: {sum(score_every_question)/75*100:.3} %', divider='rainbow')

    with st.empty():
        st.write('')

    with st.container():
        ############################ SHOW TYPE SCORE ############################
        for i in range(int(len(prompt_dict)/15)):
            # Create a two-column layout
            col1, col2, col3 = st.columns([3, 1, 3]) # this will just call methods directly in the returned objects

            q1_score = score_every_question[i*3]/5*100
            q2_score = score_every_question[i*3+1]/5*100
            q3_score = score_every_question[i*3+2]/5*100

            # Type detail score
            with col1:
                with st.expander(prompt_dict[i*15]['type'][1:-24]):
                    st.markdown(f'<p class="detail_score_of_question">Question 1:  {q1_score}%</p>', unsafe_allow_html=True)
                    st.markdown(f'<p class="detail_score_of_question">Question 2:  {q2_score}%</p>', unsafe_allow_html=True)
                    st.markdown(f'<p class="detail_score_of_question">Question 3:  {q3_score}%</p>', unsafe_allow_html=True)

            # Type score
            with col2:
                st.markdown(f'<p class="type_score_of_question">{(q1_score+q2_score+q3_score)/3:.3} %</p>', unsafe_allow_html=True)

            # with col3:
            #     st.write('dfdfbterbrefgvregbvrefbterbrefgvregbvrefbterbrefgvregbvrefbterbrefgvregbvregvegbvregbvebgvfdfdf')



    # Seperate line
    '-' * 10

    ############################ SHOW RADAR PLOT ############################
    type_list = []
    for i in range(len(score_every_question)):
        if i%3==0:
            type_list.append((score_every_question[i]+score_every_question[i+1]+score_every_question[i+2])/3)

    df = pd.DataFrame(dict(
        r=type_list,
        theta=[prompt_dict[i]['type'][1:-24] for i in range(len(prompt_dict)) if i%15==0]))
    
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    fig.update_layout(font=dict(size=16))
    st.plotly_chart(fig, use_container_width=True)


    ############################ DO AGAIN BUTTON ############################
    if st.button('Do again !'):
        # Reset
        st.session_state.question_order = 0
        # Initial wait for llm processing
        st.session_state.user_chat_time = True
        # Initial log
        st.session_state.open_ai_call_back = []
        # Initial score
        st.session_state.open_ai_response = []
        # Initialize chat history
        st.session_state.messages = []
        # Initialize for one question chat room
        st.session_state.is_chatting = False
        # Initialize for Consulation or Result
        st.session_state.in_consulation = True

        # Rerun
        st.rerun()


################################### SIDE BAR (Store hisroty)###################################


with st.sidebar:
    col1,col2,col3 = st.columns([3,10,1])
    with col2:
        st.image('logo.png', width=200)

    question = [str(i+1) + '. ' + prompt_dict[i*5]['question'] for i in range(int(len(prompt_dict)/5))]
    option = st.selectbox(
        'Chat history',
        question)
    
    ########## DISPLAY
    # Display chat messages from history
    question_no = int(option.split('.')[0])-1

    with open(f'chat_history/chat_history_No.{question_no}.json', 'r') as f:
        for message in json.loads(f.read()):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


    
