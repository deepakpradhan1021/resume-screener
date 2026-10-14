# AI Resume Screener

An AI-powered web app that compares a resume with a job description, finds matching skills, and provides suggestions for improvement.

## 🚀 Live Demo
[Try the Resume Screener](https://resume-screener-fl9mggq8t6kvww6xn6pvbf.streamlit.app/)

## ✨ Features
- Upload a text-based PDF resume
- Paste a job description
- View resume–job text similarity
- Identify matched skills and possible skill gaps
- Get AI suggestions using Groq
- Download a text report
- Input validation and error messages

## 🛠️ Tech Stack
- Python
- Streamlit
- Sentence Transformers
- Scikit-learn (Cosine Similarity)
- Groq API

## ⚙️ How It Works
1. Extracts text from the uploaded PDF.
2. Converts the resume and job description into embeddings.
3. Calculates text similarity using cosine similarity.
4. Uses an LLM to generate improvement suggestions.
5. Displays the results and allows report downloads.

## 💻 Run Locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create `.streamlit/secrets.toml`:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```
3. Keep `.streamlit/` in `.gitignore`. Never commit your API key.
4. Start the app:
   ```bash
   streamlit run app.py
   ```

## 🔒 Privacy
If AI suggestions are enabled, resume and job description text may be sent to Groq for processing. Avoid uploading sensitive personal information.


## Important Limitations
- The score is text similarity, not a hiring probability or proof of ability.
- Skill detection uses a basic list and may miss synonyms.
- Scanned PDFs may not work because OCR is not included.

## Future Improvements
- Add OCR for scanned resumes
- Improve skill extraction
- Add tests and more report formats
