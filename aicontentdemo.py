import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

model_name = "llama-3.3-70b-versatile"

st.title("AI CONTENT GENERATOR ")
st.caption(" by VARSHITHA")

topic = st.text_input("give a topic")

tone = st.sidebar.selectbox("select tone",["Professional","Casual","Humorous","Inspirational"])
output_format = st.sidebar.selectbox("Output Format:",["Blog Post", "LinkedIn Post", "X post"])
word_limit = st.sidebar.slider("Word Limit:", min_value=50, max_value=1000, value=300, step=50)
if st.button("generate content"):
    if not topic.strip():
        st.warning("you didn't write a topic")
    else:
        system_prompt = f"""You are an expert content writer.
        Write a {output_format} about the given topic.
        Tone: {tone}
        Word limit: {word_limit} words.
        Format it properly based on the output type:
        - Blog Post: title, introduction, body, conclusion
        - LinkedIn Post: engaging hook, key points, call to action
        - Twitter/X Thread: numbered tweets (1/, 2/, 3/ ...) each under 280 characters
        """

        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": topic}
                ],
                temperature=0.7,
                max_tokens=1024
            )
            result = response.choices[0].message.content
            st.markdown({output_format})
            st.markdown(result)
        except Exception as e:
            st.error(f"Something went wrong: {e}")