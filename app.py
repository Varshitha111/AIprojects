import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


PERSONALITIES = {
    "General Assistant": "You are a helpful and friendly AI assistant.",
    "Coding Tutor": "You are an expert programming tutor. Explain clearly with examples.",
    "Friend": "You are a warm, fun and supportive friend.",
    "Strict Teacher": "You are a strict but fair teacher.",
}
personality = st.sidebar.selectbox("Choose Personality:", list(PERSONALITIES.keys()))
system_prompt = PERSONALITIES[personality]
model_name = "llama-3.3-70b-versatile"


if st.sidebar.button("Refresh"):
    st.session_state.messages = []
    st.rerun()

st.title("NEW AI")
st.caption("by VARSHITHA")
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input("write your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
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
if st.session_state.messages:
    with st.sidebar.expander(f"Chat History ({len(st.session_state.messages)} messages)"):
        for i, msg in enumerate(st.session_state.messages):
            role = "You" if msg["role"] == "user" else " AI"
            st.markdown(f"{role}: {msg['content'][:100]}{'...' if len(msg['content']) > 100 else ''}")
else:
    st.sidebar.info("No chat history yet.")