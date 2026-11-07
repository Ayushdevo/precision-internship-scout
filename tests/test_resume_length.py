"""Cap decoded text to limit accidental processing of oversized resumes."""
from io import BytesIO
import pytest
from resume import MAX_TEXT_CHARS, extract_resume_text


def make_upload(text):
    upload = BytesIO(text.encode("utf-8"))
    upload.name = "resume.txt"
    return upload


def test_text_limit_accepts_exact_boundary():
    assert len(extract_resume_text(make_upload("x" * MAX_TEXT_CHARS))) == MAX_TEXT_CHARS


def test_text_limit_rejects_one_character_too_many():
    with pytest.raises(ValueError, match="100,000 characters"):
        extract_resume_text(make_upload("x" * (MAX_TEXT_CHARS + 1)))
