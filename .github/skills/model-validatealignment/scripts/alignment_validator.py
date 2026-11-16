"""Deterministic cross-model alignment validator.

Implements the decision logic of `references/cross-model-alignment-contract.md`
Section 4 over in-memory model documents. `alignment_loader.py` builds those
documents from real boundary folders (main.md, domain-model.md,
use-case-model.json + scripts, ui-model.json); `validate_alignment.py` is the
command-line entry point. Tests may also construct the documents directly.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

BOUNDARY_TYPES = ("software", "non-software", "unknown")
UNRESOLVED_MARKER = "[UNRESOLVED"


# ---------------------------------------------------------------------------
# Shared reference types (contract Section 1)
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
    boundary_name: str = ""


@dataclass(frozen=True)
class ActorRef:
    actor_id: str
    actor_name: str
    boundary_id: str
    actor_kind: str = "human"


# ---------------------------------------------------------------------------
# Model documents
# ---------------------------------------------------------------------------

@dataclass
class DomainModelDoc:
    """The entities actually present in a boundary's domain-model.md."""
    boundary_id: str
    entities: dict  # entity_id -> entity_name; an entity without an ID is keyed by its name

    def resolves(self, ref: str) -> bool:
        """An entity reference resolves by ID or by exact (case-insensitive) name."""
        wanted = ref.strip().casefold()
        return any(wanted in (eid.casefold(), name.casefold()) for eid, name in self.entities.items())


@dataclass
class ScriptDoc:
    """What the validator needs from one use-case script file."""
    path: str
    has_ui_references: bool = False


@dataclass
class UseCaseModelDoc:
    boundary_ref: BoundaryRef  # as declared inside the use-case model itself
    actors: list = field(default_factory=list)       # dicts with actor_id
    use_cases: list = field(default_factory=list)    # dicts as in use-case-model.json
    referenced_entities: list = field(default_factory=list)  # ScopedEntityRef claims made by the model/scripts
    scripts: dict = field(default_factory=dict)      # use_case_id -> ScriptDoc, or None when script_ref does not resolve


@dataclass
class UIModelDoc:
    entries: list = field(default_factory=list)  # dicts as in ui-model.json's entries


@dataclass
class Finding:
    finding_id: str
    severity: str  # "error" | "clarification-needed"
    description: str
    affected_models: list
    reference_a: Optional[dict] = None
    reference_b: Optional[dict] = None


@dataclass
class AlignmentReport:
    round_id: str
    status: str
    findings: list = field(default_factory=list)
    clarification_questions: list = field(default_factory=list)


def _ref_id(ref, key: str) -> Optional[str]:
    """A reference may be a bare ID string or an object carrying the ID under `key`."""
    if isinstance(ref, dict):
        return ref.get(key)
    return ref


# ---------------------------------------------------------------------------
# The validator (contract Section 4)
# ---------------------------------------------------------------------------

