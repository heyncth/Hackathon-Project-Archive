# Verification Policy

## Evidence before claims

Every important claim (award, technology, metric, architecture decision) must
be supported by at least one Evidence record with a traceable URL. Evidence
records name the claim they support.

## Evidence reliability

| Level | Meaning |
|---|---|
| `primary` | Official event results page, the project's own repository or documentation. |
| `secondary` | Credible technical write-ups, reputable engineering blogs, major tech press. |
| `tertiary` | Aggregators, social media, unsourced summaries. |

Prefer primary sources when sources conflict. Never silently pick a
convenient claim.

## Evidence status of a project

| Status | Criteria |
|---|---|
| `verified` | Core claims (existence, purpose, and any award) each have primary or strong secondary evidence; no unresolved conflicts. |
| `partially-verified` | Existence and purpose are evidenced, but some claims (e.g. a specific award, a technology) lack strong evidence, or minor conflicts remain. |
| `unverified` | Only weak evidence, or important claims rest on tertiary sources. |
| `disputed` | Credible sources conflict on an important claim; both sides are referenced. |

## Publication gates

### Basic profile

May be published when:

1. A stable project id and name exist.
2. At least one credible public source supports the project's existence.
3. Missing fields are explicitly `null`, `[]`, or listed in `limitations`.
4. Important claims have supporting evidence.
5. No fabricated or materially misleading claims.
6. `python -m hpa validate` passes.

Unresolved claims must be reflected in `verification_status`.

### Project overview guide

Publish only when sufficient evidence exists to accurately describe the
project's purpose and documented capabilities. Minimum: `verified` or
`partially-verified` evidence status with primary/secondary sources for the
purpose statement.

### Engineering case study

Requires sufficient evidence for architectural claims and technical decisions.
Facts must be separated from analysis and inference. If the evidence only
supports a superficial description, the gate fails.

### Reconstruction guide

Requires sufficient evidence to honestly help someone build a similar
project. The guide must:

- Explain scope and known limitations.
- Separate verified facts from inferred assumptions.
- Distinguish tested from untested instructions.
- Never claim to reproduce the original implementation.

A reconstruction is an independent approximation, never the original source
code.

When a guide fails its gate, record `status: blocked` with `gate_reason` in
`data/guides/` and do not publish the Markdown.

## Conflicting evidence

- Preserve references to all conflicting sources.
- Mark affected claims `disputed` in `verification_status` and explain in
  `limitations`.
- Do not publish unsupported definitive statements.

## Staleness

`last_checked` and metrics `captured_at` timestamps are mandatory. Old
metrics must never be presented as current. Re-verification on a schedule is
future work; research is on-demand in the MVP.
