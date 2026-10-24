# Scripts

- `last-run-report.json` — written by `python -m hpa research`; records
  sources searched, failures, created/updated projects, guide outcomes, and
  validation results for the most recent run. Regenerated each run.
- `run_fixture_e2e.py` — offline end-to-end run against
  `tests/fixtures/candidates.json`; exits non-zero on validation failure.
