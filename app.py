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
    You are Akilah Ismail. Always respond in first person as Akilah. Maintain a friendly intonation. If you can, provide your own judgement in your answers, but dont stray too far from the actual context. 
    Use this information about yourself to answer questions:
    
    {st.session_state.profile}
    
    # Personality & Communication Style
    - **Tone:** Friendly, professional, and conversational. Imagine you're at a networking event.
    - **Depth:** Be expansive and engaging. When you have information, share relevant details, short anecdotes, or your reasoning.
    - **Style:** Show, don't just tell. For example, don't say "I know Python." Say, "I use Python with Pandas for my projects, like the time I built an ETL pipeline to automate our reporting."
    - **Honesty:** If information is not in the context, politely state you don't know and pivot to something you do know. E.g., "I don't have that specific detail, but I'm currently learning SQL on DataCamp which has been great!"
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
st.set_page_config(page_title="Akilah Ismail | Portfolio", layout="wide")

col1, col2 = st.columns([3,2])
with col2:
    st.image("images/akilah_image.png", width=400)

with col1:
    st.title("👋 HI, I'M AKILAH ISMAIL")
    st.subheader("Data Analyst | MSc Analytics & Business Intelligence")
    st.write(
    "LOVE exploring data through hands-on experimentation. " \
    "This portfolio showcases pesonal projects where I combine APIs, visualization tools, and analytics to uncover interesting patterns (that no one asked for..) "
)

# --- Portfolio Section ---
st.header("📂 MY PROJECTS")
projects = [
    {
        "title": "Predicting Rental Property Prices in Urban Malaysia (Penang, KL, Johor)",
        "desc": """
        - Machine learning model to predict property rental prices using rental listings from Mudah.my.
        - Dataset are further enriched with extracting surrounding amenities (within 2km) via Open Street Map API.
        - TOOLS 🛠️ : Python (Pandas, Scikit-learn), OpenStreetMap API, Streamlit, Git/GitHub
        """,
        "link": "https://github.com/akilaism/predict-rental",
    },
    {
        "title": "ZUS COFFEE'S Stores Distributon Analysis",
        "desc": """
        - Analysis of ZUS COFFEE's store distribution and market coverage across Malaysia. 
        - Combines geospatial data, population insights, and Google Places API to highlight saturated districts and underserved area.  
        - TOOLS 🛠️ : Python (Pandas, GeoPandas), GCP (Google Maps API), GeoJSON, Streamlit, Git/GitHub
        """,
        "link": "https://zusakilah.streamlit.app/",
    },
]

for p in projects:
    st.markdown(f"**[{p['title']}]({p['link']})**")
    st.markdown(p["desc"])

# professional experience
st.markdown("---")
st.header("💼 PROFESSIONAL EXPERIENCE")

st.markdown("""
**DATA ANALYST (MONITORING & EVALUATION)**  
**CHUMBAKA** - *04/2025 - 07/2025*  
- Analyzing survey and feedback data using **Python** and **Google Sheets pipelines**.  
- Developing modular **data analysis scripts** with automated cleaning and summarization.  
- Supporting decision-making with actionable insights for program monitoring.

**SENIOR ANALYST, ANALYTICAL R&D**  
**NOVUGEN (ONCOLOGY) PHARMA** – *2020 - 2023*  
- Led analytical method development for **pharmaceutical formulations**.  
- Collaborated cross-functionally to ensure **compliance and accuracy in testing**.  
- Supervised junior analysts and optimized workflows for efficiency.

**EXECUTIVE, ANALYTICAL R&D**  
**DUOPHARMA INNOVATION** – *2018 - 2020*  
- Performed analytical validation and quality control testing.  
- Developed SOPs for consistent laboratory procedures.  
""")

# --- Chatbot Section ---
st.markdown("---")
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

st.markdown("---")
st.header("📫 LET'S CONNECT")
st.markdown("""
- **Email:** [sitinurakilah93@gmail.com](mailto:akilah@email.com)  
- **LinkedIn:** [linkedin.com/in/akilah-ismail](https://linkedin.com/in/akilah-ismail)  
- **GitHub:** [github.com/akilahismail](https://github.com/akilahis)  
- **Download My Resume:** [akilah's CV](https://www.notion.so/AKILAH-S-JOB-APPLICATION-25a404f6f86b8071a6d1c26447fcec14)
""")

