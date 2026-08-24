#!/usr/bin/env python3
"""Compile a LaTeX note and prepare structural and visual PDF QA artifacts."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CJK_PATTERN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
PLACEHOLDER_PATTERN = re.compile(
    r"\[(?:Topic Name|One line|where taught|problem location|Definition /|First step|"
    r"Second step|Continue until|Concept \d|Technique/recipe|what it tested|step)"
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def available(name: str) -> str | None:
    return shutil.which(name)


def engine_order(requested: str, contains_cjk: bool) -> list[str]:
    if requested != "auto":
        return [requested]
    if contains_cjk:
        return ["xelatex", "tectonic", "latexmk", "pdflatex"]
    return ["tectonic", "latexmk", "xelatex", "pdflatex"]


def compile_with(engine: str, tex: Path, output_dir: Path) -> tuple[int, str, list[list[str]]]:
    executable = available(engine)
    if executable is None:
        return 127, f"{engine} is not available on PATH", []

    commands: list[list[str]]
    if engine == "tectonic":
        commands = [[executable, "--outdir", str(output_dir), str(tex)]]
    elif engine == "latexmk":
        commands = [
            [
                executable,
                "-pdf",
                "-interaction=nonstopmode",
                "-halt-on-error",
                f"-outdir={output_dir}",
                str(tex),
            ]
        ]
    elif engine in {"xelatex", "pdflatex"}:
        command = [
            executable,
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            f"-output-directory={output_dir}",
            str(tex),
        ]
        commands = [command, command]
    else:
        return 2, f"unsupported engine {engine}", []

    output_parts: list[str] = []
    executed: list[list[str]] = []
    for command in commands:
        result = run(command, tex.parent)
        executed.append(command)
        output_parts.append(result.stdout)
        if result.returncode:
            return result.returncode, "\n".join(output_parts), executed
    return 0, "\n".join(output_parts), executed


def inspect_pdf(pdf: Path) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    try:
        from pypdf import PdfReader
    except ImportError:
        return {"status": "metadata_unavailable", "reason": "pypdf is not installed"}, [
            "pypdf is required for complete structural traversal"
        ]

    try:
        reader = PdfReader(str(pdf), strict=False)
        if reader.is_encrypted:
            return {"status": "fail", "encrypted": True}, ["output PDF is encrypted"]
        pages = len(reader.pages)
        if pages < 1:
            return {"status": "fail", "encrypted": False, "pages": pages}, ["output PDF has no pages"]
        text_characters: list[int] = []
        extraction_errors: list[dict[str, Any]] = []
        for index, page in enumerate(reader.pages, 1):
            try:
                text_characters.append(len(page.extract_text() or ""))
            except Exception as exc:
                text_characters.append(0)
                extraction_errors.append({"page": index, "error": str(exc)})
        if extraction_errors:
            errors.append(f"text extraction failed on {len(extraction_errors)} page(s)")
        return {
            "status": "pass" if not errors else "fail",
            "encrypted": False,
            "pages": pages,
            "text_characters_per_page": text_characters,
            "extraction_errors": extraction_errors,
        }, errors
    except Exception as exc:
        return {"status": "fail", "reason": str(exc)}, [f"PDF reopen failed: {exc}"]


def representative_pages(page_count: int, text_counts: list[int]) -> list[int]:
    if page_count <= 0:
        return []
    candidates = {1, page_count, (page_count + 1) // 2}
    if text_counts:
        densest = max(range(len(text_counts)), key=text_counts.__getitem__) + 1
        candidates.add(densest)
    return sorted(candidates)


def render_pages(pdf: Path, output_dir: Path, pages: list[int]) -> tuple[list[str], list[str]]:
    executable = available("pdftoppm")
    if executable is None:
        return [], ["pdftoppm is not available; representative pages were not rendered"]
    render_dir = output_dir / "qa-render"
    render_dir.mkdir(parents=True, exist_ok=True)
    rendered: list[str] = []
    errors: list[str] = []
    for page in pages:
        prefix = render_dir / f"{pdf.stem}-p{page:03d}"
        command = [
            executable,
            "-png",
            "-r",
            "144",
            "-f",
            str(page),
            "-l",
            str(page),
            "-singlefile",
            str(pdf),
            str(prefix),
        ]
        result = run(command, pdf.parent)
        image = prefix.with_suffix(".png")
        if result.returncode or not image.is_file():
            errors.append(f"page {page} render failed: {result.stdout[-500:]}")
        else:
            rendered.append(str(image.resolve()))
    return rendered, errors


def write_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tex", type=Path, help="main LaTeX source")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--engine",
        choices=["auto", "tectonic", "latexmk", "xelatex", "pdflatex"],
        default="auto",
    )
    parser.add_argument("--report", type=Path, help="defaults to <output-dir>/<stem>.qa.json")
    parser.add_argument("--skip-render", action="store_true")
    parser.add_argument("--fail-on-placeholders", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    tex = args.tex.resolve()
    output_dir = args.output_dir.resolve()
    report_path = (args.report or (output_dir / f"{tex.stem}.qa.json")).resolve()
    if not tex.is_file():
        print(f"LaTeX source not found: {tex}", file=sys.stderr)
        return 2

    source = tex.read_text(encoding="utf-8")
    placeholders = sorted(set(match.group(0) for match in PLACEHOLDER_PATTERN.finditer(source)))
    if placeholders and args.fail_on_placeholders:
        print(f"unresolved template placeholders: {placeholders}", file=sys.stderr)
        return 2
    output_dir.mkdir(parents=True, exist_ok=True)

    attempts: list[dict[str, Any]] = []
    selected_engine: str | None = None
    commands: list[list[str]] = []
    compiler_output = ""
    for engine in engine_order(args.engine, bool(CJK_PATTERN.search(source))):
        code, output, executed = compile_with(engine, tex, output_dir)
        attempts.append({"engine": engine, "return_code": code, "available": code != 127})
        if code == 0:
            selected_engine = engine
            commands = executed
            compiler_output = output
            break
        if code != 127:
            compiler_output = output

    log_path = output_dir / f"{tex.stem}.build.log"
    log_path.write_text(compiler_output, encoding="utf-8")
    pdf = output_dir / f"{tex.stem}.pdf"
    compile_ok = selected_engine is not None and pdf.is_file()
    structure: dict[str, Any] = {"status": "not-run"}
    structure_errors: list[str] = []
    renders: list[str] = []
    render_errors: list[str] = []

    if compile_ok:
        structure, structure_errors = inspect_pdf(pdf)
        if not args.skip_render and structure.get("pages"):
            pages = representative_pages(
                int(structure["pages"]), list(structure.get("text_characters_per_page", []))
            )
            renders, render_errors = render_pages(pdf, output_dir, pages)

    report = {
        "schema_version": 1,
        "generated_at": utc_now(),
        "source": str(tex),
        "pdf": str(pdf.resolve()) if pdf.is_file() else None,
        "compiler": {
            "status": "pass" if compile_ok else "fail",
            "selected_engine": selected_engine,
            "attempts": attempts,
            "commands": commands,
            "log": str(log_path.resolve()),
        },
        "placeholders": {"status": "pass" if not placeholders else "warning", "matches": placeholders},
        "pdf_structure": structure,
        "structural_errors": structure_errors,
        "visual_review": {
            "status": "pending" if renders and not render_errors else "unavailable",
            "rendered_pages": renders,
            "errors": render_errors,
            "instruction": "Inspect every rendered page before changing visual status to pass.",
        },
    }
    write_report(report_path, report)

    if not compile_ok:
        print(f"compile failed; report={report_path} log={log_path}", file=sys.stderr)
        return 1
    if structure.get("status") != "pass" or render_errors:
        print(f"PDF QA incomplete or failed; report={report_path}", file=sys.stderr)
        return 4
    print(
        f"build: engine={selected_engine} pdf={pdf} pages={structure.get('pages')} "
        f"visual_review={report['visual_review']['status']} report={report_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
