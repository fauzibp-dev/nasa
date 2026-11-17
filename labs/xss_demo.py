"""Offline XSS teaching example: unsafe HTML output vs correct escaping.

This module renders strings only. It opens no browser, starts no server,
sends no requests and contains no actual attack against a live service.
"""
from html import escape


def vulnerable_greeting(name: str) -> str:
    """INTENTIONALLY UNSAFE for demonstration: inserts untrusted HTML."""
    return f"<p>Hello, {name}</p>"


def safe_greeting(name: str) -> str:
    """Escape user-provided content before adding it to an HTML text node."""
    return f"<p>Hello, {escape(name, quote=True)}</p>"
