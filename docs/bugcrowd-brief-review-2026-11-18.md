# NASA Bugcrowd engagement: research brief review (2026-11-18)

**Source and status:** This document is based on a user-provided text copy of the public NASA Bugcrowd engagement shown on 2026-11-18. The copied page labels its last update **2026-05-01 20:24:52 UTC**. It is a **snapshot, not a live authorization token**. The Bugcrowd page could not be independently inspected in full without its rendered engagement content. Re-check the live engagement before any real research.

- NASA engagement: https://bugcrowd.com/engagements/nasa-vdp
- NASA official VDP (version 1.6.2, April 30, 2026): https://www.nasa.gov/vulnerability-disclosure-policy/
- Repository visibility: **PUBLIC**. Never record an undisclosed issue or sensitive artifacts here.
- Current research decision: **NO-GO for active external testing** until the exact asset, service, environment, and proposed technique are checked against the live program rules.
- No NASA target has been scanned or tested as part of creating this review.

## A. Listed targets in the supplied Bugcrowd copy

| Target website / scope row | Hostname(s) shown in supplied Bugcrowd table | Assessment |
|---|---|---|
| NASA (one website entry) | `nasa.gov` and `www.nasa.gov` | Same website entry with root and www forms; verify live |
| USGEO | `usgeo.gov` | Listed in supplied snapshot; verify live |
| GLOBE | `globe.gov` | Listed in supplied snapshot; verify live |

**Count clarification:** The user-provided Bugcrowd table contains **three website entries**, not four independent website targets. The NASA entry displays both `nasa.gov` and `www.nasa.gov`, which are **two hostnames associated with one listed website**. This distinction does not broaden authorization for other subdomains, services or test types.

The pasted brief says listed targets and **their subdomains within defined scope** may be tested, while separately saying **unlisted services are not authorized**. Interpret conservatively: the hostname alone does not authorize an unspecified connected service, third-party system, particular environment or test technique. Do not treat `*.nasa.gov` or any arbitrary subdomain as automatically permitted.

### Important source discrepancy

NASA's general policy page (as read on 2026-11-18) names `nasa.gov`, `usgeo.gov`, `globe.gov`, `nspires.nasaprs.com` and `nsc.nasa.gov` under its systems section. The **supplied Bugcrowd Scope table did not list `nspires.nasaprs.com` or `nsc.nasa.gov`**. These additional entries must **not** be added to a testing allowlist based only on the general policy page. Ask Bugcrowd/NASA to clarify any mismatch before testing.

Do not copy any of the above names automatically into `scope.txt`. The file stays intentionally empty until manual, current, target-specific validation.

## B. Explicit exclusions from the supplied brief

The pasted brief lists these testing/report classes as not authorized or not eligible:

- Social engineering; denial of service, rate-limit abuse or spamming; attacks requiring physical access.
- Clickjacking on pages without sensitive actions; content spoofing/text injection.
- Reports involving the endpoints `/wp-json/wp/v2/users` or `xmlrpc.php`.
- Known vulnerable libraries or versions **without a working exploitability demonstration**; scanner-only output without exploitability evidence; version disclosure alone.
- Missing best practices (e.g. missing CAPTCHA or security headers) without a consequential flaw; insecure TLS/cipher/cert observations; security headers without direct vulnerability impact.
- Form autocomplete observation; weak cookie flags on non-sensitive cookies; directory listing.
- Host-header injection claims without a demonstrated path to theft of user data.
- Old-browser-only issues; verbose/descriptive error messages; non-technical observations.

This is a condensed review, **not an exhaustive replacement for the current official brief**. Neither the pasted scope nor these exclusions guarantee that any unlisted technique is permitted.

## C. Operational constraints: all gates must pass

- [ ] Open the official, current Bugcrowd program details under the account used for disclosure.
- [ ] Record the live policy review timestamp **privately**; identify the exact target and its specific service.
- [ ] Confirm the target's administrative ownership, in-scope status, exclusions, and environmental restrictions; no third-party/internally accessible services.
- [ ] If an authorized non-production or public test environment exists, **test only in that environment**, not production.
- [ ] Confirm the method is explicitly permitted, low-impact, and does not create denial of service, spam, credential attacks, data transfer or user harm.
- [ ] If the intended target, service, technique, or scope is unclear, **do not test**; ask the NASA VDP contact/Bugcrowd support.
- [ ] Use only owned test identities and synthetic data if allowed; **stop immediately** on confirmation or any sensitive/private data.
- [ ] Keep details confidential. Send actual findings **privately** via the official NASA Bugcrowd engagement; do not create a public GitHub issue.

The NASA policy requires limited proof, prohibits exfiltration/persistence/lateral movement and requests that issues be reported promptly. Keep confidential for the policy-requested 90 days from submission **and until disclosure permission is explicitly granted** under the engagement terms. If those requirements differ, follow the stricter applicable rule or ask the program.

## D. Report and recognition gates

- The pasted page advertises expedited Bugcrowd triage and says NASA will acknowledge receipt within **three business days**. This is not a guaranteed time-to-fix or a promised reward.
- Useful reports explain the precise vulnerability, exact affected asset, minimum steps to reproduce, actual impact, and appropriate redacted evidence. English is preferred if possible.
- NASA offers no cash payout through this VDP.
- A **Letter of Recognition (LOR)** is available only for a **P1–P4** report that is **validated, accepted and confirmed fixed**. Duplicates and previously known issues are excluded. A submission, triage acknowledgment, or fictional lab does not qualify.
- Public portfolio recognition must be supported by a genuine NASA-issued artifact and any needed disclosure authorization.

## E. Safe next step

Continue the repository's offline IDOR, SQL injection and XSS labs; use authorized PortSwigger training labs. **No active NASA testing is initiated by this repository or its CI.** A researcher may separately verify the live brief and then choose low-impact, expressly permitted work. Keep live findings outside this public repo.

### Research status

| Event | Status as of 2026-11-18 |
|---|---|
| Bugcrowd text snapshot reviewed | Completed |
| NASA general VDP independently read | Completed |
| Current authenticated Bugcrowd scope, service-level authorization | **Pending** |
| Live NASA testing | **Not performed** |
| Accepted NASA report or issued NASA LOR | **None documented** |
