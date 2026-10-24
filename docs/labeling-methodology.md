# Labeling Methodology

Qualitative labels only. No numeric overall score or weighted ranking in the
MVP. Use labels only when their definitions are satisfied.

## Project category

| Label | Definition |
|---|---|
| `award-winning` | Evidence confirms the project received an award at a hackathon or competition. Popularity alone never implies this. |
| `community-notable` | Meaningful community interest or educational/technical value, evidenced by metrics, activity, demos, or credible write-ups. |

A project may carry both labels.

## Popularity

Assigned from **captured metrics and documented indicators**, never from
subjective intuition. Record which indicators were available and when they
were checked (via MetricsSnapshot records).

| Label | Definition (GitHub-centric initial thresholds) |
|---|---|
| `high` | ≥ 1,000 stars on the original repository, or multiple strong independent indicators (e.g. widespread press coverage plus high stars). |
| `moderate` | 100–999 stars, or equivalent community activity. |
| `limited` | < 100 stars and no other strong indicator. |
| `unknown` | No metrics captured. |

Stars are one indicator, not a quality score. A high-star project can have
`limited` documentation quality.

## Evidence status

See `docs/verification-policy.md` for `verified`, `partially-verified`,
`unverified`, `disputed`.

## Documentation quality

| Label | Definition |
|---|---|
| `strong` | README plus substantive docs (setup, architecture, or usage guides) sufficient for a newcomer to understand and run the project. |
| `partial` | README with some useful detail, but gaps in setup, architecture, or usage. |
| `limited` | Minimal or placeholder documentation. |
| `unknown` | Documentation not assessed. |

## Reproducibility

| Label | Definition |
|---|---|
| `tested` | Someone has actually recorded a test of the relevant workflow (this archive's own reconstruction or the project's documented setup). A README alone is not enough. |
| `documented-not-tested` | Setup or build instructions exist but have not been executed and verified. |
| `not-assessed` | Reproducibility not evaluated. |

## Educational value

Tracked separately from popularity. Observable criteria:

| Label | Criteria (any one suffices) |
|---|---|
| `high` | Explicitly designed for teaching/learning, unusually clear write-up of the engineering, or widely used as a reference implementation. |
| `moderate` | Some reusable lessons in the code or write-up, but not a primary teaching artifact. |
| `low` | Little educational content beyond the code itself. |
| `unknown` | Not assessed. |

## Rules

1. Never invent an indicator to justify a label. If the data is missing, use
   `unknown`.
2. Keep raw metrics (stars, forks, dates) separate from the label.
3. Re-label only when new evidence or metrics justify it, and update
   `last_checked`.
