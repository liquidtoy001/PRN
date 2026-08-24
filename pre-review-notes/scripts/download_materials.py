#!/usr/bin/env python3
"""Download local-only course materials from a CSV or JSON manifest.

The script verifies optional byte counts and SHA-256 digests, writes downloads
atomically, and refuses unsafe filenames. It does not grant or verify a licence.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


USER_AGENT = "pre-review-notes-material-fetcher/0.1"


@dataclass(frozen=True)
class Material:
    identifier: str
    filename: str
    url: str
    expected_bytes: int | None
    expected_sha256: str | None


def parse_optional_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    parsed = int(value)
    if parsed < 0:
        raise ValueError("byte count cannot be negative")
    return parsed


def normalise_record(record: dict[str, Any], index: int) -> Material:
    filename = str(record.get("file") or record.get("filename") or "").strip()
    url = str(record.get("url") or "").strip()
    identifier = str(
        record.get("id") or record.get("lecture") or record.get("title") or f"item-{index:03d}"
    ).strip()
    if not filename or not url:
        raise ValueError(f"record {index} requires file/filename and url")

    relative = Path(filename)
    if relative.is_absolute() or not relative.parts or ".." in relative.parts:
        raise ValueError(f"record {index} has unsafe filename {filename!r}")

    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.scheme not in {"http", "https"}:
        raise ValueError(f"record {index} URL must use http or https")

    digest = str(record.get("sha256") or "").strip().lower() or None
    if digest is not None and (len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest)):
        raise ValueError(f"record {index} has an invalid SHA-256 digest")

    return Material(
        identifier=identifier,
        filename=relative.as_posix(),
        url=url,
        expected_bytes=parse_optional_int(record.get("bytes")),
        expected_sha256=digest,
    )


def load_manifest(path: Path) -> list[Material]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            records = list(csv.DictReader(handle))
    elif suffix == ".json":
        raw = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(raw, list):
            records = raw
        elif isinstance(raw, dict):
            records = raw.get("materials") or raw.get("slides") or raw.get("items")
        else:
            records = None
        if not isinstance(records, list):
            raise ValueError("JSON manifest must be a list or contain materials/slides/items")
    else:
        raise ValueError("manifest must use .csv or .json")

    materials: list[Material] = []
    for index, record in enumerate(records, 1):
        if not isinstance(record, dict):
            raise ValueError(f"record {index} must be an object")
        materials.append(normalise_record(record, index))
    if not materials:
        raise ValueError("manifest contains no material records")
    filenames = [item.filename.casefold() for item in materials]
    if len(filenames) != len(set(filenames)):
        raise ValueError("manifest contains duplicate destination filenames")
    return materials


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_file(path: Path, material: Material) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return ["missing"]
    actual_bytes = path.stat().st_size
    if material.expected_bytes is not None and actual_bytes != material.expected_bytes:
        errors.append(f"bytes expected {material.expected_bytes}, got {actual_bytes}")
    if material.expected_sha256 is not None:
        actual_digest = sha256_file(path)
        if actual_digest != material.expected_sha256:
            errors.append(f"sha256 expected {material.expected_sha256}, got {actual_digest}")
    if path.suffix.lower() == ".pdf":
        with path.open("rb") as handle:
            if handle.read(5) != b"%PDF-":
                errors.append("missing PDF header")
    return errors


def safe_destination(output_dir: Path, filename: str) -> Path:
    root = output_dir.resolve()
    target = (root / Path(filename)).resolve()
    try:
        common = Path(os.path.commonpath([str(root), str(target)]))
    except ValueError as exc:
        raise ValueError(f"unsafe destination {filename!r}") from exc
    if common != root:
        raise ValueError(f"destination escapes output directory {filename!r}")
    return target


def download(material: Material, destination: Path, timeout: float) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    partial = destination.with_name(destination.name + ".part")
    partial.unlink(missing_ok=True)
    request = urllib.request.Request(material.url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response, partial.open("wb") as handle:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                handle.write(chunk)
        errors = verify_file(partial, material)
        if errors:
            raise ValueError("; ".join(errors))
        partial.replace(destination)
    except Exception:
        partial.unlink(missing_ok=True)
        raise


def format_errors(errors: Iterable[str]) -> str:
    return "; ".join(errors)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="CSV or JSON material manifest")
    parser.add_argument("--output-dir", type=Path, default=Path("downloads"))
    parser.add_argument("--verify-only", action="store_true", help="verify local files without network access")
    parser.add_argument("--dry-run", action="store_true", help="validate and show destinations only")
    parser.add_argument("--force", action="store_true", help="redownload even when a local file verifies")
    parser.add_argument("--timeout", type=float, default=60.0, help="per-request timeout in seconds")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        materials = load_manifest(args.manifest.resolve())
    except (OSError, ValueError, json.JSONDecodeError, csv.Error) as exc:
        print(f"manifest error: {exc}", file=sys.stderr)
        return 2

    output_dir = args.output_dir.resolve()
    failures = 0
    verified = 0
    downloaded = 0
    for material in materials:
        try:
            destination = safe_destination(output_dir, material.filename)
            if args.dry_run:
                print(f"PLAN {material.identifier}: {destination} <- {material.url}")
                continue

            existing_errors = verify_file(destination, material)
            if not existing_errors and not args.force:
                print(f"OK   {material.identifier}: {material.filename}")
                verified += 1
                continue
            if args.verify_only:
                print(
                    f"FAIL {material.identifier}: {material.filename}: {format_errors(existing_errors)}",
                    file=sys.stderr,
                )
                failures += 1
                continue

            download(material, destination, args.timeout)
            print(f"GET  {material.identifier}: {material.filename}")
            downloaded += 1
        except (OSError, ValueError, urllib.error.URLError) as exc:
            print(f"FAIL {material.identifier}: {material.filename}: {exc}", file=sys.stderr)
            failures += 1

    print(
        f"summary: items={len(materials)} verified={verified} "
        f"downloaded={downloaded} failures={failures}"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
