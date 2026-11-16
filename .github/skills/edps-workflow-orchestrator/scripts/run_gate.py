#!/usr/bin/env python3
"""Evaluate an EDPS skill's completion gate (gate.json) against real files.

This is the executable implementation of the gate semantics described in
edps-workflow-orchestrator/references/gate-schema.md. It only reads files;
it never writes project state.

Usage:
  run_gate.py <skill-name> --project <project-dir> [options]
  run_gate.py --lint [skill-name ...]

Options:
  --project DIR     Project root (OrgDocument/projects/[NN] - [Project Name])
  --process DIR     orgModel process folder, for {process}/ paths
  --boundary DIR    Boundary folder, for {boundary}/ paths
  --target DIR      Target folder for {target}/ paths (e.g. a newly created skill)
  --archetype NAME  standard | rapid | compliance (default: standard)
  --mode NAME       solo | traditional (default: project-metadata.json's
                    collaboration_mode, else traditional)
  --json            Print the full result as JSON
  --lint            Validate gate.json files instead of evaluating one

Exit codes: 0 = progression allowed, 1 = gate failed, 2 = incomplete or usage error.
"""

from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parents[2]
REPO_ROOT = SKILLS_DIR.parents[1]

SCOPES = ("project", "process", "boundary", "target", "repo")
ARCHETYPES = ("standard", "rapid", "compliance")
QUALITY_THRESHOLD = {"standard": 0.80, "rapid": 0.80, "compliance": 0.95}
COMPLIANCE_BLOCK_BELOW = 0.80

# check type -> (required keys, optional keys)
COMMON_KEYS = {"id", "type", "severity", "description", "remediation", "applies_when"}
CHECK_TYPES = {
    "artifact_existence": ({"artifacts"}, set()),
    "content_pattern": ({"file"}, {"must_contain", "must_not_contain", "must_contain_pattern",
                                   "must_not_contain_pattern", "min_matches", "json_path"}),
    "file_content": ({"file"}, {"min_lines", "must_contain"}),
    "file_count": ({"pattern"}, {"min_count", "max_count"}),
    "folder_structure": ({"base_path"}, {"required_folders", "folder_pattern", "min_folders",
                                         "min_files", "file_extensions"}),
    "json_schema": ({"file", "required_fields"}, {"json_path", "non_empty_fields"}),
    "json_query": ({"file", "json_path"}, {"min_value", "max_value", "expected_value"}),
    "threshold": ({"file", "json_path"}, {"min_value", "max_value"}),
    "field_completeness": ({"file", "json_path", "min_percent_complete"}, set()),
    "stakeholder_confirmation": ({"role", "confirmation_statement"}, set()),
}
PATH_KEYS = ("file", "artifacts", "pattern", "base_path")


class ScopeMissing(Exception):
    """A path needs a scope folder (e.g. --boundary) that was not supplied."""


# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------

def split_scope(spec: str) -> tuple:
    """'{boundary}/ui-model.json' -> ('boundary', 'ui-model.json'); bare paths are project-scoped."""
    m = re.match(r"^\{(\w+)\}/?(.*)$", spec)
    if m:
        return m.group(1), m.group(2)
    return "project", spec


def resolve(spec: str, ctx: dict) -> list:
    """Resolve a gate path (optionally scoped, optionally a glob) to existing paths."""
    scope, rel = split_scope(spec)
    if scope not in SCOPES:
        raise ValueError(f"unknown path scope '{{{scope}}}' in '{spec}'")
    base = ctx.get(scope)
    if base is None:
        raise ScopeMissing(scope)
    pattern = str(Path(base) / rel) if rel else str(base)
    if glob.has_magic(rel):
        return [Path(p) for p in sorted(glob.glob(pattern, recursive=True))]
    return [Path(pattern)] if Path(pattern).exists() else []


def show(path: Path, ctx: dict) -> str:
    try:
        return str(path.relative_to(ctx["repo"]))
    except ValueError:
        return str(path)


# ---------------------------------------------------------------------------
# Minimal JSONPath: $, .key, .*, [*], [n], and a trailing .length on arrays
# ---------------------------------------------------------------------------

_TOKEN = re.compile(r"\.([A-Za-z_][\w-]*|\*)|\[(\*|\d+)\]")


