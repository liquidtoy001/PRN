from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
SCRIPTS = REPOSITORY / "pre-review-notes" / "scripts"


def run_script(script: str, *arguments: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *(str(argument) for argument in arguments)],
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


class InventoryAndCitationTests(unittest.TestCase):
    def test_download_manifest_verifies_existing_local_pdf(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "downloads"
            output.mkdir()
            payload = b"%PDF-1.4\nlocal fixture\n%%EOF\n"
            (output / "lecture.pdf").write_bytes(payload)
            digest = hashlib.sha256(payload).hexdigest()
            manifest = root / "materials.csv"
            manifest.write_text(
                "file,url,bytes,sha256\n"
                f"lecture.pdf,https://example.invalid/lecture.pdf,{len(payload)},{digest}\n",
                encoding="utf-8",
            )
            result = run_script(
                "download_materials.py",
                manifest,
                "--output-dir",
                output,
                "--verify-only",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("verified=1", result.stdout)

    def test_inventory_ids_survive_an_incremental_rerun(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            materials = root / "materials"
            materials.mkdir()
            (materials / "lecture-01.txt").write_text("regression", encoding="utf-8")
            output = root / "inventory.json"

            first = run_script("inventory_materials.py", materials, "--output", output)
            self.assertEqual(first.returncode, 0, first.stderr)
            first_data = json.loads(output.read_text(encoding="utf-8"))
            original_id = first_data["materials"][0]["id"]

            (materials / "00-syllabus.txt").write_text("assessment", encoding="utf-8")
            second = run_script("inventory_materials.py", materials, "--output", output)
            self.assertEqual(second.returncode, 0, second.stderr)
            second_data = json.loads(output.read_text(encoding="utf-8"))
            ids = {item["path"]: item["id"] for item in second_data["materials"]}
            self.assertEqual(ids["lecture-01.txt"], original_id)
            self.assertEqual(len(set(ids.values())), 2)

    def test_citation_validator_accepts_known_id_and_rejects_unknown_id(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            inventory = root / "inventory.json"
            inventory.write_text(
                json.dumps({"materials": [{"id": "S001", "path": "lecture.pdf"}]}),
                encoding="utf-8",
            )
            note = root / "note.md"
            note.write_text("Regression [source:S001|PDF p. 2]", encoding="utf-8")
            valid = run_script("validate_citations.py", note, "--inventory", inventory)
            self.assertEqual(valid.returncode, 0, valid.stderr)

            note.write_text("Regression [source:S999|PDF p. 2]", encoding="utf-8")
            invalid = run_script("validate_citations.py", note, "--inventory", inventory)
            self.assertEqual(invalid.returncode, 1)
            self.assertIn("unknown source id S999", invalid.stderr)


class StateTests(unittest.TestCase):
    def test_verified_chapter_is_reused_only_for_the_same_digest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            state = Path(temporary) / "study_state.json"
            digest = "a" * 64
            initialised = run_script(
                "manage_state.py",
                "init",
                "--output",
                state,
                "--course-id",
                "STAT3007",
                "--course-title",
                "Deep Learning",
                "--mode",
                "lightweight",
                "--language",
                "zh",
                "--format",
                "latex",
            )
            self.assertEqual(initialised.returncode, 0, initialised.stderr)
            updated = run_script(
                "manage_state.py",
                "update-chapter",
                state,
                "--slug",
                "regression",
                "--title",
                "Regression",
                "--status",
                "verified",
                "--input-digest",
                digest,
                "--source-id",
                "S001",
                "--qa-citations",
                "pass",
                "--qa-reasoning",
                "pass",
            )
            self.assertEqual(updated.returncode, 0, updated.stderr)

            reuse = run_script(
                "manage_state.py",
                "needs-rebuild",
                state,
                "--slug",
                "regression",
                "--input-digest",
                digest,
            )
            self.assertEqual(reuse.returncode, 0, reuse.stderr)
            changed = run_script(
                "manage_state.py",
                "needs-rebuild",
                state,
                "--slug",
                "regression",
                "--input-digest",
                "b" * 64,
            )
            self.assertEqual(changed.returncode, 3, changed.stderr)

    def test_pdf_delivery_requires_visual_and_structural_qa(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            state = Path(temporary) / "study_state.json"
            initialised = run_script(
                "manage_state.py",
                "init",
                "--output",
                state,
                "--course-id",
                "TEST",
                "--course-title",
                "Test course",
                "--mode",
                "lightweight",
                "--language",
                "en",
                "--format",
                "latex-pdf",
            )
            self.assertEqual(initialised.returncode, 0, initialised.stderr)
            rejected = run_script(
                "manage_state.py",
                "update-chapter",
                state,
                "--slug",
                "chapter-one",
                "--title",
                "Chapter one",
                "--status",
                "delivered",
                "--qa-citations",
                "pass",
                "--qa-reasoning",
                "pass",
            )
            self.assertEqual(rejected.returncode, 2)
            self.assertIn("pdf_structure, visual", rejected.stderr)


if __name__ == "__main__":
    unittest.main()
