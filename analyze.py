import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # reads the .env file
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_skill_gap(resume_text, jd_text):
    """Asks the LLM to list missing skills and suggestions."""
    prompt = f"""
    Compare this resume and job description.
    
    RESUME:
    {resume_text}
    
    JOB DESCRIPTION:
    {jd_text}
    
   Give me:
1. Top 5 skills that are explicitly mentioned in the JOB DESCRIPTION but missing from the RESUME.
2. One short suggestion for each missing skill.

Important rules:
- Only use skills explicitly mentioned in the JOB DESCRIPTION.
- Do not add related or implied skills.
- Do not invent skills.
- Do not include tools or technologies that are not mentioned in the JOB DESCRIPTION.
- If fewer than 5 skills are missing, list only the skills that are actually missing.
- Keep the answer short and in bullet points.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Test it
if __name__ == "__main__":
    from extract import extract_text_from_pdf

    resume = extract_text_from_pdf("sample_resume.pdf")
    jd = """We are looking for a Python developer with experience in 
    machine learning, data analysis, and SQL. Knowledge of Flask or 
    Django is a plus."""

    result = get_skill_gap(resume, jd)
    print(result)