"""LOCAL TRAINING ONLY: SQL injection contrasted with parameterized queries.

In-memory SQLite database with synthetic users, no internet access.
"""
from __future__ import annotations
import sqlite3


def make_lab_database() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE TABLE users (username TEXT NOT NULL)")
    connection.executemany(
        "INSERT INTO users (username) VALUES (?)", [("alice",), ("bob",)]
    )
    return connection


def vulnerable_user_lookup(connection: sqlite3.Connection, username: str) -> list[str]:
    """INTENTIONALLY BAD: SQL is constructed through untrusted string interpolation."""
    query = f"SELECT username FROM users WHERE username = '{username}' ORDER BY username"
    return [row[0] for row in connection.execute(query).fetchall()]


def secure_user_lookup(connection: sqlite3.Connection, username: str) -> list[str]:
    """Safe variant: bind parameters instead of interpolating SQL text."""
    return [
        row[0]
        for row in connection.execute(
            "SELECT username FROM users WHERE username = ? ORDER BY username",
            (username,),
        ).fetchall()
    ]
