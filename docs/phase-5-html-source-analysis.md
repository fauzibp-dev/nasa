# Phase 5 — review of user-supplied NASA search HTML (2026-11-18)

**Evidence:** User-provided HTML source from an ordinary `https://www.nasa.gov/?search=artemis` search. Parsed **offline**; raw HTML and any transient tokens were **not committed** to this public repo. Snapshot is approximately 295 kB and 2,500 lines. It is a single benign request, **not** a penetration test or proof of exploitability.

## Grounded observations

| HTML context | Exact evidence in provided copy | What it establishes |
|---|---|---|
| `<title>` | `23489 Search Results for &quot;artemis&quot;` (line 14) | HTML title contains the term and encoded surrounding quotes |
| Main `<h1>` | `Search Results for: <span>artemis</span>` (line 1398) | The normal search term appears in a text node |
| Search URL | `https://www.nasa.gov/?search=artemis` | Browser-visible search stays on the listed `www.nasa.gov` host |
| Pagination anchors | `/search/?search=artemis&search_page=2` (HTML-encoded separator in source, lines 2265–2269) | Search term is retained in normal navigation URLs |
| Survey form action | `/?search=artemis` (line 2408) | A separate form inherits the page URL; this is not automatically a vulnerable entry point |
| Search engine hint | `data-search-engine="vertex"` (line 1413) | Markup references `vertex`; this does **not** identify a confirmed backend deployment or attack surface |

### Offline markup context inventory

The local script `tools/search_markup_review.py` counts elements containing the benign term (some match **static content titles**, not reflected query output). Observed counts from the supplied snapshot:

| Context counted | Count |
|---|---:|
| HTML title text | 1 |
| Main heading text | 1 |
| URL link attributes (including article results) | 25 |
| Form action attributes | 1 |
| Meta content attributes | 1 |
| Input value attributes (includes a static Artemis category) | 1 |
| Image alt/src metadata | 23 |
| Other attributes | 2 |
| Other text nodes (including ordinary search result headlines) | 61 |
| Inline script data containing `artemis` | 0 |

**Caution:** Counts are syntactic HTML nodes or attributes, not independently established taint/reflection flows. E.g. NASA articles about Artemis naturally contain the search word without being derived from the query. HTML entities around the title's quotes do **not** prove arbitrary user input is safely escaped.

No unsafe execution, payload behavior, authentication bypass, data exfiltration, redirect, or valid XSS is demonstrated by this benign input. The visible WordPress/plugin metadata is not itself a reportable vulnerability; the VDP explicitly excludes unsupported version-only reports.

### Backend discrepancy with earlier public research

Previous [Phase 4 research](phase-4-search-boundary.md) cites a **2023 USAGov post** documenting NASA's historical Search.gov adoption. This 2026 HTML snapshot has `data-search-engine="vertex"`, so **do not assert that the current search results are necessarily powered by Search.gov**. The HTML hint also does **not prove** Google's Vertex implementation or whether services behind it are within NASA's disclosure scope.

## Run the reproducible offline check

For a privately stored HTML file that the researcher is authorized to inspect:

```bash
python tools/search_markup_review.py /private/path/to/search-results.html --term artemis
python -m unittest discover -s tests -v
```

The checker prints only counts and safe enumerated hints, and never opens network connections. Do **not** commit source snapshots: HTML may contain transient attribution or form values and other material irrelevant to a public portfolio. Use redacted reports, not raw HTML.

## Security decision

- **Current result: inconclusive for XSS, no confirmed security vulnerability.**
- Live Bugcrowd scope and any nonproduction requirement still govern future experiments. Do not perform uncontrolled automated fuzzing/scans, credential attacks, or extract data.
- To establish a real issue, the researcher would need a separately authorized, narrowly scoped demonstration of unsafe output handling and actual impact, ideally in a provided test environment.
- Do not submit to Bugcrowd just because a benign search term appears in HTML.

Project metrics remain: **0 validated NASA vulnerabilities, 0 real Bugcrowd submissions, 0 NASA Letters of Recognition**.
