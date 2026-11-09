"""Report generation and round/revision tracking for model-validatealignment.

Builds on alignment_validator.py's validate_round() decision logic (T01) to
add:
  - Markdown + JSON report rendering per contract Section 4.2's schema
  - Round persistence and staleness detection (contract Section 4.4):
    a later edit to any model within a round's boundary_scope invalidates
    that round's PASS status, and resume must check source_model_versions
    against current artifacts before trusting a prior PASS.
  - Deterministic output: same inputs always produce the same report
    (finding order, finding_id assignment) -- required by T04's own
    Validation Tests ("deterministic output").

This module does not change validate_round()'s decision semantics; it wraps
its output for persistence/consumption and adds the round-lifecycle concerns
that sit above a single validation call.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from alignment_validator import AlignmentReport, BoundaryRef


# ---------------------------------------------------------------------------
# Report rendering (contract Section 4.2)
# ---------------------------------------------------------------------------

def report_to_json(
    report: AlignmentReport,
    boundary_scope: list,
    source_model_versions: dict,
    generated_at: Optional[str] = None,
) -> dict:
    """Renders an AlignmentReport to the exact JSON schema in contract Section 4.2.

    Deterministic: finding order is preserved from validate_round()'s own
    (deterministic, insertion-ordered) findings list -- never re-sorted or
    re-derived in a way that could vary between identical runs.
    """
    return {
        "round_id": report.round_id,
        "boundary_scope": [
            {"boundary_id": b.boundary_id, "boundary_type": b.boundary_type}
            for b in boundary_scope
        ],
        "source_model_versions": source_model_versions,
        "status": report.status,
        "findings": [
            {
                "finding_id": f.finding_id,
                "severity": f.severity,
                "description": f.description,
                "affected_models": f.affected_models,
            }
            for f in report.findings
        ],
        "clarification_questions": report.clarification_questions,
        "generated_at": generated_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def report_to_markdown(report_json: dict) -> str:
    """Renders the same report as human-readable Markdown, mirroring the
    existing EDPS convention of a paired .md/.json output (e.g.,
    screen-inventory.md/.json).
    """
    lines = [
        f"# Alignment Report — {report_json['round_id']}",
        "",
        f"**Status**: {report_json['status']}",
        f"**Generated**: {report_json['generated_at']}",
        "",
        "## Boundary Scope",
        "",
    ]
    for b in report_json["boundary_scope"]:
        lines.append(f"- `{b['boundary_id']}` ({b['boundary_type']})")
    lines += ["", "## Source Model Versions", ""]
    for k, v in report_json["source_model_versions"].items():
        lines.append(f"- **{k}**: {v}")
    lines += ["", "## Findings", ""]
    if not report_json["findings"]:
        lines.append("*(None.)*")
    else:
        for f in report_json["findings"]:
            lines.append(f"### {f['finding_id']} — {f['severity']}")
            lines.append(f["description"])
            lines.append(f"**Affected models**: {', '.join(f['affected_models'])}")
            lines.append("")
    if report_json["clarification_questions"]:
        lines += ["## Clarification Questions", ""]
        for q in report_json["clarification_questions"]:
            lines.append(f"- {q}")
    lines += ["", "---", f"**Round ID**: {report_json['round_id']}"]
    return "\n".join(lines) + "\n"


def write_report(
    report: AlignmentReport,
    boundary_scope: list,
    source_model_versions: dict,
    output_dir: Path,
    generated_at: Optional[str] = None,
) -> tuple:
    """Writes alignment-report-[round-id].md and .json to output_dir.

    Per contract Section 4.2: prior rounds' reports are never overwritten.
    This function refuses to write if a report for this exact round_id
    already exists with different content -- a round_id must be unique per
    actual round, never reused for a different run.
    """
    report_json = report_to_json(report, boundary_scope, source_model_versions, generated_at)
    json_path = output_dir / f"alignment-report-{report.round_id}.json"
    md_path = output_dir / f"alignment-report-{report.round_id}.md"

    if json_path.exists():
        existing = json.loads(json_path.read_text(encoding="utf-8"))
        # Allow idempotent re-write of the identical content (e.g., a retry
        # of the same round with no input change); refuse silent overwrite
        # of genuinely different content under the same round_id.
        comparable_existing = {k: v for k, v in existing.items() if k != "generated_at"}
        comparable_new = {k: v for k, v in report_json.items() if k != "generated_at"}
        if comparable_existing != comparable_new:
            raise ValueError(
                f"Refusing to overwrite existing report for round_id={report.round_id} "
                f"with different content. Prior rounds' reports are preserved, never "
                f"overwritten (contract Section 4.2) -- use a new round_id."
            )

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report_json, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(report_to_markdown(report_json), encoding="utf-8")
    return md_path, json_path


# ---------------------------------------------------------------------------
# Round/revision staleness tracking (contract Section 4.4)
# ---------------------------------------------------------------------------

@dataclass
class RoundState:
    """What the orchestrator/resume logic persists about a round's result,
    per contract Section 4.4's revision-invalidation requirement."""
    round_id: str
    status: str
    boundary_scope_ids: list
    source_model_versions: dict  # as recorded at the time this round ran


def is_stale(prior_round: RoundState, current_model_versions: dict) -> bool:
    """Returns True if any model version in prior_round's recorded
    source_model_versions no longer matches current_model_versions for the
    same model key -- meaning an edit happened after the round's report was
    written, and that report's PASS (if it was PASS) is no longer trustworthy.

    This is the direct implementation of: "A later edit to any model document
    within a round's boundary_scope invalidates the prior round's success for
    the affected model set; resume must check versions."
    """
    for model_key, recorded_version in prior_round.source_model_versions.items():
        current_version = current_model_versions.get(model_key)
        if current_version != recorded_version:
            return True
    return False


def resolve_round_for_resume(
    prior_round: Optional[RoundState],
    current_model_versions: dict,
) -> str:
    """Returns one of: 'no_prior_round', 'stale', 'valid'.

    A caller (orchestrator or manual resume) must not report alignment
    completion against a 'stale' prior round -- it must trigger a fresh
    validate_round() call instead. This function makes that decision
    mechanical rather than left to each call site's own judgment.
    """
    if prior_round is None:
        return "no_prior_round"
    if prior_round.status != "PASS":
        # A NEEDS_CLARIFICATION or INVALID_INPUT round was never "aligned" in
        # the first place; staleness is moot -- it still needs a fresh run.
        return "stale"
    if is_stale(prior_round, current_model_versions):
        return "stale"
    return "valid"


# ---------------------------------------------------------------------------
# Determinism helper
# ---------------------------------------------------------------------------

def reports_are_identical(report_a: dict, report_b: dict) -> bool:
    """Compares two rendered report JSON dicts for byte-for-byte-equivalent
    content, ignoring only the generated_at timestamp. Used by tests to
    prove validate_round() + report_to_json() together are deterministic:
    running the exact same inputs twice must produce the exact same findings
    in the exact same order with the exact same finding_ids.
    """
    a = {k: v for k, v in report_a.items() if k != "generated_at"}
    b = {k: v for k, v in report_b.items() if k != "generated_at"}
    return a == b
