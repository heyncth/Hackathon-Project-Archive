"""CLI entry point: python -m archive {validate,generate,check,export}."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .export import export_json
from .generate import check_readme, write_readme
from .loader import load_repo, repo_root
from .site import build_site, check_site
from .validate import validate_repo


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="archive", description="Hackathon Project Archive maintenance CLI")
    parser.add_argument("--root", type=Path, default=None, help="repository root (default: auto-detect)")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate", help="validate all project records")
    sub.add_parser("generate", help="regenerate README stats and build the site")
    sub.add_parser("check", help="fail if README or site is stale (read-only)")
    sub.add_parser("export", help="export project data as JSON")

    args = parser.parse_args(argv)
    root = args.root or repo_root()
    if not (root / "data" / "taxonomy.json").exists():
        print(f"error: no data/taxonomy.json under {root}", file=sys.stderr)
        return 2

    repo = load_repo(root)

    if args.command == "validate":
        errors = validate_repo(repo)
        if errors:
            for e in errors:
                print(e, file=sys.stderr)
            print(f"\n{len(errors)} error(s) in {len(repo.projects)} project file(s)", file=sys.stderr)
            return 1
        print(f"OK: {len(repo.projects)} project file(s) valid")
        return 0

    if args.command == "generate":
        errors = validate_repo(repo)
        if errors:
            for e in errors:
                print(e, file=sys.stderr)
            print("\nrefusing to generate from invalid data", file=sys.stderr)
            return 1
        write_readme(repo)
        site = build_site(repo)
        print("README.md updated")
        print(f"site built at {site}/")
        return 0

    if args.command == "check":
        errors = []
        err = check_readme(repo)
        if err:
            errors.append(err)
        err = check_site(repo)
        if err:
            errors.append(err)
        if errors:
            for e in errors:
                print(e, file=sys.stderr)
            return 1
        print("OK: README.md and site/ are up to date")
        return 0

    if args.command == "export":
        sys.stdout.write(export_json(repo))
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
