"""GitHub repository search adapter.

Uses the public REST search API. Reads an optional GITHUB_TOKEN from the
environment for higher rate limits; the token value is never logged.
"""

from __future__ import annotations

import os

import requests

from hpa.adapters.base import RawCandidate, SearchAdapter, SearchFailure

API = "https://api.github.com/search/repositories"
TIMEOUT = 20


class GitHubAdapter(SearchAdapter):
    name = "github"

    def _headers(self) -> dict[str, str]:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "hackathon-project-archive",
        }
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def search(self, query: str, limit: int = 10) -> list[RawCandidate]:
        params = {"q": query, "per_page": min(limit, 30), "sort": "stars", "order": "desc"}
        try:
            resp = requests.get(API, params=params, headers=self._headers(), timeout=TIMEOUT)
        except requests.RequestException as exc:
            raise SearchFailure(f"github: network error: {exc}") from exc

        if resp.status_code == 403 and "rate limit" in resp.text.lower():
            raise SearchFailure("github: rate limited (unauthenticated 60/hr; set GITHUB_TOKEN)")
        if resp.status_code == 401:
            raise SearchFailure("github: authentication failed (check GITHUB_TOKEN)")
        if resp.status_code != 200:
            raise SearchFailure(f"github: HTTP {resp.status_code}")

        try:
            payload = resp.json()
        except ValueError as exc:
            raise SearchFailure("github: invalid JSON response") from exc

        candidates: list[RawCandidate] = []
        for item in payload.get("items", [])[:limit]:
            html_url = item.get("html_url")
            if not html_url:
                continue
            candidates.append(
                RawCandidate(
                    source_id=self.source_id,
                    source_url=html_url,
                    name=item.get("name") or html_url,
                    description=item.get("description"),
                    repo_url=html_url,
                    stars=item.get("stargazers_count"),
                    forks=item.get("forks_count"),
                    language=item.get("language"),
                    topics=list(item.get("topics") or []),
                    official_url=item.get("homepage") or None,
                    # A public repository is primary evidence of existence.
                    evidence=[
                        {
                            "claim": "Repository exists and is publicly accessible.",
                            "url": html_url,
                            "source_type": "repository",
                            "reliability": "primary",
                            "notes": None,
                        }
                    ],
                )
            )
        return candidates
