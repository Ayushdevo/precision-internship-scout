import unittest


class RegressionTest(unittest.TestCase):
    def test_unsafe_links_are_omitted(self):
        import csv
        from io import StringIO
        from exports import export_matches_csv
        from jobs import fetch_vetted_jobs
        jobs = fetch_vetted_jobs('')
        jobs[0]['target_link'] = 'javascript:alert(1)'
        rows = list(csv.DictReader(StringIO(export_matches_csv(jobs, 'Python'))))
        self.assertEqual(rows[0]['careers_url'], '')
        self.assertTrue(rows[1]['careers_url'].startswith('https://'))


if __name__ == "__main__":
    unittest.main()