def json_select(doc, path: str) -> list:
    """Return every value the path selects (an empty list when nothing matches)."""
    if not path.startswith("$"):
        raise ValueError(f"json_path must start with '$': {path}")
    rest = path[1:]
    tokens = []
    pos = 0
    while pos < len(rest):
        m = _TOKEN.match(rest, pos)
        if not m:
            raise ValueError(f"unsupported json_path syntax at '{rest[pos:]}' in {path}")
        tokens.append(m.group(1) if m.group(1) is not None else f"[{m.group(2)}]")
        pos = m.end()
    nodes = [doc]
    for i, tok in enumerate(tokens):
        nxt = []
        for node in nodes:
            if tok in ("*", "[*]"):
                if isinstance(node, list):
                    nxt.extend(node)
                elif isinstance(node, dict):
                    nxt.extend(node.values())
            elif tok.startswith("["):
                idx = int(tok[1:-1])
                if isinstance(node, list) and idx < len(node):
                    nxt.append(node[idx])
            elif isinstance(node, dict) and tok in node:
                nxt.append(node[tok])
            elif tok == "length" and i == len(tokens) - 1 and isinstance(node, (list, dict, str)):
                nxt.append(len(node))
        nodes = nxt
    return nodes


def is_empty(value) -> bool:
    return value is None or value == "" or value == [] or value == {}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Check implementations. Each returns (passed: bool, detail: str).
# ---------------------------------------------------------------------------

def _files(check: dict, ctx: dict, key: str = "file") -> list:
    paths = [p for p in resolve(check[key], ctx) if p.is_file()]
    if not paths:
        raise FileNotFoundError(check[key])
    return paths


def check_artifact_existence(check, ctx):
    missing = [spec for spec in check["artifacts"] if not resolve(spec, ctx)]
    return (not missing, f"missing: {', '.join(missing)}" if missing else "all artifacts exist")


def _text_problems(text: str, check: dict) -> list:
    problems = []
    for needle in check.get("must_contain", []):
        if needle not in text:
            problems.append(f"missing text {needle!r}")
    for needle in check.get("must_not_contain", []):
        if needle in text:
            problems.append(f"forbidden text {needle!r} present")
    if "must_contain_pattern" in check:
        found = len(re.findall(check["must_contain_pattern"], text))
        need = check.get("min_matches", 1)
        if found < need:
            problems.append(f"pattern matched {found} time(s), need {need}")
    if "must_not_contain_pattern" in check:
        found = len(re.findall(check["must_not_contain_pattern"], text))
        if found:
            problems.append(f"forbidden pattern matched {found} time(s)")
    return problems


def check_content_pattern(check, ctx):
    problems = []
    for path in _files(check, ctx):
        if "json_path" in check:
            # Apply the text rules to each selected value; no values selected passes vacuously.
            for value in json_select(load_json(path), check["json_path"]):
                text = value if isinstance(value, str) else json.dumps(value)
                problems += [f"{show(path, ctx)} [{text[:40]}]: {p}" for p in _text_problems(text, check)]
        else:
            text = path.read_text(encoding="utf-8")
            problems += [f"{show(path, ctx)}: {p}" for p in _text_problems(text, check)]
    return (not problems, "; ".join(problems) or "content rules satisfied")


def check_file_content(check, ctx):
    problems = []
    for path in _files(check, ctx):
        text = path.read_text(encoding="utf-8")
        lines = len(text.splitlines())
        if lines < check.get("min_lines", 0):
            problems.append(f"{show(path, ctx)}: {lines} line(s), need {check['min_lines']}")
        problems += [f"{show(path, ctx)}: {p}" for p in _text_problems(text, {"must_contain": check.get("must_contain", [])})]
    return (not problems, "; ".join(problems) or "content rules satisfied")


def check_file_count(check, ctx):
    count = len([p for p in resolve(check["pattern"], ctx) if p.is_file()])
    lo, hi = check.get("min_count", 0), check.get("max_count")
    ok = count >= lo and (hi is None or count <= hi)
    return (ok, f"{count} file(s) match (allowed {lo}..{'any' if hi is None else hi})")


def check_folder_structure(check, ctx):
    bases = [p for p in resolve(check["base_path"], ctx) if p.is_dir()]
    if not bases:
        raise FileNotFoundError(check["base_path"])
    problems = []
    for base in bases:
        for folder in check.get("required_folders", []):
            if not (base / folder).is_dir():
                problems.append(f"{show(base, ctx)}: missing folder '{folder}'")
        if "folder_pattern" in check and "min_folders" in check:
            found = [p for p in base.glob(check["folder_pattern"].rstrip("/")) if p.is_dir()]
            if len(found) < check["min_folders"]:
                problems.append(f"{show(base, ctx)}: {len(found)} folder(s) match "
                                f"'{check['folder_pattern']}', need {check['min_folders']}")
        if "min_files" in check:
            exts = tuple(check.get("file_extensions", []))
            found = [p for p in base.iterdir() if p.is_file() and (not exts or p.name.endswith(exts))]
            if len(found) < check["min_files"]:
                problems.append(f"{show(base, ctx)}: {len(found)} file(s), need {check['min_files']}")
    return (not problems, "; ".join(problems) or "folder structure satisfied")


