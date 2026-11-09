"""CLI entry point: run the validator against each fixture and write real
alignment-report-[round-id].md/.json output, then diff against each
fixture's expected-report.json to prove end-to-end behavior, not just the
in-memory unit tests in test_alignment_contract.py / test_alignment_report.py.

Usage: python3 run_fixtures.py
Writes reports to: ../fixtures/[fixture-name]/generated-report.json/.md
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from alignment_validator import (
    BoundaryRef,
    DomainModelDoc,
    ScopedEntityRef,
    UIModelDoc,
    UseCaseModelDoc,
    validate_round,
)
from alignment_report import report_to_json, report_to_markdown

FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures"


def run_three_level_valid():
    boundaries = [
        BoundaryRef("BND-ROOT", "non-software", 0, "root-boundary/", None),
        BoundaryRef("BND-CHILD-SW", "software", 1, "root-boundary/child-software-boundary/", "BND-ROOT"),
        BoundaryRef("BND-GRANDCHILD", "software", 2, "root-boundary/child-software-boundary/grandchild-boundary/", "BND-CHILD-SW"),
    ]
    domain_models = {
        "BND-ROOT": DomainModelDoc("BND-ROOT", {"E-001": "Customer", "E-002": "ServiceRequest"}),
        "BND-CHILD-SW": DomainModelDoc("BND-CHILD-SW", {"E-002": "ServiceRequest", "E-003": "Technician"}),
        "BND-GRANDCHILD": DomainModelDoc("BND-GRANDCHILD", {"E-004": "TimeEntry"}),
    }
    use_case_models = {
        "BND-CHILD-SW": UseCaseModelDoc(boundary_ref=boundaries[1]),
        "BND-GRANDCHILD": UseCaseModelDoc(boundary_ref=boundaries[2]),
    }
    report = validate_round(
        round_id="ROUND-FIXTURE-001",
        boundaries=boundaries,
        domain_models=domain_models,
        use_case_models=use_case_models,
        ui_models={},
    )
    versions = {"domain_model": "fixture-v1", "process_model": "fixture-v1 (not exercised by this fixture)",
                "use_case_model": "fixture-v1 (not exercised by this fixture)", "ui_model": None}
    return report, boundaries, versions


def run_unknown_boundary_type():
    boundaries = [BoundaryRef("BND-UNCLASSIFIED", "unknown", 0, "unclassified-boundary/", None)]
    report = validate_round(
        round_id="ROUND-FIXTURE-002",
        boundaries=boundaries,
        domain_models={},
        use_case_models={"BND-UNCLASSIFIED": UseCaseModelDoc(boundary_ref=boundaries[0])},
        ui_models={},
    )
    versions = {"domain_model": "fixture-v1", "process_model": "fixture-v1",
                "use_case_model": "fixture-v1", "ui_model": None}
    return report, boundaries, versions


def run_missing_applicable_model():
    boundaries = [BoundaryRef("BND-ORDER-INTAKE", "software", 0, "order-intake-boundary/", None)]
    report = validate_round(
        round_id="ROUND-FIXTURE-003",
        boundaries=boundaries,
        domain_models={"BND-ORDER-INTAKE": DomainModelDoc("BND-ORDER-INTAKE", {"E-100": "Order"})},
        use_case_models={},
        ui_models={},
    )
    versions = {"domain_model": "fixture-v1", "process_model": "fixture-v1",
                "use_case_model": "MISSING", "ui_model": "MISSING"}
    return report, boundaries, versions


def run_manifest_source_disagreement():
    boundaries = [BoundaryRef("BND-BILLING", "software", 0, "billing-boundary/", None)]
    domain_models = {"BND-BILLING": DomainModelDoc("BND-BILLING", {"E-010": "Invoice"})}
    false_claim = ScopedEntityRef(
        entity_id="E-011", entity_name="DiscountCode",
        scope="billing-boundary", defined_in="billing-boundary/domain-model.md",
    )
    use_case_models = {"BND-BILLING": UseCaseModelDoc(boundary_ref=boundaries[0], referenced_entities=[false_claim])}
    report = validate_round(
        round_id="ROUND-FIXTURE-004",
        boundaries=boundaries,
        domain_models=domain_models,
        use_case_models=use_case_models,
        ui_models={},
    )
    versions = {"domain_model": "fixture-v1", "process_model": "fixture-v1 (not exercised)",
                "use_case_model": "fixture-v1", "ui_model": None}
    return report, boundaries, versions


def run_software_boundary_no_ui_required():
    boundaries = [BoundaryRef("BND-BATCH-RECON", "software", 0, "batch-recon-boundary/", None)]
    use_case_models = {
        "BND-BATCH-RECON": UseCaseModelDoc(
            boundary_ref=boundaries[0],
            actors=[{"actor_id": "A-001", "actor_name": "Nightly Scheduler"}],
            use_cases=[{"use_case_id": "UC-001", "name": "Reconcile Daily Transactions"}],
        ),
    }
    ui_models = {"BND-BATCH-RECON": UIModelDoc(entries=[])}
    report = validate_round(
        round_id="ROUND-FIXTURE-005",
        boundaries=boundaries,
        domain_models={},
        use_case_models=use_case_models,
        ui_models=ui_models,
    )
    versions = {"domain_model": "fixture-v1 (not exercised)", "process_model": "fixture-v1 (not exercised)",
                "use_case_model": "fixture-v1", "ui_model": "fixture-v1"}
    return report, boundaries, versions


FIXTURE_RUNNERS = {
    "three-level-valid": run_three_level_valid,
    "unknown-boundary-type": run_unknown_boundary_type,
    "missing-applicable-model": run_missing_applicable_model,
    "manifest-source-disagreement": run_manifest_source_disagreement,
    "software-boundary-no-ui-required": run_software_boundary_no_ui_required,
}


def main():
    all_matched = True
    for name, runner in FIXTURE_RUNNERS.items():
        report, boundaries, versions = runner()
        rendered = report_to_json(report, boundaries, versions, generated_at="2026-11-08T00:00:00Z")
        fixture_dir = FIXTURES_DIR / name
        (fixture_dir / "generated-report.json").write_text(json.dumps(rendered, indent=2) + "\n", encoding="utf-8")
        (fixture_dir / "generated-report.md").write_text(report_to_markdown(rendered), encoding="utf-8")

        expected = json.loads((fixture_dir / "expected-report.json").read_text(encoding="utf-8"))
        status_match = rendered["status"] == expected["status"]
        marker = "OK" if status_match else "MISMATCH"
        if not status_match:
            all_matched = False
        print(f"[{marker}] {name}: generated status={rendered['status']!r}, expected status={expected['status']!r}")

    if not all_matched:
        print("\nFAILURE: one or more fixtures did not match their expected status.")
        sys.exit(1)
    print("\nAll 5 fixtures: generated status matches expected-report.json status.")


if __name__ == "__main__":
    main()
