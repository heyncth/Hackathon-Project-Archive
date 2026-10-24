"""Stable ID and slug helpers."""

from __future__ import annotations

import re
import unicodedata

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(value: str, max_length: int = 64) -> str:
    """Lowercase ASCII slug; stable across runs."""
    text = unicodedata.normalize("NFKD", value)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = _SLUG_RE.sub("-", text.lower()).strip("-")
    if not text:
        text = "untitled"
    return text[:max_length].strip("-")


def canonical_repo_url(url: str) -> str:
    """Normalize repository URLs for duplicate detection."""
    url = url.strip().rstrip("/")
    # strip query/fragment
    url = url.split("#", 1)[0].split("?", 1)[0].lower()
    # github.com: owner/repo is case-insensitive
    m = re.match(r"^(https?://)?(www\.)?github\.com/(.+)$", url)
    if m:
        parts = m.group(3).split("/")
        if len(parts) >= 2:
            return f"https://github.com/{parts[0].lower()}/{parts[1].lower()}"
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url
