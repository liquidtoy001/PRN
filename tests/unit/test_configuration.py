"""Exercise configuration persistence through the public state CLI."""
import json
import tempfile
import unittest
from pathlib import Path

from test_scripts import REPOSITORY, run_script


class ConfigurationTests(unittest.TestCase):
    def test_exam_cram_requires_calendar_date_and_positive_finite_hours(self):
        with tempfile.TemporaryDirectory() as folder:
            state = Path(folder) / "state.json"
            init = ("manage_state.py", "init", "--output", state, "--course-id", "R",
                    "--course-title", "Review", "--mode", "exam-cram", "--language", "en",
                    "--format", "markdown")
            cases = [(None, None), (None, "3"), ("2028-02-29", None),
                     ("2027-02-29", "1"), ("20280229", "1"),
                     *(("2028-02-29", hours) for hours in ("0", "-2", "nan", "inf"))]
            for deadline, hours in cases:
                with self.subTest(deadline=deadline, hours=hours):
                    args = list(init)
                    if deadline is not None:
                        args.extend(["--assessment-date", deadline])
                    if hours is not None:
                        args.extend(["--study-hours", hours])
                    result = run_script(*args)
                    self.assertNotEqual(result.returncode, 0, result.stderr)
                    self.assertFalse(state.exists())
            good = run_script(*init, "--assessment-date", "2028-02-29", "--study-hours", "0.5")
            self.assertEqual(good.returncode, 0, good.stderr)
            self.assertEqual(run_script("manage_state.py", "validate", state).returncode, 0)
            data = json.loads(state.read_text())
            data["preferences"]["assessment_date"] = None
            state.write_text(json.dumps(data))
            before = state.read_bytes()
            self.assertNotEqual(run_script("manage_state.py", "validate", state).returncode, 0)
            view = run_script("manage_state.py", "render-progress", state, "--output", Path(folder) / "progress.md")
            self.assertEqual(view.returncode, 0, view.stderr)
            self.assertEqual(state.read_bytes(), before)

    def test_preview_round_trip_keeps_custom_choices_and_existing_purposes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            configuration = json.loads(
                (REPOSITORY / 'pre-review-notes/assets/note-configuration.json').read_text(encoding='utf-8')
            )
            configuration.update(
                purpose='preview', confirmed=True, scope='Lecture 1, pages 1-20',
                page_size='A5', depth='extended', paper_enrichment='integrated',
                include_code=True, deliverables=['pdf', 'latex'],
            )
            settings = root / 'settings.json'
            settings.write_text(json.dumps(configuration), encoding='utf-8')
            state = root / 'state.json'
            result = run_script(
                'manage_state.py', 'init', '--output', state,
                '--course-id', 'PREVIEW', '--course-title', 'Preview trial',
                '--mode', 'full', '--language', 'en', '--format', 'latex-pdf',
                '--learning-output', 'flashcards', '--note-configuration', settings,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            saved = json.loads(state.read_text(encoding='utf-8'))
            self.assertEqual(saved['preferences']['note_configuration'], configuration)
            self.assertEqual(saved['preferences']['learning_outputs'], ['flashcards'])
            self.assertEqual(saved['preferences']['mode'], 'full')
            self.assertEqual(saved['preferences']['language'], 'en')
            for purpose in ('preview', 'knowledge', 'exam'):
                with self.subTest(purpose=purpose):
                    saved['preferences']['note_configuration']['purpose'] = purpose
                    state.write_text(json.dumps(saved), encoding='utf-8')
                    before = state.read_bytes()
                    result = run_script('manage_state.py', 'validate', state)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(state.read_bytes(), before)

    def test_round_trip_and_legacy_compatibility(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            configuration = json.loads((REPOSITORY / 'pre-review-notes/assets/note-configuration.json').read_text())
            configuration.update(purpose='exam', confirmed=True, page_size='A5', deliverables=['pdf', 'markdown'])
            settings = root / 'settings.json'
            settings.write_text(json.dumps(configuration), encoding='utf-8')
            state = root / 'state.json'
            result = run_script('manage_state.py', 'init', '--output', state,
                                '--course-id', 'TEST', '--course-title', 'Test',
                                '--mode', 'lightweight', '--language', 'zh',
                                '--format', 'markdown-pdf', '--note-configuration', settings)
            self.assertEqual(result.returncode, 0, result.stderr)
            saved = json.loads(state.read_text(encoding='utf-8'))
            self.assertEqual(saved['preferences']['note_configuration'], configuration)
            self.assertEqual(run_script('manage_state.py', 'validate', state).returncode, 0)
            for value in ('off', 'reading-list', 'integrated'):
                saved['preferences']['note_configuration']['paper_enrichment'] = value
                state.write_text(json.dumps(saved), encoding='utf-8')
                self.assertEqual(run_script('manage_state.py', 'validate', state).returncode, 0)
            saved['preferences']['note_configuration']['paper_enrichment'] = ['invalid']
            state.write_text(json.dumps(saved), encoding='utf-8')
            result = run_script('manage_state.py', 'validate', state)
            self.assertEqual(result.returncode, 1)
            self.assertIn('paper_enrichment', result.stderr)
            del saved['preferences']['note_configuration']['paper_enrichment']
            state.write_text(json.dumps(saved), encoding='utf-8')
            self.assertEqual(run_script('manage_state.py', 'validate', state).returncode, 0)
            del saved['preferences']['note_configuration']
            state.write_text(json.dumps(saved), encoding='utf-8')
            self.assertEqual(run_script('manage_state.py', 'validate', state).returncode, 0)
            saved['preferences']['note_configuration'] = {'purpose': ['invalid']}
            state.write_text(json.dumps(saved), encoding='utf-8')
            result = run_script('manage_state.py', 'validate', state)
            self.assertEqual(result.returncode, 1)
            self.assertIn('note_configuration.purpose', result.stderr)
