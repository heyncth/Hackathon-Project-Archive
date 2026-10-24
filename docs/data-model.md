# Data Model

Structured JSON/YAML files under `data/` are the source of truth. Markdown
guides under `guides/` are generated from, or must stay consistent with,
these records. Every entity has a stable, human-readable `id`.

## Entities

### Project (`data/projects/<id>.yaml`)

Canonical project identity.

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Stable slug, e.g. `fixture-alpha`. |
| `name` | yes | Human-readable project name. |
| `description` | yes | One or two sentences. `null` only if genuinely unknown and marked in `limitations`. |
| `categories` | yes | List of `award-winning` and/or `community-notable`. |
| `tags` | yes | Free-form topic tags; may be empty. |
| `status` | yes | `active`, `archived`, `unknown`. |
| `repository_ids` | yes | References to `data/repositories/`. Empty if no repo found. |
| `official_url` | yes | Official project page, or `null`. |
| `demo_url` | yes | Public demo, or `null`. |
| `participation_ids` | yes | References to `data/participations/`. |
| `technologies` | yes | Verified technologies only. Empty list if none verified. |
| `evidence_ids` | yes | Evidence supporting core claims. |
| `metrics_ids` | yes | References to `data/metrics/` snapshots. |
| `popularity` | yes | `high`, `moderate`, `limited`, `unknown`. See labeling methodology. |
| `documentation_quality` | yes | `strong`, `partial`, `limited`, `unknown`. |
| `reproducibility` | yes | `tested`, `documented-not-tested`, `not-assessed`. |
| `verification_status` | yes | `verified`, `partially-verified`, `unverified`, `disputed`. |
| `educational_value` | yes | `high`, `moderate`, `low`, `unknown`. |
| `guide_ids` | yes | References to `data/guides/` records if any. |
| `first_seen` | yes | ISO-8601 timestamp. |
| `last_checked` | yes | ISO-8601 timestamp. |
| `limitations` | yes | List of strings describing missing or disputed information. May be empty. |
| `notes` | yes | Free-form maintainer notes, or `null`. |

Unknown values are represented as `null` (for scalar fields) or `[]` (for list
fields), never invented to satisfy a schema.

### Repository (`data/repositories/<id>.yaml`)

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Stable slug. |
| `project_id` | yes | Owning project. |
| `url` | yes | Canonical repository URL. |
| `relationship` | yes | `original`, `related`, or `reference`. |
| `primary_language` | yes | Or `null`. |
| `license` | yes | SPDX id or `null` if unknown. |
| `last_checked` | yes | ISO-8601 timestamp. |

### Event (`data/events/<id>.yaml`)

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Stable slug. |
| `name` | yes | Event name. |
| `year` | yes | Integer year. |
| `platform` | yes | e.g. `devpost`, `mlh`, `official-site`, `fixture`. |
| `url` | yes | Official event or results URL, or `null`. |
| `location` | yes | Or `null`. |

### Participation (`data/participations/<id>.yaml`)

Relationship between a project and an event. One project may have many.

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Stable slug. |
| `project_id` | yes | |
| `event_id` | yes | |
| `award_name` | yes | e.g. `Grand Prize`, or `null` if none / unknown. |
| `award_category` | yes | e.g. `overall`, `best-ai`, or `null`. |
| `evidence_ids` | yes | Evidence for the participation/award claim. |
| `verified` | yes | Boolean; true only when an authoritative source confirms it. |

### Evidence (`data/evidence/<id>.yaml`)

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Stable slug. |
| `claim` | yes | The specific claim this evidence supports. |
| `url` | yes | Source URL. |
| `source_type` | yes | `official-results`, `repository`, `blog`, `video`, `demo`, `documentation`, `other`. |
| `reliability` | yes | `primary`, `secondary`, `tertiary`. |
| `accessed_at` | yes | ISO-8601 timestamp. |
| `notes` | yes | Or `null`. |

### MetricsSnapshot (`data/metrics/<id>.yaml`)

Point-in-time public metrics. Never presented as current without the
`captured_at` date.

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Stable slug. |
| `repository_id` | yes | |
| `stars` | yes | Integer, or `null`. |
| `forks` | yes | Integer, or `null`. |
| `watchers` | yes | Integer, or `null`. |
| `captured_at` | yes | ISO-8601 timestamp. |
| `source_url` | yes | Where the metric was read. |

### Guide (`data/guides/<id>.yaml`)

Registry of generated or hand-authored guides.

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Stable slug. |
| `project_id` | yes | |
| `type` | yes | `overview`, `case-study`, or `reconstruction`. |
| `path` | yes | Repo-relative path to the Markdown file. |
| `status` | yes | `published`, `draft`, or `blocked`. |
| `gate_reason` | yes | Why blocked, or `null`. |
| `evidence_ids` | yes | Evidence the guide relies on. |
| `generated_at` | yes | ISO-8601 timestamp. |

## Relationships

- Project 1—N Repository (via `repository_ids`)
- Project 1—N Participation (via `participation_ids`)
- Participation N—1 Event
- Project 1—N Evidence (via `evidence_ids`)
- Participation N—N Evidence (via `evidence_ids`)
- Repository 1—N MetricsSnapshot
- Project 1—N Guide (via `guide_ids`)

A project that wins awards at two events has **one** project record and
**two** participation records.

## Schema files

Machine-readable JSON Schemas live in `schemas/`. The validator
(`python -m hpa validate`) enforces them. Fields not present in the schema
are rejected so schema drift is caught early.
