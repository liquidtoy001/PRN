#!/usr/bin/env python3
"""Materialise format-neutral resources into independently installable skill folders."""
from __future__ import annotations

import argparse
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
SKILLS = ("pre-review-notes", "pre-review-notes-html")
SHARED_FILES = (
    "references/coverage-and-depth.md",
    "references/source-visuals.md",
    "references/evidence-workflow.md",
    "references/paper-enrichment.md",
    "references/measurement-and-capacity.md",
    "assets/coverage-template.md",
    "assets/pricing-template.json",
    "scripts/inventory_materials.py",
    "scripts/assess_capacity.py",
    "scripts/token_estimation.py",
    "scripts/usage_ledger.py",
    "scripts/download_materials.py",
    "scripts/validate_citations.py",
)


def sync(repository: Path, *, check: bool) -> list[str]:
    """Return stale paths; check mode never mutates files."""
    stale = []
    # Read all sources first: a missing canonical file must not cause a partial sync.
    sources = {name: (repository / "shared" / name).read_bytes() for name in SHARED_FILES}
    for skill in SKILLS:
        for name, data in sources.items():
            target = repository / skill / name
            if not target.is_file() or target.read_bytes() != data:
                stale.append(f"{skill}/{name}")
                if not check:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(data)
    return stale


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail on drift without writing")
    args = parser.parse_args()
    stale = sync(REPOSITORY, check=args.check)
    for path in stale:
        print(f"{'STALE' if args.check else 'SYNCED'} {path}")
    print(f"shared resources: {len(SHARED_FILES)} per skill, {len(stale)} differences")
    return 1 if args.check and stale else 0


if __name__ == "__main__":
    raise SystemExit(main())
