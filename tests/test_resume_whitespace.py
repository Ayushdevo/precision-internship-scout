"""A whitespace-only upload is not usable candidate evidence."""
from io import BytesIO

import pytest

from resume import extract_resume_text


@pytest.mark.parametrize("raw", [b" ", b"\n\t  \r\n", b"\xef\xbb\xbf\n "])
def test_txt_without_actual_text_is_rejected(raw):
    upload = BytesIO(raw)
    upload.name = "cv.txt"
    with pytest.raises(ValueError, match="No text"):
        extract_resume_text(upload)
