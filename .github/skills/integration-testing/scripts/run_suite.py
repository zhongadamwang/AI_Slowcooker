#!/usr/bin/env python3
"""Run every executable check in the EDPS skill suite and report the results.

Checks, in order:
  1. Skill structure  - every skill has SKILL.md with valid frontmatter and a gate.json
  2. Catalogue        - every skill is in the orchestrator's Skill Catalogue, and its
                        gate's skill_id matches the catalogue
  3. Gate definitions - run_gate.py --lint over every gate
  4. Test suites      - every test_*.py under .github/skills (unittest)
  5. Fixtures         - model-validatealignment's run_fixtures.py
  6. Project gates    - with --project: every gate of the chosen archetype against
                        that project, in catalogue order (reported, not counted as
                        suite failures, since a project may legitimately be partway)

Usage:
  run_suite.py [--project DIR] [--archetype standard|rapid|compliance] [--report-dir DIR]

With --report-dir (normally the project's artifacts/Testing), writes
integration-test-report.md and integration-test-results.json there.
Exit code: 0 when checks 1-5 all pass, 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parents[2]
REPO_ROOT = SKILLS_DIR.parents[1]
RUN_GATE = SKILLS_DIR / "edps-workflow-orchestrator" / "scripts" / "run_gate.py"
ORCHESTRATOR = SKILLS_DIR / "edps-workflow-orchestrator" / "SKILL.md"
ALLOWED_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}

# Skills each archetype runs, in catalogue order (see the orchestrator's Workflow Archetypes).
ARCHETYPE_SKILLS = {
    "standard": ["S18", "S00", "S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10",
                 "S11", "S12", "S13", "S15", "S16", "S17", "S19", "S23", "S24", "S25", "S26", "S27", "S20"],
    "rapid": ["S03", "S05", "S06", "S09", "S15", "S16", "S12", "S13"],
    "compliance": ["S10", "S12", "S13", "S22", "S11", "S26", "S27", "S20"],
}
# Skills whose gates need a folder other than the project; they are reported as needing it.
SCOPED = {"S09": "--process", "S10": "--process", "S11": "--process", "S32": "--boundary", "S40": "--boundary"}


def result(name, passed, detail=""):
    return {"check": name, "passed": passed, "detail": detail}


def catalogue() -> dict:
    """skill name -> skill ID, from the orchestrator's Skill Catalogue table."""
    text = ORCHESTRATOR.read_text(encoding="utf-8")
    return {name: sid for sid, name in re.findall(r"^\| (S\d\d) \| `([a-z0-9-]+)` \|", text, re.M)}


def frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    keys = re.findall(r"^([A-Za-z][\w-]*):", m.group(1), re.M)
    desc = re.search(r"^description: (.*)$", m.group(1), re.M)
    name = re.search(r"^name: (.*)$", m.group(1), re.M)
    return {"keys": keys, "description": desc.group(1).strip() if desc else "", "name": name.group(1).strip() if name else ""}


def check_structure(skills: list) -> list:
    out = []
    for skill in skills:
        problems = []
        fm = frontmatter(SKILLS_DIR / skill / "SKILL.md")
        if fm is None:
            problems.append("no YAML frontmatter")
        else:
            extra = set(fm["keys"]) - ALLOWED_KEYS
            if extra:
                problems.append(f"unexpected frontmatter keys {sorted(extra)}")
            if fm["name"] != skill:
                problems.append(f"name '{fm['name']}' does not match folder")
            if not fm["description"]:
                problems.append("empty description")
            elif len(fm["description"]) > 1024:
                problems.append(f"description is {len(fm['description'])} characters (max 1024)")
            if "license" not in fm["keys"]:
                problems.append("no license")
        if not (SKILLS_DIR / skill / "gate.json").exists():
            problems.append("no gate.json")
        for link in re.findall(r"\]\(((?:references|scripts|assets|examples)/[^)#\s]+)", (SKILLS_DIR / skill / "SKILL.md").read_text(encoding="utf-8")):
            if not (SKILLS_DIR / skill / link).exists():
                problems.append(f"broken link {link}")
        out.append(result(f"structure: {skill}", not problems, "; ".join(problems) or "ok"))
    return out


def check_catalogue(skills: list) -> list:
    cat = catalogue()
    out = []
    for skill in skills:
        if skill not in cat:
            out.append(result(f"catalogue: {skill}", False, "not in the Skill Catalogue"))
            continue
        gate = SKILLS_DIR / skill / "gate.json"
        sid = json.loads(gate.read_text(encoding="utf-8")).get("skill_id") if gate.exists() else None
        out.append(result(f"catalogue: {skill}", sid == cat[skill],
                          f"{cat[skill]}" if sid == cat[skill] else f"gate says {sid}, catalogue says {cat[skill]}"))
    return out


