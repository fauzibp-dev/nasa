#!/usr/bin/env python3
"""Offline NASA search-handoff hostname review.

NO network, browser automation, payload delivery, authentication or scanning.
Reads only provided URLs and prints NO path, query, fragment, or credentials.
An exact-host match is NOT permission to test an application or technique.
"""
from __future__ import annotations

import argparse
import ipaddress
from urllib.parse import urlsplit

NASA_ENTRY_HOSTS = frozenset({"nasa.gov", "www.nasa.gov"})
INVALID = "INVALID_OR_UNSAFE_URL"
EXTERNAL = "EXTERNAL_HOST_NOT_AUTOMATICALLY_AUTHORIZED"
LISTED = "LISTED_HOST__SERVICE_AND_METHOD_STILL_REQUIRE_REVIEW"


def hostname_from_https(url: str) -> str | None:
    """Return normalized DNS name from strict HTTPS URL; never makes a request."""
    if not isinstance(url, str) or not url or url != url.strip():
        return None
    try:
        parsed = urlsplit(url)
        if parsed.scheme != "https" or not parsed.netloc:
            return None
        if parsed.username is not None or parsed.password is not None:
            return None
        # A fragment is a client-side value and is not needed for this check.
        if parsed.fragment or parsed.port not in (None, 443):
            return None
        host = parsed.hostname
        if not host or host.startswith(".") or host.endswith("."):
            return None
        host = host.encode("idna").decode("ascii").lower()
        if len(host) > 253:
            return None
        labels = host.split(".")
        if len(labels) < 2:
            return None
        if not all(
            1 <= len(label) <= 63
            and label[0].isascii() and label[0].isalnum()
            and label[-1].isascii() and label[-1].isalnum()
            and all(c.isascii() and (c.isalnum() or c == "-") for c in label)
            for label in labels
        ):
            return None
        try:
            ipaddress.ip_address(host)
        except ValueError:
            return host
        return None
    except (ValueError, UnicodeError):
        return None


def classify_search_handoff(start_url: str, destination_url: str) -> dict[str, str | bool]:
    """Classification is only a scope reminder, not permission or a bug report."""
    source = hostname_from_https(start_url)
    dest = hostname_from_https(destination_url)
    if source is None or dest is None:
        return {"source_host": source or "<invalid>", "destination_host": dest or "<invalid>",
                "status": INVALID, "authorized_to_test": False}
    if source not in NASA_ENTRY_HOSTS:
        return {"source_host": source, "destination_host": dest,
                "status": INVALID, "authorized_to_test": False}
    return {
        "source_host": source,
        "destination_host": dest,
        "status": LISTED if dest in NASA_ENTRY_HOSTS else EXTERNAL,
        "authorized_to_test": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="OFFLINE host-boundary review of ordinary NASA search navigation"
    )
    parser.add_argument("source", help="Starting page URL (e.g., https://www.nasa.gov/)")
    parser.add_argument("destination", help="Destination URL copied from normal navigation; avoid secrets")
    args = parser.parse_args()
    row = classify_search_handoff(args.source, args.destination)
    print(f"Starting host: {row['source_host']}")
    print(f"Destination host: {row['destination_host']}")
    print(f"Status: {row['status']}")
    print("Authorized to conduct active security tests: NO (verify current program and service)")
    print("This tool does not send requests or evaluate whether a vulnerability exists.")
    return 2 if row["status"] == INVALID else 0


if __name__ == "__main__":
    raise SystemExit(main())
