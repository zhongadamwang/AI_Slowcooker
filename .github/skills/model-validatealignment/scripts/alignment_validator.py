"""Deterministic cross-model alignment validator (T01 fixture-proving skeleton).

This module implements just enough of the contract in
`references/cross-model-alignment-contract.md` to mechanically prove that the
five fixtures under `fixtures/` resolve to their `expected-report.json`
status. It is intentionally minimal: a full implementation (parsing real
domain-model.md/use-case-model.json/ui-model.json artifacts across arbitrary
project layouts) is the scope of a later task (model-validatealignment's own
build-out), not T01. T01's job is to prove the CONTRACT is checkable, using
hand-authored fixture data as direct Python structures mirroring each
fixture's scenario.md, not a full file-tree parser.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Section 1: Shared Reference Types (contract Section 1)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ScopedEntityRef:
    entity_id: str
    entity_name: str
    scope: str
    defined_in: str

    def identity(self) -> tuple:
        """Identity is (scope, entity_id) -- never entity_id alone (Section 1.1)."""
        return (self.scope, self.entity_id)


@dataclass(frozen=True)
class BoundaryRef:
    boundary_id: str
    boundary_type: str  # "software" | "non-software" | "unknown"
    hierarchy_level: int = 0
    hierarchy_path: str = ""
    parent_boundary_id: Optional[str] = None


@dataclass(frozen=True)
class ActorRef:
    actor_id: str
    actor_name: str
    boundary_id: str
    actor_kind: str = "human"


# ---------------------------------------------------------------------------
# Minimal model inputs (hand-authored, mirroring each fixture's scenario.md)
# ---------------------------------------------------------------------------

@dataclass
class DomainModelDoc:
    """Mirrors the *actual* parsed content of a domain-model.md file."""
    boundary_id: str
    entities: dict  # entity_id -> entity_name, as ACTUALLY present in the doc


@dataclass
class UseCaseModelDoc:
    boundary_ref: BoundaryRef
    actors: list = field(default_factory=list)
    use_cases: list = field(default_factory=list)
    referenced_entities: list = field(default_factory=list)  # ScopedEntityRef, claims made by the use-case model


@dataclass
class UIModelDoc:
    entries: list = field(default_factory=list)  # each entry: {"referenced_boundary_id": str}


@dataclass
class Finding:
    finding_id: str
    severity: str
    description: str
    affected_models: list


@dataclass
class AlignmentReport:
    round_id: str
    status: str
    findings: list = field(default_factory=list)
    clarification_questions: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# The validator (contract Section 4)
# ---------------------------------------------------------------------------

def validate_round(
    round_id: str,
    boundaries: list,
    domain_models: dict,              # boundary_id -> DomainModelDoc | None (None = missing)
    use_case_models: dict,            # boundary_id -> UseCaseModelDoc | None (None = missing)
    ui_models: dict,                  # boundary_id -> UIModelDoc | None (None = not applicable/absent)
) -> AlignmentReport:
    """Implements the PASS / NEEDS_CLARIFICATION / INVALID_INPUT decision
    exactly as specified in contract Section 4.3, resolving every reference
    against its claimed `defined_in` document rather than trusting the claim.
    """
    findings: list[Finding] = []
    clarifications: list[str] = []
    invalid = False

    for boundary in boundaries:
        bid = boundary.boundary_id

        # --- Boundary typing (Section 2.1): unknown is unresolved, never defaulted ---
        if boundary.boundary_type == "unknown":
            clarifications.append(
                f"Is {bid} a software system with its own UI, or a non-software "
                f"real-world boundary? This must be answered and recorded before "
                f"any UIModelEntry may reference it."
            )
            findings.append(Finding(
                finding_id=f"F-{len(findings)+1:03d}",
                severity="clarification-needed",
                description=(
                    f"Boundary {bid} has no explicitly declared boundary_type. "
                    f"Dependent use-case/UI content cannot proceed until this is resolved."
                ),
                affected_models=["use-case", "ui"],
            ))
            # An unknown boundary with a UI entry attempted against it is a
            # defense-in-depth catch; ui-generatemodel should never have
            # produced it, but the validator still flags it if present.
            ui_model = ui_models.get(bid)
            if ui_model and ui_model.entries:
                findings[-1] = Finding(
                    finding_id=findings[-1].finding_id,
                    severity="clarification-needed",
                    description=(
                        f"Boundary {bid} has undeclared boundary_type AND a UIModelEntry "
                        f"was attempted against it -- UI must only exist in explicitly "
                        f"software-typed boundaries (Section 2.2)."
                    ),
                    affected_models=["use-case", "ui"],
                )
            continue

        # --- R-011 enforcement: UI only in software boundaries (Section 2.2) ---
        ui_model = ui_models.get(bid)
        if boundary.boundary_type == "non-software" and ui_model and ui_model.entries:
            findings.append(Finding(
                finding_id=f"F-{len(findings)+1:03d}",
                severity="error",
                description=(
                    f"Boundary {bid} is non-software but has {len(ui_model.entries)} "
                    f"UIModelEntry/entries referencing it. UI may only exist in "
                    f"explicitly software-typed boundaries."
                ),
                affected_models=["ui"],
            ))
            invalid = True

        # --- Missing applicable model (Section 4.3: INVALID_INPUT, not silent skip) ---
        if boundary.boundary_type == "software":
            use_case_model = use_case_models.get(bid)
            if use_case_model is None:
                findings.append(Finding(
                    finding_id=f"F-{len(findings)+1:03d}",
                    severity="error",
                    description=(
                        f"use-case-model.json is required for boundary {bid} "
                        f"(a software boundary in round scope) but does not exist. "
                        f"Reported as a missing applicable model, not silently "
                        f"treated as not-applicable."
                    ),
                    affected_models=["use-case"],
                ))
                invalid = True
                continue  # cannot check entity references without the model

            # --- Manifest/source disagreement (Section 1.1, 4.3): resolve for real ---
            domain_model = domain_models.get(bid)
            for ref in use_case_model.referenced_entities:
                if domain_model is None or ref.entity_id not in domain_model.entities:
                    findings.append(Finding(
                        finding_id=f"F-{len(findings)+1:03d}",
                        severity="error",
                        description=(
                            f"Use case references entity {ref.entity_id} "
                            f"({ref.entity_name}) claiming it is defined in "
                            f"{ref.defined_in}, but that document does not "
                            f"actually contain an entity with that ID."
                        ),
                        affected_models=["domain", "use-case"],
                    ))
                    invalid = True

    if invalid:
        status = "INVALID_INPUT"
    elif clarifications:
        status = "NEEDS_CLARIFICATION"
    else:
        status = "PASS"

    return AlignmentReport(
        round_id=round_id,
        status=status,
        findings=findings,
        clarification_questions=clarifications,
    )


def entity_identity_demo(entity_a: ScopedEntityRef, entity_b: ScopedEntityRef) -> bool:
    """Returns True if the two scoped entity references are the SAME entity.

    Identity is (scope, entity_id) per Section 1.1 -- this directly proves the
    three-level-valid fixture's collision (same entity_id, different scope)
    resolves as two DIFFERENT entities, not a conflict.
    """
    return entity_a.identity() == entity_b.identity()
