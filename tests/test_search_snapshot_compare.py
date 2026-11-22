"""Tests use fictional HTML; no NASA network requests or live payloads."""
import unittest

from tools.search_snapshot_compare import compare_snapshots


FIRST = """<!doctype html><title>Results for &quot;artemis&quot;</title>
<h1>Search Results for: <span>artemis</span></h1>
<h3>Artemis mission content</h3>
<div data-search-engine="vertex"></div>
"""

SECOND = """<!doctype html><title>Results for &quot;OrbitStudy2026&quot;</title>
<h1>Search Results for: <span>OrbitStudy2026</span></h1>
<h3>Other unrelated article</h3>
<div data-search-engine="vertex"></div>
"""


class SearchSnapshotCompareTests(unittest.TestCase):
    def test_two_benign_terms_match_expected_text_contexts(self):
        result = compare_snapshots(FIRST, SECOND, "artemis", "OrbitStudy2026")
        self.assertTrue(result["second_term_present"])
        self.assertEqual(result["second_snapshot"]["context_counts"]["title_text"], 1)
        self.assertEqual(result["second_snapshot"]["context_counts"]["h1_text"], 1)
        self.assertEqual(result["second_snapshot"]["engine_hints"], ["vertex"])
        self.assertFalse(result["vulnerability_confirmed"])
        self.assertFalse(result["script_execution_tested"])
        self.assertEqual(result["network_requests"], 0)

    def test_search_term_not_observed_is_inconclusive(self):
        result = compare_snapshots(FIRST, FIRST, "artemis", "OrbitStudy2026")
        self.assertFalse(result["second_term_present"])
        self.assertIn("NO_CONCLUSION", result["interpretation"])

    def test_inline_script_is_not_automatically_vulnerable(self):
        result = compare_snapshots(
            FIRST, "<script>const q = 'OrbitStudy2026';</script>",
            "artemis", "OrbitStudy2026"
        )
        self.assertEqual(result["second_snapshot"]["context_counts"]["inline_script"], 1)
        self.assertFalse(result["vulnerability_confirmed"])

    def test_does_not_expose_raw_source_or_tokens(self):
        secret = "PRIVATE-ATTRIBUTION-VALUE"
        result = compare_snapshots(
            FIRST,
            '<div data-attribution-token="' + secret + '">OrbitStudy2026</div>',
            "artemis", "OrbitStudy2026"
        )
        self.assertNotIn(secret, repr(result))
        self.assertNotIn("OrbitStudy2026", repr(result))

    def test_rejects_exploit_like_terms(self):
        for term in ("<script>", "' OR 1=1 --", "", "a", "artemis"):
            with self.subTest(term=term):
                with self.assertRaises(ValueError):
                    compare_snapshots(FIRST, SECOND, "artemis", term)

    def test_rejects_same_term_case_insensitively(self):
        with self.assertRaises(ValueError):
            compare_snapshots(FIRST, SECOND, "artemis", "ARTEMIS")


if __name__ == "__main__":
    unittest.main()
