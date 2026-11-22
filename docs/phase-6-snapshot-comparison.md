# Phase 6 — two-snapshot search reflection comparison (offline)

**Status (2026-11-22):** Tool and synthetic tests implemented. Only one real NASA HTML snapshot has been supplied so far (ordinary search for 'artemis'). A second independently saved HTML snapshot has **not** been analyzed. No XSS or other vulnerability is confirmed.

## Why this comparison matters

The supplied 'artemis' HTML contains mission article titles, links, image descriptions and query-related headings. A single common term cannot distinguish static indexed content from content actually derived from a query. Counting occurrences is **not** proof of unsafe reflection.

The [Phase 5 report](phase-5-html-source-analysis.md) recorded many static-result text/URL/image matches and zero inline-script text matches for the benign term. These are syntax-context counts, not separate vulnerability instances.

## Safe, limited procedure

1. Keep the previously supplied NASA search HTML privately as 'artemis.html'. Do not commit it to GitHub.
2. Check current Bugcrowd policy, restrictions and allowed environment. Through the normal public search interface, make **one** ordinary search with a benign, distinctive alphanumeric word such as 'OrbitStudy2026'. Do not submit markup, JavaScript, attack strings or automated requests.
3. Save the page source privately as 'orbitstudy.html'. If any navigation goes to a third-party service, do not perform security testing on that service without separate authorization.
4. Run the local no-network script:

    python tools/search_snapshot_compare.py artemis.html orbitstudy.html --second-term OrbitStudy2026

5. Review **only the context counts** (HTML title, heading, attributes, scripts) and keep any original HTML private.

## What the output can establish

| Second-term observation | Interpretation | Not established |
|---|---|---|
| Only normal title/heading text | Consistent with ordinary search results | XSS or arbitrary-input escaping |
| URL or form attributes | Query retained in navigation or form state | Attribute injection or security impact |
| Inline JavaScript text | Context may deserve separate, authorized review | Script execution or exploitability |
| Not found anywhere | Data is incomplete or term not displayed | Safety of the application |

The comparator **always** reports vulnerability_confirmed=false and network_requests=0. Even if the marker is found, do not file a Bugcrowd report solely on that basis.

## Data protection

The tool handles private snapshots on disk, caps them at 8 MiB, permits only plain alphanumeric/hyphen terms, and outputs **counts, whitelisted engine hints and broad conclusions**, never raw HTML, paths, query strings, tokens, cookies or user data. Do not publish unredacted snapshots, including seemingly harmless HTML form tokens.

## Current NASA research status

- Real HTML source snapshots analyzed: 1 ('artemis', benign search).
- Additional comparison snapshot analyzed: 0.
- Proven vulnerabilities: 0.
- Submitted NASA reports: 0.
- NASA Letters of Recognition: 0.

The NASA VDP and its Bugcrowd engagement determine all permitted assets and methods. If a nonproduction test environment is provided, follow NASA's requirement to use it. No automation, mass enumeration, credential attacks or external exploitation are part of this procedure.
