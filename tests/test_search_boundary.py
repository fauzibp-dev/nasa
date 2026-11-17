"""Offline tests for URL handoff boundary: all hosts and URLs are synthetic or public."""
import unittest

from tools.search_boundary import (
    EXTERNAL, INVALID, LISTED, classify_search_handoff, hostname_from_https,
)


class SearchBoundaryTests(unittest.TestCase):
    def test_exact_nasa_host_never_grants_permission(self):
        r = classify_search_handoff("https://www.nasa.gov/", "https://nasa.gov/search/?q=test")
        self.assertEqual(r["status"], LISTED)
        self.assertFalse(r["authorized_to_test"])
        self.assertEqual(r["destination_host"], "nasa.gov")

    def test_external_service_requires_separate_review(self):
        r = classify_search_handoff("https://www.nasa.gov/", "https://search.example.gov/results?q=demo")
        self.assertEqual(r["status"], EXTERNAL)
        self.assertFalse(r["authorized_to_test"])

    def test_hostname_suffix_is_not_nasa(self):
        r = classify_search_handoff("https://nasa.gov/", "https://nasa.gov.attacker.example/")
        self.assertEqual(r["status"], EXTERNAL)

    def test_fragments_userinfo_and_nonstandard_port_rejected(self):
        urls = [
            "http://nasa.gov/",
            "https://nasa.gov:8443/",
            "https://nasa.gov@attacker.example/",
            "https://someone:secret@nasa.gov/",
            "https://nasa.gov/#x",
            "https://127.0.0.1/",
            "https://localhost/",
            "javascript:alert(1)",
            " https://nasa.gov/",
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertIsNone(hostname_from_https(url))
                self.assertEqual(
                    classify_search_handoff("https://nasa.gov/", url)["status"], INVALID
                )

    def test_unlisted_source_is_invalid(self):
        r = classify_search_handoff("https://external.example/", "https://nasa.gov/")
        self.assertEqual(r["status"], INVALID)

    def test_query_is_not_returned_to_output(self):
        r = classify_search_handoff(
            "https://www.nasa.gov/", "https://other.example/search?q=DO_NOT_PRINT_ME"
        )
        self.assertEqual(r["destination_host"], "other.example")
        self.assertNotIn("DO_NOT_PRINT_ME", repr(r))


if __name__ == "__main__":
    unittest.main()
