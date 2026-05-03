import streamlit as st
from groq import Groq

st.set_page_config(page_title="My AI Assistant", page_icon="🤖", layout="centered")

# ===================== HARD CODED API KEY =====================
# WARNING: This key is visible to anyone who sees your code
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

# ===================== CONFIG =====================
MODELS = {
    "Llama 3.3 70B (Recommended)": "llama-3.3-70b-versatile",
    "Llama 3.1 8B": "llama-3.1-8b-instant",
}

PERSONALITIES = {
    "General Assistant": "You are a helpful and friendly AI assistant.",
    "Coding Tutor": "You are an expert programming tutor. Explain clearly with examples.",
    "Friendly Friend": "You are a warm, fun and supportive friend.",
    "Strict Teacher": "You are a strict but fair teacher.",
}

# ===================== SIDEBAR =====================
st.sidebar.title("⚙️ Settings")

personality = st.sidebar.selectbox("Choose Personality:", list(PERSONALITIES.keys()))
system_prompt = PERSONALITIES[personality]

selected_model = st.sidebar.selectbox("Choose Model:", list(MODELS.keys()))
model_name = MODELS[selected_model]

if st.sidebar.button("🔄 New Chat"):
    st.session_state.messages = []
    st.rerun()

# ===================== MAIN CHAT =====================
st.title("🤖 My AI Assistant")
st.caption(f"Personality: **{personality}** | Powered by Groq")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
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
                assistant_reply = response.choices[0].message.content
                
                st.markdown(assistant_reply)
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
            except Exception as e:
                st.error(f"Something went wrong: {e}")

st.caption("Made with ❤️ using Groq + Streamlit")