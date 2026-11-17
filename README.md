# NASA VDP Research Workspace

[![CI](https://github.com/fauzibp-dev/nasa/actions/workflows/ci.yml/badge.svg)](https://github.com/fauzibp-dev/nasa/actions/workflows/ci.yml)

**Independent security research and learning portfolio. Not affiliated with, sponsored by, or endorsed by NASA.**

This repository supports **authorized, responsible vulnerability research** and clear disclosure reports. It is a *workspace*, not proof of having discovered a NASA vulnerability or received an award.

## Current status
- Workspace and documentation: started 2026-11-18.
- External NASA targets tested: **none**.
- Valid NASA reports submitted: **none**.
- NASA Letter of Recognition received: **none**.

## Quick start

Requires Python 3.10+. The offline scope reminder makes **no network requests**.

```bash
python -m unittest discover -s tests -v
python tools/scope_guard.py https://example.org
```

`scope.txt` is intentionally empty, so the command above says **DENIED**. An approved hostname must be **manually verified against the current, live program scope** before being placed in the scope file. A hostname being present in the file is *not* legal authorization.

## Official policies and references

- [NASA Vulnerability Disclosure Policy](https://www.nasa.gov/vulnerability-disclosure-policy/) — version 1.6.2, dated April 30, 2026 (checked 2026-11-18)
- [NASA Bugcrowd engagement](https://bugcrowd.com/engagements/nasa-vdp) — **official report channel**, review current engagement targets and rules
- [PortSwigger Web Security Academy](https://portswigger.net/web-security) — legal training labs
- [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) — deliberately vulnerable practice application

**Authorization:** NASA says testing is allowed only on *listed in-scope targets*, and third-party services aren't automatically included. Some test types are explicitly prohibited. Read both official sources immediately before doing any research. Don't scan all `*.nasa.gov`, do credential attacks, or test outside scope. See [scope/safety checklist](docs/scope-and-safety.md).

**Disclosure:** Stop immediately after confirming a vulnerability or encountering sensitive data. Report real NASA findings privately through Bugcrowd, never via a public GitHub issue. The policy asks researchers to refrain from public disclosure for 90 days unless otherwise coordinated.

**Recognition:** NASA offers a possible Letter of Recognition (LOR) only for accepted, validated, fixed P1–P4 findings (excluding duplicates/known issues); **not a guaranteed certificate or payment**.

## Repository layout

| Path | Purpose |
|---|---|
| `docs/scope-and-safety.md` | Pre-engagement authorization checklist |
| `docs/report-template.md` | Private report format |
| `docs/learning-plan.md` | Four-week practice roadmap |
| `docs/research-playbook.md` | Structured lab-to-disclosure workflow |
| `docs/project-tracker.md` | Work plan and acceptance gates |
| `docs/threat-model.md` | Data handling and operational risks |
| `docs/recognition.md` | NASA award eligibility and evidence |
| `scope.txt` | **Empty** exact-host allowlist, never a permission grant |
| `tools/scope_guard.py` | Offline, exact-host scope reminder |
| `tools/report_lint.py` | Offline sanitized report structure checker |
| `tests/` | Automated unit tests; no network traffic |
| `.github/workflows/ci.yml` | Offline Python checks on pushes and PRs |

## Verify

```bash
python -m unittest discover -s tests -v
python tools/report_lint.py examples/lab-report.md
```

The example is fabricated training content only; it does not claim a real NASA vulnerability.

## Public repository safety

Never commit real vulnerability proof-of-concept for unpatched services, raw HTTP traces containing live credentials, secrets, private user data, official Bugcrowd report details, or NASA non-public data. Keep report drafts and evidence in private, access-controlled storage. See [SECURITY.md](SECURITY.md).

## Legacy starter migration
The initial files were migrated from a separate GitHub practice branch. The original practice repository is left unchanged; subsequent improvements live here.
