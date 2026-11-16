#!/usr/bin/env python3
"""Validate cross-model alignment for a modeling round, against real boundary folders.

Usage:
  validate_alignment.py --round-id ID (--scope DIR [--scope DIR ...] | --root DIR)
                        [--output-dir DIR] [--base-dir DIR]
  validate_alignment.py --check-stale REPORT.json [--base-dir DIR]

  --scope DIR       A boundary folder (holds main.md) in this round's scope; repeatable
  --root DIR        Validate every boundary at or below DIR (folders whose main.md
                    has a "## System Boundary" section)
  --output-dir DIR  Write alignment-report-[round-id].md/.json and alignment-status.json
                    here (normally the project's artifacts/Analysis folder)
  --base-dir DIR    Folder that recorded paths are relative to (default: current directory)
  --check-stale     Re-hash the models a prior report covered and say whether its
                    result still holds

Exit codes: 0 = PASS (or prior report still valid), 1 = NEEDS_CLARIFICATION,
2 = INVALID_INPUT, 3 = prior report is stale, 64 = usage error.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from alignment_loader import current_versions, discover_boundaries, load_round
from alignment_report import RoundState, report_to_json, resolve_round_for_resume, write_report
from alignment_validator import validate_round

EXIT = {"PASS": 0, "NEEDS_CLARIFICATION": 1, "INVALID_INPUT": 2}


def run_round(round_id: str, folders: list, base_dir: Path, output_dir=None, generated_at=None) -> dict:
    """Load the boundary folders, validate them, and (optionally) persist the report."""
    loaded = load_round(folders, base_dir)
    report = validate_round(round_id, loaded.boundaries, loaded.domain_models,
                            loaded.use_case_models, loaded.ui_models, loaded.load_errors)
    if output_dir is not None:
        write_report(report, loaded.boundaries, loaded.versions, Path(output_dir), generated_at)
    return report_to_json(report, loaded.boundaries, loaded.versions, generated_at)


def check_stale(report_path: Path, base_dir: Path) -> str:
    """Returns 'valid' or 'stale' for a previously written round report."""
    prior = json.loads(report_path.read_text(encoding="utf-8"))
    folders = {b["boundary_id"]: b["hierarchy_path"] for b in prior["boundary_scope"]}
    state = RoundState(prior["round_id"], prior["status"], list(folders), prior["source_model_versions"])
    return resolve_round_for_resume(state, current_versions(folders, base_dir))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--round-id")
    parser.add_argument("--scope", action="append", default=[])
    parser.add_argument("--root")
    parser.add_argument("--output-dir")
    parser.add_argument("--base-dir", default=".")
    parser.add_argument("--check-stale")
    args = parser.parse_args(argv)
    base_dir = Path(args.base_dir)

    if args.check_stale:
        result = check_stale(Path(args.check_stale), base_dir)
        print(f"{args.check_stale}: {result}")
        if result == "stale":
            print("Revalidation required: this report is not PASS, or a model in its scope changed after it was written.")
        return 0 if result == "valid" else 3

    if not args.round_id or bool(args.scope) == bool(args.root):
        parser.print_usage(sys.stderr)
        print("error: give --round-id and exactly one of --scope or --root", file=sys.stderr)
        return 64
    folders = [Path(s) for s in args.scope] if args.scope else discover_boundaries(Path(args.root))
    if not folders:
        print(f"error: no boundary folders found under {args.root}", file=sys.stderr)
        return 64
    try:
        report = run_round(args.round_id, folders, base_dir, args.output_dir)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 64

    print(f"Round {report['round_id']}: {report['status']}")
    for b in report["boundary_scope"]:
        print(f"  boundary {b['boundary_id']} ({b['boundary_type']}) at {b['hierarchy_path']}")
    for f in report["findings"]:
        print(f"  {f['finding_id']} [{f['severity']}] {f['description']}")
    for q in report["clarification_questions"]:
        print(f"  ? {q}")
    if args.output_dir:
        print(f"Report written to {args.output_dir}/alignment-report-{report['round_id']}.md")
    return EXIT[report["status"]]


if __name__ == "__main__":
    sys.exit(main())
