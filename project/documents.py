import fitz

def extract_text_from_pdf(file_path) -> list:
    with fitz.open(file_path) as pdf_document:
        content = []
        for page in pdf_document:
            content.append(page.get_text())
    
    return "\n".join(content).splitlines()

def load_checks() -> list:
    checklist_path = "checklist.pdf"
    ctd_questions_path = "ctd questions.pdf"

    checklist_lines = extract_text_from_pdf(checklist_path)
    ctd_questions_lines = extract_text_from_pdf(ctd_questions_path)

    combined_checks = checklist_lines + ctd_questions_lines

    return [line.strip() for line in combined_checks if line.strip()]

def load_documents(file) -> str:
    with fitz.open(stream=file.read(), filetype="pdf") as pdf_document:
        content = []
        for page in pdf_document:
            content.append(page.get_text())
        
        return "\n".join(content)