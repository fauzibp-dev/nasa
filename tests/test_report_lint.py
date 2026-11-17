"""Offline report format checks (no real findings or secrets)."""
from pathlib import Path
import unittest

from tools.report_lint import lint_report


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = (ROOT / "examples" / "lab-report.md").read_text(encoding="utf-8")


class ReportLintTests(unittest.TestCase):
    def test_example_passes(self):
        self.assertEqual(lint_report(EXAMPLE), [])

    def test_missing_section_fails(self):
        text = EXAMPLE.replace("## Remediation", "## Another section")
        self.assertTrue(any("Remediation" in issue for issue in lint_report(text)))

    def test_private_key_is_rejected(self):
        text = EXAMPLE + "\n-----BEGIN PRIVATE KEY-----\nFAKE\n"
        self.assertTrue(any("private key" in issue for issue in lint_report(text)))

    def test_authorization_header_is_rejected(self):
        text = EXAMPLE + "\nAuthorization: Bearer something-secret\n"
        self.assertTrue(any("bearer token" in issue for issue in lint_report(text)))


if __name__ == "__main__":
    unittest.main()
