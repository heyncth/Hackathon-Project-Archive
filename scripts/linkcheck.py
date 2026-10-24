#!/usr/bin/env python3
"""Optional online link checker. Never runs in CI.

Usage: python scripts/linkcheck.py [--timeout 10]

Best-effort only: timeouts, rate limits, and 5xx responses mean
"unreachable right now", not "resource is gone". This script reports;
it never modifies project records.
"""

import argparse
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))

from archive.loader import load_repo, repo_root  # noqa: E402

TIMEOUT_DEFAULT = 10
USER_AGENT = "Hackathon-Project-Archive-LinkCheck/0.1"


def check_url(url: str, timeout: float) -> str:
    """Return a status label for a URL."""
    for method in ("HEAD", "GET"):
        req = Request(url, method=method, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(req, timeout=timeout) as resp:
                return f"ok ({resp.status})"
        except HTTPError as exc:
            if exc.code == 405 and method == "HEAD":
                continue  # server dislikes HEAD, try GET
            if 400 <= exc.code < 500:
                return f"BROKEN ({exc.code}) - likely invalid"
            return f"unreachable ({exc.code}) - may be temporary"
        except (URLError, TimeoutError, OSError) as exc:
            reason = getattr(exc, "reason", exc)
            return f"unreachable ({reason}) - may be temporary"
    return "unreachable (no response)"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=TIMEOUT_DEFAULT)
    parser.add_argument("files", nargs="*", help="specific project files (default: all)")
    args = parser.parse_args()

    repo = load_repo(repo_root())
    broken = 0
    checked = 0
    for doc in repo.projects:
        if args.files and not any(
            doc.path.name == f or doc.path.as_posix().endswith(f) for f in args.files
        ):
            continue
        if not doc.data:
            continue
        urls = []
        links = doc.data.get("links") or {}
        if isinstance(links, dict):
            urls.extend(links.values())
        for item in doc.data.get("evidence") or []:
            if isinstance(item, dict) and "url" in item:
                urls.append(item["url"])
        for url in urls:
            checked += 1
            status = check_url(url, args.timeout)
            print(f"{doc.path.name}: {url} -> {status}")
            if status.startswith("BROKEN"):
                broken += 1

    print(f"\nchecked {checked} URL(s); {broken} definitely broken (4xx)")
    print("note: 'unreachable' results are inconclusive - do not delete records based on them")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
