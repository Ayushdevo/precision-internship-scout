import unittest


class RegressionTest(unittest.TestCase):
    def test_failed_parse_has_no_success_badge(self):
        import ast
        from pathlib import Path
        from types import SimpleNamespace
        tree = ast.parse((Path(__file__).resolve().parents[1] / 'app.py').read_text())
        branch = next(n for n in ast.walk(tree) if isinstance(n, ast.If) and ast.unparse(n.test) == 'resume_file is not None')
        calls = []
        ns = dict(resume_file=object(), extract_resume_text=lambda _: '', st=SimpleNamespace(markdown=lambda *a, **k: calls.append(a)))
        exec(compile(ast.Module(body=branch.body, type_ignores=[]), '<upload>', 'exec'), ns)
        self.assertEqual(calls, [])
        ns['extract_resume_text'] = lambda _: 'Python'
        exec(compile(ast.Module(body=branch.body, type_ignores=[]), '<upload>', 'exec'), ns)
        self.assertEqual(len(calls), 1)


if __name__ == "__main__":
    unittest.main()