def check_json_schema(check, ctx):
    problems = []
    for path in _files(check, ctx):
        # No nodes selected (e.g. an empty array under [*]) passes vacuously.
        nodes = json_select(load_json(path), check.get("json_path", "$"))
        for i, node in enumerate(nodes):
            if not isinstance(node, dict):
                problems.append(f"{show(path, ctx)}: selected node {i} is not an object")
                continue
            for field in check["required_fields"]:
                if node.get(field) is None or node.get(field) == "":
                    problems.append(f"{show(path, ctx)}: node {i} missing '{field}'")
            for field in check.get("non_empty_fields", []):
                if is_empty(node.get(field)):
                    problems.append(f"{show(path, ctx)}: node {i} has empty '{field}'")
    return (not problems, "; ".join(problems[:8]) or "required fields present")


def check_json_query(check, ctx):
    problems = []
    for path in _files(check, ctx):
        values = json_select(load_json(path), check["json_path"])
        if not values:
            problems.append(f"{show(path, ctx)}: {check['json_path']} selects nothing")
        for value in values:
            if "expected_value" in check and value != check["expected_value"]:
                problems.append(f"{show(path, ctx)}: {value!r} != expected {check['expected_value']!r}")
            for key, bad in (("min_value", lambda v, lim: v < lim), ("max_value", lambda v, lim: v > lim)):
                if key in check:
                    if isinstance(value, bool) or not isinstance(value, (int, float)):
                        problems.append(f"{show(path, ctx)}: {value!r} is not a number")
                    elif bad(value, check[key]):
                        problems.append(f"{show(path, ctx)}: {value} violates {key} {check[key]}")
    return (not problems, "; ".join(problems) or "value within bounds")


def check_field_completeness(check, ctx):
    m = re.match(r"^(.*(?:\[\*\]|\.\*))\.([A-Za-z_][\w-]*)$", check["json_path"])
    if not m:
        raise ValueError(f"field_completeness json_path must end in '[*].field' or '.*.field': {check['json_path']}")
    problems = []
    for path in _files(check, ctx):
        items = json_select(load_json(path), m.group(1))
        if not items:
            continue
        done = sum(1 for it in items if isinstance(it, dict) and not is_empty(it.get(m.group(2))))
        pct = 100.0 * done / len(items)
        if pct < check["min_percent_complete"]:
            problems.append(f"{show(path, ctx)}: {pct:.0f}% of items have '{m.group(2)}', "
                            f"need {check['min_percent_complete']}%")
    return (not problems, "; ".join(problems) or "completeness threshold met")


def check_stakeholder_confirmation(check, ctx):
    state_files = resolve("project-state.json", ctx)
    records = load_json(state_files[0]).get("confirmations", []) if state_files else []
    role = check["role"].strip().lower()
    for rec in records:
        if str(rec.get("role", "")).strip().lower() == role:
            return True, f"confirmed by {rec.get('confirmed_by', 'unknown')} ({rec.get('timestamp', 'no timestamp')})"
    if ctx["mode"] == "solo":
        return True, (f"no record on file; solo mode self-attests as {check['role']} — "
                      f"record this confirmation in project-state.json")
    return False, f"no confirmation on file for role '{check['role']}'"


RUNNERS = {
    "artifact_existence": check_artifact_existence,
    "content_pattern": check_content_pattern,
    "file_content": check_file_content,
    "file_count": check_file_count,
    "folder_structure": check_folder_structure,
    "json_schema": check_json_schema,
    "json_query": check_json_query,
    "threshold": check_json_query,
    "field_completeness": check_field_completeness,
    "stakeholder_confirmation": check_stakeholder_confirmation,
}


# ---------------------------------------------------------------------------
# Gate evaluation
# ---------------------------------------------------------------------------

def effective_severity(check: dict, mode: str) -> str:
    """Only stakeholder_confirmation is mode-aware; every other type keeps its declared severity."""
    if check["type"] == "stakeholder_confirmation":
        return "soft" if mode == "solo" else "hard"
    return check.get("severity", "hard")


