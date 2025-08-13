import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# --- Configure Gemini ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Page Config ---
st.set_page_config(page_title="Akilah Ismail | Portfolio")

# --- Header ---
st.title("👋 Hi, I'm Akilah Ismail")
st.subheader("Data Analyst | M&E Specialist | MSc Analytics & BI")
st.write(
    "I specialize in data-driven insights, business intelligence, "
    "and analytical solutions. This page showcases my work and lets you chat with me via AI."
)

# --- Portfolio Section ---
st.header("📂 My Projects")
projects = [
    {
        "title": "Predicting Rental Property Prices in Malaysia",
        "desc": "Machine learning model to predict property prices using housing market data.",
        "link": "https://github.com/akilaism/predict-rental"
    },
    {
        "title": "Education Program Feedback Analysis",
        "desc": "Automated pipeline to process and analyze survey and feedback data from Google Sheets.",
        "link": "https://github.com/akilaism/edu-feedback-analysis"
    }
]

for p in projects:
    st.markdown(f"**[{p['title']}]({p['link']})**")
    st.write(p["desc"])
    st.markdown("---")

# --- Chatbot Section ---
st.header("💬 Chat with My AI Assistant")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ask me anything about my work or skills:")
if st.button("Send") and user_input:
    # Append user message
    st.session_state.chat_history.append(("You", user_input))
    
    # Get AI response
    response = model.generate_content(user_input)
    st.session_state.chat_history.append(("AI", response.text))
    
# Display chat history
for speaker, message in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {message}")