def run(cmd: list, cwd: Path) -> tuple:
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def summary_line(output: str) -> str:
    lines = [l for l in output.splitlines() if l.strip()]
    keep = [l for l in lines if re.match(r"^(Ran \d+|OK|FAILED|All \d+|\d+/\d+ gates)", l)]
    return " | ".join(keep) or (lines[-1] if lines else "")


def check_lint() -> list:
    code, output = run([sys.executable, str(RUN_GATE), "--lint"], REPO_ROOT)
    return [result("gate definitions (run_gate.py --lint)", code == 0, summary_line(output) if code == 0 else output[-1500:])]


def check_tests() -> list:
    out = []
    for test in sorted(SKILLS_DIR.rglob("test_*.py")):
        code, output = run([sys.executable, "-m", "unittest", test.stem], test.parent)
        out.append(result(f"tests: {test.relative_to(SKILLS_DIR)}", code == 0, summary_line(output) if code == 0 else output[-1500:]))
    fixtures = SKILLS_DIR / "model-validatealignment" / "scripts" / "run_fixtures.py"
    code, output = run([sys.executable, fixtures.name], fixtures.parent)
    out.append(result("fixtures: model-validatealignment/run_fixtures.py", code == 0, summary_line(output) if code == 0 else output[-1500:]))
    return out


def check_project(project: Path, archetype: str) -> list:
    by_id = {sid: name for name, sid in catalogue().items()}
    out = []
    for sid in ARCHETYPE_SKILLS[archetype]:
        skill = by_id.get(sid)
        if skill is None:
            continue
        if sid in SCOPED:
            out.append({"skill": skill, "skill_id": sid, "status": "not_run",
                        "detail": f"needs {SCOPED[sid]}; run run_gate.py for each folder"})
            continue
        code, output = run([sys.executable, str(RUN_GATE), skill, "--project", str(project), "--archetype", archetype, "--json"], REPO_ROOT)
        try:
            data = json.loads(output)
            failed = [c["id"] for c in data.get("checks", []) if c["status"] == "failed"]
            out.append({"skill": skill, "skill_id": sid, "status": data["status"], "detail": ", ".join(failed) or ""})
        except json.JSONDecodeError:
            out.append({"skill": skill, "skill_id": sid, "status": "error", "detail": output[-300:]})
    return out


def render_markdown(report: dict) -> str:
    mark = lambda ok: "✅" if ok else "❌"
    lines = [
        "# Integration Test Report", "",
        f"**Generated**: {report['generated_at']}",
        f"**Suite Status**: {'PASS' if report['suite_passed'] else 'FAIL'} "
        f"({report['passed']}/{report['total']} checks passed)", "",
        "## Suite Checks", "", "| | Check | Detail |", "|---|---|---|",
    ]
    for r in report["checks"]:
        detail = r["detail"].replace("\n", " ").replace("|", "\\|")[:300]
        lines.append(f"| {mark(r['passed'])} | {r['check']} | {detail} |")
    if report.get("project"):
        lines += ["", f"## Project Gates — {report['project']} ({report['archetype']})", "",
                  "| Skill | Gate status | Failed checks |", "|---|---|---|"]
        for g in report["project_gates"]:
            lines.append(f"| {g['skill_id']} {g['skill']} | {g['status']} | {g['detail']} |")
        lines += ["", "Project gate results describe where the project stands; they are not suite failures."]
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project")
    parser.add_argument("--archetype", choices=sorted(ARCHETYPE_SKILLS), default="standard")
    parser.add_argument("--report-dir")
    args = parser.parse_args(argv)

    skills = sorted(p.name for p in SKILLS_DIR.iterdir() if (p / "SKILL.md").exists())
    checks = check_structure(skills) + check_catalogue(skills) + check_lint() + check_tests()
    passed = sum(1 for c in checks if c["passed"])
    report = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "suite_passed": passed == len(checks), "passed": passed, "total": len(checks),
        "checks": checks,
    }
    if args.project:
        report.update(project=args.project, archetype=args.archetype,
                      project_gates=check_project(Path(args.project).resolve(), args.archetype))

    for c in checks:
        if not c["passed"]:
            print(f"FAIL {c['check']}: {c['detail'][:400]}")
    print(f"Suite: {passed}/{len(checks)} checks passed")
    for g in report.get("project_gates", []):
        print(f"  {g['skill_id']} {g['skill']}: {g['status']} {g['detail']}")

    if args.report_dir:
        out = Path(args.report_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "integration-test-results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        (out / "integration-test-report.md").write_text(render_markdown(report), encoding="utf-8")
        print(f"Report written to {out / 'integration-test-report.md'}")
    return 0 if report["suite_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
