import io
import os
import re
from datetime import datetime

import pdfplumber
import streamlit as st
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
st.set_page_config(page_title="AI Resume Screener", page_icon="📄", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1120px; padding-top: 2rem;}
.hero {padding: 1.5rem; border-radius: 16px; background: linear-gradient(120deg,#111827,#243b53); color: white;}
.hero h1 {color:white; margin-bottom:.3rem;}
.hero p {color:#dbeafe; margin:0;}
div[data-testid="stMetric"] {
    background: var(--secondary-background-color);
    color: var(--text-color);
    padding: 1rem;
    border: 1px solid var(--border-color);
    border-radius: 12px;
}
</style>
<div class="hero"><h1>📄 AI Resume Screener</h1>
<p>Compare a resume with a job description and find skills to improve.</p></div>
""", unsafe_allow_html=True)

@st.cache_resource(show_spinner="Loading language model (first run may take a minute)...")
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

def extract_pdf_text(file):
    try:
        with pdfplumber.open(io.BytesIO(file.getvalue())) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages).strip()
    except Exception as exc:
        raise ValueError("I couldn't read this PDF. Please upload a valid, text-based PDF.") from exc

def calculate_score(resume, job):
    model = load_model()
    vectors = model.encode([resume, job])
    return round(max(0, min(100, float(cosine_similarity([vectors[0]], [vectors[1]])[0][0]) * 100)))

SKILLS = [
    "python","java","c++","sql","machine learning","deep learning","generative ai",
    "natural language processing","nlp","pandas","numpy","scikit-learn","tensorflow",
    "pytorch","streamlit","flask","fastapi","data analysis","statistics","power bi",
    "tableau","excel","git","github","docker","aws","azure","html","css","javascript",
    "react","rest api","llm","prompt engineering","computer vision","opencv",
    "data structures","algorithms","communication","teamwork","problem solving"
]

def find_skills(text):
    found = []
    for skill in SKILLS:
        if re.search(r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])", text.lower()):
            found.append(skill)
    return found

def groq_key():
    key = os.getenv("GROQ_API_KEY", "").strip()
    if key:
        return key
    try:
        return str(st.secrets.get("GROQ_API_KEY", "")).strip()
    except Exception:
        return ""

def ai_suggestions(resume, job, missing):
    key = groq_key()
    if not key:
        return "AI suggestions are off. Add GROQ_API_KEY to .streamlit/secrets.toml locally or Streamlit Cloud Secrets."
    try:
        from groq import Groq
        client = Groq(api_key=key)
        result = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role":"system","content":"You are a careful resume coach. Use only requirements explicitly in the job description. Do not invent experience. Give at most 5 short bullet points with honest learning/project suggestions."},
                {"role":"user","content":f"JOB DESCRIPTION:\n{job[:10000]}\n\nRESUME:\n{resume[:10000]}\n\nPossible missing skills: {', '.join(missing) or 'None detected'}. Give practical, concise suggestions."}
            ],
            temperature=0.2,
            max_tokens=500,
        )
        suggestions = result.choices[0].message.content or ""
return suggestions.strip() or "No suggestions were returned. Please try again."
    except Exception:
        return "AI suggestions could not be generated. Check your Groq API key and Streamlit logs."
with st.sidebar:
    st.header("About this tool")
    st.write(
        "Compare your resume with a job description, "
        "check matching skills, and find areas to improve."
    )
    st.caption(
        "Privacy: If AI suggestions are enabled, your resume "
        "and job description text may be sent to Groq for processing. "
        "Avoid uploading sensitive personal information."
    )

col1, col2 = st.columns(2, gap="large")
with col1:
    st.subheader("1. Upload your resume")
    pdf = st.file_uploader("Choose a PDF resume", type=["pdf"])
    st.caption("Text-based PDFs work best. Remove private details before uploading.")
with col2:
    st.subheader("2. Paste the job description")
    jd = st.text_area("Job description", height=210, placeholder="Paste the role, skills, and responsibilities...")

if st.button("🔍 Analyze resume", type="primary", use_container_width=True):
    if pdf is None:
        st.error("Please upload a resume PDF.")
        st.stop()
    if len(jd.strip()) < 40:
        st.error("Please paste a longer job description (at least 40 characters).")
        st.stop()
    try:
        with st.spinner("Reading resume..."):
            resume = extract_pdf_text(pdf)
        if len(resume) < 30:
            st.error("No readable text found. This may be a scanned PDF. Try a text-based PDF.")
            st.stop()
        with st.spinner("Comparing text..."):
            score = calculate_score(resume, jd.strip())
            resume_skills, jd_skills = find_skills(resume), find_skills(jd)
            matched = [s for s in jd_skills if s in resume_skills]
            missing = [s for s in jd_skills if s not in resume_skills]
        with st.spinner("Preparing suggestions..."):
            suggestions = ai_suggestions(resume, jd, missing)

        st.divider()
        st.header("Your results")
        a, b, c = st.columns(3)
        a.metric("Text similarity", f"{score}%")
        a.progress(score / 100)
        b.metric("Matched skills found", len(matched))
        b.write(", ".join(matched) if matched else "No known matching skills detected.")
        c.metric("Possible skill gaps", len(missing))
        c.write(", ".join(missing) if missing else "No known skill gaps detected.")
        st.info("This percentage is text similarity, not a hiring probability or proof of ability. Skill detection uses simple text matching and may miss synonyms.")
        st.subheader("AI suggestions")
        st.markdown(suggestions)

        report = "\n".join([
            "AI RESUME SCREENER — RESULTS",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"Text similarity: {score}%",
            "",
            "MATCHED SKILLS:", *([f"- {s}" for s in matched] or ["- None detected"]),
            "",
            "POSSIBLE SKILL GAPS:", *([f"- {s}" for s in missing] or ["- None detected"]),
            "",
            "SUGGESTIONS:", suggestions,
            "",
            "Note: The score is text similarity, not a hiring probability."
        ])
        name = re.sub(r"[^A-Za-z0-9_-]+", "_", pdf.name.rsplit(".",1)[0]).strip("_") or "resume"
        st.download_button("⬇️ Download results", report, file_name=f"{name}_screening_report.txt", mime="text/plain", use_container_width=True)
    except ValueError as exc:
        st.error(str(exc))
    except Exception:
        st.error("Analysis failed. Please try again or check the Streamlit logs.")

st.divider()
st.caption("Built with Python, Streamlit, Sentence Transformers, scikit-learn, pdfplumber, and Groq.")
