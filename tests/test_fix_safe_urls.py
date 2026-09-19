import unittest


class RegressionTest(unittest.TestCase):
    def test_malformed_urls(self):
        from rendering import safe_careers_url
        for url in ('https://example.com:bad/jobs', 'https://example.com:65536/jobs', 'https://exa\x00mple.com', 'https://example.com\\@evil.test'):
            self.assertIsNone(safe_careers_url(url))
        self.assertEqual(safe_careers_url('https://example.com:443/jobs'), 'https://example.com:443/jobs')


if __name__ == "__main__":
    unittest.main()
