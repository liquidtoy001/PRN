"""Regression coverage for paper identity, review gates and source-display preferences."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from test_html import FIXTURE, HTML_SKILL, run
from test_scripts import REPOSITORY, run_script


class ReviewWorkflowTests(unittest.TestCase):
    def test_visible_code_preference_persists_and_rejects_non_booleans(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            config = json.loads((REPOSITORY / "pre-review-notes/assets/note-configuration.json").read_text(encoding="utf-8"))
            self.assertIs(config["include_code"], False)
            config.update(confirmed=True, deliverables=["markdown"], paper_enrichment="off")
            settings = root / "settings.json"

            def initialise(name):
                settings.write_text(json.dumps(config), encoding="utf-8")
                return run_script("manage_state.py", "init", "--output", root / name,
                                  "--course-id", "READING", "--course-title", "Reading fixture",
                                  "--mode", "lightweight", "--language", "zh", "--format", "markdown",
                                  "--note-configuration", settings)

            for enabled in (False, True):
                config["include_code"] = enabled
                name = f"code-{enabled}.json"
                result = initialise(name)
                self.assertEqual(result.returncode, 0, result.stderr)
                saved = json.loads((root / name).read_text(encoding="utf-8"))
                self.assertIs(saved["preferences"]["note_configuration"]["include_code"], enabled)
            for invalid in ("false", 0, None, []):
                config["include_code"] = invalid
                result = initialise("invalid.json")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("include_code", result.stderr)
                self.assertFalse((root / "invalid.json").exists())
            config.pop("include_code")
            result = initialise("legacy.json")
            self.assertEqual(result.returncode, 0, result.stderr)
            saved = json.loads((root / "legacy.json").read_text(encoding="utf-8"))
            self.assertNotIn("include_code", saved["preferences"]["note_configuration"])

    def test_identical_papers_keep_ids_and_changed_question_stays_distinct(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            sources = root / "sources"
            sources.mkdir()
            original = "Q1. Find the mean of 1, 2, 3."
            for name in ("exam-2024.txt", "exam-2025.txt"):
                (sources / name).write_text(original, encoding="utf-8")
            (sources / "new-2025.txt").write_text("Q1. Find the mean of 1, 2, 6.", encoding="utf-8")
            inventory = root / "inventory.json"
            result = run_script("inventory_materials.py", sources, "--output", inventory)
            self.assertEqual(result.returncode, 0, result.stderr)
            first = json.loads(inventory.read_text(encoding="utf-8"))
            ids = {item["path"]: item["id"] for item in first["materials"]}
            self.assertEqual(len(set(ids.values())), 3)
            self.assertEqual(len(first["duplicate_groups"]), 1)
            self.assertEqual(set(first["duplicate_groups"][0]["source_ids"]), {ids["exam-2024.txt"], ids["exam-2025.txt"]})
            self.assertEqual(len(list(sources.iterdir())), 3)
            result = run_script("inventory_materials.py", sources, "--output", inventory)
            self.assertEqual(result.returncode, 0, result.stderr)
            second = json.loads(inventory.read_text(encoding="utf-8"))
            self.assertEqual(first["duplicate_groups"], second["duplicate_groups"])
            self.assertEqual(first["inventory_digest"], second["inventory_digest"])

    def test_review_gate_rejects_unreviewed_and_changed_drafts(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            config = json.loads((REPOSITORY / "pre-review-notes/assets/note-configuration.json").read_text())
            config.update(confirmed=True, deliverables=["markdown"], paper_enrichment="off")
            settings = root / "settings.json"
            settings.write_text(json.dumps(config), encoding="utf-8")
            state_path = root / "state.json"
            result = run_script("manage_state.py", "init", "--output", state_path,
                                "--course-id", "ORIGINAL", "--course-title", "Original fixture",
                                "--mode", "lightweight", "--language", "en", "--format", "markdown",
                                "--note-configuration", settings)
            self.assertEqual(result.returncode, 0, result.stderr)
            result = run_script("assess_capacity.py", FIXTURE / "inventory.json",
                                "--output", root / "capacity.json", "--study-state", state_path)
            self.assertEqual(result.returncode, 0, result.stderr)
            result = run_script("usage_ledger.py", "record", "--ledger", root / "usage.jsonl",
                                "--operation", "fixture", "--unavailable-reason", "No model call in this test",
                                "--study-state", state_path)
            self.assertEqual(result.returncode, 0, result.stderr)
            common = ["update-chapter", state_path, "--slug", "mean", "--title", "Mean",
                      "--status", "verified", "--input-digest", "a" * 64,
                      "--qa-citations", "pass", "--qa-reasoning", "pass",
                      "--qa-capacity-disclosure", "pass", "--qa-usage-accounting", "pass"]
            before = state_path.read_bytes()
            rejected = run_script("manage_state.py", *common)
            self.assertEqual(rejected.returncode, 2, rejected.stderr)
            self.assertIn("second_pass", rejected.stderr)
            self.assertIn("teaching_depth", rejected.stderr)
            self.assertEqual(before, state_path.read_bytes())
            accepted = run_script("manage_state.py", *common,
                                  "--qa-teaching-depth", "pass", "--qa-second-pass", "pass")
            self.assertEqual(accepted.returncode, 0, accepted.stderr)
            self.assertEqual(run_script("manage_state.py", "validate", state_path).returncode, 0)
            common[common.index("a" * 64)] = "b" * 64
            before = state_path.read_bytes()
            rejected = run_script("manage_state.py", *common)
            self.assertEqual(rejected.returncode, 2, rejected.stderr)
            self.assertEqual(before, state_path.read_bytes())
            # A historical chapter without the new policy stays readable, not newly reviewed.
            legacy = json.loads(before)
            legacy["chapters"][0].pop("second_pass_review")
            legacy["chapters"][0]["qa"].pop("second_pass")
            legacy["chapters"][0]["qa"].pop("teaching_depth")
            state_path.write_text(json.dumps(legacy), encoding="utf-8")
            self.assertEqual(run_script("manage_state.py", "validate", state_path).returncode, 0)

    def test_private_evidence_is_checked_and_hashes_use_actual_bytes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            note = root / "note.md"
            evidence = root / "evidence.md"
            report = root / "report.json"
            note.write_bytes(b"# Mean\r\nThe mean is 2.\r\n")
            evidence.write_bytes(b"## mean\r\nK001 [source:S001|section Mean and squared error]\r\n")
            args = [note, "--inventory", FIXTURE / "inventory.json", "--evidence", evidence, "--report", report]
            result = run_script("validate_citations.py", *args)
            self.assertEqual(result.returncode, 0, result.stderr)
            saved = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(saved["inline_citation_count"], 0)
            self.assertEqual(saved["note_sha256"], hashlib.sha256(note.read_bytes()).hexdigest())
            self.assertEqual(saved["evidence_sha256"], hashlib.sha256(evidence.read_bytes()).hexdigest())
            evidence.write_text("## mean\n[source:S999|section Mean]\n", encoding="utf-8")
            result = run_script("validate_citations.py", *args)
            self.assertEqual(result.returncode, 1)
            self.assertIn("unknown source id", result.stderr)

    def test_html_evidence_is_bound_to_exact_question_anchors(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            content = root / "chapter.html"
            content.write_text('<h2 id="mean">Mean</h2><p>The mean is 2.</p>'
                               '<details class="qa" id="Q001" data-k-ids="K001">'
                               '<summary>What is the mean of 1, 2, 3?</summary><p>2, since (1+2+3)/3=2.</p></details>', encoding="utf-8")
            config = json.loads((HTML_SKILL / "assets/note-configuration.json").read_text())
            note = config["preferences"]["note_configuration"]
            note.update(confirmed=True, self_test="folded-qa", answers_initial="closed", paper_enrichment="off")
            settings = root / "config.json"
            settings.write_text(json.dumps(config), encoding="utf-8")
            evidence = root / "evidence.md"
            body = "## mean\nK001 [source:S001|section Mean and squared error]\n"
            answer = "## Q001\nK001 [source:S001|section Mean and squared error]\n"
            evidence.write_text(body + answer, encoding="utf-8")
            args = ["--content", content, "--configuration", settings,
                    "--inventory", FIXTURE / "inventory.json", "--title", "Original example", "--evidence", evidence]
            result = run(HTML_SKILL / "scripts/build_html.py", *args, "--output-dir", root / "valid")
            self.assertEqual(result.returncode, 0, result.stderr)
            page = (root / "valid/index.html").read_text(encoding="utf-8")
            self.assertNotIn("[source:", page)
            self.assertNotIn(note["scope"], page)
            self.assertEqual((root / "valid/evidence.md").read_bytes(), evidence.read_bytes())
            report = json.loads((root / "valid/build-report.json").read_text())
            self.assertEqual(report["inputs"]["evidence"], hashlib.sha256(evidence.read_bytes()).hexdigest())
            self.assertEqual(report["second_pass_review"], "pending")
            for bad in (body, body + answer.replace("Q001", "Q002"), body + answer.replace("S001", "S999"), body + answer + answer):
                evidence.write_text(bad, encoding="utf-8")
                result = run(HTML_SKILL / "scripts/build_html.py", *args, "--output-dir", root / "invalid")
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((root / "invalid").exists())

    def test_html_presentation_preferences_and_legacy_configuration(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            content = root / "chapter.html"
            content.write_text('<h2 id="mean">Mean</h2><p>The mean is 2. [source:S001|section Mean]</p>', encoding="utf-8")
            config = json.loads((HTML_SKILL / "assets/note-configuration.json").read_text())
            note = config["preferences"]["note_configuration"]
            note.update(confirmed=True, scope="EXPLICIT-SCOPE-SENTINEL")
            settings = root / "config.json"

            def build(name):
                settings.write_text(json.dumps(config), encoding="utf-8")
                return run(HTML_SKILL / "scripts/build_html.py", "--content", content,
                           "--configuration", settings, "--inventory", FIXTURE / "inventory.json",
                           "--title", "Mean", "--output-dir", root / name)

            self.assertEqual(build("off").returncode, 0)
            self.assertNotIn(note["scope"], (root / "off/index.html").read_text(encoding="utf-8"))
            note["show_source_explanations"] = True
            self.assertEqual(build("on").returncode, 0)
            self.assertIn(note["scope"], (root / "on/index.html").read_text(encoding="utf-8"))
            note["include_code"] = True
            self.assertEqual(build("code-enabled").returncode, 0)
            original = dict(note)
            for key, value in (("show_source_index", "false"), ("second_pass_review", []),
                               ("include_code", "false"), ("include_code", 1),
                               ("exam_basis_source_ids", ["S001", "S001"]),
                               ("exam_basis_source_ids", ["missing"]), ("exam_answer_language", [])):
                note[key] = value
                self.assertNotEqual(build("bad").returncode, 0)
                self.assertFalse((root / "bad").exists())
                note.clear()
                note.update(original)
            for key in ("exam_organisation", "exam_basis_source_ids", "exam_answer_language",
                        "show_source_index", "show_source_explanations", "second_pass_review", "include_code"):
                note.pop(key)
            self.assertEqual(build("legacy").returncode, 0)
            content.write_text(content.read_text(encoding="utf-8") + '<section class="source-index"><h2 id="sources">Sources</h2><p>S001</p></section>', encoding="utf-8")
            self.assertNotEqual(build("index-off").returncode, 0)
            note["show_source_index"] = True
            self.assertEqual(build("index-on").returncode, 0)
