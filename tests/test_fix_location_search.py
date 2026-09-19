import unittest


class RegressionTest(unittest.TestCase):
    def test_location_search(self):
        from jobs import fetch_vetted_jobs
        self.assertEqual([j['company'] for j in fetch_vetted_jobs('  LONDON  ')], ['Google DeepMind'])
        self.assertEqual(fetch_vetted_jobs('Atlantis'), [])


if __name__ == "__main__":
    unittest.main()
