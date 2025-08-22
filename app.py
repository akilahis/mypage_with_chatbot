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
    You are Akilah Ismail. Always respond in first person as Akilah. Keep everything brief and concise. Maintain a friendly intonation. 
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

col1, col2 = st.columns([3,1])
with col2:
    st.image("images/akilah_image.png", width=200)

with col1:
    st.title("👋 Hi, I'm Akilah Ismail")
    st.subheader("Data Analyst | MSc Analytics & Business Intelligence")
    st.write(
    "LOVE exploring data through hands-on experimentation. " \
    "This portfolio showcases pesonal projects where I combine APIs, visualization tools, and analytics to uncover interesting patterns (that no one asked for..) "
)

# --- Portfolio Section ---
st.header("📂 My Projects")
projects = [
    {
        "title": "Predicting Rental Property Prices in Urban Malaysia",
        "desc": "Machine learning model to predict property rental prices using rental listings from Mudah.my",
        "link": "https://github.com/akilaism/predict-rental",
    },
    {
        "title": "ZUS COFFEE Store Distributon Analysis",
        "desc": "Automated pipeline to process and analyze survey and feedback data from Google Sheets.",
        "link": "https://github.com/akilaism/edu-feedback-analysis",
    },
]

for p in projects:
    st.markdown(f"**[{p['title']}]({p['link']})**")
    st.write(p["desc"])
    st.markdown("---")

# --- Chatbot Section ---
st.title("💬 Let's Chat !")
st.subheader("PS: I'm a simple chatbot that uses Gemini API's (free model). Please be gentle with me 😎")
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