import unittest


class RegressionTest(unittest.TestCase):
    def test_language_boundaries(self):
        from scoring import compute_dynamic_match
        self.assertEqual(compute_dynamic_match(['C', 'C++', 'C#'], 'C++')[1:], (['C++'], ['C', 'C#']))
        self.assertEqual(compute_dynamic_match(['C'], 'C, Python')[0], 100)


if __name__ == "__main__":
    unittest.main()
