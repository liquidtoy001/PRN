#!/usr/bin/env python3
"""Validate machine-readable source references in a generated note."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any


LATEX_CITATION = re.compile(
    r"\\(?P<kind>source|assess)ref\s*\{(?P<id>[^{}]+)\}\s*\{(?P<locator>[^{}]+)\}"
)
MARKDOWN_CITATION = re.compile(
    r"\[(?P<kind>source|assessment):(?P<id>[^|\]]+)\|(?P<locator>[^\]]+)\]"
)
PLACEHOLDER_MARKERS = ("[", "]", "e.g.", "example", "source id", "locator")


def load_inventory(path: Path) -> tuple[dict[str, dict[str, Any]], list[str]]:
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        materials = []
        for position, row in enumerate(rows, 1):
            item = dict(row)
            item["id"] = str(row.get("id") or f"S{position:03d}")
            item["path"] = str(row.get("path") or row.get("file") or row.get("filename") or "")
            materials.append(item)
    else:
        raw = json.loads(path.read_text(encoding="utf-8"))
        materials = raw.get("materials")
        if not isinstance(materials, list):
            raise ValueError("JSON inventory must contain a materials list")
    index: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    for position, item in enumerate(materials, 1):
        if not isinstance(item, dict):
            errors.append(f"inventory item {position} is not an object")
            continue
        identifier = str(item.get("id", "")).strip()
        if not identifier:
            errors.append(f"inventory item {position} has no id")
        elif identifier in index:
            errors.append(f"duplicate inventory id {identifier}")
        else:
            index[identifier] = item
    return index, errors


def find_citations(text: str, suffix: str) -> list[dict[str, str]]:
    pattern = LATEX_CITATION if suffix.lower() == ".tex" else MARKDOWN_CITATION
    citations: list[dict[str, str]] = []
    for match in pattern.finditer(text):
        kind = match.group("kind")
        if kind == "assess":
            kind = "assessment"
        citations.append(
            {
                "kind": kind,
                "id": match.group("id").strip(),
                "locator": match.group("locator").strip(),
                "offset": str(match.start()),
            }
        )
    return citations


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("note", type=Path, help="generated .tex or .md note")
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--materials-root", type=Path, help="optionally verify inventoried files exist")
    parser.add_argument("--allow-empty", action="store_true", help="allow a note with no source references")
    parser.add_argument("--report", type=Path, help="write a JSON validation report")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        text = args.note.read_text(encoding="utf-8")
        inventory, errors = load_inventory(args.inventory)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError, csv.Error) as exc:
        print(f"validation setup error: {exc}", file=sys.stderr)
        return 2

    citations = find_citations(text, args.note.suffix)
    if not citations and not args.allow_empty:
        errors.append("note contains no machine-readable source references")

    for citation in citations:
        location = line_number(text, int(citation["offset"]))
        identifier = citation["id"]
        locator = citation["locator"]
        if identifier not in inventory:
            errors.append(f"line {location}: unknown source id {identifier}")
        lower_locator = locator.casefold()
        if not locator or any(marker in lower_locator for marker in PLACEHOLDER_MARKERS):
            errors.append(f"line {location}: unresolved or empty locator for {identifier}")

    if args.materials_root:
        root = args.materials_root.resolve()
        for identifier in sorted({citation["id"] for citation in citations if citation["id"] in inventory}):
            relative = inventory[identifier].get("path")
            if not isinstance(relative, str) or not (root / relative).is_file():
                errors.append(f"inventory source {identifier} is missing under {root}")

    report = {
        "schema_version": 1,
        "note": str(args.note.resolve()),
        "inventory": str(args.inventory.resolve()),
        "status": "pass" if not errors else "fail",
        "citation_count": len(citations),
        "source_ids": sorted({citation["id"] for citation in citations}),
        "errors": errors,
        "scope_note": (
            "This validator checks reference syntax and source IDs; it does not prove that every "
            "factual or assessment claim is cited correctly."
        ),
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for error in errors:
        print(f"ERROR {error}", file=sys.stderr)
    print(
        f"citations: status={report['status']} count={len(citations)} "
        f"unique_sources={len(report['source_ids'])}"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
