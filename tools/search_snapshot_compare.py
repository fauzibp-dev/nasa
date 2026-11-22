#!/usr/bin/env python3
"""Compare two privately saved, benign search HTML snapshots, entirely OFFLINE.

This is context counting, NOT proof of XSS or permission to test any website.
Do not commit raw snapshots: they may contain transient tokens or user data.
Only safe counts and whitelisted engine hints are emitted.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

if __package__:
    from .search_markup_review import review_source
else:
    from search_markup_review import review_source


BENIGN_TERM = re.compile(r"[A-Za-z][A-Za-z0-9-]{4,79}\Z")
MAX_BYTES = 8 * 1024 * 1024


def compare_snapshots(first_html: str, second_html: str,
                      first_term: str, second_term: str) -> dict:
    """Compare literal text contexts. Never claim a vulnerability or permission."""
    for term in (first_term, second_term):
        if not isinstance(term, str) or not BENIGN_TERM.fullmatch(term):
            raise ValueError("Use only ordinary alphanumeric/hyphen search terms")
    if first_term.casefold() == second_term.casefold():
        raise ValueError("The terms must differ")
    if not isinstance(first_html, str) or not isinstance(second_html, str):
        raise ValueError("HTML snapshots must be text")
    first = review_source(first_html, first_term)
    second = review_source(second_html, second_term)
    # Cross-check terms against the opposite snapshot. Static articles can
    # contain the first search term even when the query itself has changed.
    old_term_in_second = review_source(second_html, first_term)
    new_term_in_first = review_source(first_html, second_term)
    found = sum(second["counted_elements"].values()) > 0
    return {
        "first_snapshot": {
            "context_counts": first["counted_elements"],
            "engine_hints": first["public_engine_hints"],
        },
        "second_snapshot": {
            "context_counts": second["counted_elements"],
            "engine_hints": second["public_engine_hints"],
        },
        "second_term_present": found,
        "cross_snapshot_context_counts": {
            "first_term_in_second_snapshot": old_term_in_second["counted_elements"],
            "second_term_in_first_snapshot": new_term_in_first["counted_elements"],
        },
        "interpretation": (
            "SECOND_BENIGN_TERM_OBSERVED__REFLECTION_POSSIBLE_NOT_PROVEN"
            if found else "SECOND_TERM_NOT_OBSERVED__NO_CONCLUSION"
        ),
        "network_requests": 0,
        "script_execution_tested": False,
        "vulnerability_confirmed": False,
        "warning": (
            "Static/article text may match either term; DOM or HTML text presence "
            "does not establish a taint flow, lack of escaping, or XSS."
        ),
    }


def read_private_snapshot(path: Path) -> str:
    size = path.stat().st_size
    if size > MAX_BYTES:
        raise ValueError("Snapshot exceeds the offline size limit")
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="OFFLINE benign search snapshot comparison (no HTTP requests)"
    )
    parser.add_argument("first_html", type=Path, help="Private baseline HTML file")
    parser.add_argument("second_html", type=Path, help="Private second HTML file")
    parser.add_argument("--first-term", default="artemis", help="Benign baseline search term")
    parser.add_argument("--second-term", required=True, help="Different benign search term")
    args = parser.parse_args()
    try:
        first = read_private_snapshot(args.first_html)
        second = read_private_snapshot(args.second_html)
        result = compare_snapshots(first, second, args.first_term, args.second_term)
    except (OSError, UnicodeError, ValueError):
        print("ERROR: invalid private snapshot(s) or benign search terms")
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    print("No actual security vulnerability is confirmed by this output.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
