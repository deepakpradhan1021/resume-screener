# AI Resume Screening & Job Recommendation System

An AI tool that compares a resume against a job description, gives a match score, and suggests missing skills using LLM analysis.

## Features
- Upload resume (PDF)
- Paste job description
- Get a match score (0-100%)
- Get AI-generated skill-gap suggestions

## Tech Stack
- Python
- Sentence Transformers (embeddings)
- Cosine Similarity (scoring)
- Groq API (LLM analysis)
- Streamlit (UI)

## How It Works
1. Extracts text from the uploaded resume PDF
2. Converts resume and JD into embeddings
3. Calculates similarity score using cosine similarity
4. Sends both texts to an LLM to identify missing skills
5. Displays score and suggestions

## Live Demo
[Add your Streamlit Cloud link here]

## Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## What I Learned
- Working with embeddings and vector similarity
- Using LLM APIs for text analysis
- Building and deploying a Streamlit app
