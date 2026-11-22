# NASA VDP project tracker

Date initialized: 2026-11-18. No claim of NASA authorization beyond the program's written policy or of finding vulnerabilities.

## Engineering acceptance criteria

- [x] Migrate starter documentation and source code to `fauzibp-dev/nasa`.
- [x] Add offline exact-host scope guard and unit tests.
- [x] Add deliberately vulnerable isolated training examples (IDOR and SQLi).
- [x] Add isolated synthetic XSS text-context escaping lab and tests.
- [x] Add report structure linter and a fictional example.
- [x] Add GitHub Actions CI for offline checks.
- [x] Extract the 2026-11-18 user-provided NASA Bugcrowd brief into a review of scope, exclusions, and reporting rules (no testing conducted).
- [ ] Verify the exact service-level scope against the *current authenticated* Bugcrowd engagement, especially the discrepancy with NASA's general policy, before any external testing.
- [ ] Complete hands-on practice labs (requires actual learner participation).
- [x] Review supplied Bugcrowd submission screenshot: exactly three target website choices (NASA, USGEO, GLOBE).
- [x] Gather five public-page feature observations and build deterministic offline triage and tests (not confirmed vulnerabilities).
- [x] Review public evidence of NASA's 2023 Search.gov integration; note current backend remains unverified and third-party destinations are NO-GO absent scope authorization.
- [x] Add offline URL handoff classifier and regression tests, with no network activity.
- [x] Analyze researcher-supplied NASA search HTML offline: text/URL contexts, `data-search-engine="vertex"` hint, no observed inline-script term, no exploit demonstrated.
- [x] Add privacy-preserving offline HTML source context review and synthetic regression tests.
- [x] Implement an offline comparison tool for two benign search page snapshots; synthetic unit tests do not contact NASA.
- [ ] Obtain and privately compare a distinct, benign second search page only after verifying current service restrictions; do not commit unredacted HTML.
- [ ] Confirm Bugcrowd account access and the current target-level scope immediately before authorized testing.
- [ ] Produce a valid, unique NASA finding (unpredictable; **not guaranteed**).
- [ ] Submit any real finding privately to Bugcrowd (only if genuinely found).
- [ ] Receive acceptance, confirmation of fix, and any LOR (entirely NASA's decision).

## Metrics: verified vs unverified

| Metric | Initial state |
|---|---|
| Real NASA targets actively tested | 0 |
| Real confirmed vulnerabilities found | 0 |
| Official Bugcrowd submissions | 0 |
| Valid/accepted NASA reports | 0 |
| NASA Letters of Recognition | 0 |
| Isolated lab samples | 3 (simulated IDOR, SQLi, XSS) |

Do not increase a metric based on assumption or theoretical bug, and do not place live findings into this public repository.

## Next practical checkpoints

1. Review green GitHub Actions CI run and fix any failures.
2. Complete 10+ introductory Web Security Academy labs.
3. Read NASA live VDP and Bugcrowd brief before considering an eligible target.
4. Maintain privately stored evidence and report drafts, no public PoCs for unpatched targets.

### Project boundaries

The GitHub plugin can prepare repo artifacts and review code, but does not itself log into Bugcrowd, operate an external penetration-testing environment, certify vulnerability impact, or award NASA LORs. Continuous execution requires a supported ongoing automation/workflow and cannot be assumed.
