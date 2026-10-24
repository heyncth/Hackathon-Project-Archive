#!/usr/bin/env python3
"""Offline end-to-end run against synthetic fixtures.

Creates a temporary working copy of schemas/ and sources/, runs the full
pipeline on tests/fixtures/candidates.json, prints the report, and exits
non-zero if validation fails. Network is never used.
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hpa.pipeline import run_pipeline  # noqa: E402


def main() -> int:
    fixtures = ROOT / "tests" / "fixtures" / "candidates.json"
    with tempfile.TemporaryDirectory(prefix="hpa-e2e-") as tmp:
        tmp_root = Path(tmp)
        shutil.copytree(ROOT / "schemas", tmp_root / "schemas")
        shutil.copytree(ROOT / "sources", tmp_root / "sources")
        (tmp_root / "data").mkdir()
        report = run_pipeline(
            tmp_root,
            adapter="fixture",
            query=f"file:{fixtures}",
            limit=10,
        )
        print(json.dumps(report, indent=2, sort_keys=True))
        ok = (report.get("validation") or {}).get("ok", False)
        return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
