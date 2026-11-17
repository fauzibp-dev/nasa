# Threat model for this research workspace

## Assets
- Researcher's GitHub account and repositories
- Program eligibility and authorization context
- Private reports, evidence, screenshots, raw traffic, and proof-of-concept files
- Third-party user privacy and service availability
- Integrity of publicly stated achievements

## Trust boundaries

GitHub repository is **public**. Actual NASA findings belong in NASA's private Bugcrowd report channel, not GitHub. A local `scope.txt` allowlist is not an authoritative permission grant. CI must never make exploratory network requests to third-party targets.

## Main threats and mitigations

| Risk | Mitigation |
|---|---|
| Accidental out-of-scope testing | Deny-by-default exact-host reminder; verify official live program scope, application, and allowed action before every activity |
| Harmful automation | No scanner or active target integration; CI only runs offline tests |
| Publishing unpatched finding | Real reports and evidence kept outside public repo; clear `SECURITY.md` and `.gitignore` |
| Credentials or personal data pushed | No secrets in examples; static checks; manually inspect diffs and use GitHub secret scanning if available |
| Misstated findings or achievements | Explicit public metrics, links to official confirmation only after actually issued |
| Reproduction with real third-party accounts | Practice entirely with synthetic records and in-memory SQLite |
| Supply-chain surprises | Python standard library only; GitHub workflow uses standard actions |

## Residual risk

`.gitignore` does not protect already-tracked files or prevent deliberate forced adds. Regular-expression checks cannot identify all secret formats or personal data. Human review of every public commit remains necessary. Even checking an exact hostname in `scope.txt` does not mean its specific service/path/test type is authorized.
