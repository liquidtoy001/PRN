from __future__ import annotations

import csv
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


def sample_learning_bank() -> dict[str, object]:
    return {
        "schema_version": 1,
        "course_id": "STAT3007",
        "chapter_slug": "regression",
        "language": "zh",
        "generated_from": {"chapter_input_digest": "a" * 64, "source_ids": ["S001"]},
        "items": [
            {
                "id": "regression-Q001",
                "kind": "short-answer",
                "prompt": "What does OLS minimise?",
                "answer": "The residual sum of squares.",
                "rationale": "This is the course objective definition.",
                "difficulty": 2,
                "estimated_minutes": 2,
                "tags": ["regression", "ols"],
                "source_refs": [
                    {"source_id": "S001", "locator": "PDF p. 2", "type": "source"}
                ],
                "assessment_weight": 0.9,
                "priority_evidence": [
                    {
                        "source_id": "S002",
                        "locator": "2025 final Q1",
                        "type": "assessment",
                    }
                ],
            },
            {
                "id": "regression-Q002",
                "kind": "flashcard",
                "prompt": "Define ridge regression.",
                "answer": "OLS with an L2 parameter penalty.",
                "difficulty": 3,
                "estimated_minutes": 3,
                "tags": ["regression", "ridge"],
                "source_refs": [
                    {"source_id": "S001", "locator": "PDF p. 4", "type": "source"}
                ],
                "assessment_weight": None,
                "priority_evidence": [],
            },
        ],
    }


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
            self.assertEqual(first_data["materials"][0]["token_estimate"]["status"], "estimated")
            self.assertGreater(
                first_data["materials"][0]["token_estimate"]["upper_bound_tokens"], 0
            )

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


