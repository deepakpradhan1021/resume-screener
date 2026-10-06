from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the embedding model (downloads once, then cached)
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_match_score(resume_text, jd_text):
    """Compares resume and job description, returns similarity % """
    embeddings = model.encode([resume_text, jd_text])
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return round(score * 100, 2)

# Test it
if __name__ == "__main__":
    from extract import extract_text_from_pdf

    resume = extract_text_from_pdf("sample_resume.pdf")
    jd = """We are looking for a Python developer with experience in 
    machine learning, data analysis, and SQL. Knowledge of Flask or 
    Django is a plus."""

    match_percent = get_match_score(resume, jd)
    print(f"Match Score: {match_percent}%")