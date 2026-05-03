import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="My AI Assistant", page_icon="🤖", layout="centered")

# Models and Personalities
MODELS = {
    "Llama 3.3 70B (Recommended)": "llama-3.3-70b-versatile",
    "Llama 3.1 8B": "llama-3.1-8b-instant",
}

PERSONALITIES = {
    "General Assistant": "You are a helpful and friendly AI assistant.",
    "Coding Tutor": "You are an expert programming tutor. Explain concepts clearly with examples.",
    "Friendly Friend": "You are a warm, fun and supportive friend.",
    "Strict Teacher": "You are a strict but fair teacher.",
}

# Sidebar
st.sidebar.title("⚙️ Settings")

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("Enter Groq API Key:", type="password", help="Get it from console.groq.com")

client = Groq(api_key=api_key) if api_key else None

personality = st.sidebar.selectbox("Choose Personality:", list(PERSONALITIES.keys()))
system_prompt = PERSONALITIES[personality]

model_name = st.sidebar.selectbox("Choose Model:", list(MODELS.values()), 
                                  format_func=lambda x: [k for k,v in MODELS.items() if v==x][0])

if st.sidebar.button("🔄 New Chat"):
    st.session_state.messages = []
    st.rerun()

# Main Chat
st.title("🤖 My Custom AI Chatbot")
st.caption(f"Personality: **{personality}**")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Ask me anything..."):
    if not api_key:
        st.error("⚠️ Please enter your Groq API key in the sidebar.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            *st.session_state.messages
                        ],
                        temperature=0.7,
                        max_tokens=1024
                    )
                    reply = response.choices[0].message.content
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"Error: {e}")