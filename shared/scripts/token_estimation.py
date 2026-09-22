#!/usr/bin/env python3
"""Model-independent, explicitly approximate token estimates for local files."""

from __future__ import annotations

import html
import json
import math
import re
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree


TEXT_EXTENSIONS = {
    ".c",
    ".cpp",
    ".csv",
    ".h",
    ".html",
    ".htm",
    ".ipynb",
    ".java",
    ".js",
    ".json",
    ".md",
    ".py",
    ".r",
    ".sql",
    ".tex",
    ".ts",
    ".txt",
    ".yaml",
    ".yml",
}
OFFICE_EXTENSIONS = {".docx", ".pptx", ".xlsx"}
MAX_TEXT_BYTES = 64 * 1024 * 1024
MAX_OFFICE_XML_BYTES = 128 * 1024 * 1024

CJK_PATTERN = re.compile(
    "["
    "\u3400-\u4dbf"
    "\u4e00-\u9fff"
    "\uf900-\ufaff"
    "\u3040-\u30ff"
    "\uac00-\ud7af"
    "]"
)
HTML_TAG_PATTERN = re.compile(r"<[^>]+>")


def estimate_text_tokens(text: str, *, basis: str = "complete-text") -> dict[str, Any]:
    """Return a conservative range, not a tokenizer- or model-exact count."""

    visible = "".join(character for character in text if not character.isspace())
    characters = len(visible)
    cjk_characters = len(CJK_PATTERN.findall(visible))
    other_characters = max(0, characters - cjk_characters)
    lower = math.ceil(cjk_characters * 0.70 + other_characters / 5.0)
    estimate = math.ceil(cjk_characters * 1.00 + other_characters / 4.0)
    upper = math.ceil(cjk_characters * 1.60 + other_characters / 2.5)
    return {
        "status": "estimated",
        "method": "character-heuristic-v1",
        "basis": basis,
        "confidence": "low",
        "characters": characters,
        "cjk_characters": cjk_characters,
        "lower_bound_tokens": lower,
        "estimated_tokens": estimate,
        "upper_bound_tokens": upper,
        "notice": "Model-independent estimate; use provider-reported usage for exact accounting.",
    }


def _decode_text(payload: bytes) -> tuple[str, str]:
    for encoding in ("utf-8-sig", "utf-16"):
        try:
            return payload.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    return payload.decode("utf-8", errors="replace"), "utf-8-replacement"


def _not_available(reason: str) -> dict[str, Any]:
    return {
        "status": "unavailable",
        "method": None,
        "confidence": "none",
        "reason": reason,
    }


def _extract_notebook_text(path: Path) -> tuple[str, str]:
    raw, encoding = _decode_text(path.read_bytes())
    data = json.loads(raw)
    cells = data.get("cells", []) if isinstance(data, dict) else []
    parts: list[str] = []
    for cell in cells:
        if not isinstance(cell, dict):
            continue
        source = cell.get("source", [])
        if isinstance(source, str):
            parts.append(source)
        elif isinstance(source, list):
            parts.append("".join(str(value) for value in source))
    return "\n".join(parts), f"notebook-cells:{encoding}"


def _extract_text_file(path: Path) -> tuple[str, str]:
    if path.stat().st_size > MAX_TEXT_BYTES:
        raise ValueError(f"file exceeds {MAX_TEXT_BYTES} byte extraction limit")
    if path.suffix.lower() == ".ipynb":
        return _extract_notebook_text(path)
    text, encoding = _decode_text(path.read_bytes())
    if path.suffix.lower() in {".html", ".htm"}:
        text = html.unescape(HTML_TAG_PATTERN.sub(" ", text))
        encoding = f"html-text:{encoding}"
    return text, encoding


def _office_entry_is_relevant(extension: str, name: str) -> bool:
    normalized = name.replace("\\", "/")
    if extension == ".docx":
        return normalized.startswith("word/") and normalized.endswith(".xml")
    if extension == ".pptx":
        return (
            normalized.startswith("ppt/slides/")
            or normalized.startswith("ppt/notesSlides/")
        ) and normalized.endswith(".xml")
    if extension == ".xlsx":
        return (
            normalized == "xl/sharedStrings.xml"
            or normalized.startswith("xl/worksheets/")
        ) and normalized.endswith(".xml")
    return False


def _extract_office_text(path: Path) -> tuple[str, str]:
    parts: list[str] = []
    consumed = 0
    extension = path.suffix.lower()
    with zipfile.ZipFile(path) as bundle:
        for info in sorted(bundle.infolist(), key=lambda value: value.filename):
            if not _office_entry_is_relevant(extension, info.filename):
                continue
            consumed += info.file_size
            if consumed > MAX_OFFICE_XML_BYTES:
                raise ValueError(
                    f"office XML exceeds {MAX_OFFICE_XML_BYTES} byte extraction limit"
                )
            payload = bundle.read(info)
            try:
                root = ElementTree.fromstring(payload)
            except ElementTree.ParseError:
                continue
            values = [node.text for node in root.iter() if node.text and node.text.strip()]
            if values:
                parts.append(" ".join(values))
    if not parts:
        raise ValueError("no readable Office XML text was found")
    return "\n".join(parts), f"office-xml:{extension[1:]}"


def estimate_file_tokens(path: Path) -> dict[str, Any]:
    """Estimate tokens for formats that can be read without provider-specific tooling."""

    resolved = path.resolve()
    if not resolved.is_file():
        return _not_available(f"file does not exist: {resolved}")
    extension = resolved.suffix.lower()
    try:
        if extension in TEXT_EXTENSIONS:
            text, extraction = _extract_text_file(resolved)
        elif extension in OFFICE_EXTENSIONS:
            text, extraction = _extract_office_text(resolved)
        else:
            return _not_available(f"unsupported local text extraction for {extension or 'no extension'}")
    except (OSError, ValueError, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        return _not_available(str(exc))
    estimate = estimate_text_tokens(text)
    estimate["extraction"] = extraction
    return estimate


def extrapolate_sample_estimate(
    sample_text: str,
    *,
    sampled_pages: int,
    total_pages: int,
) -> dict[str, Any]:
    """Estimate a whole PDF from sampled extracted text, with a wide safety range."""

    if sampled_pages <= 0 or total_pages <= 0 or not sample_text.strip():
        return _not_available("no extractable sampled PDF text")
    sample = estimate_text_tokens(sample_text, basis="sampled-pdf-text")
    factor = total_pages / sampled_pages
    estimate = dict(sample)
    estimate.update(
        {
            "basis": "sampled-pdf-text-extrapolation",
            "sampled_pages": sampled_pages,
            "total_pages": total_pages,
            "lower_bound_tokens": math.floor(sample["lower_bound_tokens"] * factor * 0.75),
            "estimated_tokens": math.ceil(sample["estimated_tokens"] * factor),
            "upper_bound_tokens": math.ceil(sample["upper_bound_tokens"] * factor * 1.35),
            "confidence": "low",
            "notice": (
                "Extrapolated from sampled PDF pages; layout, OCR, equations, and page density "
                "can materially change the true model token count."
            ),
        }
    )
    return estimate
