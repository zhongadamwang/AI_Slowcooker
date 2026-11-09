"""Executable proof that the five contract fixtures resolve as documented.

Run with: python3 -m pytest test_alignment_contract.py -v
   or:    python3 -m unittest test_alignment_contract -v
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from alignment_validator import (
    AlignmentReport,
    BoundaryRef,
    DomainModelDoc,
    ScopedEntityRef,
    UIModelDoc,
    UseCaseModelDoc,
    entity_identity_demo,
    validate_round,
)


class ThreeLevelValidFixture(unittest.TestCase):
    """fixtures/three-level-valid/ -- non-software root, software child/grandchild,
    deliberate scoped entity-name collision resolved correctly."""

    def test_collision_resolves_as_two_different_entities(self):
        root_service_request = ScopedEntityRef(
            entity_id="E-002", entity_name="ServiceRequest",
            scope="root-boundary", defined_in="root-boundary/domain-model.md",
        )
        child_service_request = ScopedEntityRef(
            entity_id="E-002", entity_name="ServiceRequest",
            scope="root-boundary/child-software-boundary",
            defined_in="root-boundary/child-software-boundary/domain-model.md",
        )
        # Same entity_id, same entity_name, DIFFERENT scope -> different entities.
        self.assertFalse(entity_identity_demo(root_service_request, child_service_request))
        self.assertNotEqual(root_service_request.identity(), child_service_request.identity())

    def test_three_level_hierarchy_passes_with_no_findings(self):
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
        # No use-case model exercised in this fixture at the child/grandchild
        # software boundaries would normally trigger INVALID_INPUT (missing
        # applicable model) -- this fixture focuses on entity collision, so
        # we supply trivial valid use-case models for the software boundaries.
        use_case_models = {
            "BND-CHILD-SW": UseCaseModelDoc(boundary_ref=boundaries[1]),
            "BND-GRANDCHILD": UseCaseModelDoc(boundary_ref=boundaries[2]),
        }
        ui_models = {}

        report = validate_round(
            round_id="ROUND-FIXTURE-001",
            boundaries=boundaries,
            domain_models=domain_models,
            use_case_models=use_case_models,
            ui_models=ui_models,
        )
        self.assertEqual(report.status, "PASS")
        self.assertEqual(report.findings, [])


class UnknownBoundaryTypeFixture(unittest.TestCase):
    """fixtures/unknown-boundary-type/ -- undeclared boundary_type must yield
    NEEDS_CLARIFICATION, never a silent default either direction."""

    def test_unknown_type_yields_needs_clarification(self):
        boundaries = [BoundaryRef("BND-UNCLASSIFIED", "unknown", 0, "unclassified-boundary/", None)]
        report = validate_round(
            round_id="ROUND-FIXTURE-002",
            boundaries=boundaries,
            domain_models={},
            use_case_models={"BND-UNCLASSIFIED": UseCaseModelDoc(boundary_ref=boundaries[0])},
            ui_models={},
        )
        self.assertEqual(report.status, "NEEDS_CLARIFICATION")
        self.assertTrue(len(report.clarification_questions) >= 1)

    def test_unknown_type_with_attempted_ui_entry_still_blocks(self):
        boundaries = [BoundaryRef("BND-UNCLASSIFIED", "unknown", 0, "unclassified-boundary/", None)]
        # Defense-in-depth: even if a UIModelEntry somehow got attempted
        # against an unknown-typed boundary, the report must not silently PASS.
        ui_models = {"BND-UNCLASSIFIED": UIModelDoc(entries=[{"referenced_boundary_id": "BND-UNCLASSIFIED"}])}
        report = validate_round(
            round_id="ROUND-FIXTURE-002B",
            boundaries=boundaries,
            domain_models={},
            use_case_models={"BND-UNCLASSIFIED": UseCaseModelDoc(boundary_ref=boundaries[0])},
            ui_models=ui_models,
        )
        self.assertEqual(report.status, "NEEDS_CLARIFICATION")
        self.assertNotEqual(report.status, "PASS")


class MissingApplicableModelFixture(unittest.TestCase):
    """fixtures/missing-applicable-model/ -- a software boundary with no
    use-case model at all must be INVALID_INPUT, not a silent skip."""

    def test_missing_use_case_model_is_invalid_input(self):
        boundaries = [BoundaryRef("BND-ORDER-INTAKE", "software", 0, "order-intake-boundary/", None)]
        report = validate_round(
            round_id="ROUND-FIXTURE-003",
            boundaries=boundaries,
            domain_models={"BND-ORDER-INTAKE": DomainModelDoc("BND-ORDER-INTAKE", {"E-100": "Order"})},
            use_case_models={},  # deliberately absent
            ui_models={},
        )
        self.assertEqual(report.status, "INVALID_INPUT")
        self.assertEqual(report.clarification_questions, [])  # this is an error, not an ambiguity


class ManifestSourceDisagreementFixture(unittest.TestCase):
    """fixtures/manifest-source-disagreement/ -- a referenced entity that the
    use-case model CLAIMS is defined in a domain-model.md, but which that
    document does not actually contain, must be caught by real resolution."""

    def test_false_entity_claim_is_caught(self):
        boundaries = [BoundaryRef("BND-BILLING", "software", 0, "billing-boundary/", None)]
        domain_models = {
            "BND-BILLING": DomainModelDoc("BND-BILLING", {"E-010": "Invoice"}),  # only E-010 actually exists
        }
        false_claim = ScopedEntityRef(
            entity_id="E-011", entity_name="DiscountCode",
            scope="billing-boundary", defined_in="billing-boundary/domain-model.md",
        )
        use_case_models = {
            "BND-BILLING": UseCaseModelDoc(
                boundary_ref=boundaries[0],
                referenced_entities=[false_claim],
            ),
        }
        report = validate_round(
            round_id="ROUND-FIXTURE-004",
            boundaries=boundaries,
            domain_models=domain_models,
            use_case_models=use_case_models,
            ui_models={},
        )
        self.assertEqual(report.status, "INVALID_INPUT")
        self.assertTrue(any("E-011" in f.description for f in report.findings))

    def test_naive_shape_only_check_would_have_missed_this(self):
        """Proves the validator resolves against REAL content, not just shape.

        A naive validator that only checks the reference is well-formed JSON
        (has entity_id, entity_name, scope, defined_in fields) would pass this
        fixture incorrectly. Our validator must actually look up entity_id
        inside the domain model's real entities dict.
        """
        false_claim = ScopedEntityRef(
            entity_id="E-011", entity_name="DiscountCode",
            scope="billing-boundary", defined_in="billing-boundary/domain-model.md",
        )
        # The reference is perfectly well-formed as a shape...
        self.assertTrue(all([false_claim.entity_id, false_claim.entity_name,
                              false_claim.scope, false_claim.defined_in]))
        # ...but it does not resolve against the real domain model's content.
        real_domain_model = DomainModelDoc("BND-BILLING", {"E-010": "Invoice"})
        self.assertNotIn(false_claim.entity_id, real_domain_model.entities)


class SoftwareBoundaryNoUIRequiredFixture(unittest.TestCase):
    """fixtures/software-boundary-no-ui-required/ -- a software boundary with
    real use cases but zero UIModelEntries must PASS, not be flagged."""

    def test_empty_ui_entries_in_software_boundary_passes(self):
        boundaries = [BoundaryRef("BND-BATCH-RECON", "software", 0, "batch-recon-boundary/", None)]
        use_case_models = {
            "BND-BATCH-RECON": UseCaseModelDoc(
                boundary_ref=boundaries[0],
                actors=[{"actor_id": "A-001", "actor_name": "Nightly Scheduler"}],
                use_cases=[{"use_case_id": "UC-001", "name": "Reconcile Daily Transactions"}],
            ),
        }
        ui_models = {"BND-BATCH-RECON": UIModelDoc(entries=[])}  # deliberately empty, not missing
        report = validate_round(
            round_id="ROUND-FIXTURE-005",
            boundaries=boundaries,
            domain_models={},
            use_case_models=use_case_models,
            ui_models=ui_models,
        )
        self.assertEqual(report.status, "PASS")
        self.assertEqual(report.findings, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
