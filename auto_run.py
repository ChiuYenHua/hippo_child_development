import streamlit as st
import time
from llm_helper import model
import pandas as pd
import plotly.express as px
import random
from streamlit_extras.metric_cards import style_metric_cards

# Set page config
st.set_page_config(
        page_title="Child Development",
        page_icon="baby.png",
        layout="centered",
    )

# Title
st.title("Child development consultants :frog:")


################################### FUNCTION GENERATE RESPONSE ###################################
def generate_response(prompt):
    # Initial Prompt for system, assitant, user
    system_prompt = "You are a child development doctor. Your goal is to score child developmental milestones by standard"
    ai_prompt = prompt_dict[st.session_state.question_order]['question']
    user_prompt = prompt


    #"I spent the afternoon with Sarah, a 6-year-old who loves building with LEGO bricks. We decided to collaborate on constructing a miniature city, discussing our ideas and making joint decisions about the design. It was fascinating to see her creativity at work, and our shared attention to detail made the activity more enjoyable."

        
    # Using model
    #callback, score = llm.model(system_prompt, ai_prompt, user_prompt)
    callback = f"""
    Tokens Used: {st.session_state.question_order} \nPrompt Tokens: {st.session_state.llm_is_processing} \nCompletion Tokens: 22 \nSuccessful Requests: 1 \nTotal Cost (USD): $0.004064
    """
    score = """
    content="I'm sorry, I didn't understand your response. Could you please provide more information or clarify your answer?"
    """

    time.sleep(1.1)

    # Store (log + score)
    st.session_state.open_ai_call_back.append(callback)
    st.session_state.open_ai_score.append(score)






    # To slow down for better gui
    time.sleep(0.3)

    # Rerun for asking next question
    #st.rerun()




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

# Initial stop
if "stop" not in st.session_state:
    st.session_state.stop = False


################################### CHAT SECTION ###################################

########## DISPLAY
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])




########## USER CHAT
# Accept user input
# if prompt := st.chat_input("Please answer the question above"): # User semi-trasparent input
prompt = st.chat_input("Please answer the question above")

if not st.session_state.stop:

    # Display assistant response in chat message container
    if st.session_state.llm_is_processing:
        with st.chat_message("user"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Max of quesiton_order is 75
            if st.session_state.question_order < len(prompt_dict):
                assistant_response = prompt_dict[st.session_state.question_order]['answer']

                # Simulate stream of response with milliseconds delay
                for chunk in assistant_response.split():
                    full_response += chunk + " "
                    time.sleep(0.1)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response) 
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "user", "content": full_response})

        time.sleep(1)

        # Unlock session for assitant to talk
        st.session_state.llm_is_processing = False

        # question_order +1 (next question)
        st.session_state.question_order += 5

    ########## ASSITANT CHAT (Ask question)
    # Avoid assitant talk before llm process
    if not st.session_state.llm_is_processing:
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):

                message_placeholder = st.empty()
                full_response = ""
                
                # Max of quesiton_order is 75
                if st.session_state.question_order < len(prompt_dict):
                    # Generate response
                    generate_response(prompt)

                    assistant_response = prompt_dict[st.session_state.question_order]['question']
                    
                else:
                    assistant_response = "It's the end of consulation!!"
                    st.session_state.stop = True

                # Simulate stream of response with milliseconds delay
                for chunk in assistant_response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response) 
                
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        # unlock for user to use
        st.session_state.llm_is_processing = True


        st.rerun()

else:
################################### SIDE BAR ###################################
    with st.sidebar:
        st.caption('Last Updated on November 25th, 2023')

        score_percent = random.sample(range(57, 99), 5)
        score_change_percent = random.sample(range(0, 8), 5)

        # col1, col2, col3, col4, col5 = st.columns(5)
        # col1.metric("Shared Attention", f"{score_percent[0]} %", f"{score_change_percent[0]} %")
        # col2.metric("Support and Encouragement", f"{score_percent[1]} %", f"{score_change_percent[1]} %")
        # col3.metric("Naming", f"{score_percent[2]} %", f"{score_change_percent[2]} %")
        # col4.metric("Turn-Taking", f"{score_percent[3]} %", f"{score_change_percent[3]} %")
        # col5.metric("Closure and Transition", f"{score_percent[4]} %", f"{score_change_percent[4]} %")
        col1, col2, col3 = st.columns(3)

        col1.metric(label="Gain", value=5000, delta=1000)
        col2.metric(label="Loss", value=5000, delta=-1000)
        col3.metric(label="No Change", value=5000, delta=0)

        style_metric_cards()



        df = pd.DataFrame(dict(
            r=score_percent,
            theta=['Shared Attention','Support and Encouragement','Naming',
                'Turn-Taking', 'Closure and Transition']))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        st.plotly_chart(fig, use_container_width=True)




################################### PROGRESS BAR ###################################
quesiton_progress_bar = st.progress(0, text='run')

display_loading_text_numerator = int(st.session_state.question_order/5)
display_loading_text_denominator = int(len(prompt_dict)/5)
display_loading_bar = float(display_loading_text_numerator/display_loading_text_denominator)

quesiton_progress_bar.progress(display_loading_bar, text=f'{display_loading_text_numerator}/{display_loading_text_denominator}')





