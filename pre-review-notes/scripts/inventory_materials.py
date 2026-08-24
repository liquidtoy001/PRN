#!/usr/bin/env python3
"""Create a deterministic, citation-ready inventory of course materials."""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_EXTENSIONS = {
    ".csv",
    ".doc",
    ".docx",
    ".html",
    ".htm",
    ".ipynb",
    ".md",
    ".pdf",
    ".ppt",
    ".pptx",
    ".tex",
    ".txt",
    ".xlsx",
}

ROLE_PATTERNS = [
    ("official-solution", re.compile(r"solution|answer|marking|rubric|examiner", re.I)),
    ("past-assessment", re.compile(r"past.?exam|final|midterm|sample.?exam|mock|quiz", re.I)),
    ("assessment-specification", re.compile(r"syllabus|course.?profile|assessment|outline", re.I)),
    ("graded-work", re.compile(r"assignment|coursework|project|homework|\bhw\b", re.I)),
    ("practice", re.compile(r"worksheet|tutorial|practice|problem.?set|lab|prac", re.I)),
    ("lecture", re.compile(r"lecture|slide|transcript|reading|notes?", re.I)),
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def infer_role(relative_path: str) -> str:
    for role, pattern in ROLE_PATTERNS:
        if pattern.search(relative_path):
            return role
    return "other"


def inspect_pdf(path: Path, sample_pages: int) -> tuple[dict[str, Any], list[str]]:
    warnings: list[str] = []
    try:
        from pypdf import PdfReader
    except ImportError:
        return {"status": "metadata_unavailable", "reason": "pypdf is not installed"}, [
            f"{path.name}: PDF metadata unavailable because pypdf is not installed"
        ]

    logging.getLogger("pypdf").setLevel(logging.ERROR)
    try:
        reader = PdfReader(str(path), strict=False)
        encrypted = bool(reader.is_encrypted)
        if encrypted:
            return {"status": "encrypted", "encrypted": True}, [f"{path.name}: encrypted PDF"]
        page_count = len(reader.pages)
        sampled = min(page_count, max(1, sample_pages))
        characters = 0
        extraction_errors = 0
        for page in reader.pages[:sampled]:
            try:
                characters += len(page.extract_text() or "")
            except Exception:
                extraction_errors += 1
        threshold = sampled * 20
        needs_ocr = page_count > 0 and characters < threshold
        if needs_ocr:
            warnings.append(f"{path.name}: little extractable text; OCR may be required")
        if extraction_errors:
            warnings.append(f"{path.name}: text extraction failed on {extraction_errors} sampled page(s)")
        return {
            "status": "checked",
            "encrypted": False,
            "pages": page_count,
            "sampled_pages": sampled,
            "sampled_text_characters": characters,
            "sample_extraction_errors": extraction_errors,
            "needs_ocr": needs_ocr,
        }, warnings
    except Exception as exc:
        return {"status": "error", "reason": str(exc)}, [f"{path.name}: PDF inspection failed: {exc}"]


def load_previous(path: Path) -> tuple[dict[tuple[str, str], str], dict[str, list[str]], int]:
    if not path.is_file():
        return {}, {}, 0
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}, {}, 0
    exact: dict[tuple[str, str], str] = {}
    by_hash: dict[str, list[str]] = {}
    maximum = 0
    for item in raw.get("materials", []):
        identifier = str(item.get("id", ""))
        digest = str(item.get("sha256", ""))
        relative = str(item.get("path", ""))
        if identifier and digest and relative:
            exact[(relative, digest)] = identifier
            by_hash.setdefault(digest, []).append(identifier)
            match = re.fullmatch(r"S(\d+)", identifier)
            if match:
                maximum = max(maximum, int(match.group(1)))
    return exact, by_hash, maximum


def assign_identifier(
    relative: str,
    digest: str,
    exact: dict[tuple[str, str], str],
    by_hash: dict[str, list[str]],
    used: set[str],
    next_number: list[int],
) -> str:
    candidate = exact.get((relative, digest))
    if candidate is None:
        previous = [value for value in by_hash.get(digest, []) if value not in used]
        if len(previous) == 1:
            candidate = previous[0]
    if candidate is None or candidate in used:
        next_number[0] += 1
        candidate = f"S{next_number[0]:03d}"
    used.add(candidate)
    return candidate


def inventory_digest(materials: list[dict[str, Any]]) -> str:
    stable = [
        {"id": item["id"], "path": item["path"], "sha256": item["sha256"]}
        for item in materials
    ]
    payload = json.dumps(stable, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="directory containing local course materials")
    parser.add_argument("--output", type=Path, required=True, help="inventory JSON path")
    parser.add_argument("--sample-pages", type=int, default=5, help="PDF pages sampled for OCR detection")
    parser.add_argument("--no-pdf-metadata", action="store_true")
    parser.add_argument(
        "--extensions",
        help="comma-separated extension allowlist; defaults to common course formats",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    output = args.output.resolve()
    if not root.is_dir():
        print(f"material root is not a directory: {root}", file=sys.stderr)
        return 2
    if args.sample_pages < 1:
        print("--sample-pages must be at least 1", file=sys.stderr)
        return 2

    if args.extensions:
        extensions = {
            value if value.startswith(".") else f".{value}"
            for value in (part.strip().lower() for part in args.extensions.split(","))
            if value
        }
    else:
        extensions = DEFAULT_EXTENSIONS

    exact, by_hash, maximum = load_previous(output)
    next_number = [maximum]
    used: set[str] = set()
    materials: list[dict[str, Any]] = []
    warnings: list[str] = []

    candidates = sorted(
        (
            path
            for path in root.rglob("*")
            if path.is_file()
            and not path.is_symlink()
            and path.suffix.lower() in extensions
            and path.resolve() != output
            and not any(part.startswith(".") for part in path.relative_to(root).parts)
        ),
        key=lambda path: path.relative_to(root).as_posix().casefold(),
    )

    for path in candidates:
        relative = path.relative_to(root).as_posix()
        digest = sha256_file(path)
        identifier = assign_identifier(relative, digest, exact, by_hash, used, next_number)
        item: dict[str, Any] = {
            "id": identifier,
            "path": relative,
            "extension": path.suffix.lower(),
            "bytes": path.stat().st_size,
            "sha256": digest,
            "role_guess": infer_role(f"{root.name}/{relative}"),
        }
        if path.suffix.lower() == ".pdf" and not args.no_pdf_metadata:
            metadata, pdf_warnings = inspect_pdf(path, args.sample_pages)
            item["pdf"] = metadata
            warnings.extend(f"{relative}: {warning}" for warning in pdf_warnings)
        materials.append(item)

    result = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "root": str(root),
        "inventory_digest": inventory_digest(materials),
        "materials": materials,
        "warnings": warnings,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.name + ".tmp")
    temporary.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(output)
    print(
        f"inventory: files={len(materials)} warnings={len(warnings)} "
        f"digest={result['inventory_digest']} output={output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
