import unittest
import re

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

class TestSkillMatching(unittest.TestCase):
    def test_find_skills_present(self):
        text = "Experienced software engineer skilled in Python, SQL, Docker, and Machine Learning."
        skills = find_skills(text)
        self.assertIn("python", skills)
        self.assertIn("sql", skills)
        self.assertIn("docker", skills)
        self.assertIn("machine learning", skills)

    def test_word_boundary_isolation(self):
        # Should match javascript, but NOT isolate java unless java appears independently
        text = "Building web apps using JavaScript and React."
        skills = find_skills(text)
        self.assertIn("javascript", skills)
        self.assertIn("react", skills)
        self.assertNotIn("java", skills)

    def test_skill_gap_calculation(self):
        resume_skills = ["python", "sql", "git"]
        jd_skills = ["python", "sql", "docker", "aws"]
        
        matched = [s for s in jd_skills if s in resume_skills]
        missing = [s for s in jd_skills if s not in resume_skills]
        
        self.assertEqual(matched, ["python", "sql"])
        self.assertEqual(missing, ["docker", "aws"])

    def test_empty_input(self):
        skills = find_skills("")
        self.assertEqual(skills, [])

if __name__ == "__main__":
    unittest.main()
