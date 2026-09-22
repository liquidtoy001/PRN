"""Regression tests for legitimate example locators and local-source containment."""
import json
from pathlib import Path
import tempfile
import unittest

from test_html import run, HTML_SKILL, FIXTURE


class CitationBoundaryTests(unittest.TestCase):
    def test_example_locators_are_valid_but_unresolved_slots_fail(self):
        with tempfile.TemporaryDirectory() as folder:
            note = Path(folder) / "note.md"
            for locator in ("Example 3.2", "例题 2", "section Worked examples", "PDF p. 18"):
                note.write_text(f"[source:S001|{locator}]", encoding="utf-8")
                with self.subTest(locator=locator):
                    self.assertEqual(run(HTML_SKILL / "scripts/validate_citations.py", note, "--inventory", FIXTURE / "inventory.json").returncode, 0)
            for locator in ("TBD", "TODO", "unknown", "?", "PDF p. TBD", "PDF p. ?", "[page]"):
                note.write_text(f"[source:S001|{locator}]", encoding="utf-8")
                with self.subTest(locator=locator):
                    self.assertNotEqual(run(HTML_SKILL / "scripts/validate_citations.py", note, "--inventory", FIXTURE / "inventory.json").returncode, 0)

    def test_material_root_rejects_absolute_and_parent_paths(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            materials = root / "materials"
            materials.mkdir()
            outside = root / "outside.md"
            outside.write_text("existing but outside", encoding="utf-8")
            (materials / "inside.md").write_text("inside", encoding="utf-8")
            note = root / "note.md"
            note.write_text("[source:S001|Example 3.2]", encoding="utf-8")
            inventory = root / "inventory.json"
            for path, expected in (("inside.md", 0), ("../outside.md", 1), (str(outside), 1)):
                inventory.write_text(json.dumps({"materials": [{"id": "S001", "path": path}]}), encoding="utf-8")
                with self.subTest(path=path):
                    result = run(HTML_SKILL / "scripts/validate_citations.py", note, "--inventory", inventory, "--materials-root", materials)
                    self.assertEqual(result.returncode, expected, result.stderr)
