#!/usr/bin/env python3
"""Offline-only HTML context inventory for a benign public search term.

No network traffic, browser testing, or exploitation. This is NOT an XSS test.
Never commit unredacted website HTML containing transient tokens or form data.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

VOID = frozenset({
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
})


class SearchMarkupReview(HTMLParser):
    """Count term occurrences in syntax contexts, NOT proven reflections."""

    def __init__(self, term: str):
        if not isinstance(term, str) or not term or len(term) > 100:
            raise ValueError("A nonempty benign term up to 100 characters is required")
        super().__init__(convert_charrefs=True)
        self.term = term.casefold()
        self.stack: list[str] = []
        self.counts: Counter[str] = Counter()
        self.engine_hints: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name == "data-search-engine" and value in {"vertex", "searchgov"}:
                self.engine_hints.add(value)
            if not isinstance(value, str) or self.term not in value.casefold():
                continue
            if tag == "a" and name == "href":
                category = "link_href"
            elif tag == "form" and name == "action":
                category = "form_action"
            elif tag == "meta" and name == "content":
                category = "meta_content"
            elif tag == "input" and name == "value":
                category = "input_value"
            elif name in {"src", "alt"}:
                category = "asset_or_image_metadata"
            else:
                category = "other_attribute"
            self.counts[category] += 1
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag in self.stack:
            match_from_end = self.stack[::-1].index(tag)
            self.stack = self.stack[:len(self.stack) - 1 - match_from_end]

    def handle_data(self, data: str) -> None:
        if self.term not in data.casefold():
            return
        if "script" in self.stack:
            category = "inline_script"
        elif "style" in self.stack:
            category = "inline_style"
        elif "title" in self.stack:
            category = "title_text"
        elif "h1" in self.stack:
            category = "h1_text"
        else:
            category = "other_text"
        self.counts[category] += 1


def review_source(source: str, term: str) -> dict:
    parser = SearchMarkupReview(term)
    parser.feed(source)
    parser.close()
    return {
        "counted_elements": dict(sorted(parser.counts.items())),
        "public_engine_hints": sorted(parser.engine_hints),
        "network_requests": 0,
        "security_conclusion": "UNDETERMINED: benign-source context inventory is not an XSS test",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Local-only HTML syntax context review")
    parser.add_argument("html_file", type=Path, help="Private HTML snapshot, never committed")
    parser.add_argument("--term", default="artemis", help="Benign term to count (not printed)")
    args = parser.parse_args()
    try:
        if args.html_file.stat().st_size > 8 * 1024 * 1024:
            raise ValueError("Private HTML too large")
        report = review_source(args.html_file.read_text(encoding="utf-8"), args.term)
    except (OSError, UnicodeError, ValueError):
        print("ERROR: could not parse the local HTML file or term")
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    print("Do not publish private source snapshots or report as a vulnerability.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
