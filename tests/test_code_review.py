"""Tests for read-only, non-network pattern review."""
import unittest

from tools.code_review import review_python


class CodeReviewTests(unittest.TestCase):
    def test_dynamic_code_is_flagged(self):
        source = "result = eval(value)"
        self.assertIn("DYNAMIC_CODE", [x.rule for x in review_python(source)])

    def test_shell_true_is_flagged(self):
        source = "import subprocess\nsubprocess.run('echo hello', shell=True)"
        self.assertIn("SHELL_TRUE", [x.rule for x in review_python(source)])

    def test_direct_dynamic_sql_is_flagged(self):
        source = "def query(conn, value):\n    return conn.execute(f\"SELECT * FROM t WHERE id = '{value}'\")"
        self.assertIn("DYNAMIC_SQL", [x.rule for x in review_python(source)])

    def test_parameterized_sql_not_flagged(self):
        source = "def query(conn, value):\n    return conn.execute('SELECT * FROM t WHERE id = ?', (value,))"
        self.assertEqual(review_python(source), [])

    def test_pickle_is_flagged(self):
        source = "import pickle\nvalue = pickle.loads(blob)"
        self.assertIn("UNSAFE_DESERIALIZATION", [x.rule for x in review_python(source)])


if __name__ == "__main__":
    unittest.main()
