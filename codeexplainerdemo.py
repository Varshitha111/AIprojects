import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)
model_name = "llama-3.3-70b-versatile"
st.title("Code Explainer")
st.caption("-by VARSHITHA")

language = st.sidebar.selectbox("lang",["Python","Java","JavaScript","C","C++","C#","SQL","HTML/CSS","Other"])
mode = st.sidebar.radio("mode of explanation :", ["beginner", "Advanced"])
bug_detection = st.sidebar.checkbox("detect bug")
code_input = st.text_area("write code:", height=300)
if st.button("code explanation"):
    if not code_input.strip():
        st.warning("write some code")
    else:
        if mode == "Beginner":
            mode_prompt = "Explain in very simple language as if teaching a complete beginner. Avoid jargon."
        else:
            mode_prompt = "Explain in detail with technical terms suitable for an experienced developer."
        system_prompt = f"""You are an expert programming tutor.
        The user will give you {language} code.
        {mode_prompt}
        Always explain step by step, covering what each part does.
        {"Also detect any bugs or issues in the code and suggest fixes." if bug_detection else ""}
        Format your response as:
        EXPLANATION:
        [step by step explanation]        
        {"BUG DETECTION:" if bug_detection else ""}
        {"[list any bugs found and how to fix them]" if bug_detection else ""}
        """
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": code_input}
                ],
                temperature=0.4,
                max_tokens=1024
            )
            result = response.choices[0].message.content
            st.markdown("Code Explanation")
            st.markdown(result)
        except Exception as e:
            st.error(f"Something went wrong: {e}")