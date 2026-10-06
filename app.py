import streamlit as st
import tempfile
from extract import extract_text_from_pdf
from match import get_match_score
from analyze import get_skill_gap

st.set_page_config(page_title="AI Resume Screener", page_icon="📄")
st.title("📄 AI Resume Screening & Job Match")
st.write("Upload your resume and paste a job description to see your match score and skill gaps.")

# Upload resume
resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Job description input
jd_text = st.text_area("Paste Job Description", height=200)

if st.button("Analyze"):
    if resume_file is None or jd_text.strip() == "":
        st.warning("Please upload a resume AND paste a job description.")
    else:
        with st.spinner("Analyzing..."):
            # Save uploaded file temporarily so extract.py can read it
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(resume_file.read())
                tmp_path = tmp.name

            resume_text = extract_text_from_pdf(tmp_path)
            score = get_match_score(resume_text, jd_text)
            feedback = get_skill_gap(resume_text, jd_text)

        # Show results
        st.subheader("Match Score")
        st.progress(int(score))
        st.write(f"**{score}% match**")

        st.subheader("Skill Gap Analysis")
        st.write(feedback)