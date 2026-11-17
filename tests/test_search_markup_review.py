"""Offline, synthetic-only tests for HTML syntax review."""
import unittest

from tools.search_markup_review import review_source


class SearchMarkupReviewTests(unittest.TestCase):
    def test_search_contexts_and_engine_hint(self):
        source = """<!doctype html><html><head>
<title>Search Results for &quot;artemis&quot;</title></head><body>
<h1>Search Results for: <span>artemis</span></h1>
<div data-search-engine="vertex"></div>
<a href="/search/?search=artemis&amp;search_page=2">Page 2</a>
<form action="/?search=artemis"></form>
<script>const harmless = "other";</script>
</body></html>"""
        result = review_source(source, "artemis")
        self.assertEqual(result["counted_elements"]["title_text"], 1)
        self.assertEqual(result["counted_elements"]["h1_text"], 1)
        self.assertEqual(result["counted_elements"]["link_href"], 1)
        self.assertEqual(result["counted_elements"]["form_action"], 1)
        self.assertNotIn("inline_script", result["counted_elements"])
        self.assertEqual(result["public_engine_hints"], ["vertex"])
        self.assertEqual(result["network_requests"], 0)
        self.assertIn("UNDETERMINED", result["security_conclusion"])

    def test_detects_term_in_inline_script_but_does_not_claim_xss(self):
        result = review_source("<script>var query = 'artemis'</script>", "artemis")
        self.assertEqual(result["counted_elements"]["inline_script"], 1)
        self.assertIn("UNDETERMINED", result["security_conclusion"])

    def test_no_secrets_emitted_in_summary(self):
        raw = '<div data-attribution-token="sensitive-example"><h1>artemis</h1></div>'
        report = review_source(raw, "artemis")
        self.assertNotIn("sensitive-example", repr(report))

    def test_rejects_empty_term(self):
        with self.assertRaises(ValueError):
            review_source("<h1>test</h1>", "")


if __name__ == "__main__":
    unittest.main()
