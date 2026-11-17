#!/usr/bin/env python3
"""Offline AST-based Python review: patterns to manually inspect, NOT proven bugs.

Only reads files on disk. Makes no connections to remote hosts, NASA, or Bugcrowd.
"""
from __future__ import annotations

import argparse
import ast
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    file: str
    line: int
    rule: str
    detail: str


def call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        left = call_name(node.value)
        return f"{left}.{node.attr}" if left else node.attr
    return ""


def review_python(source: str, filename: str = "<string>") -> list[Finding]:
    tree = ast.parse(source, filename=filename)
    found: list[Finding] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = call_name(node.func)
        if name in {"eval", "exec", "builtins.eval", "builtins.exec"}:
            found.append(Finding(filename, node.lineno, "DYNAMIC_CODE",
                                 "Dynamic code execution requires explicit trusted-input review."))
        if name in {"pickle.loads", "pickle.load", "marshal.loads", "marshal.load"}:
            found.append(Finding(filename, node.lineno, "UNSAFE_DESERIALIZATION",
                                 "Do not deserialize untrusted bytes with this API."))
        if name in {"subprocess.run", "subprocess.call", "subprocess.Popen", "subprocess.check_output"}:
            if any(
                keyword.arg == "shell"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in node.keywords
            ):
                found.append(Finding(filename, node.lineno, "SHELL_TRUE",
                                     "Review whether attacker input reaches a shell command."))
        # Only trivial direct interpolations; indirect dynamic SQL requires manual review.
        if name.endswith(".execute") and node.args:
            expr = node.args[0]
            if isinstance(expr, (ast.JoinedStr, ast.BinOp)):
                found.append(Finding(filename, node.lineno, "DYNAMIC_SQL",
                                     "SQL string construction may require parameter binding."))
    return sorted(found, key=lambda item: (item.line, item.rule))


def review_path(path: Path) -> list[Finding]:
    files = sorted(path.rglob("*.py")) if path.is_dir() else [path]
    results: list[Finding] = []
    for item in files:
        try:
            results.extend(review_python(item.read_text(encoding="utf-8"), str(item)))
        except (OSError, UnicodeError, SyntaxError) as error:
            results.append(Finding(str(item), 0, "READ_OR_PARSE_ERROR", str(error)))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline heuristic Python code review")
    parser.add_argument("path", type=Path, help="A local .py file or directory")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any pattern is flagged")
    args = parser.parse_args()
    results = review_path(args.path)
    print(json.dumps([asdict(finding) for finding in results], indent=2))
    print(f"Review flags: {len(results)} (heuristics only; not validated vulnerabilities)")
    return 1 if (args.strict and results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
