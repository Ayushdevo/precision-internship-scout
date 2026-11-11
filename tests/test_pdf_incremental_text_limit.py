import pytest
from io import BytesIO
from types import SimpleNamespace
from unittest.mock import Mock
import pypdf
from resume import extract_resume_text, MAX_TEXT_CHARS
def test_extraction_stops_before_later_pages_after_limit(monkeypatch):
    later = Mock(return_value='later page')
    pages = [SimpleNamespace(extract_text=lambda: 'x'*(MAX_TEXT_CHARS+1)), SimpleNamespace(extract_text=later)]
    monkeypatch.setattr(pypdf, 'PdfReader', lambda _: SimpleNamespace(is_encrypted=False, pages=pages))
    upload = BytesIO(b'pdf'); upload.name = 'resume.pdf'
    with pytest.raises(ValueError, match='100,000'):
        extract_resume_text(upload)
    later.assert_not_called()
