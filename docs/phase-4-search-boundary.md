# Phase 4: NASA website search — service-boundary review

**Date:** 2026-11-18
**Status:** Public-source architecture research completed. **No security flaw demonstrated** and **no active security testing performed**.

## What was confirmed

1. The ordinary public homepage at https://www.nasa.gov/ exposes a site search UI. This is **not** a vulnerability.
2. The official [USAGov post from December 2023](https://www.usa.gov/blog/2023/12/less-is-more-improving-the-publics-web-search-experience-with-filters) documents that NASA adopted Search.gov technology for search filtering during its 2023 website redesign, covering the flagship NASA web experience.
3. [Search.gov developer documentation](https://search.gov/developer/) describes Search.gov as a government search service with its own infrastructure and source code. Third-party service boundaries matter for authorization.
4. NASA's current [official disclosure policy](https://www.nasa.gov/vulnerability-disclosure-policy/) and [Bugcrowd program](https://bugcrowd.com/engagements/nasa-vdp) restrict testing to the defined in-scope **systems, services and methods**. A link embedded on NASA.gov does **not** place the link destination in scope.
5. Attempts to retrieve specific NASA search-result URLs using available public-page retrieval returned fetch/cache errors. **No current search redirect, request parameters, HTML reflection, URL encoding or security behavior was independently established.** Therefore none should be claimed.

**Historical integration evidence does NOT prove that the NASA homepage's search form currently redirects to Search.gov or that any specific Search.gov host is in scope.**

## Follow-up evidence: ordinary NASA search URL (2026-11-18)

A researcher supplied the final browser URL from an ordinary search for **Artemis**:

`https://www.nasa.gov/?search=artemis`

This directly confirms that the browser's final visible **hostname** was `www.nasa.gov` and the search term was conveyed in the `search` URL query parameter. The researcher did not provide an HTTP archive, response headers, HTML source or a browser security trace.

An independent **public-page text retrieval** of the same URL produced a search results page with the visible heading **“Search Results for: artemis”** and ordinary search results. The retrieval provider reports an earlier crawl, so it confirms what the retrieved public page contained, not necessarily today's fresh server response.

### What can (and cannot) be concluded

- **Confirmed:** the ordinary search route can be represented on `www.nasa.gov` with `?search=artemis`; the retrieved public page displayed the search term in a human-readable results heading.
- **Not confirmed:** whether the raw HTML safely encodes all input; whether there is script execution; whether search input is reflected in HTML attributes, scripts or other contexts; which backend currently powers search; or whether any vulnerability exists.
- **Scope boundary:** a browser-visible URL on the listed hostname is useful context but **does not authorize** arbitrary security testing of every related service. The live Bugcrowd restrictions and nonproduction rules continue to apply.
- **No vulnerability report submitted.** Displaying a benign search term is expected behavior, not evidence of XSS.

Minimal next technical step: in a controlled *offline* training page, contrast escaped vs unescaped interpolation of a user search query and verify the behavior with regression tests. Any actual NASA test must be limited to methods/environments explicitly covered by the current program.

> **Follow-up (2026-11-18):** A researcher later provided a full benign search-results HTML snapshot. See [Phase 5 HTML analysis](phase-5-html-source-analysis.md) for confirmed `?search=artemis` contexts and the `data-search-engine="vertex"` hint. Earlier statements below record the evidence available during Phase 4 and should not be treated as the latest HTML analysis.

## Security triage decision

| Question | Current evidence | Decision |
|---|---|---|
| Does NASA homepage offer search? | Yes, public homepage | Research lead only |
| Is search powered by Search.gov in 2026? | Historical 2023 official documentation only | Unverified currently |
| Is the final search-results service authorized in this NASA Bugcrowd engagement? | Service-level authorization not established | NO-GO if it leaves listed hosts |
| Is a real XSS or other vulnerability confirmed? | No response/payload verification | No report |
| Do we have permission to flood, fuzz or scan these services? | No such permission | Do not do so |

## Offline URL-boundary helper

This repo provides an **offline, no-network** classifier. It displays hostnames only, strips paths/query parameters from output, and never claims to authorize testing.

```bash
python -m unittest tests.test_search_boundary -v
python tools/search_boundary.py 'https://www.nasa.gov/' 'https://search.example.gov/results?q=artemis'
```

Expected destination status: `EXTERNAL_HOST_NOT_AUTOMATICALLY_AUTHORIZED`.

If a researcher legitimately navigates the ordinary search interface in their own browser, they may check the **final hostname** to determine whether a distinct system is involved. **Never paste cookie headers, credentials, authentication tokens or full sensitive query values into public GitHub.** Ordinary URL navigation is not a security vulnerability.

If the final host is inside the program's listing, it STILL must satisfy service/method restrictions, and nonproduction requirements if available. If it is external or unclear, pause and seek clarification from the program.

## Next technical step

For hands-on security evidence, continue against locally controlled labs. Demonstrate input/output handling and report it as a *training* issue. For NASA specifically, only conduct a carefully scoped, minimal-impact test once current program authorization for that exact feature and technique has been established. Do not create a Bugcrowd submission without a reproducible, validated issue.

**Current project metrics: 0 NASA vulnerabilities, 0 NASA Bugcrowd submissions, 0 NASA LORs.**
