"""LOCAL TRAINING ONLY: broken access control and a fixed implementation.

No HTTP server, no network requests, no production targets.
Data and account names are fictional.
"""
from __future__ import annotations

DOCUMENTS = {
    "doc-100": {"owner": "alice", "title": "Alice's demo record"},
    "doc-200": {"owner": "bob", "title": "Bob's demo record"},
}


def vulnerable_get_document(document_id: str, current_user: str) -> dict | None:
    """INTENTIONALLY BAD: ignores current_user and returns another user's data."""
    record = DOCUMENTS.get(document_id)
    return dict(record) if record else None


def secure_get_document(document_id: str, current_user: str) -> dict | None:
    """Safe variant: enforce ownership on every object access."""
    record = DOCUMENTS.get(document_id)
    if record is None or record["owner"] != current_user:
        return None
    return dict(record)
