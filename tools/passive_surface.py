#!/usr/bin/env python3
"""Offline review of public website surface observations; NEVER accesses target hosts.

This tool organizes user-confirmed scope entries and public homepage features.
It is *not* a vulnerability scanner, authorization oracle or exploit tester.
"""
from __future__ import annotations
import argparse
import ipaddress
import json
from pathlib import Path
from urllib.parse import urlsplit

DEFAULT_INVENTORY = Path(__file__).resolve().parent.parent / "research" / "passive-surface-2026-11-18.json"


def safe_hostname(url: str) -> str | None:
    """Parse a standard HTTPS hostname without performing network I/O."""
    if not isinstance(url, str) or not url or url != url.strip():
        return None
    try:
        value = urlsplit(url)
        if value.scheme != "https" or not value.netloc or value.fragment:
            return None
        if value.username is not None or value.password is not None:
            return None
        if value.port not in (None, 443):
            return None
        host = value.hostname
        if host is None or host.startswith(".") or host.endswith("."):
            return None
        host = host.encode("idna").decode("ascii").lower()
        try:
            ipaddress.ip_address(host)
            return None
        except ValueError:
            pass
        labels = host.split(".")
        if len(labels) < 2 or len(host) > 253:
            return None
        if not all(
            1 <= len(label) <= 63 and label[0].isalnum() and label[-1].isalnum()
            and all(char.isascii() and (char.isalnum() or char == "-") for char in label)
            for label in labels
        ):
            return None
        return host
    except (ValueError, UnicodeError):
        return None


def summarize_inventory(data: dict) -> list[dict]:
    """Return passive review rows; exact host matches never imply testing permission."""
    entries = data.get("program_entries", [])
    if not isinstance(entries, list) or len(entries) != 3:
        raise ValueError("Expected three scope-table website entries")
    known: dict[str, str] = {}
    for item in entries:
        target = item["target"]
        if not isinstance(target, str) or not target:
            raise ValueError("Target name required")
        for host in item["hostnames_in_supplied_brief"]:
            if safe_hostname("https://" + host) != host:
                raise ValueError("Invalid exact hostname in supplied snapshot")
            if host in known and known[host] != target:
                raise ValueError("Hostname claimed by multiple entries")
            known[host] = target
    rows = []
    for feature in data.get("passive_features", []):
        host = safe_hostname(feature["public_url"])
        if host is None:
            raise ValueError("Public URL must be a strict HTTPS DNS URL")
        rows.append({
            "target": feature["target"],
            "host": host,
            "feature": feature["feature"],
            "status": "EXACT_HOST_IN_SNAPSHOT__METHOD_UNVERIFIED"
                      if known.get(host) == feature["target"]
                      else "SERVICE_AND_HOST_REVIEW_REQUIRED",
            "active_testing_authorized": False,
        })
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="OFFLINE feature inventory (never scans)")
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    args = parser.parse_args()
    try:
        inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
        rows = summarize_inventory(inventory)
    except (OSError, UnicodeError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: invalid local inventory: {exc}")
        return 2
    print("PUBLIC FEATURES ONLY; NO ACTIVE NASA SECURITY TESTING")
    print("Target | Host | Feature | Review status")
    print("--- | --- | --- | ---")
    for row in rows:
        print(f"{row['target']} | {row['host']} | {row['feature']} | {row['status']}")
    print("RESULT: 0 validated vulnerabilities, 0 reports; verify the live Bugcrowd policy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
