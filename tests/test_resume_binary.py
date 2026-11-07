"""Reject binary content masquerading as an ordinary TXT resume."""
from io import BytesIO
import pytest
from resume import extract_resume_text


def test_nul_in_text_resume_is_not_accepted_as_keyword_evidence():
    upload = BytesIO(b"Python\\x00SQL".replace(b"\\x00", b"\x00"))
    upload.name = "resume.txt"
    with pytest.raises(ValueError, match="NUL"):
        extract_resume_text(upload)
