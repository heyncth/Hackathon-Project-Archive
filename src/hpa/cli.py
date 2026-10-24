"""Command-line interface for the Hackathon Project Archive pipeline."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from hpa.pipeline import run_pipeline, write_report
from hpa.validate import check_links, validate_datastore
from hpa.store import DataStore


def _find_root(start: Path | None = None) -> Path:
    """Walk up until we find sources/sources.yaml or schemas/."""
    cur = (start or Path.cwd()).resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / "sources" / "sources.yaml").is_file():
            return candidate
    return cur


def cmd_research(args: argparse.Namespace) -> int:
    root = Path(args.root) if args.root else _find_root()
    query = args.query or ""
    if args.adapter == "fixture" and args.input:
        query = f"file:{args.input}"
    if not query:
        print("error: --query is required (or --input with --adapter fixture)", file=sys.stderr)
        return 2
    report = run_pipeline(
        root,
        adapter=args.adapter,
        query=query,
        limit=args.limit,
        source_id=args.source,
    )
    report_path = write_report(root, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"\nreport written to {report_path}", file=sys.stderr)
    validation = report.get("validation") or {}
    return 0 if validation.get("ok", False) else 1


def cmd_validate(args: argparse.Namespace) -> int:
    root = Path(args.root) if args.root else _find_root()
    store = DataStore(root)
    report = validate_datastore(store)
    output = report.to_dict()
    if args.check_links:
        output["links"] = check_links(store)
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if report.ok else 1


def cmd_generate(args: argparse.Namespace) -> int:
    root = Path(args.root) if args.root else _find_root()
    # Regenerate overviews by re-processing nothing: use generate directly on existing data.
    from hpa.generate import overview_markdown, write_if_changed
    from hpa.gates import evaluate_gates

    store = DataStore(root)
    data = store.load_everything()
    written = []
    for gid, guide in data["guides"].items():
        if guide["type"] != "overview" or guide["status"] != "published":
            continue
        proj = data["projects"][guide["project_id"]]
        repos = [data["repositories"][r] for r in proj.get("repository_ids", []) if r in data["repositories"]]
        parts = [data["participations"][p] for p in proj.get("participation_ids", []) if p in data["participations"]]
        evs = [data["evidence"][e] for e in proj.get("evidence_ids", []) if e in data["evidence"]]
        mets = [data["metrics"][m] for m in proj.get("metrics_ids", []) if m in data["metrics"]]
        gates = evaluate_gates(proj, repos)
        if not gates["overview"]["passed"]:
            print(f"skip {gid}: overview gate no longer passes ({gates['overview']['reason']})", file=sys.stderr)
            continue
        md = overview_markdown(proj, repos, parts, data["events"], evs, mets)
        if write_if_changed(root / guide["path"], md):
            written.append(guide["path"])
    print(json.dumps({"regenerated": written}, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="hpa",
        description="Hackathon Project Archive pipeline",
    )
    parser.add_argument("--root", help="repository root (default: auto-detect)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_research = sub.add_parser("research", help="run an on-demand discovery + ingestion")
    p_research.add_argument("--adapter", choices=["github", "devpost", "fixture"], required=True)
    p_research.add_argument("--query", default="", help="search query (not needed with --input)")
    p_research.add_argument("--input", help="fixture adapter: path to candidates JSON")
    p_research.add_argument("--limit", type=int, default=10)
    p_research.add_argument("--source", help="restrict to one registry source id")
    p_research.set_defaults(func=cmd_research)

    p_validate = sub.add_parser("validate", help="validate data/, schemas, gates, markdown sync")
    p_validate.add_argument("--check-links", action="store_true", help="also HEAD-check URLs (network)")
    p_validate.set_defaults(func=cmd_validate)

    p_generate = sub.add_parser("generate", help="regenerate Markdown from structured data")
    p_generate.set_defaults(func=cmd_generate)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
