# Source Policy

## Purpose

The source registry (`sources/sources.yaml`) lists every discovery source the
pipeline knows about. It is editable; add new sources here as they are found.

## Source record fields

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Stable slug, e.g. `github-search`. |
| `name` | yes | Human-readable name. |
| `type` | yes | `github`, `devpost`, `official-site`, `blog`, `video`, `demo`, `documentation`, `other`. |
| `base_url` | yes | Root or discovery URL. |
| `adapter` | yes | Adapter key the pipeline uses: `github`, `devpost`, `fixture`, `generic`. |
| `discovery_method` | yes | Short description of how to query it. |
| `limitations` | yes | Access limits, rate limits, scraping caveats. May be empty. |
| `requires_auth` | yes | Boolean. If true, which env var provides the token (never a literal secret). |
| `last_checked` | yes | ISO-8601 timestamp of last successful access, or `null`. |

## Rules

1. **Original sources first.** Prefer official event pages, official results,
   and the project's own repository over third-party summaries.
2. **Respect access controls.** Do not bypass paywalls, authentication,
   CAPTCHAs, or robots restrictions. If a source is inaccessible, record the
   failure and move on; inaccessibility is not evidence that a project does
   not exist.
3. **No secrets in the registry.** Tokens and API keys come from environment
   variables at runtime. Never write them into `sources.yaml` or logs.
4. **Record limitations honestly.** If a source is scrape-only, rate-limited,
   or requires JavaScript, say so in `limitations`.
5. **Last-checked is honest.** Only set `last_checked` after a successful
   access in the current run.

## Known limitations of the current environment

- Unauthenticated GitHub API: 60 requests/hour per IP. Set `GITHUB_TOKEN`
  for higher limits.
- Devpost: public gallery pages are HTML; no official public API. The
  `devpost` adapter parses public pages and may break if the markup changes
  or access is blocked.
- No dedicated paid search API is a mandatory dependency.

## Adding a source

1. Append a record to `sources/sources.yaml` following the schema above.
2. If a new adapter is needed, implement it under `src/hpa/adapters/`
   inheriting from `SearchAdapter`.
3. Add mock-based tests; do not make tests depend on live network access.
4. Open a pull request.
