"""
Extracts plain text from an uploaded CV file (PDF or DOCX).
Works directly with a Streamlit UploadedFile object.
"""

import io
import pdfplumber
from docx import Document


def extract_text_from_cv(uploaded_file) -> str:
    """
    uploaded_file: a Streamlit UploadedFile (from st.file_uploader)
    Returns extracted plain text, or raises ValueError on unsupported type.
    """
    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return _extract_from_pdf(uploaded_file)
    elif filename.endswith(".docx"):
        return _extract_from_docx(uploaded_file)
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or DOCX CV.")


def _extract_from_pdf(uploaded_file) -> str:
    text_chunks = []
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)
    return "\n".join(text_chunks).strip()


def _extract_from_docx(uploaded_file) -> str:
    file_bytes = io.BytesIO(uploaded_file.read())
    doc = Document(file_bytes)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs).strip()