import unittest


class RegressionTest(unittest.TestCase):
    def test_blank_uploads(self):
        from io import BytesIO
        from resume import extract_resume_text
        for data in (b'   \n', b'\xef\xbb\xbf'):
            upload = BytesIO(data)
            upload.name = 'cv.txt'
            with self.assertRaisesRegex(ValueError, 'non-whitespace'):
                extract_resume_text(upload)


if __name__ == "__main__":
    unittest.main()
