import unittest
import os

class TestPDFExtraction(unittest.TestCase):
    def setUp(self):
        self.sample_pdf = os.path.join(os.path.dirname(__file__), "..", "sample_data", "sample_resume.pdf")

    def test_sample_pdf_exists(self):
        self.assertTrue(os.path.exists(self.sample_pdf), f"Sample PDF not found at {self.sample_pdf}")

    def test_extract_text_valid_pdf(self):
        try:
            import pdfplumber
        except ImportError:
            raise unittest.SkipTest("pdfplumber not installed in this environment; skipping PDF parsing test.")
        
        text = ""
        with pdfplumber.open(self.sample_pdf) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        self.assertGreater(len(text.strip()), 50, "Extracted text is unexpectedly short")
        self.assertTrue(any(word in text.lower() for word in ["education", "experience", "skills", "projects"]))

if __name__ == "__main__":
    unittest.main()
