"""Bounded, repeatable resume extraction without writing uploads to disk."""
from io import BytesIO
from pathlib import Path

MAX_UPLOAD_BYTES = 2 * 1024 * 1024


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
            return data.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise ValueError("Save the TXT resume using UTF-8 encoding") from exc
    import pypdf
    reader = pypdf.PdfReader(BytesIO(data))
    return "".join(page.extract_text() or "" for page in reader.pages)
