# Lab Report: Insecure Direct Object Reference (SYNTHETIC EXAMPLE)

TRAINING LAB ONLY. This is fictional and not a discovery on NASA or any third party.

## Summary

The intentionally vulnerable local example `labs/idor_demo.py` fails to verify object ownership before returning a demo record. This lets one simulated user see another simulated user's sample record. The secure variant checks ownership and returns no data for unauthorized access.

## Scope and Authorization

The target is a local, deliberately vulnerable Python function in this repository. Testing does not touch any remote service, other users, or NASA infrastructure. The data contains only fictional names and generated identifiers.

## Reproduction

1. Run `python -m unittest tests.test_training_labs -v` locally.
2. Observe that `vulnerable_get_document("doc-200", "alice")` returns a record whose owner is `bob`.
3. Observe that `secure_get_document("doc-200", "alice")` returns `None`.
4. Repeat with the authorized `doc-100` record and confirm the secure function returns Alice's own data.

## Impact

In a real application, missing authorization checks could expose another user's data. Here the outcome is limited to harmless in-memory synthetic records. No real-world impact or NASA vulnerability is claimed.

## Remediation

Apply an authorization check for every record lookup based on the authenticated user's identity and the server-side access-control policy. Add regression tests to prove cross-user objects are blocked.

## Disclosure

No external system is involved. Nothing was submitted to NASA or Bugcrowd, and no public acknowledgement has been received. This report is a portfolio example for an isolated lab only.
