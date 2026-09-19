import unittest


class RegressionTest(unittest.TestCase):
    def test_compatibility_characters(self):
        from scoring import compute_dynamic_match
        self.assertEqual(compute_dynamic_match(['Python', 'Ｐｙｔｈｏｎ'], 'ＰＹＴＨＯＮ')[0], 100)
        self.assertEqual(len(compute_dynamic_match(['Python', 'Ｐｙｔｈｏｎ'], 'python')[1]), 1)


if __name__ == "__main__":
    unittest.main()
