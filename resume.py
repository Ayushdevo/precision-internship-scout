"""Bounded, repeatable resume extraction without writing uploads to disk."""
from io import BytesIO
from pathlib import Path

MAX_UPLOAD_BYTES = 2 * 1024 * 1024
MAX_TEXT_CHARS = 100000


def extract_resume_text(uploaded_file) -> str:
    if uploaded_file is None:
        return ""
    extension = Path(uploaded_file.name).suffix.casefold()
    if extension not in {".txt", ".pdf"}:
        raise ValueError("Upload a TXT or PDF resume")
    position = uploaded_file.tell()
    try:
        uploaded_file.seek(0)
        data = uploaded_file.read(MAX_UPLOAD_BYTES + 1)
    finally:
        uploaded_file.seek(position)
    if not data:
        raise ValueError("Resume file is empty")
    if len(data) > MAX_UPLOAD_BYTES:
        raise ValueError("Resume must be 2 MB or smaller")
    if extension == ".txt":
        try:
            text = data.decode("utf-8-sig")
            if not text.strip():
                raise ValueError("Resume must contain non-whitespace text")
            if len(text) > MAX_TEXT_CHARS:
                raise ValueError("Extracted resume text exceeds 100,000 characters")
            return text
        except UnicodeDecodeError as exc:
            raise ValueError("Save the TXT resume using UTF-8 encoding") from exc
    import pypdf
    try:
        reader = pypdf.PdfReader(BytesIO(data))
        if reader.is_encrypted:
            raise ValueError("Upload an unencrypted PDF resume")
        if len(reader.pages) > 50:
            raise ValueError("PDF resume must contain at most 50 pages")
        parts = []
        total = 0
        for page in reader.pages:
            part = page.extract_text() or ""
            total += len(part) + bool(parts)
            if total > MAX_TEXT_CHARS:
                raise ValueError("Extracted resume text exceeds 100,000 characters")
            parts.append(part)
        text = "\n".join(parts)
        if not text.strip():
            raise ValueError("No text found; upload a text-based PDF or TXT resume")
        return text
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError("Unable to read PDF; upload a valid text-based PDF or TXT resume") from exc

