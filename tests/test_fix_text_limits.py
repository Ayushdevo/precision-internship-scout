import unittest


class RegressionTest(unittest.TestCase):
    def test_text_limit_and_pdf_short_circuit(self):
        import sys
        from io import BytesIO
        from types import SimpleNamespace
        from unittest.mock import patch, Mock
        from resume import extract_resume_text, MAX_TEXT_CHARS
        upload = BytesIO(b'x' * (MAX_TEXT_CHARS + 1))
        upload.name = 'cv.txt'
        with self.assertRaisesRegex(ValueError, '100,000'):
            extract_resume_text(upload)
        upload.name = 'cv.pdf'
        later = Mock(side_effect=AssertionError('must stop before next page'))
        pages = [SimpleNamespace(extract_text=lambda: 'x' * (MAX_TEXT_CHARS + 1)), SimpleNamespace(extract_text=later)]
        with patch.dict(sys.modules, {'pypdf': SimpleNamespace(PdfReader=lambda _: SimpleNamespace(is_encrypted=False, pages=pages))}):
            with self.assertRaisesRegex(ValueError, '100,000'):
                extract_resume_text(upload)
        later.assert_not_called()


if __name__ == "__main__":
    unittest.main()
