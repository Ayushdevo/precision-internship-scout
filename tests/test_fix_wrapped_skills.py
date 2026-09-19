import unittest


class RegressionTest(unittest.TestCase):
    def test_wrapped_phrase(self):
        from scoring import compute_dynamic_match
        self.assertEqual(compute_dynamic_match(['Vector Databases'], 'Built Vector\n  Databases')[0], 100)
        self.assertEqual(compute_dynamic_match(['Vector Databases'], 'Vectorized Databases')[0], 0)


if __name__ == "__main__":
    unittest.main()
