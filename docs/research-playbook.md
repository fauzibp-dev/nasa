# Research playbook: from lab to responsible disclosure

This is a **process document**, not authorization to test any NASA system. NASA's live [Bugcrowd VDP](https://bugcrowd.com/engagements/nasa-vdp) and [policy](https://www.nasa.gov/vulnerability-disclosure-policy/) always take precedence.

## Phase A — local skills and baseline

1. Complete the repository's offline IDOR and SQLi labs.
2. Run `python -m unittest discover -s tests -v`.
3. Complete PortSwigger Web Security Academy's access-control, authentication, XSS, SQLi, and business-logic beginner labs.
4. For each lab write a sanitized summary of the vulnerable behavior, root cause, impact, and remediation.
5. Do not confuse vulnerable training examples with real discoveries or publish any real secrets.

## Phase B — policy and scope gate (mandatory)

Before researching ANY external asset:

1. Sign in to the appropriate engagement and read every scope item and exclusion.
2. Confirm a given hostname and *specific app/service* is listed in scope. A parent domain or similarly named service is NOT enough.
3. Understand allowed test categories and banned test types. When in doubt, ask the program via the proper support channel.
4. Record the UTC date of scope verification, the exact host, and an immutable reference to the relevant rules in a private log.
5. Confirm the test is not likely to affect users, availability, or NASA missions; **if a non-production or public test environment is available, NASA requires all testing exclusively there**.
6. Do not perform network probing from this repository's CI. `scope_guard.py` is merely an offline deny-by-default reminder.

**NO-GO** if scope is uncertain, third-party owned, sensitive data may be affected, or the program disallows the proposed method.

## Phase C — non-destructive review

- Prefer manual evaluation of permitted, low-impact app behavior and documented interfaces.
- Inspect access-control boundaries using only self-owned test accounts and synthetic test data if allowed.
- Avoid external scanning, credential attempts, user enumeration, rate-limit exhaustion, mail flooding, scraping, and high-impact automated exploitation.
- Use the minimal amount of interaction necessary to verify an issue; stop immediately after verification or seeing sensitive data.

## Phase D — private triage

Check:
- Is this truly a security boundary, not expected functionality?
- Can it be reproduced with the minimum-impact steps?
- What is the factual impact, and what is only hypothetical?
- Does it appear to be a duplicate or known issue? Availability of known-issue info may require Bugcrowd sign-in.
- Is all recorded evidence redacted and stored privately, not publicly in GitHub?

## Phase E — private report submission

Submit via the official NASA Bugcrowd VDP, in English when practical. Include exact scope, concrete steps, observed vs expected behavior, severity rationale, redacted evidence, and suggested remediation. Do NOT file real findings as public GitHub issues.

NASA's policy says it aims to acknowledge within **three business days**. Follow the actual status through Bugcrowd; this is not a guarantee of report validity.

## Phase F — remediation and recognition

- Cooperate with triage and provide requested clarifications, without exceeding testing authorization.
- Do not publicly disclose reports for at least the policy-requested **90 days after initial submission** unless otherwise coordinated. Longer delay may be necessary.
- Avoid falsely claiming a valid finding, payout, or recognition based on a submitted but unresolved report.
- NASA LOR eligibility requires a validated and accepted P1–P4 report confirmed fixed, excluding duplicates and known issues.
- Publish any acknowledgement **only after issued**, and redact private case details.

## Stop triggers

Stop and notify the program immediately when you see sensitive/private data, impact to others, unexpected access, service instability, or scope uncertainty.

## Sources and review date

- https://www.nasa.gov/vulnerability-disclosure-policy/ (v1.6.2, April 30 2026; reviewed 2026-11-18)
- https://bugcrowd.com/engagements/nasa-vdp (review live brief at each new engagement)
- https://docs.bugcrowd.com/researchers/participating-in-program/reviewing-bounty-briefs/
