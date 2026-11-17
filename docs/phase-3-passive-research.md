# Phase 3 — passive public-feature research results (2026-11-18)

**Purpose:** real, source-grounded reconnaissance at ordinary public-page level only. This is **not** a NASA vulnerability report and is not evidence of exploitation. User screenshot of the Bugcrowd submission form confirms three target choices: NASA, USGEO and GLOBE.

## Source observations

| Program target | Public homepage/source | Observed feature | Security test result |
|---|---|---|---|
| NASA | https://www.nasa.gov/ | Search field and regular content links | **Not tested** |
| USGEO | https://usgeo.gov/ | Informational pages and navigation | **Not tested** |
| GLOBE | https://www.globe.gov/ | Search, sign-in, account registration and data links | **Not tested** |
| GLOBE | https://www.globe.gov/globe-data | Public data navigation | **Not tested** |

The observations above were made from publicly readable pages; no payloads, fuzzing, logins, enumeration or production scans were sent. GLOBE's `globe.gov` homepage presents `www.globe.gov` as a destination; that **does not independently authorize every GLOBE service**. The public website links to additional subdomains and possible third-party services; those need case-specific review.

## Public-source search result

Reviewed GitHub search in the verified `nasa` organization for references to `www.nasa.gov`, `globe.gov`, and `usgeo.gov`. The broad NASA code organization has numerous unrelated projects, but **no verified mapping from the three in-scope production websites to public deployable source** was established. Do not present a bug in an unrelated NASA repo as a vulnerability on these Bugcrowd targets. For example, `nasa/earthdata-search` is a public project with security-related redirect handling, but its presence on NASA GitHub is **not** evidence that it powers `www.nasa.gov`.

## Repeatable offline processing

```sh
python tools/passive_surface.py
python -m unittest discover -s tests -v
```

`tools/passive_surface.py` consumes only the bundled JSON observation file. It never connects to a target. Its `EXACT_HOST_IN_SNAPSHOT__METHOD_UNVERIFIED` status **does not authorize testing**.

## Practical next decision

Begin with the NASA homepage **public search interface** as a *research lead*, not a claimed bug. The current VDP disallows generic content/text spoofing, missing headers, version-only and automated-tool-only findings. Only a demonstrable security issue with concrete impact and a permitted, minimal-impact reproduction can be eligible.

Before attempting any active input or exploiting any error, confirm the **live Bugcrowd service/technique scope** and whether a nonproduction environment is available. If one exists, NASA requires testing exclusively there. Stop if the intended method is not expressly permitted or if sensitive information is encountered. Keep real evidence and findings private and report through Bugcrowd.

No valid security finding, NASA submission or LOR has been obtained.
