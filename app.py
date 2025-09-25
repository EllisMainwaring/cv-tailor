import streamlit as st
import fitz  # this is pymupdf

# Helper function: extract text from PDF
def extract_text(pdf_bytes: bytes) -> str:
    text = ""
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text.strip()

st.set_page_config(page_title="AI CV Tailor", page_icon="🧵")
st.title("🧵 AI CV Tailor")

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

    st.button("Process CV and Job Description")
