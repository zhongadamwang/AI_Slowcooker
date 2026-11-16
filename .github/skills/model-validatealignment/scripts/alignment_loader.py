"""Load real boundary folders into the documents alignment_validator.py checks.

A boundary folder is any folder holding a main.md. The loader reads:
  main.md               -> BoundaryRef, from its "## System Boundary" section
  domain-model.md       -> DomainModelDoc
  use-case-model.json   -> UseCaseModelDoc (plus the scripts it links to)
  ui-model.json         -> UIModelDoc
and computes a content version (hash) for each model, so a later edit can be
detected as staleness (contract Section 4.4).
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from alignment_validator import (
    BOUNDARY_TYPES,
    BoundaryRef,
    DomainModelDoc,
    ScopedEntityRef,
    ScriptDoc,
    UIModelDoc,
    UseCaseModelDoc,
)

_FIELD = re.compile(r"^\s*[-*]\s*\*\*(.+?)\*\*\s*:\s*(.*)$")
_ENTITY_HEADING = re.compile(r"^#{2,4}\s+(.+?)\s*\*\((E-\d+)\)\*\s*$")
_MERMAID_CLASS = re.compile(r"^\s*class\s+([A-Za-z_]\w*)")
_ENTITY_ID = re.compile(r"\bE-\d{3,}\b")


@dataclass
class LoadedRound:
    boundaries: list = field(default_factory=list)       # BoundaryRef, in scope order
    folders: dict = field(default_factory=dict)          # boundary_id -> folder path as recorded in the report
    domain_models: dict = field(default_factory=dict)
    use_case_models: dict = field(default_factory=dict)
    ui_models: dict = field(default_factory=dict)
    versions: dict = field(default_factory=dict)         # boundary_id -> {model: hash | None}
    load_errors: list = field(default_factory=list)      # (boundary_id, model, message)


def _hash(paths: list) -> Optional[str]:
    """Content hash over the given files, or None when none of them exist."""
    existing = [p for p in paths if p.is_file()]
    if not existing:
        return None
    digest = hashlib.sha256()
    for path in sorted(existing):
        digest.update(path.name.encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()[:16]


def _section(text: str, heading: str) -> Optional[str]:
    """Return the body of a '## heading' section, or None when it is absent."""
    m = re.search(rf"^##\s+{re.escape(heading)}\s*$", text, re.M)
    if not m:
        return None
    rest = text[m.end():]
    nxt = re.search(r"^##\s+", rest, re.M)
    return rest[:nxt.start()] if nxt else rest


def _value(raw: str) -> str:
    """A field's value is its first `backticked` token when it has one, else the raw text."""
    m = re.search(r"`([^`]+)`", raw)
    return (m.group(1) if m else raw).strip()


def parse_boundary(main_md: Path, folder_label: str) -> BoundaryRef:
    """Read main.md's System Boundary section. A missing section, missing
    Boundary Type line, or any value other than software/non-software is
    reported as-is ('unknown' when undeclared) -- never inferred or defaulted.
    """
    text = main_md.read_text(encoding="utf-8")
    title = re.search(r"^#\s+(.+)$", text, re.M)
    name = re.sub(r"\s+[—-]\s+Main$", "", title.group(1).strip()) if title else main_md.parent.name
    fields = {}
    for line in (_section(text, "System Boundary") or "").splitlines():
        m = _FIELD.match(line)
        if m:
            fields[m.group(1).strip().lower()] = m.group(2)

    raw_type = fields.get("boundary type")
    if raw_type is None:
        boundary_type = "unknown"
    else:
        boundary_type = _value(raw_type)
        if not re.search(r"`[^`]+`", raw_type) and boundary_type not in BOUNDARY_TYPES:
            # Prose such as "(not yet declared)" is an undeclared type, not an invalid one.
            boundary_type = "unknown"

    parent = _value(fields.get("parent boundary id", "none"))
    if not parent or parent.lower().startswith("none"):
        parent = None
    level = re.search(r"^\*\*Level\*\*:\s*(\d+)", text, re.M)
    return BoundaryRef(
        boundary_id=_value(fields["boundary id"]) if "boundary id" in fields else main_md.parent.name,
        boundary_type=boundary_type,
        hierarchy_level=int(level.group(1)) if level else 0,
        hierarchy_path=folder_label,
        parent_boundary_id=parent,
        boundary_name=name,
    )


def parse_domain_model(path: Path, boundary_id: str) -> DomainModelDoc:
    """Entities are '### Name *(E-001)*' headings and Mermaid 'class Name' declarations."""
    entities = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        heading = _ENTITY_HEADING.match(line)
        if heading:
            entities[heading.group(2)] = heading.group(1).strip()
            continue
        cls = _MERMAID_CLASS.match(line)
        if cls and cls.group(1) not in entities.values():
            entities.setdefault(cls.group(1), cls.group(1))
    return DomainModelDoc(boundary_id, entities)


