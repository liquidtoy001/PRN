"""Exercise the final/draft distinction on the actual printable template."""
from importlib.util import find_spec
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest

from test_scripts import REPOSITORY, run_script


ASSETS = REPOSITORY / "pre-review-notes" / "assets"


class PrintTemplateTests(unittest.TestCase):
    def test_final_build_rejects_nested_and_shipped_placeholders_before_writing(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            main = root / "chapter.tex"
            main.write_text(r"\input{chapter-body}", encoding="utf-8")
            (root / "chapter-body.tex").write_text(r"95\% complete. \prnslot{Result}", encoding="utf-8")
            for source in (main, ASSETS / "template.tex"):
                with self.subTest(source=source):
                    output = root / "final"
                    result = run_script("build_note.py", source, "--output-dir", output)
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn("unresolved template placeholders", result.stderr)
                    self.assertFalse(output.exists())

    @unittest.skipUnless(shutil.which("xelatex") and find_spec("pypdf"), "render check needs XeLaTeX and pypdf")
    def test_draft_and_finished_template_render_without_optional_sections(self):
        from pypdf import PdfReader

        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "chapter.tex"
            template = (ASSETS / "template.tex").read_text(encoding="utf-8")
            for draft in (True, False):
                body = template
                if not draft:
                    body = re.sub(r"\\prnslot\{[^{}]*\}", "Regression", template)
                    body = body.replace(r"\end{document}", "% [Topic Name] author comment\n" + r"\end{document}")
                source.write_text(body, encoding="utf-8")
                output = root / ("draft" if draft else "final")
                args = ["--allow-placeholders"] if draft else []
                result = run_script("build_note.py", source, "--engine", "xelatex", "--skip-render",
                                    "--output-dir", output, *args)
                self.assertEqual(result.returncode, 0, result.stderr)
                report = json.loads((output / "chapter.qa.json").read_text(encoding="utf-8"))
                self.assertEqual(report["placeholders"]["status"], "warning" if draft else "pass")
                pdf = PdfReader(output / "chapter.pdf")
                text = " ".join(page.extract_text() for page in pdf.pages).lower()
                self.assertIn("chapter title" if draft else "regression", text)
                for optional in ("quick reference", "practice and staged retest", "learning bank"):
                    self.assertNotIn(optional, text)

    def test_markdown_visible_headings_only_include_teaching(self):
        markdown = (ASSETS / "markdown-template.md").read_text(encoding="utf-8")
        body = re.sub(r"<!--.*?-->", "", markdown, flags=re.S)
        self.assertEqual([line.split()[0] for line in body.splitlines() if line.startswith("#")], ["#", "##"])
        self.assertIn("example", body)
        self.assertIn("[source:", body)
