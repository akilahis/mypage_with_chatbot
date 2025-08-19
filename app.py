import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# --- Configure Gemini ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"]) #when using streamlit
#genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
#model = genai.GenerativeModel("gemini-1.5-flash")

#load personal context
if "profile" not in st.session_state:
   st.session_state.profile = st.secrets["profile"]["context"]

# Initialize model
if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel("gemini-1.5-flash")

# initial chat
if "chat" not in st.session_state:
    initial_message = f"""
    You are Akilah Ismail. Always respond in first person as Akilah. 
    Use this information about yourself to answer questions:
    
    {st.session_state.profile}
    
    If asked about something not in this information, say 
    "I don't have that information about myself."
    """
    st.session_state.chat = st.session_state.model.start_chat(history=[
        {"role": "user", "parts": [initial_message]},
        {"role": "model", "parts": ["Understood. I will respond as Akilah Ismail using the provided information."]}
    ])

# Modified send message function
def send_message_with_context(user_message):
     return st.session_state.chat.send_message(
        f"Respond as Akilah Ismail using your knowledge: {user_message}"
    )


# --- Page Config ---
st.set_page_config(page_title="Akilah Ismail | Portfolio")

# --- Header ---
st.title("👋 Hi, I'm Akilah Ismail")
st.subheader("Data Analyst | M&E Specialist | MSc Analytics & BI")
st.write(
    "I specialize in data-driven insights, business intelligence, "
    "and analytical solutions. This page showcases my work and lets you chat with me via AI."
)

# --- Chatbot Section ---
st.header("💬 Chat with My AI Assistant")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ask me anything about my work or skills:")
if st.button("Send") and user_input:
    # Append user message
    try:
        response = send_message_with_context(user_input)
        
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("AI", response.text))

    except Exception as e:
        st.error(f"Error: {e}")
    
# Display chat history
for speaker, message in st.session_state.chat_history:
    with st.chat_message("user" if speaker == "You" else "assistant"):
        st.markdown(message)