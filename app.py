from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=".venv/.env")
import streamlit as st
import fitz  # this is pymupdf

def open_ai_tailor(cv_text: str, jd_text: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""
You are AI CV Tailor. 
You must tailor the following CV to the given job description without inventing new work experience, education, or projects. 
Reorder, rephrase, and emphasise content truthfully so it aligns with the job description. 
Keep the CV ATS-friendly, no tables or columns. 
Return a fully written CV, ideally ≤2 pages (3 max if source exceeds 2 pages), followed by a brief summary of changes and any items the user should verify.

CV:
{cv_text}

JOB DESCRIPTION:
{jd_text}
"""

    response = client.responses.create(
        model="gpt-5-nano",
        input=prompt,
    )

    return response.output_text




# Helper function: extract text from PDF
def extract_text(pdf_bytes: bytes) -> str:
    text = ""
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text.strip()


st.set_page_config(page_title="CV Tailor", page_icon="🧵")
st.title("🧵 CV Tailor")


# Upload CV
cv_file = st.file_uploader("Upload your CV (PDF)", type=["pdf"])

# Paste Job Description
jd_text = st.text_area("Paste the Job Description", height=200)


if cv_file is None or not jd_text.strip():
    st.markdown(":orange-badge[⚠️Enter Job Description and Upload CV]")
else:
    st.badge("Uploaded", icon=":material/check:", color="green")



    # Extract CV text
    pdf_bytes = cv_file.read()
    cv_text = extract_text(pdf_bytes)

    # Show side-by-side
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Extracted CV Text")
        st.write(cv_text[:100000])  # show first 1000 characters only

    with col2:
        st.subheader("Job Description")
        st.write(jd_text[:100000])  # limit to first 1000 characters too

col1, col2, col3 = st.columns(3)

## Process Button
with col2:
    if st.button("Process CV and Job Description") and cv_file is not None and jd_text.strip():
        with st.spinner("Processing..."):
            tailored_text = open_ai_tailor(cv_text, jd_text)
            st.markdown(tailored_text)


# Contact Section
st.markdown("---")  # horizontal line to separate
st.markdown("## 📫 Contact Me")
st.markdown(
    """
- 📧 Email: [ellismain282@gmail.com](mailto:ellismain282@gmail.com)  
- 💼 LinkedIn: [Ellis Mainwaring](https://linkedin.com/in/ellismainwaring)  
"""
)

