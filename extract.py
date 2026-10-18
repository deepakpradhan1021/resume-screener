import pdfplumber

def extract_text_from_pdf(pdf_path):
    """Reads a PDF file and returns all its text as one string."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# Test it
if __name__ == "__main__":
    import os
    sample_path = os.path.join(os.path.dirname(__file__), "sample_data", "sample_resume.pdf") if not os.path.exists("sample_resume.pdf") else "sample_resume.pdf"
    resume_text = extract_text_from_pdf(sample_path)
    print(resume_text[:500])  # print first 500 characters to check