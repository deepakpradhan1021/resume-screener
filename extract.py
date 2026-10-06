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
    resume_text = extract_text_from_pdf("sample_resume.pdf")
    print(resume_text[:500])  # print first 500 characters to check