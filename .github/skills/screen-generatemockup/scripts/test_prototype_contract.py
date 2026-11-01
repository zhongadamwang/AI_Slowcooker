"""Static regression checks; browser interaction verification is still required."""

import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


SKILLS = Path(__file__).resolve().parents[2]
STARTER = SKILLS / "screen-generatemockup" / "assets" / "professional-starter"
CONTRACT = SKILLS / "screen-generatelayout" / "references" / "prototype-quality.md"
SCREEN_SKILLS = sorted(SKILLS.glob("screen-*"))


class Markup(HTMLParser):
    def __init__(self, content):
        super().__init__()
        self.elements = []
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


def contrast(first, second):
    def luminance(color):
        if len(color) == 4:
            color = "#" + "".join(digit * 2 for digit in color[1:])
        values = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in values]
        return sum(v * weight for v, weight in zip(linear, (.2126, .7152, .0722)))

    high, low = sorted((luminance(first), luminance(second)), reverse=True)
    return (high + .05) / (low + .05)


class PrototypeContractTests(unittest.TestCase):
    def test_skill_sections_and_contract_links(self):
        self.assertEqual(len(SCREEN_SKILLS), 6)
        for skill in SCREEN_SKILLS:
            with self.subTest(skill=skill.name):
                content = (skill / "SKILL.md").read_text(encoding="utf-8")
                for heading in ("## Intent", "## Inputs", "## Outputs", "## Workflow"):
                    self.assertIn(heading, content)
                self.assertIn("prototype-quality.md", content)
                for target in re.findall(r"\]\(([^)]+)\)", content):
                    if "prototype-quality.md" in target or "professional-starter" in target:
                        self.assertTrue((skill / target.split("#")[0]).resolve().is_file(), target)

    def test_gate_definitions_and_patterns(self):
        for skill in SCREEN_SKILLS:
            with self.subTest(skill=skill.name):
                gate = json.loads((skill / "gate.json").read_text(encoding="utf-8"))
                self.assertEqual(gate["version"], "1.1.0")
                self.assertEqual(gate["skill_name"], skill.name)
                ids = [check["id"] for check in gate["checks"]]
                self.assertEqual(len(ids), len(set(ids)))
                for check in gate["checks"]:
                    for key in ("must_contain_pattern", "must_not_contain_pattern"):
                        if key in check:
                            re.compile(check[key])

    def test_navigation_gate_is_not_a_presence_proxy(self):
        gate = json.loads((SKILLS / "screen-generatemockup" / "gate.json").read_text(encoding="utf-8"))
        check = next(c for c in gate["checks"] if c["id"] == "navigation_links_resolve")
        self.assertEqual(check["type"], "stakeholder_confirmation")
        self.assertNotIn("must_contain_pattern", check)
        self.assertIn("standalone", check["confirmation_statement"])

    def test_framework_pattern_does_not_match_padding(self):
        for name in ("screen-generatelayout", "screen-generatemockup"):
            gate = json.loads((SKILLS / name / "gate.json").read_text(encoding="utf-8"))
            pattern = next(c["must_not_contain_pattern"] for c in gate["checks"] if c["id"] == "no_framework_leakage")
            self.assertIsNone(re.search(pattern, ".card { padding-bottom: 16px; }"))
            self.assertIsNotNone(re.search(pattern, '<div ng-model="email">'))
            self.assertIsNotNone(re.search(pattern, '<button v-on:click="save">'))

    def test_starter_resource_and_navigation_contract(self):
        pages = sorted(STARTER.glob("SCR-*/mockup.html"))
        self.assertEqual(len(pages), 2)
        gate = json.loads((SKILLS / "screen-generatemockup" / "gate.json").read_text(encoding="utf-8"))
        for path in pages:
            with self.subTest(page=path.parent.name):
                content = path.read_text(encoding="utf-8")
                markup = Markup(content)
                ids = [attrs["id"] for _, attrs in markup.elements if "id" in attrs]
                self.assertEqual(len(ids), len(set(ids)))
                self.assertIn('<meta name="viewport"', content)
                self.assertIn("@media (max-width: 720px)", content)
                self.assertIn("No backend connection.", content)
                for tag, attrs in markup.elements:
                    self.assertNotIn("src", attrs)
                    if tag == "a":
                        target = (path.parent / attrs["href"]).resolve()
                        self.assertTrue(target.is_file())
                        self.assertEqual(target.parent.name, attrs["data-transition-target"])
                    if "data-ui-target" in attrs:
                        self.assertIn(attrs["data-ui-target"], ids)
                for check in gate["checks"]:
                    if check.get("file", "").endswith("/mockup.html") and "must_not_contain_pattern" in check:
                        self.assertIsNone(re.search(check["must_not_contain_pattern"], content), check["id"])

    def test_shared_tokens_and_measured_contrast(self):
        pages = sorted(STARTER.glob("SCR-*/mockup.html"))
        tokens = [dict(re.findall(r"(--[\w-]+):\s*([^;]+);", p.read_text(encoding="utf-8"))) for p in pages]
        self.assertEqual(tokens[0], tokens[1])
        theme = tokens[0]
        for foreground, background in (("--ink", "--surface"), ("--muted", "--surface"),
                                      ("--muted", "--canvas"), ("--brand", "--surface"),
                                      ("--brand-hover", "--tint"), ("--error", "--surface")):
            with self.subTest(pair=(foreground, background)):
                self.assertGreaterEqual(contrast(theme[foreground], theme[background]), 4.5)
        self.assertGreaterEqual(contrast(theme["--focus"], theme["--surface"]), 3)

    def test_contract_reference_links(self):
        for target in re.findall(r"\]\(([^)]+)\)", CONTRACT.read_text(encoding="utf-8")):
            if not target.startswith("#"):
                self.assertTrue((CONTRACT.parent / target.split("#")[0]).resolve().is_file(), target)


if __name__ == "__main__":
    unittest.main()
