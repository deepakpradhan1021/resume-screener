# AI Resume Screener

An interactive web application that analyzes the alignment between a PDF resume and a job description using dense sentence embeddings, highlights matched skills and missing qualifications, and provides targeted improvement suggestions using an LLM.

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Web%20App-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![HuggingFace](https://img.shields.io/badge/Embeddings-Sentence--Transformers-yellow?logo=huggingface&logoColor=white)](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
[![Groq](https://img.shields.io/badge/LLM%20API-Groq-orange?logo=groq&logoColor=white)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Live Demo](https://resume-screener-fl9mggq8t6kvww6xn6pvbf.streamlit.app/) • [Features](#-features) • [How It Works](#-how-it-works) • [Run Locally](#-how-to-run-locally) • [Limitations](#-limitations--privacy) • [License](#-license)

---

## 🚀 Live Demo

Try the application directly in your browser:  
👉 **[Launch AI Resume Screener](https://resume-screener-fl9mggq8t6kvww6xn6pvbf.streamlit.app/)**

---

## ✨ Features

- **PDF Resume Extraction:** Extracts text from uploaded PDF resumes using `pdfplumber`.
- **Semantic Similarity Scoring:** Uses the `all-MiniLM-L6-v2` dense embedding model and cosine similarity to compute contextual overlap between the resume and the job description.
- **Skill Detection & Gap Analysis:** Identifies overlapping skills and highlights explicit requirements missing from the resume.
- **Actionable AI Feedback:** Generates concise, grounded improvement suggestions via the **Groq API** (`openai/gpt-oss-20b`).
- **Downloadable Summary Report:** Exports a structured text report containing the score, matched skills, and suggested additions.
- **Automated Unit Tests:** Includes unit test coverage for extraction and skill parsing under `tests/`.

---

## ⚙️ How It Works

```
┌──────────────────────────┐         ┌──────────────────────────┐
│   Candidate Resume PDF   │         │     Job Description      │
└────────────┬─────────────┘         └────────────┬─────────────┘
             │                                    │
             ▼                                    ▼
      [ pdfplumber ]                         [ Raw Text ]
   (Text Extraction)                              │
             │                                    │
             ├─────────────────┬──────────────────┤
             │                 │                  │
             ▼                 ▼                  ▼
   ┌───────────────────┐ ┌───────────────┐ ┌───────────────────┐
   │ Skill Detection   │ │ MiniLM-L6-v2  │ │ Skill Detection   │
   │ (Resume Skills)   │ │ Embeddings    │ │ (Job Skills)      │
   └─────────┬─────────┘ └───────┬───────┘ └─────────┬─────────┘
             │                   │                   │
             │         [ Cosine Similarity ]         │
             │                   │                   │
             ▼                   ▼                   ▼
    ┌────────────────────────────────────────────────────────┐
    │     Matched Skills & Identified Skill Gaps             │
    └──────────────────────────┬─────────────────────────────┘
                               │
                               ▼
    ┌────────────────────────────────────────────────────────┐
    │              Groq LLM Feedback Inference               │
    │  (Actionable suggestions based on missing criteria)    │
    └──────────────────────────┬─────────────────────────────┘
                               │
                               ▼
    ┌────────────────────────────────────────────────────────┐
    │           Streamlit Interactive Web UI                 │
    │  - Semantic score gauge & skill breakdown              │
    │  - Downloadable screening report (.txt)                │
    └────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```text
resume-screener/
│
├── sample_data/             # Sample inputs for testing
│   ├── sample_resume.pdf    # Sample PDF resume
│   ├── jd_close_match.txt   # Highly aligned sample job description
│   ├── jd_partial_match.txt # Partially aligned sample job description
│   └── jd_unrelated.txt     # Unrelated sample job description
├── tests/                   # Automated unit test suite
│   ├── test_skills.py       # Unit tests for skill extraction & gap detection
│   └── test_extract.py      # Unit tests for PDF parsing & boundary handling
├── app.py                   # Main Streamlit web application
├── extract.py               # PDF text extraction utility
├── match.py                 # Semantic similarity embedding module
├── analyze.py               # Groq LLM suggestion module
├── screenshot.png           # Application preview screenshot
├── requirements.txt         # Project dependencies
├── .gitignore               # Git ignore rules (secrets, venv, caches)
└── README.md                # Project documentation
```

---

## 💻 How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/deepakpradhan1021/resume-screener.git
cd resume-screener
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run automated unit tests

```bash
python -m unittest discover -s tests
```

### 5. Configure Groq API Key (Optional for AI suggestions)

Create `.streamlit/secrets.toml` in the project root:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

*(Ensure `.streamlit/` remains in `.gitignore` to prevent committing secrets).*

### 6. Launch the application

```bash
streamlit run app.py
```

Open your browser at **`http://localhost:8501`**.

---

## 🔒 Limitations & Privacy

- **Text Similarity vs. Ability:** The score represents mathematical cosine similarity between the two texts, not proof of candidate ability or a hiring decision.
- **Scanned PDFs:** The extraction pipeline relies on text streams. Scanned or image-only PDFs require OCR preprocessing.
- **Privacy:** When AI suggestions are generated, resume and job description text are sent to Groq for model inference. Do not upload sensitive personal data (e.g. government IDs, financial information).

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).
