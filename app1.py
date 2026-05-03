import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import pdfplumber
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)
model_name = "llama-3.3-70b-versatile"
SUMMARY_STYLES = {
    "Short": "summarize the text in short",
    "Medium": "Summarize the text 100 words.",
    "Detailed": "Summarize the text in detail.",
}
st.title("VARSHITHA's Text Summarizer")
st.caption("Summarize articles, text, or PDFs instantly")
summary_style = st.sidebar.selectbox("Summary Length:", list(SUMMARY_STYLES.keys()))
bullet_points = st.sidebar.checkbox("Bullet-point summary")
tab1, tab2 = st.tabs(["write text", "upload PDF"])
user_text = ""
with tab1:
    user_text = st.text_area("Paste your text here:", height=250)

with tab2:
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    if uploaded_file:
        with pdfplumber.open(uploaded_file) as pdf:
            user_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        st.success("PDF loaded!")
if st.button("Summarize"):
    if not user_text.strip():
        st.warning("paste text or pdf")
    else:
        system_prompt = SUMMARY_STYLES[summary_style]
        if bullet_points:
            system_prompt += " Format the summary as bullet points."
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text}
                ],
                temperature=0.5,
                max_tokens=1024
            )
            summary = response.choices[0].message.content
            st.markdown(" Summary")
            st.markdown(summary)
        except Exception as e:
            st.error(f"Something went wrong: {e}")