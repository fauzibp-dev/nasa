"""No-network regression tests for the passive site inventory."""
import json
from pathlib import Path
import unittest

from tools.passive_surface import safe_hostname, summarize_inventory


INVENTORY = json.loads((Path(__file__).resolve().parents[1] / "research" /
                        "passive-surface-2026-11-18.json").read_text(encoding="utf-8"))


class PassiveSurfaceTests(unittest.TestCase):
    def test_three_program_entries_and_five_observations(self):
        self.assertEqual(len(INVENTORY["program_entries"]), 3)
        rows = summarize_inventory(INVENTORY)
        self.assertEqual(len(rows), 5)
        self.assertTrue(all(r["active_testing_authorized"] is False for r in rows))

    def test_known_exact_host_still_requires_method_review(self):
        rows = summarize_inventory(INVENTORY)
        nasa = next(r for r in rows if r["target"] == "NASA website")
        self.assertEqual(nasa["host"], "www.nasa.gov")
        self.assertEqual(nasa["status"], "EXACT_HOST_IN_SNAPSHOT__METHOD_UNVERIFIED")

    def test_www_globe_redirect_not_automatically_added(self):
        rows = summarize_inventory(INVENTORY)
        globe = next(r for r in rows if r["target"] == "GLOBE website")
        self.assertEqual(globe["status"], "SERVICE_AND_HOST_REVIEW_REQUIRED")

    def test_exact_host_parsing_rejects_bypasses(self):
        bad = (
            "http://nasa.gov/", "https://nasa.gov.evil.example/",
            "https://nasa.gov@evil.example/", "https://nasa.gov:8443/",
            "https://nasa.gov/#secret", "https://127.0.0.1/",
            "https://localhost/", " https://nasa.gov/",
        )
        for url in bad:
            host = safe_hostname(url)
            if url == "https://nasa.gov.evil.example/":
                self.assertEqual(host, "nasa.gov.evil.example")
            elif url == "https://nasa.gov@evil.example/":
                self.assertIsNone(host)
            else:
                self.assertIsNone(host, url)

    def test_unlisted_host_never_authorized(self):
        data = json.loads(json.dumps(INVENTORY))
        data["passive_features"].append({
            "target": "NASA website",
            "public_url": "https://external.example/",
            "feature": "Never assumed in scope",
        })
        self.assertEqual(summarize_inventory(data)[-1]["status"], "SERVICE_AND_HOST_REVIEW_REQUIRED")


if __name__ == "__main__":
    unittest.main()