def validate_round(
    round_id: str,
    boundaries: list,
    domain_models: dict,              # boundary_id -> DomainModelDoc | None (None = missing)
    use_case_models: dict,            # boundary_id -> UseCaseModelDoc | None (None = missing)
    ui_models: dict,                  # boundary_id -> UIModelDoc | None (None = absent)
    load_errors: Optional[list] = None,  # (boundary_id, model, message) for files that exist but could not be read
) -> AlignmentReport:
    """Decide PASS / NEEDS_CLARIFICATION / INVALID_INPUT per contract Section 4.3,
    resolving every reference against the documents it claims to point at.
    """
    findings: list = []
    clarifications: list = []
    unreadable = set()

    def add(severity, description, affected, reference_a=None, reference_b=None):
        findings.append(Finding(
            finding_id=f"F-{len(findings) + 1:03d}",
            severity=severity,
            description=description,
            affected_models=affected,
            reference_a=reference_a,
            reference_b=reference_b,
        ))

    for bid, model, message in load_errors or []:
        unreadable.add((bid, model))
        add("error", f"The {model} model for boundary {bid} could not be read: {message}", [model],
            {"boundary_id": bid})

    for boundary in boundaries:
        bid = boundary.boundary_id
        bref = {"boundary_id": bid, "boundary_type": boundary.boundary_type}
        ui_model = ui_models.get(bid)
        ui_entries = ui_model.entries if ui_model else []

        # --- Boundary typing (Section 2.1): unknown is unresolved, never defaulted ---
        if boundary.boundary_type == "unknown":
            clarifications.append(
                f"Is {bid} a software system with its own UI, or a non-software "
                f"real-world boundary? This must be answered and recorded in its "
                f"main.md System Boundary section before any UIModelEntry may reference it."
            )
            if ui_entries:
                # Defense in depth: ui-generatemodel should never have produced these.
                description = (
                    f"Boundary {bid} has undeclared boundary_type AND a UIModelEntry "
                    f"was attempted against it -- UI must only exist in explicitly "
                    f"software-typed boundaries (Section 2.2)."
                )
            else:
                description = (
                    f"Boundary {bid} has no explicitly declared boundary_type. "
                    f"Dependent use-case/UI content cannot proceed until this is resolved."
                )
            add("clarification-needed", description, ["use-case", "ui"], bref)
            continue

        if boundary.boundary_type not in BOUNDARY_TYPES:
            add("error",
                f"Boundary {bid} declares boundary_type '{boundary.boundary_type}', which is not one of "
                f"software, non-software, or unknown.", ["use-case", "ui"], bref)
            continue

        # --- R-011: UI only in software boundaries (Section 2.2) ---
        if boundary.boundary_type == "non-software" and ui_entries:
            add("error",
                f"Boundary {bid} is non-software but has {len(ui_entries)} "
                f"UIModelEntry/entries referencing it. UI may only exist in "
                f"explicitly software-typed boundaries.", ["ui"], bref)

        # --- Missing applicable models (Section 4.3: INVALID_INPUT, not a silent skip) ---
        domain_model = domain_models.get(bid)
        if domain_model is None and (bid, "domain") not in unreadable:
            add("error",
                f"domain-model.md is required for boundary {bid} but does not exist. "
                f"Entity references for this boundary cannot be resolved.", ["domain"], bref)

        use_case_model = use_case_models.get(bid)
        if use_case_model is None:
            if (bid, "use-case") not in unreadable:
                add("error",
                    f"use-case-model.json is required for boundary {bid} "
                    f"(a {boundary.boundary_type} boundary in round scope) but does not exist. "
                    f"Reported as a missing applicable model, not silently "
                    f"treated as not-applicable.", ["use-case"], bref)
        else:
            _check_use_case_model(boundary, use_case_model, domain_model, add)

        if boundary.boundary_type == "software":
            _check_ui_model(boundary, ui_entries, domain_model, use_case_model, add, clarifications)

    if any(f.severity == "error" for f in findings):
        status = "INVALID_INPUT"
    elif clarifications or findings:
        status = "NEEDS_CLARIFICATION"
    else:
        status = "PASS"

    return AlignmentReport(
        round_id=round_id,
        status=status,
        findings=findings,
        clarification_questions=clarifications,
    )


