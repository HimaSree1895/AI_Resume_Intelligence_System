from pdfminer.high_level import extract_text

def extract_resume_text(file):
    text = extract_text(file)
    return text.lower()