def applies(check: dict, ctx: dict):
    """Evaluate a structured applies_when condition. Returns True, False, or a skip reason (str)."""
    cond = check.get("applies_when")
    if cond is None:
        return True
    try:
        paths = [p for p in resolve(cond["file"], ctx) if p.is_file()]
    except ScopeMissing as exc:
        return f"applies_when needs --{exc}"
    if "json_path" not in cond:
        # File-existence condition: {"file": ..., "exists": true|false}
        return bool(cond.get("exists", True)) == bool(paths)
    if not paths:
        return f"applies_when file not found: {cond['file']}"
    values = json_select(load_json(paths[0]), cond["json_path"])
    value = values[0] if values else None
    if "equals" in cond:
        return value == cond["equals"]
    if "not_equals" in cond:
        return value != cond["not_equals"]
    return bool(cond.get("exists", True)) == bool(values)


def run_check(check: dict, ctx: dict) -> dict:
    result = {"id": check["id"], "type": check["type"],
              "severity": effective_severity(check, ctx["mode"]),
              "description": check.get("description", "")}
    applicable = applies(check, ctx)
    if applicable is False:
        return {**result, "status": "not_applicable", "detail": "applies_when condition is false"}
    if isinstance(applicable, str):
        return {**result, "status": "skipped", "detail": applicable}
    runner = RUNNERS.get(check["type"])
    if runner is None:
        return {**result, "status": "failed", "detail": f"unknown check type '{check['type']}'",
                "remediation": "Fix the gate definition (see references/gate-schema.md)"}
    try:
        passed, detail = runner(check, ctx)
    except ScopeMissing as exc:
        return {**result, "status": "skipped", "detail": f"needs --{exc} to resolve its path"}
    except FileNotFoundError as exc:
        passed, detail = False, f"not found: {exc}"
    except (ValueError, json.JSONDecodeError, re.error) as exc:
        passed, detail = False, f"could not evaluate: {exc}"
    result.update(status="passed" if passed else "failed", detail=detail)
    if not passed:
        result["remediation"] = check.get("remediation", "")
    return result


def evaluate_gate(skill: str, ctx: dict, archetype: str = "standard") -> dict:
    gate_path = SKILLS_DIR / skill / "gate.json"
    if not gate_path.exists():
        return {"skill": skill, "status": "no_gate", "allowed": True, "checks": []}
    gate = load_json(gate_path)
    level = gate.get("workflow_archetypes", {}).get(archetype, gate.get("severity", "hard"))
    base = {"skill": skill, "skill_id": gate.get("skill_id"), "archetype": archetype,
            "collaboration_mode": ctx["mode"], "archetype_level": level}
    if level == "bypass":
        return {**base, "status": "bypassed", "allowed": True, "checks": []}

    checks = [run_check(c, ctx) for c in gate["checks"]]
    passed = [c for c in checks if c["status"] == "passed"]
    failed = [c for c in checks if c["status"] == "failed"]
    skipped = [c for c in checks if c["status"] == "skipped"]
    hard_failed = [c for c in failed if c["severity"] == "hard"]
    hard_skipped = [c for c in skipped if c["severity"] == "hard"]
    evaluated = len(passed) + len(failed)
    score = round(len(passed) / evaluated, 2) if evaluated else None
    below = score is not None and score < QUALITY_THRESHOLD[archetype]

    # A gate whose archetype level is "soft" reports hard-check failures as warnings.
    if hard_failed and level == "hard":
        status = "failed"
    elif archetype == "compliance" and score is not None and score < COMPLIANCE_BLOCK_BELOW:
        status = "failed"
    elif hard_skipped:
        status = "incomplete"
    elif failed or below:
        status = "passed_with_warnings"
    else:
        status = "passed"
    return {**base, "status": status, "allowed": status not in ("failed", "incomplete"),
            "quality_score": score, "quality_below_threshold": below, "checks": checks}


def print_report(result: dict) -> None:
    print(f"Gate {result.get('skill_id') or ''} {result['skill']}: {result['status'].upper()}"
          f"  (archetype={result.get('archetype')}, mode={result.get('collaboration_mode')},"
          f" quality={result.get('quality_score')})")
    marks = {"passed": "PASS", "failed": "FAIL", "skipped": "SKIP", "not_applicable": "N/A "}
    for c in result["checks"]:
        print(f"  [{marks[c['status']]}] {c['severity']:<4} {c['id']}: {c['detail']}")
        if c["status"] == "failed" and c.get("remediation"):
            print(f"         remediation: {c['remediation']}")
    if result["status"] == "incomplete":
        print("  Some hard checks could not be evaluated; supply the missing scope folders and re-run.")


# ---------------------------------------------------------------------------
# Lint
# ---------------------------------------------------------------------------

