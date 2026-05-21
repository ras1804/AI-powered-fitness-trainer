import streamlit as st
import tempfile
import os

import google.generativeai as genai
from dotenv import load_dotenv

import ai_trainer as at

load_dotenv()

st.set_page_config(page_title="AI Fitness Trainer")

st.title("Your AI Powered Fitness Assistant")
st.write("Welcome, let's begin...")

tab1, tab2 = st.tabs(["Fitness Trainer", "Chatbot"])

# ================= FITNESS TRAINER =================

with tab1:

    workout = st.selectbox(
        "Select Workout",
        ['select', 'Bicep-Curl', 'Squats', 'Push-Ups']
    )

    uploaded_file = st.file_uploader(
        "Upload Workout Video",
        type=["mp4", "avi", "mov"]
    )

    if st.button("Letss goo!!!"):

        if workout == "select":
            st.warning("Please select a workout.")
            st.stop()

        if uploaded_file is None:
            st.warning("Please upload a video.")
            st.stop()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(uploaded_file.read())
            video_path = temp_file.name

        st.success("Processing video...")

        if workout == 'Bicep-Curl':
            at.bicepCurls(video_path)

        elif workout == 'Squats':
            at.squats(video_path)

        elif workout == 'Push-Ups':
            at.pushUps(video_path)

# ================= CHATBOT =================

with tab2:

    api_key = os.getenv("GOOGLE_API_KEY")

    if api_key:

        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-2.0-flash")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        st.header("Gemini AI Chatbot")

        user_input = st.text_input("Ask something")

        if st.button("Ask") and user_input:

            response = model.generate_content(user_input)

            st.session_state.chat_history.append(
                ("You", user_input)
            )

            st.session_state.chat_history.append(
                ("Bot", response.text)
            )

        for role, text in st.session_state.chat_history:
            st.write(f"**{role}:** {text}")

    else:
        st.error("GOOGLE_API_KEY not found in environment variables.")

# import os
# os.environ["QT_QPA_PLATFORM"] = "offscreen"

# import streamlit as st
# import tempfile
# import google.generativeai as genai
# from dotenv import load_dotenv

# import ai_trainer as at

# load_dotenv()

# st.set_page_config(page_title="Q&A Demo")

# st.title("Your AI powered fitness assistant")
# st.write("Welcome, lets begin.....")


# tab1, tab2 = st.tabs(["Fitness Trainer", "Chatbot"])

# with tab1:
    
#     col1, col2 = st.columns(2)

#     with col1:
#         workout = st.selectbox("Select what you are performing",['select', 'Bicep-Curl','Squats', 'Push-Ups'])
#     with col2:
#         camera_option = st.selectbox("Select your video type", ['select', 'Open-webcam', 'Upload video'])

#     video_path = None
#     if camera_option == "Upload video":
#         uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])
#         if uploaded_file is not None:
#             # Save uploaded file to a temp path
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
#                 temp_file.write(uploaded_file.read())
#                 video_path = temp_file.name 


#     if st.button("Letss goo!!!"):
#         para1 = video_path

#         match workout:
#             case 'Bicep-Curl':
#                 at.bicepCurls(para1)
#             case 'Squats':
#                 at.squats(para1)
#             case 'Push-Ups': 
#                 # st.write(str(para1))
#                 at.pushUps(para1)


# with tab2:
#     genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#     model=genai.GenerativeModel("gemini-2.0-flash") 
#     chat = model.start_chat(history=[])
#     def get_gemini_response(question):
        
#         response=chat.send_message(question,stream=True)
#         return response

#     ##initialize our streamlit app

    

#     st.header("Gemini LLM Application")

#     # Initialize session state for chat history if it doesn't exist
#     if 'chat_history' not in st.session_state:
#         st.session_state['chat_history'] = []

#     input=st.text_input("Input: ",key="input")
#     submit=st.button("Ask the question")

#     if submit and input:
#         response=get_gemini_response(input)
#         # Add user query and response to session state chat history
#         st.session_state['chat_history'].append(("You", input))
#         st.subheader("The Response is")
#         for chunk in response:
#             st.write(chunk.text)
#             st.session_state['chat_history'].append(("Bot", chunk.text))
#     st.subheader("The Chat History is")
        
#     for role, text in st.session_state['chat_history']:
#         st.write(f"{role}: {text}")
    
