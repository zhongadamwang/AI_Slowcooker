"""Run the validator end-to-end over each fixture's real boundary files.

For every folder under ../fixtures/, this loads the boundary tree from disk
(main.md, domain-model.md, use-case-model.json + scripts, ui-model.json),
validates it, writes generated-report.json/.md next to the fixture, and
compares status, finding IDs, and severities against expected-report.json.

Usage: python3 run_fixtures.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from alignment_loader import discover_boundaries
from alignment_report import report_to_markdown
from validate_alignment import run_round

FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures"
GENERATED_AT = "2026-11-08T00:00:00Z"  # fixed, so generated reports are reproducible


def run_fixture(fixture_dir: Path) -> dict:
    """Validate every boundary found in a fixture folder; paths are recorded relative to it."""
    expected = json.loads((fixture_dir / "expected-report.json").read_text(encoding="utf-8"))
    folders = discover_boundaries(fixture_dir)
    return run_round(expected["round_id"], folders, fixture_dir, generated_at=GENERATED_AT)


def summarize(report: dict) -> tuple:
    return report["status"], [(f["finding_id"], f["severity"]) for f in report["findings"]]


def main() -> int:
    fixtures = sorted(p for p in FIXTURES_DIR.iterdir() if (p / "expected-report.json").is_file())
    all_matched = True
    for fixture_dir in fixtures:
        generated = run_fixture(fixture_dir)
        (fixture_dir / "generated-report.json").write_text(json.dumps(generated, indent=2) + "\n", encoding="utf-8")
        (fixture_dir / "generated-report.md").write_text(report_to_markdown(generated), encoding="utf-8")

        expected = json.loads((fixture_dir / "expected-report.json").read_text(encoding="utf-8"))
        matched = summarize(generated) == summarize(expected)
        all_matched = all_matched and matched
        print(f"[{'OK' if matched else 'MISMATCH'}] {fixture_dir.name}: "
              f"generated {summarize(generated)}, expected {summarize(expected)}")

    if not all_matched:
        print("\nFAILURE: one or more fixtures did not match their expected status and findings.")
        return 1
    print(f"\nAll {len(fixtures)} fixtures: generated status and findings match expected-report.json.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
