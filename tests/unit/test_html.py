"""Exercise the actual HTML CLI, failure boundaries and independently installable ZIPs."""
from __future__ import annotations

import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

REPOSITORY = Path(__file__).resolve().parents[2]
HTML_SKILL = REPOSITORY / "pre-review-notes-html"
FIXTURE = REPOSITORY / "tests/fixtures/html"


def run(script, *args):
    return subprocess.run([sys.executable, str(script), *map(str, args)], capture_output=True,
                          text=True, encoding="utf-8", errors="replace", check=False)


class Elements(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.elements = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


class HTMLBuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(FIXTURE, self.root / "input")
        self.content = self.root / "input/chapter.html"
        self.config = json.loads((HTML_SKILL / "assets/note-configuration.json").read_text(encoding="utf-8"))
        self.note = self.config["preferences"]["note_configuration"]
        self.note.update(confirmed=True, self_test="folded-qa", answers_initial="closed", paper_enrichment="off")

    def build(self, name="result", skill=HTML_SKILL):
        settings = self.root / "config.json"
        settings.write_text(json.dumps(self.config), encoding="utf-8")
        return run(skill / "scripts/build_html.py", "--content", self.content,
                   "--configuration", settings, "--inventory", self.root / "input/inventory.json",
                   "--title", "中文 <chapter> & math", "--output-dir", self.root / name)

    def test_offline_bundle_closed_and_open_answers(self):
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        page = (self.root / "result/index.html").read_text(encoding="utf-8")
        elements = Elements(page).elements
        details = [attrs for tag, attrs in elements if tag == "details"]
        self.assertEqual(len(details), 2)
        self.assertTrue(all("open" not in attrs for attrs in details))
        self.assertTrue(any(tag == "math" for tag, attrs in elements))
        self.assertIn("中文 &lt;chapter&gt; &amp; math", page)
        for tag, attrs in elements:
            if "src" in attrs:
                self.assertTrue((self.root / "result" / attrs["src"]).is_file())
        self.assertEqual((self.root / "result/assets/loss.svg").read_bytes(), (FIXTURE / "assets/loss.svg").read_bytes())
        report = json.loads((self.root / "result/build-report.json").read_text())
        self.assertEqual(report["artifacts"]["index.html"], hashlib.sha256(page.encode()).hexdigest())
        self.assertEqual(report["browser_review"], "pending")
        self.assertEqual(report["semantic_review"], "pending")
        self.note["answers_initial"] = "open"
        self.assertEqual(self.build("open").returncode, 0)
        opened = Elements((self.root / "open/index.html").read_text(encoding="utf-8"))
        self.assertTrue(all("open" in attrs for tag, attrs in opened.elements if tag == "details"))

    def test_knowledge_without_questions_and_no_accidental_full_mode_quiz(self):
        self.config["preferences"]["mode"] = "full"
        self.note.update(self_test="none", answers_initial=None)
        self.assertNotEqual(self.build().returncode, 0)
        self.assertFalse((self.root / "result").exists())
        self.content.write_text('<h2 id="concept">Concept</h2><p>Complete teaching. [source:S001|section Mean and squared error]</p>', encoding="utf-8")
        self.assertEqual(self.build().returncode, 0)
        page = Elements((self.root / "result/index.html").read_text(encoding="utf-8"))
        self.assertFalse(any(tag in ("details", "script", "button") for tag, attrs in page.elements))

    def test_configuration_rejection_before_output(self):
        for key, value in (("confirmed", False), ("deliverables", ["pdf"]), ("page_size", "A4"),
                           ("theme", []), ("answers_initial", None)):
            original = dict(self.note)
            self.note[key] = value
            with self.subTest(key=key):
                self.assertNotEqual(self.build().returncode, 0)
                self.assertFalse((self.root / "result").exists())
            self.note.clear()
            self.note.update(original)
        self.config["preferences"]["mode"] = "exam-cram"
        self.assertNotEqual(self.build().returncode, 0)
        self.config["preferences"].update(assessment_date="2026-10-01", study_hours_available=4)
        self.assertEqual(self.build().returncode, 0)

    def test_rejects_markup_assets_links_and_missing_citations(self):
        original = self.content.read_text(encoding="utf-8")
        mutations = {
            "script": original + '<script>alert(1)</script>',
            "handler": original.replace('<p>', '<p onclick="alert(1)">', 1),
            "remote": original.replace('assets/loss.svg', 'https://example.org/loss.svg'),
            "missing": original.replace('assets/loss.svg', 'assets/missing.png'),
            "traversal": original.replace('assets/loss.svg', 'assets/%2e%2e/source.md'),
            "anchor": original.replace('href="#mean-heading"', 'href="#absent"'),
            "duplicate": original + '<p id="Q001">Duplicate</p>',
            "unknown source": original.replace('source:S001', 'source:S999'),
            "unbalanced": original + '<p><em>Not closed</p>',
            "empty alt": original.replace('alt="等权平方损失对比：c为1和3时均为5/3，c为2时为2/3。"', 'alt=""'),
            "hidden citation only": '<h2 id="c">Content</h2><!-- [source:S001|section Mean] -->',
        }
        for case, text in mutations.items():
            with self.subTest(case=case):
                self.content.write_text(text, encoding="utf-8")
                self.assertNotEqual(self.build().returncode, 0)
                self.assertFalse((self.root / "result").exists())

    def test_active_svg_is_not_bundled(self):
        (self.root / "input/assets/loss.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"><image href="https://example.org/x.png"/></svg>', encoding="utf-8")
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("SVG", result.stderr)
        self.assertFalse((self.root / "result").exists())

    def test_existing_output_is_untouched(self):
        (self.root / "result").mkdir()
        sentinel = self.root / "result/index.html"
        sentinel.write_bytes(b"user owned")
        self.assertNotEqual(self.build().returncode, 0)
        self.assertEqual(sentinel.read_bytes(), b"user owned")

    def test_print_state_flags_fail_before_any_html_side_effect(self):
        state = self.root / "state.json"
        shutil.copyfile(HTML_SKILL / "assets/study-state-template.json", state)
        original = state.read_bytes()
        ledger, report = self.root / "usage.jsonl", self.root / "capacity.json"
        capacity = run(HTML_SKILL / "scripts/assess_capacity.py", FIXTURE / "inventory.json",
                       "--output", report, "--study-state", state)
        usage = run(HTML_SKILL / "scripts/usage_ledger.py", "record", "--ledger", ledger,
                    "--operation", "test", "--unavailable-reason", "test", "--study-state", state)
        for result in (capacity, usage):
            self.assertEqual(result.returncode, 2)
            self.assertIn("unavailable in this entry", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
        self.assertFalse(ledger.exists())
        self.assertFalse(report.exists())
        self.assertEqual(state.read_bytes(), original)
        self.assertEqual(run(HTML_SKILL / "scripts/assess_capacity.py", FIXTURE / "inventory.json", "--output", report).returncode, 0)
        self.assertEqual(run(HTML_SKILL / "scripts/usage_ledger.py", "record", "--ledger", ledger,
                             "--operation", "test", "--unavailable-reason", "test").returncode, 0)

    def test_html_citations_are_not_accepted_from_comments_or_attributes(self):
        self.content.write_text('<h2 title="[source:S001|section Mean]">Content</h2><!-- [source:S001|section Mean] --><script>"[source:S001|section Mean]"</script>', encoding="utf-8")
        result = run(HTML_SKILL / "scripts/validate_citations.py", self.content, "--inventory", FIXTURE / "inventory.json")
        self.assertNotEqual(result.returncode, 0)
        self.content.write_text('<p>[source:S001|section Mean &amp; squared error]</p>', encoding="utf-8")
        self.assertEqual(run(HTML_SKILL / "scripts/validate_citations.py", self.content, "--inventory", FIXTURE / "inventory.json").returncode, 0)


class PackagingTests(unittest.TestCase):
    def test_output_inside_skill_is_rejected_before_writes(self):
        with tempfile.TemporaryDirectory() as folder:
            copied = Path(folder) / "pre-review-notes-html"
            shutil.copytree(HTML_SKILL, copied, ignore=shutil.ignore_patterns("__pycache__"))
            before = {path.relative_to(copied): path.read_bytes() for path in copied.rglob("*") if path.is_file()}
            for output in (copied, copied / "dist"):
                result = run(REPOSITORY / "tools/package_skill.py", "--skill-dir", copied, "--output-dir", output)
                self.assertEqual(result.returncode, 2)
                self.assertIn("outside skill", result.stderr)
            after = {path.relative_to(copied): path.read_bytes() for path in copied.rglob("*") if path.is_file()}
            self.assertEqual(before, after)

    def test_reproducible_distinct_isolated_packages(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for skill in ("pre-review-notes", "pre-review-notes-html"):
                for repeat in ("one", "two"):
                    result = run(REPOSITORY / "tools/package_skill.py", "--skill-dir", REPOSITORY / skill, "--output-dir", root / repeat)
                    self.assertEqual(result.returncode, 0, result.stderr)
                archive = root / "one" / f"{skill}-v0.2.10.zip"
                self.assertEqual(archive.read_bytes(), (root / "two" / archive.name).read_bytes())
                with zipfile.ZipFile(archive) as bundle:
                    names = bundle.namelist()
                    self.assertEqual(len(names), len(set(names)))
                    self.assertIn("SKILL.md", names)
                    self.assertIn("LICENSE", names)
                    self.assertFalse(any(Path(name).suffix in (".pdf", ".pyc", ".zip") for name in names))
                    if skill.endswith("-html"):
                        self.assertNotIn("scripts/build_note.py", names)
                        self.assertNotIn("references/pdf-workflow.md", names)
                        self.assertFalse(any(name.endswith(".tex") for name in names))
                        installed = root / "isolated" / skill
                        bundle.extractall(installed)
                    else:
                        self.assertNotIn("scripts/build_html.py", names)
                        self.assertNotIn("assets/template.html", names)
            # Actually run a ZIP-extracted HTML package with no sibling/shared checkout.
            config = json.loads((installed / "assets/note-configuration.json").read_text())
            config["preferences"]["note_configuration"].update(confirmed=True, self_test="folded-qa", answers_initial="closed", paper_enrichment="off")
            settings = root / "configuration.json"
            settings.write_text(json.dumps(config), encoding="utf-8")
            result = run(installed / "scripts/build_html.py", "--configuration", settings,
                         "--content", FIXTURE / "chapter.html", "--inventory", FIXTURE / "inventory.json",
                         "--title", "Isolated package", "--output-dir", root / "rendered")
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_shared_drift_blocks_packaging_without_silently_repairing(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in ("tools", "shared", "pre-review-notes", "pre-review-notes-html"):
                shutil.copytree(REPOSITORY / name, root / name, ignore=shutil.ignore_patterns("__pycache__"))
            drift = root / "pre-review-notes-html/references/coverage-and-depth.md"
            drift.write_text("deliberate drift", encoding="utf-8")
            self.assertNotEqual(run(root / "tools/sync_shared.py", "--check").returncode, 0)
            result = run(root / "tools/package_skill.py")
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((root / "dist").exists())
            self.assertEqual(drift.read_text(), "deliberate drift")
            self.assertEqual(run(root / "tools/sync_shared.py").returncode, 0)
            self.assertEqual(run(root / "tools/sync_shared.py", "--check").returncode, 0)


if __name__ == "__main__":
    unittest.main()
