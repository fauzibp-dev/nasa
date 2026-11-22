# Phase 6 — two-snapshot search reflection comparison (offline)

**Status (2026-11-22):** Both user-supplied benign search HTML snapshots have now been analyzed **offline**: `artemis` and `OrbitStudy2026`. Cross-snapshot checks were added to the tool. **No XSS or other vulnerability is confirmed.**

## Why this comparison matters

The supplied 'artemis' HTML contains mission article titles, links, image descriptions and query-related headings. A single common term cannot distinguish static indexed content from content actually derived from a query. Counting occurrences is **not** proof of unsafe reflection.

The [Phase 5 report](phase-5-html-source-analysis.md) recorded many static-result text/URL/image matches and zero inline-script text matches for the benign term. These are syntax-context counts, not separate vulnerability instances.

## Actual analysis of the two privately supplied snapshots (2026-11-22)

The user supplied a second HTML source from an ordinary search for `OrbitStudy2026`. Both sources were read privately and compared with a no-network HTML parser. **No full HTML, cookie, transient form value, or secret was published to the repository.** These are *observations of two provided sources*, not reproducible evidence of an exploit.

| Counted context containing the matching search term | `artemis` snapshot | `OrbitStudy2026` snapshot |
|---|---:|---:|
| `title_text` | 1 | 1 |
| `h1_text` | 1 | 1 |
| `link_href` | 25 | 4 |
| `form_action` | 1 | 1 |
| `meta_content` | 1 | 1 |
| `input_value` | 1 | 0 |
| `asset_or_image_metadata` | 23 | 0 |
| `other_attribute` | 2 | 0 |
| `other_text` | 61 | 0 |
| `inline_script` | 0 | 0 |

The literal terms occur **118** and **8** times respectively in the two raw source files; the context counter counts **HTML elements/attribute values containing each term**, not raw substring frequency. Each snapshot includes a `data-search-engine="vertex"` hint, which remains insufficient to establish backend deployment.

### Cross-snapshot check

- The new term `OrbitStudy2026` appears **zero times** in the earlier `artemis` snapshot.
- The old term `artemis` still appears **13 times** in the `OrbitStudy2026` snapshot, classified as **5 links**, **5 ordinary text nodes**, and **3 image metadata attributes**.
- This illustrates how NASA content about Artemis can appear even when someone searches for a different word; **static/indexed content can contaminate naive reflection counts**.
- The new term appears in the second HTML page's title, visible heading, four ordinary pagination links, one form action, and one meta attribute. It is **not observed in inline script text** in this snapshot.
- The two page titles show different displayed result counts (`23489` vs `15006`). Those counts are application text, not evidence of a security flaw, and do not prove how ranking or filtering operates.

**Conclusion:** The data support ordinary search-query propagation into markup. They do not demonstrate unsafe HTML interpretation, unescaped arbitrary characters, JavaScript execution, a privilege boundary violation, or meaningful security impact. **Do not submit a vulnerability report based on these snapshots.**

The enhanced `tools/search_snapshot_compare.py` includes `cross_snapshot_context_counts` to identify when a term persists in the opposite snapshot. It prints aggregated counts only.

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

- Real HTML source snapshots analyzed: **2** (benign searches `artemis` and `OrbitStudy2026`).
- Additional comparison snapshot analyzed: **1**.
- Security conclusion: **inconclusive; no XSS confirmed**.
- Proven vulnerabilities: 0.
- Submitted NASA reports: 0.
- NASA Letters of Recognition: 0.

The NASA VDP and its Bugcrowd engagement determine all permitted assets and methods. If a nonproduction test environment is provided, follow NASA's requirement to use it. No automation, mass enumeration, credential attacks or external exploitation are part of this procedure.
