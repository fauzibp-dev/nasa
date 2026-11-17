# Local XSS Prevention: Synthetic Training Report

This is a **fictional and intentionally vulnerable local training example**. There is no NASA finding and no third-party web target, credential, screenshot, browser session, or real user data.

## Summary

The sample function `vulnerable_greeting` concatenates an untrusted string into an HTML text context without escaping it. The fixed function `safe_greeting` escapes HTML metacharacters using Python's standard-library `html.escape`.

## Scope and Authorization

The only target is `labs/xss_demo.py` from this repository. This is a fully offline learning exercise; no HTTP request, browser automation, NASA asset, or third-party service is involved.

## Reproduction

1. Execute `python -m unittest tests.test_xss_demo -v` from the repository root.
2. The test passes the synthetic text `<img src=x onerror=alert(1)>` to `vulnerable_greeting`.
3. Observe that the unsafe string is included in the returned HTML, while the fixed variant encodes its characters.
4. Confirm ordinary text remains readable after escaping.

## Impact

If the unsafe pattern were used in a real HTML response and interpreted by a browser, untrusted input could create markup or executable attributes. Here the returned string is never sent to a browser, so no live exploitation or external impact has occurred.

## Remediation

Use framework-appropriate contextual output encoding and avoid inserting untrusted input directly as HTML. Context-specific encoding matters: this example only addresses an HTML text-node context and is not a general-purpose JavaScript or URL escaping solution.

## Disclosure

This is an educational code exercise only. No vulnerability was submitted to NASA, no third-party system was tested, and no official recognition is claimed.
