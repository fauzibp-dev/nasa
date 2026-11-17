"""Offline checks for intentionally vulnerable and remediated HTML rendering."""
import unittest

from labs.xss_demo import safe_greeting, vulnerable_greeting


class XssTrainingTests(unittest.TestCase):
    def test_intentionally_vulnerable_rendering(self):
        payload = '<img src=x onerror=alert(1)>'
        self.assertIn(payload, vulnerable_greeting(payload))
        self.assertNotIn("<img", safe_greeting(payload))
        self.assertIn("&lt;img", safe_greeting(payload))

    def test_quotes_and_ampersands_are_escaped(self):
        rendered = safe_greeting('Anne & "Bob"')
        self.assertIn("Anne &amp; &quot;Bob&quot;", rendered)

    def test_regular_text_still_renders(self):
        self.assertEqual(safe_greeting("Alice"), "<p>Hello, Alice</p>")


if __name__ == "__main__":
    unittest.main()