def _load_use_case_model(folder: Path, label: str, boundary: BoundaryRef) -> tuple:
    """Returns (UseCaseModelDoc, script paths) for a folder's use-case-model.json."""
    data = json.loads((folder / "use-case-model.json").read_text(encoding="utf-8"))
    ref = data.get("boundary_ref") or {}
    declared = BoundaryRef(
        boundary_id=ref.get("boundary_id", boundary.boundary_id),
        boundary_type=ref.get("boundary_type", boundary.boundary_type),
    )
    domain_path = f"{label}/domain-model.md"
    claims, scripts, script_paths = [], {}, []
    for uc in data.get("use_cases", []):
        for claim in uc.get("referenced_entities", []):
            claims.append(ScopedEntityRef(claim.get("entity_id", ""), claim.get("entity_name", ""),
                                          claim.get("scope", label), claim.get("defined_in", domain_path)))
        script_ref = uc.get("script_ref")
        if not script_ref:
            continue
        script_path = folder / script_ref
        if not script_path.is_file():
            scripts[uc.get("use_case_id")] = None
            continue
        script_paths.append(script_path)
        text = script_path.read_text(encoding="utf-8")
        scripts[uc.get("use_case_id")] = ScriptDoc(
            path=f"{label}/{script_ref}",
            has_ui_references=bool(re.search(r"^##\s+UI References\s*$", text, re.M)),
        )
        for entity_id in sorted(set(_ENTITY_ID.findall(text))):
            claims.append(ScopedEntityRef(entity_id, "", label, domain_path))
    doc = UseCaseModelDoc(boundary_ref=declared, actors=data.get("actors", []),
                          use_cases=data.get("use_cases", []), referenced_entities=claims, scripts=scripts)
    return doc, script_paths


def discover_boundaries(root: Path) -> list:
    """Every folder at or below root whose main.md has a System Boundary section, parents first."""
    found = []
    for main_md in sorted(root.rglob("main.md"), key=lambda p: (len(p.parts), p.as_posix())):
        if _section(main_md.read_text(encoding="utf-8"), "System Boundary") is not None:
            found.append(main_md.parent)
    return found


def load_round(folders: list, base_dir: Path) -> LoadedRound:
    """Load every boundary folder in scope. Paths recorded in the result are relative to base_dir."""
    loaded = LoadedRound()
    for folder in folders:
        folder = Path(folder).resolve()
        main_md = folder / "main.md"
        if not main_md.is_file():
            raise ValueError(f"not a boundary folder (no main.md): {folder}")
        try:
            label = folder.relative_to(Path(base_dir).resolve()).as_posix()
        except ValueError:
            label = folder.as_posix()
        boundary = parse_boundary(main_md, label)
        bid = boundary.boundary_id
        if bid in loaded.folders:
            raise ValueError(f"boundary ID {bid} is declared by both {loaded.folders[bid]} and {label}")
        loaded.boundaries.append(boundary)
        loaded.folders[bid] = label

        domain_path = folder / "domain-model.md"
        loaded.domain_models[bid] = parse_domain_model(domain_path, bid) if domain_path.is_file() else None

        script_paths = []
        loaded.use_case_models[bid] = None
        if (folder / "use-case-model.json").is_file():
            try:
                loaded.use_case_models[bid], script_paths = _load_use_case_model(folder, label, boundary)
            except (json.JSONDecodeError, AttributeError, TypeError) as exc:
                loaded.load_errors.append((bid, "use-case", f"{label}/use-case-model.json: {exc}"))

        loaded.ui_models[bid] = None
        if (folder / "ui-model.json").is_file():
            try:
                data = json.loads((folder / "ui-model.json").read_text(encoding="utf-8"))
                loaded.ui_models[bid] = UIModelDoc(entries=data.get("entries", []))
            except (json.JSONDecodeError, AttributeError) as exc:
                loaded.load_errors.append((bid, "ui", f"{label}/ui-model.json: {exc}"))

        loaded.versions[bid] = {
            "boundary": _hash([main_md]),
            "domain_model": _hash([domain_path]),
            "process_model": _hash([folder / "process.md"]),
            "use_case_model": _hash([folder / "use-case-model.json"] + script_paths),
            "ui_model": _hash([folder / "ui-model.json"]),
        }
    return loaded


def current_versions(folders_by_boundary: dict, base_dir: Path) -> dict:
    """Recompute model versions for the boundary folders a prior report recorded."""
    versions = {}
    for bid, label in folders_by_boundary.items():
        folder = Path(base_dir) / label
        if not (folder / "main.md").is_file():
            versions[bid] = None
            continue
        versions[bid] = load_round([folder], base_dir).versions.popitem()[1]
    return versions
