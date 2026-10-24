# Test fixtures

`candidates.json` contains **synthetic** candidate records used by the
fixture adapter for offline tests and deterministic demos.

- Project names, events, awards, star counts, and `example.invalid` URLs are
  fabricated. They are **not** real hackathon projects.
- `github.com/hpa-fixture-org/*` URLs are likewise synthetic placeholders for
  dedupe/metrics logic; do not treat them as real repositories.
- Live discovery uses the `github` or `devpost` adapters instead.

What the four candidates exercise:

| Candidate | Purpose |
|---|---|
| Fixture Alpha | Full award-winning path: verified award, repo, metrics, overview gate pass. |
| Fixture Beta | No-repo path: community-notable from secondary evidence; reconstruction gate should fail (docs only partial). |
| Alpha Fixture | Duplicate of Alpha's repo URL under a different name; dedupe test. |
| Fixture Delta | Unverified award claim; must not receive `award-winning`. |
