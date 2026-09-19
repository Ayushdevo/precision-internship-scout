import unittest


class RegressionTest(unittest.TestCase):
    def test_display_uses_normalized_requirement_count(self):
        from pathlib import Path
        import ast
        source = (Path(__file__).resolve().parents[1] / 'app.py').read_text()
        tree = ast.parse(source)
        verdict = next(n.value for n in ast.walk(tree) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'verdict_text' for t in n.targets))
        result = eval(compile(ast.Expression(verdict), '<verdict>', 'eval'), {}, dict(matched_reqs=['Python'], missing_reqs=['SQL'], matched_str='Python', missing_str='SQL', job={'requirements':['Python','python','SQL','']}))
        self.assertIn('1 of 2 requirements', result)


if __name__ == "__main__":
    unittest.main()