class CapacityAndUsageTests(unittest.TestCase):
    def test_capacity_report_requires_chunking_and_discloses_evidence_limits(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            materials = root / "materials"
            materials.mkdir()
            (materials / "lecture-notes.txt").write_text("regression " * 2000, encoding="utf-8")
            inventory = root / "inventory.json"
            inventoried = run_script("inventory_materials.py", materials, "--output", inventory)
            self.assertEqual(inventoried.returncode, 0, inventoried.stderr)
            report = root / "capacity.json"
            markdown = root / "capacity.md"
            assessed = run_script(
                "assess_capacity.py",
                inventory,
                "--output",
                report,
                "--markdown",
                markdown,
                "--language",
                "zh",
                "--context-window",
                1000,
                "--reserved-output-tokens",
                100,
                "--overhead-tokens",
                100,
                "--safety-margin",
                0.1,
            )
            self.assertEqual(assessed.returncode, 0, assessed.stderr)
            data = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(data["context_fit"]["status"], "chunking-required")
            codes = {
                notice["code"] for notice in data["quality_ceiling"]["mandatory_notices"]
            }
            self.assertIn("MATERIALS_EXCEED_SAFE_CONTEXT", codes)
            self.assertIn("NO_ASSESSMENT_EVIDENCE", codes)
            self.assertIn("NO_OFFICIAL_SOLUTIONS", codes)
            self.assertIn("成品质量上限", markdown.read_text(encoding="utf-8"))

    def test_usage_ledger_records_provider_usage_and_priced_components(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            response = root / "response.json"
            response.write_text(
                json.dumps(
                    {
                        "usage": {
                            "input_tokens": 1000,
                            "input_tokens_details": {
                                "cached_tokens": 200,
                                "cache_write_tokens": 0,
                            },
                            "output_tokens": 500,
                            "output_tokens_details": {"reasoning_tokens": 100},
                            "total_tokens": 1500,
                        }
                    }
                ),
                encoding="utf-8",
            )
            pricing = root / "pricing.json"
            pricing.write_text(
                json.dumps(
                    {
                        "currency": "USD",
                        "source": "provider price table",
                        "as_of": "2026-08-25",
                        "models": {
                            "test-model": {
                                "input_per_million": 2,
                                "cached_input_per_million": 1,
                                "cache_write_per_million": None,
                                "output_per_million": 10,
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            ledger = root / "usage.jsonl"
            recorded = run_script(
                "usage_ledger.py",
                "record",
                "--ledger",
                ledger,
                "--generation-id",
                "gen-test-001",
                "--operation",
                "chapter-generation",
                "--provider",
                "openai",
                "--model",
                "test-model",
                "--usage-file",
                response,
                "--pricing-file",
                pricing,
            )
            self.assertEqual(recorded.returncode, 0, recorded.stderr)
            entry = json.loads(ledger.read_text(encoding="utf-8").strip())
            self.assertEqual(entry["measurement"], "provider-reported")
            self.assertEqual(entry["token_usage"]["reasoning_tokens"], 100)
            self.assertEqual(entry["cost"]["status"], "calculated")
            self.assertEqual(entry["cost"]["amount"], "0.00680000")
            summary = run_script("usage_ledger.py", "summary", "--ledger", ledger)
            self.assertEqual(summary.returncode, 0, summary.stderr)
            self.assertIn('"generation_count": 1', summary.stdout)

    def test_usage_file_estimate_is_explicitly_partial(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "selected.md"
            output = root / "chapter.md"
            source.write_text("input source " * 100, encoding="utf-8")
            output.write_text("generated chapter " * 50, encoding="utf-8")
            ledger = root / "usage.jsonl"
            result = run_script(
                "usage_ledger.py",
                "record",
                "--ledger",
                ledger,
                "--operation",
                "chapter-generation",
                "--input-file",
                source,
                "--output-file",
                output,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            entry = json.loads(ledger.read_text(encoding="utf-8").strip())
            self.assertEqual(entry["measurement"], "partial-estimate")
            self.assertIn("system instructions", entry["measurement_details"]["scope_notice"])
            self.assertGreater(entry["token_usage"]["upper_bound_tokens"], 0)

    def test_usage_unavailable_still_creates_an_audit_record(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            ledger = Path(temporary) / "usage.jsonl"
            result = run_script(
                "usage_ledger.py",
                "record",
                "--ledger",
                ledger,
                "--operation",
                "quiz-generation",
                "--unavailable-reason",
                "host platform did not expose token usage",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            entry = json.loads(ledger.read_text(encoding="utf-8").strip())
            self.assertEqual(entry["measurement"], "unavailable")
            self.assertIsNone(entry["token_usage"]["total_tokens"])
            self.assertEqual(entry["cost"]["status"], "not-calculated")


class LearningLoopTests(unittest.TestCase):
    def test_learning_bank_attempt_plan_and_exports(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bank_path = root / "bank.json"
            bank_path.write_text(json.dumps(sample_learning_bank()), encoding="utf-8")
            inventory = root / "inventory.json"
            inventory.write_text(
                json.dumps(
                    {
                        "materials": [
                            {"id": "S001", "path": "lecture.pdf"},
                            {"id": "S002", "path": "exam.pdf"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            validated = run_script(
                "manage_learning.py", "validate-bank", bank_path, "--inventory", inventory
            )
            self.assertEqual(validated.returncode, 0, validated.stderr)

            state = root / "learning-state.json"
            initialised = run_script(
                "manage_learning.py",
                "init",
                "--bank",
                bank_path,
                "--output",
                state,
                "--inventory",
                inventory,
                "--assessment-date",
                "2026-09-10",
            )
            self.assertEqual(initialised.returncode, 0, initialised.stderr)
            attempted = run_script(
                "manage_learning.py",
                "record-attempt",
                "--bank",
                bank_path,
                "--state",
                state,
                "--item-id",
                "regression-Q001",
                "--correct",
                "no",
                "--confidence",
                5,
                "--attempted-at",
                "2026-09-01T10:00:00Z",
                "--mistake-tag",
                "objective-confusion",
            )
            self.assertEqual(attempted.returncode, 0, attempted.stderr)
            state_data = json.loads(state.read_text(encoding="utf-8"))
            first = state_data["items"]["regression-Q001"]
            self.assertEqual(first["status"], "relearn")
            self.assertEqual(first["due_at"], "2026-09-02")
            self.assertEqual(first["lapses"], 1)

            plan = root / "plan.json"
            planned = run_script(
                "manage_learning.py",
                "plan",
                "--bank",
                bank_path,
                "--state",
                state,
                "--output",
                plan,
                "--as-of",
                "2026-09-02",
                "--available-minutes",
                2,
            )
            self.assertEqual(planned.returncode, 0, planned.stderr)
            plan_data = json.loads(plan.read_text(encoding="utf-8"))
            self.assertEqual(plan_data["selected"][0]["item_id"], "regression-Q001")
            self.assertTrue(plan_data["selected"][0]["priority_basis"]["evidence_backed"])
            self.assertTrue(plan_data["uncovered"])

            csv_output = root / "bank.csv"
            anki_output = root / "bank.tsv"
            csv_export = run_script(
                "manage_learning.py",
                "export",
                "--bank",
                bank_path,
                "--format",
                "csv",
                "--output",
                csv_output,
                "--inventory",
                inventory,
            )
            anki_export = run_script(
                "manage_learning.py",
                "export",
                "--bank",
                bank_path,
                "--format",
                "anki",
                "--output",
                anki_output,
                "--inventory",
                inventory,
            )
            self.assertEqual(csv_export.returncode, 0, csv_export.stderr)
            self.assertEqual(anki_export.returncode, 0, anki_export.stderr)
            with csv_output.open(encoding="utf-8", newline="") as handle:
                self.assertEqual(len(list(csv.reader(handle))), 3)
            self.assertEqual(len(anki_output.read_text(encoding="utf-8").splitlines()), 2)
            self.assertIn("S001", anki_output.read_text(encoding="utf-8"))

    def test_assessment_weight_without_evidence_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            bank = sample_learning_bank()
            bank["items"][0]["priority_evidence"] = []  # type: ignore[index]
            path = Path(temporary) / "bank.json"
            path.write_text(json.dumps(bank), encoding="utf-8")
            result = run_script("manage_learning.py", "validate-bank", path)
            self.assertEqual(result.returncode, 1)
            self.assertIn("assessment_weight requires priority_evidence", result.stderr)


class StateTests(unittest.TestCase):
    def test_qa_flags_cannot_bypass_missing_capacity_and_usage_records(self) -> None:
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
                "latex",
            )
            self.assertEqual(initialised.returncode, 0, initialised.stderr)
            bypass = run_script(
                "manage_state.py",
                "update-chapter",
                state,
                "--slug",
                "chapter-one",
                "--title",
                "Chapter one",
                "--status",
                "verified",
                "--input-digest",
                "a" * 64,
                "--qa-citations",
                "pass",
                "--qa-reasoning",
                "pass",
                "--qa-capacity-disclosure",
                "pass",
                "--qa-usage-accounting",
                "pass",
            )
            self.assertEqual(bypass.returncode, 2)
            self.assertIn("requires a recorded capacity report", bypass.stderr)
            self.assertIn("requires at least one usage-ledger record", bypass.stderr)

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
            state_data = json.loads(state.read_text(encoding="utf-8"))
            state_data["capacity"].update(
                {
                    "report_path": "capacity.json",
                    "status": "fits-estimate",
                    "last_checked_at": "2026-08-25T00:00:00Z",
                }
            )
            state_data["usage"].update(
                {
                    "ledger_path": "usage.jsonl",
                    "generation_count": 1,
                    "last_generation_id": "gen-test",
                    "last_measurement": "partial-estimate",
                    "updated_at": "2026-08-25T00:00:00Z",
                }
            )
            state.write_text(json.dumps(state_data), encoding="utf-8")
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
                "--qa-capacity-disclosure",
                "pass",
                "--qa-usage-accounting",
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

    def test_schema_one_migration_preserves_historical_delivery_without_fake_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            state = Path(temporary) / "study_state.json"
            state.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "course": {"id": "TEST", "title": "Test course"},
                        "preferences": {
                            "mode": "lightweight",
                            "language": "en",
                            "format": "latex",
                            "assessment_date": None,
                            "study_hours_available": None,
                        },
                        "materials": {"inventory_path": None, "inventory_digest": None},
                        "evidence_boundary": {
                            "assessment_specification": "unknown",
                            "past_assessments": "unknown",
                            "official_solutions": "unknown",
                            "notes": [],
                        },
                        "chapters": [
                            {
                                "slug": "legacy",
                                "title": "Legacy chapter",
                                "status": "delivered",
                                "priority_basis": "unknown",
                                "source_ids": ["S001"],
                                "input_digest": "a" * 64,
                                "artifacts": ["legacy.tex"],
                                "qa": {
                                    "citations": "pass",
                                    "reasoning": "pass",
                                    "pdf_structure": "not-applicable",
                                    "visual": "not-applicable",
                                },
                                "updated_at": "2026-08-24T00:00:00Z",
                            }
                        ],
                        "last_action": "legacy generation",
                        "next_action": None,
                        "updated_at": "2026-08-24T00:00:00Z",
                    }
                ),
                encoding="utf-8",
            )
            migrated = run_script("manage_state.py", "migrate", state)
            self.assertEqual(migrated.returncode, 0, migrated.stderr)
            data = json.loads(state.read_text(encoding="utf-8"))
            self.assertEqual(data["schema_version"], 2)
            chapter = data["chapters"][0]
            self.assertTrue(chapter["legacy_generation"])
            self.assertEqual(chapter["qa"]["usage_accounting"], "not-applicable")
            validated = run_script("manage_state.py", "validate", state)
            self.assertEqual(validated.returncode, 0, validated.stderr)

    def test_capacity_and_usage_scripts_unlock_new_chapter_verification(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            state = root / "study_state.json"
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
                "latex",
            )
            self.assertEqual(initialised.returncode, 0, initialised.stderr)
            created = run_script(
                "manage_state.py",
                "update-chapter",
                state,
                "--slug",
                "chapter-one",
                "--title",
                "Chapter one",
            )
            self.assertEqual(created.returncode, 0, created.stderr)

            materials = root / "materials"
            materials.mkdir()
            (materials / "lecture.txt").write_text("course content", encoding="utf-8")
            inventory = root / "inventory.json"
            self.assertEqual(
                run_script("inventory_materials.py", materials, "--output", inventory).returncode,
                0,
            )
            capacity = run_script(
                "assess_capacity.py",
                inventory,
                "--output",
                root / "capacity.json",
                "--context-window",
                10000,
                "--reserved-output-tokens",
                100,
                "--overhead-tokens",
                100,
                "--study-state",
                state,
                "--chapter-slug",
                "chapter-one",
            )
            self.assertEqual(capacity.returncode, 0, capacity.stderr)
            generated = root / "chapter.md"
            generated.write_text("generated answer", encoding="utf-8")
            usage = run_script(
                "usage_ledger.py",
                "record",
                "--ledger",
                root / "usage.jsonl",
                "--operation",
                "chapter-generation",
                "--output-file",
                generated,
                "--study-state",
                state,
                "--chapter-slug",
                "chapter-one",
            )
            self.assertEqual(usage.returncode, 0, usage.stderr)
            verified = run_script(
                "manage_state.py",
                "update-chapter",
                state,
                "--slug",
                "chapter-one",
                "--status",
                "verified",
                "--input-digest",
                "b" * 64,
                "--qa-citations",
                "pass",
                "--qa-reasoning",
                "pass",
            )
            self.assertEqual(verified.returncode, 0, verified.stderr)
            data = json.loads(state.read_text(encoding="utf-8"))
            chapter = data["chapters"][0]
            self.assertEqual(chapter["qa"]["capacity_disclosure"], "pass")
            self.assertEqual(chapter["qa"]["usage_accounting"], "pass")
            self.assertEqual(data["usage"]["generation_count"], 1)


if __name__ == "__main__":
    unittest.main()
