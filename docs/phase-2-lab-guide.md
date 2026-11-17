# Phase 2: Three offline vulnerability demonstrations

This repo contains deliberately vulnerable and remediated implementations for three common web security classes:

| Class | Unsafe example | Safer pattern | Test |
|---|---|---|---|
| Broken object-level authorization (IDOR) | Return a record based only on an ID | Verify the requesting user's ownership | `tests/test_training_labs.py` |
| SQL injection | Interpolate untrusted data into SQL | Bind parameters in SQLite | `tests/test_training_labs.py` |
| Cross-site scripting (XSS) | Insert user text into HTML unsafely | Escape content for its HTML text context | `tests/test_xss_demo.py` |

## Run the exercises

```bash
python -m unittest discover -s tests -v
python -m unittest tests.test_xss_demo -v
python tools/report_lint.py examples/lab-report.md
python tools/report_lint.py examples/xss-lab-report.md
```

All exercises operate on synthetic local data. They create no listener, send no external requests, and never target NASA. Compare the vulnerable result with the fixed behavior and write a report describing **what you observed**, not speculation.

## Ethical research workflow

1. Finish the offline labs and confirm the complete CI suite is green.
2. Continue with legal PortSwigger Web Security Academy labs.
3. Read the **live** NASA policy and Bugcrowd engagement, including asset-level scope and prohibited activity.
4. Only if a real asset and intended technique are authorized, perform the minimum-impact research necessary, stop on sensitive data or unexpected access, and report privately through Bugcrowd.
5. Avoid calling a simulated lab finding a NASA vulnerability. Acceptance and recognition are NASA's decision.

**Report hygiene:** The examples are synthetic and may be public. Real unpatched third-party findings, account data, raw requests with secrets, and Bugcrowd case identifiers must never be committed to this public repository.