def _check_use_case_model(boundary, model, domain_model, add):
    bid = boundary.boundary_id
    bref = {"boundary_id": bid, "boundary_type": boundary.boundary_type}

    # The use-case model's own boundary_ref must agree with main.md (the owning document, Section 1.4).
    declared = model.boundary_ref
    if declared.boundary_id != bid or declared.boundary_type != boundary.boundary_type:
        add("error",
            f"The use-case model for boundary {bid} declares boundary_ref "
            f"{declared.boundary_id} ({declared.boundary_type}), but main.md declares "
            f"{bid} ({boundary.boundary_type}). main.md is the authoritative source.",
            ["use-case"], bref,
            {"boundary_id": declared.boundary_id, "boundary_type": declared.boundary_type})

    actor_ids = {a.get("actor_id") for a in model.actors if isinstance(a, dict)}
    for uc in model.use_cases:
        ucid = uc.get("use_case_id", "<no id>")
        uref = {"use_case_id": ucid, "boundary_id": bid}
        actor = _ref_id(uc.get("primary_actor_ref"), "actor_id")
        if actor is not None and actor not in actor_ids:
            add("error",
                f"Use case {ucid} in boundary {bid} names primary actor {actor}, "
                f"which is not defined in this boundary's use-case model.", ["use-case"], uref)
        uc_boundary = _ref_id(uc.get("boundary_ref"), "boundary_id")
        if uc_boundary is not None and uc_boundary != bid:
            add("error",
                f"Use case {ucid} references boundary {uc_boundary}, but it belongs to the "
                f"use-case model of boundary {bid}. A use case never references a different boundary.",
                ["use-case"], uref, {"boundary_id": uc_boundary})
        for req in uc.get("requirement_refs") or []:
            if UNRESOLVED_MARKER in str(req):
                add("clarification-needed",
                    f"Use case {ucid} in boundary {bid} carries an unresolved requirement reference: {req}",
                    ["use-case"], uref)
        if ucid in model.scripts:
            script = model.scripts[ucid]
            if script is None:
                add("error",
                    f"Use case {ucid} in boundary {bid} points at script "
                    f"{uc.get('script_ref')}, which does not exist.", ["use-case"], uref)
            elif script.has_ui_references and boundary.boundary_type != "software":
                add("error",
                    f"The script for use case {ucid} ({script.path}) has a UI References section, "
                    f"but boundary {bid} is {boundary.boundary_type}. UI references are only "
                    f"permitted in software boundaries (Section 2.2).", ["use-case", "ui"], uref)

    # Entity references must resolve against the real domain model, not be trusted as claims (Section 1.1).
    seen = set()
    for ref in model.referenced_entities:
        if ref.entity_id in seen:
            continue
        seen.add(ref.entity_id)
        if domain_model is None or not domain_model.resolves(ref.entity_id):
            label = f" ({ref.entity_name})" if ref.entity_name else ""
            add("error",
                f"Use case references entity {ref.entity_id}{label} claiming it is defined in "
                f"{ref.defined_in}, but that document does not actually contain an entity with that ID.",
                ["domain", "use-case"],
                {"entity_id": ref.entity_id, "entity_name": ref.entity_name,
                 "scope": ref.scope, "defined_in": ref.defined_in})


def _check_ui_model(boundary, entries, domain_model, use_case_model, add, clarifications):
    bid = boundary.boundary_id
    use_case_ids = {uc.get("use_case_id") for uc in use_case_model.use_cases} if use_case_model else set()
    for entry in entries:
        eid = entry.get("entry_id", "<no id>")
        eref = {"entry_id": eid, "boundary_id": bid}
        entry_boundary = entry.get("boundary_ref", entry.get("referenced_boundary_id"))
        if entry_boundary is not None and entry_boundary != bid:
            add("error",
                f"UIModelEntry {eid} in boundary {bid}'s UI model declares boundary_ref "
                f"{entry_boundary}. An entry belongs to the boundary whose UI model contains it.",
                ["ui"], eref, {"boundary_id": entry_boundary})
        for ref in entry.get("domain_entity_refs") or []:
            if UNRESOLVED_MARKER in str(ref):
                clarifications.append(
                    f"UIModelEntry {eid} in boundary {bid} has an unresolved entity reference ({ref}). "
                    f"Which entity should it reference, or should the entry be removed?")
                add("clarification-needed",
                    f"UIModelEntry {eid} in boundary {bid} carries an unresolved entity reference: {ref}",
                    ["domain", "ui"], eref)
            elif domain_model is None or not domain_model.resolves(str(ref)):
                add("error",
                    f"UIModelEntry {eid} references entity {ref}, which is not defined in "
                    f"boundary {bid}'s domain model.", ["domain", "ui"], eref, {"entity_ref": ref})
        for ref in entry.get("source_use_case_refs") or []:
            if UNRESOLVED_MARKER in str(ref):
                add("clarification-needed",
                    f"UIModelEntry {eid} in boundary {bid} carries an unresolved use-case reference: {ref}",
                    ["use-case", "ui"], eref)
            elif ref not in use_case_ids:
                add("error",
                    f"UIModelEntry {eid} cites use case {ref}, which is not defined in "
                    f"boundary {bid}'s use-case model.", ["use-case", "ui"], eref, {"use_case_id": ref})


def entity_identity_demo(entity_a: ScopedEntityRef, entity_b: ScopedEntityRef) -> bool:
    """Returns True if the two scoped entity references are the SAME entity.

    Identity is (scope, entity_id) per Section 1.1: the same entity_id in two
    different scopes is two different entities, not a conflict.
    """
    return entity_a.identity() == entity_b.identity()
