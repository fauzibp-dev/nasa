#!/usr/bin/env python3
"""Offline structure and common-secret checks for SANITIZED security reports.

This tool cannot prove the report is safe to publish or a vulnerability is valid.
Never publish unresolved vulnerabilities or private Bugcrowd evidence.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

REQUIRED_SECTIONS = (
    "Summary",
    "Scope and Authorization",
    "Reproduction",
    "Impact",
    "Remediation",
    "Disclosure",
)
SECRET_MARKERS = (
    ("private key", re.compile(r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("bearer token", re.compile(r"(?im)^\s*Authorization:\s*Bearer\s+\S+")),
)


def lint_report(markdown: str) -> list[str]:
    """Return report format issues; no networking or filesystem access."""
    issues: list[str] = []
    headings = {
        re.sub(r"\s+", " ", m.group(1).strip()).casefold()
        for m in re.finditer(r"^##\s+(.+?)\s*$", markdown, re.MULTILINE)
    }
    for section in REQUIRED_SECTIONS:
        if section.casefold() not in headings:
            issues.append(f"Missing required heading: ## {section}")
    for name, pattern in SECRET_MARKERS:
        if pattern.search(markdown):
            issues.append(f"Possible {name} in report: never commit real credentials")
    if len(markdown.strip()) < 200:
        issues.append("Report too short for meaningful reproduction and impact")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline sanitized report structure check")
    parser.add_argument("report", type=Path, help="Local sanitized Markdown file")
    args = parser.parse_args()
    try:
        body = args.report.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"ERROR: cannot read report: {error}")
        return 2
    issues = lint_report(body)
    if issues:
        for issue in issues:
            print(f"FAIL: {issue}")
        return 1
    print("PASS: basic report structure and marker checks")
    print("NOTE: This does NOT verify scope, validity, privacy, or publishability.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
