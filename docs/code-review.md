# Offline static code review

The repository includes a tiny, dependency-free AST code-review tool that looks for **some** suspicious Python constructs. It is not a vulnerability scanner for remote assets. Nothing is uploaded and no network request is made.

Run it against source files you own or have permission to review:

```bash
python tools/code_review.py labs
python tools/code_review.py tools --strict
```

Detected patterns:
- `eval()` and `exec()` dynamic code
- `pickle.load[s]()` and `marshal.load[s]()` risky deserialization
- `subprocess` calls specifying `shell=True`
- SQL execution where SQL is built **directly** using f-strings or binary concatenation

These are only **review flags**, not evidence of exploitable vulnerabilities. A flagged occurrence can be safe, and many real bugs will be missed. For example, SQL passed through a variable can evade this basic checker.

The mini-labs intentionally contain vulnerable code. Their test cases demonstrate secure alternatives. Do not use source-code access as permission to test any corresponding deployed system.
