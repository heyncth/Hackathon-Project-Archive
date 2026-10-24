"""Devpost public gallery adapter (best-effort HTML parsing).

Devpost has no official public API. This adapter fetches public search
pages and extracts software cards with the stdlib HTML parser. It may break
if markup changes or access is blocked; failures are recorded, not fatal.
Award claims are NEVER inferred from search listings alone.
"""

from __future__ import annotations

from html.parser import HTMLParser

import requests

from hpa.adapters.base import RawCandidate, SearchAdapter, SearchFailure

TIMEOUT = 20


class _SoftwareCardParser(HTMLParser):
    """Collects software-name / url / tagline triples from gallery markup."""

    def __init__(self) -> None:
        super().__init__()
        self.cards: list[dict[str, str]] = []
        self._in_title = False
        self._in_tagline = False
        self._current: dict[str, str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {k: (v or "") for k, v in attrs}
        classes = attr.get("class", "")
        if tag == "li" and "software" in classes and "locked" not in classes:
            self._current = {}
        if self._current is None:
            return
        if tag == "a" and "title" in classes and attr.get("href"):
            self._current["url"] = attr["href"]
            self._in_title = True
        elif tag == "h5" and "card-name" in classes:
            self._in_title = True
        elif tag == "p" and "tagline" in classes:
            self._in_tagline = True

    def handle_data(self, data: str) -> None:
        if self._current is None:
            return
        text = data.strip()
        if not text:
            return
        if self._in_title:
            self._current["name"] = self._current.get("name", "") + text
        elif self._in_tagline:
            self._current["tagline"] = self._current.get("tagline", "") + text

    def handle_endtag(self, tag: str) -> None:
        if self._in_title and tag in ("a", "h5"):
            self._in_title = False
        elif self._in_tagline and tag == "p":
            self._in_tagline = False
        elif tag == "li" and self._current is not None:
            if "name" in self._current:
                self.cards.append(self._current)
            self._current = None


class DevpostAdapter(SearchAdapter):
    name = "devpost"

    def search(self, query: str, limit: int = 10) -> list[RawCandidate]:
        url = self.source.get("base_url", "https://devpost.com/software/search")
        try:
            resp = requests.get(
                url,
                params={"query": query},
                headers={"User-Agent": "hackathon-project-archive"},
                timeout=TIMEOUT,
            )
        except requests.RequestException as exc:
            raise SearchFailure(f"devpost: network error: {exc}") from exc

        if resp.status_code == 429:
            raise SearchFailure("devpost: rate limited (HTTP 429)")
        if resp.status_code in (401, 403):
            raise SearchFailure(f"devpost: access restricted (HTTP {resp.status_code})")
        if resp.status_code == 404:
            raise SearchFailure("devpost: page not found (HTTP 404)")
        if resp.status_code != 200:
            raise SearchFailure(f"devpost: HTTP {resp.status_code}")

        parser = _SoftwareCardParser()
        try:
            parser.feed(resp.text)
        except Exception as exc:  # HTMLParser is tolerant; belt and braces
            raise SearchFailure(f"devpost: parse error: {exc}") from exc

        if not parser.cards:
            # Markup may have changed or the page shape differs.
            raise SearchFailure("devpost: no software cards parsed (markup change or empty page)")

        candidates: list[RawCandidate] = []
        for card in parser.cards[:limit]:
            card_url = card.get("url")
            if not card_url:
                continue
            candidates.append(
                RawCandidate(
                    source_id=self.source_id,
                    source_url=card_url,
                    name=card.get("name", card_url),
                    description=card.get("tagline"),
                    repo_url=None,  # Devpost listings do not expose the repo reliably
                    official_url=card_url,
                    evidence=[
                        {
                            "claim": "Project is listed on Devpost.",
                            "url": card_url,
                            "source_type": "other",
                            "reliability": "secondary",
                            "notes": "Devpost gallery listing; award claims need the event results page.",
                        }
                    ],
                )
            )
        return candidates
