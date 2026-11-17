# Offline, intentionally vulnerable mini-labs

Both examples run **entirely in memory**. There is no server, credential harvesting, network scanner, NASA target, or remote request.

- `idor_demo.py`: a broken object-level authorization check compared to a proper owner check
- `sql_injection_demo.py`: unsafe SQL text construction compared to bound parameters in a temporary SQLite database

Run from the repository root:

```bash
python -m unittest tests.test_training_labs -v
```

The tests show *both* the simulated vulnerability and the regression fix. Never reuse the vulnerable functions in a real application.

For an example write-up, see [examples/lab-report.md](../examples/lab-report.md).
