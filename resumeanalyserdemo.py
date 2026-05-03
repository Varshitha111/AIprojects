import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import pdfplumber
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)
model_name = "llama-3.3-70b-versatile"
st.title("resume analyser by varshitha")
uploaded_file = st.file_uploader("upload resume", type=["pdf"])
job_description = st.text_area("write jd", height=200)
resume_text = ""
if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        resume_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
if st.button("analyze resume"):
    if not resume_text.strip():
        st.warning("upload resume")
    elif not job_description.strip():
        st.warning("Please enter a job description.")
    else:
        system_prompt = """You are an expert resume analyzer and career coach.
        Given a resume and job description, you must respond in this exact format:
        MATCH SCORE: [X]%
        FEEDBACK:
        - [feedback point 1]
        - [feedback point 2]
        - [feedback point 3]
        IMPROVEMENT SUGGESTIONS:
        - [suggestion 1]
        - [suggestion 2]
        - [suggestion 3]
        SUGGESTED RESUME BULLET POINTS:
        - [bullet point 1]
        - [bullet point 2]
        - [bullet point 3]
        """
        user_prompt=f"resume:\n{resume_text}\nJob Description:\n{job_description}"
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.5,
                max_tokens=1024
            )
            result = response.choices[0].message.content
            st.markdown("Analysis result")
            st.markdown(result)
        except Exception as e:
            st.error(f"got an error {e}")