def lint_gate(skill: str) -> list:
    """Return a list of problems with a skill's gate.json (empty when clean)."""
    gate_path = SKILLS_DIR / skill / "gate.json"
    if not gate_path.exists():
        return ["no gate.json"]
    try:
        gate = load_json(gate_path)
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]
    problems = []
    for key in ("skill_id", "skill_name", "checks", "workflow_archetypes"):
        if key not in gate:
            problems.append(f"missing top-level '{key}'")
    if gate.get("skill_name") != skill:
        problems.append(f"skill_name '{gate.get('skill_name')}' does not match folder")
    for arch, level in gate.get("workflow_archetypes", {}).items():
        if arch not in ARCHETYPES or level not in ("hard", "soft", "bypass"):
            problems.append(f"workflow_archetypes: bad entry {arch}={level}")
    seen = set()
    for check in gate.get("checks", []):
        cid = check.get("id", "<no id>")
        if cid in seen:
            problems.append(f"{cid}: duplicate check id")
        seen.add(cid)
        ctype = check.get("type")
        if ctype not in CHECK_TYPES:
            problems.append(f"{cid}: unknown type '{ctype}'")
            continue
        required, optional = CHECK_TYPES[ctype]
        if required - check.keys():
            problems.append(f"{cid}: missing {sorted(required - check.keys())}")
        extra = check.keys() - required - optional - COMMON_KEYS
        if extra:
            problems.append(f"{cid}: unsupported keys {sorted(extra)}")
        if ctype != "stakeholder_confirmation" and check.get("severity") not in ("hard", "soft"):
            problems.append(f"{cid}: severity must be 'hard' or 'soft'")
        if ctype == "content_pattern" and not check.keys() & {"must_contain", "must_not_contain",
                                                               "must_contain_pattern", "must_not_contain_pattern"}:
            problems.append(f"{cid}: content_pattern has no rule to check")
        for key in ("must_contain_pattern", "must_not_contain_pattern"):
            if key in check:
                try:
                    re.compile(check[key])
                except re.error as exc:
                    problems.append(f"{cid}: {key} does not compile: {exc}")
        specs = [s for key in PATH_KEYS for s in ([check[key]] if isinstance(check.get(key), str) else check.get(key, []))]
        cond = check.get("applies_when")
        if cond is not None:
            if not isinstance(cond, dict) or "file" not in cond:
                problems.append(f"{cid}: applies_when must be an object with a 'file' (see gate-schema.md)")
            else:
                specs.append(cond["file"])
        for spec in specs:
            scope, rel = split_scope(spec)
            if scope not in SCOPES:
                problems.append(f"{cid}: unknown scope in '{spec}'")
            elif rel.startswith(("OrgDocument/", "orgModel/", ".github/", "/")) and scope != "repo":
                problems.append(f"{cid}: '{spec}' looks repo-relative; use a scope prefix")
        if "json_path" in check:
            try:
                json_select({}, check["json_path"])
            except ValueError as exc:
                problems.append(f"{cid}: {exc}")
    return problems


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("skills", nargs="*")
    parser.add_argument("--project")
    parser.add_argument("--process")
    parser.add_argument("--boundary")
    parser.add_argument("--target")
    parser.add_argument("--archetype", choices=ARCHETYPES, default="standard")
    parser.add_argument("--mode", choices=("solo", "traditional"))
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--lint", action="store_true")
    args = parser.parse_args(argv)

    if args.lint:
        skills = args.skills or sorted(p.name for p in SKILLS_DIR.iterdir() if (p / "SKILL.md").exists())
        bad = 0
        for skill in skills:
            problems = lint_gate(skill)
            bad += bool(problems)
            for problem in problems:
                print(f"{skill}: {problem}")
        print(f"{len(skills) - bad}/{len(skills)} gates clean")
        return 1 if bad else 0

    if len(args.skills) != 1:
        parser.error("give exactly one skill name (or use --lint)")
    ctx = {"repo": REPO_ROOT}
    for scope in ("project", "process", "boundary", "target"):
        value = getattr(args, scope)
        if value:
            if not Path(value).is_dir():
                parser.error(f"--{scope} is not a directory: {value}")
            ctx[scope] = Path(value).resolve()
    mode = args.mode
    if mode is None:
        mode = "traditional"
        meta = ctx.get("project") and ctx["project"] / "project-metadata.json"
        if meta and meta.exists():
            mode = load_json(meta).get("collaboration_mode") or "traditional"
    ctx["mode"] = mode

    result = evaluate_gate(args.skills[0], ctx, args.archetype)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result)
    if result["status"] == "incomplete":
        return 2
    return 0 if result["allowed"] else 1


if __name__ == "__main__":
    sys.exit(main())
