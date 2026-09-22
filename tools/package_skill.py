#!/usr/bin/env python3
"""Build a deterministic, flattened skill ZIP for a GitHub release."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import zipfile
from pathlib import Path

from sync_shared import REPOSITORY, SKILLS, sync


EXCLUDED_PARTS = {"__pycache__", "tmp", "evals"}
EXCLUDED_SUFFIXES = {".pdf", ".pyc", ".zip"}
FIXED_TIMESTAMP = (2020, 1, 1, 0, 0, 0)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def included_files(skill_dir: Path) -> list[Path]:
    files: list[Path] = []
    for path in skill_dir.rglob("*"):
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(skill_dir)
        if EXCLUDED_PARTS.intersection(relative.parts):
            continue
        if path.suffix.lower() in EXCLUDED_SUFFIXES or path.name in {".DS_Store"}:
            continue
        files.append(path)
    return sorted(files, key=lambda path: path.relative_to(skill_dir).as_posix())


def build_parser() -> argparse.ArgumentParser:
    repository = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", type=Path, default=repository / "pre-review-notes")
    parser.add_argument("--output-dir", type=Path, default=repository / "dist")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    skill_dir = args.skill_dir.resolve()
    output_dir = args.output_dir.resolve()
    protected = [skill_dir, REPOSITORY / "shared", *(REPOSITORY / name for name in SKILLS)]
    if any(output_dir.is_relative_to(path.resolve()) for path in protected):
        print("output directory must be outside skill and shared-source directories", file=sys.stderr)
        return 2
    if skill_dir in {(REPOSITORY / name).resolve() for name in SKILLS}:
        stale = sync(REPOSITORY, check=True)
        if stale:
            print("shared resources are stale; run tools/sync_shared.py", file=sys.stderr)
            return 2
    skill_file = skill_dir / "SKILL.md"
    version_file = skill_dir / "VERSION"
    repository_license = Path(__file__).resolve().parents[1] / "LICENSE"
    if not skill_file.is_file() or not version_file.is_file():
        print("skill directory must contain SKILL.md and VERSION", file=sys.stderr)
        return 2
    version = version_file.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        print(f"invalid VERSION value: {version!r}", file=sys.stderr)
        return 2

    name_match = re.search(r"^name: ([a-z0-9-]+)$", skill_file.read_text(encoding="utf-8"), re.M)
    if not name_match or name_match.group(1) != skill_dir.name:
        print("skill directory and frontmatter name must match", file=sys.stderr)
        return 2
    skill_name = name_match.group(1)

    files = included_files(skill_dir)
    if skill_file not in files:
        print("SKILL.md was excluded unexpectedly", file=sys.stderr)
        return 2
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"{skill_name}-v{version}.zip"
    temporary = archive.with_name(archive.name + ".tmp")
    temporary.unlink(missing_ok=True)

    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for path in files:
            relative = path.relative_to(skill_dir).as_posix()
            info = zipfile.ZipInfo(relative, date_time=FIXED_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, path.read_bytes())
        if repository_license.is_file():
            info = zipfile.ZipInfo("LICENSE", date_time=FIXED_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, repository_license.read_bytes())
    temporary.replace(archive)

    with zipfile.ZipFile(archive) as bundle:
        names = bundle.namelist()
        if "SKILL.md" not in names:
            print("archive is not flattened; SKILL.md is missing from ZIP root", file=sys.stderr)
            return 2
        forbidden = [name for name in names if Path(name).suffix.lower() in EXCLUDED_SUFFIXES]
        if forbidden:
            print(f"archive contains forbidden generated/source artifacts: {forbidden}", file=sys.stderr)
            return 2

    digest = sha256_file(archive)
    checksum = archive.with_suffix(archive.suffix + ".sha256")
    checksum.write_text(f"{digest}  {archive.name}\n", encoding="ascii")
    print(f"package: {archive}")
    print(f"files: {len(names)}")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
