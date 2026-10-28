#!/usr/bin/env python3
"""Read-only, heuristic publication audit of tracked files and main/tag history.

This is not a comprehensive secret scanner. Reports locations, never matched secret values.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    "private-key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github-token": re.compile(rb"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b"),
    "provider-key": re.compile(rb"\b(?:sk-(?:proj-|ant-)?[A-Za-z0-9_-]{32,}|AIza[A-Za-z0-9_-]{30,}|AKIA[A-Z0-9]{16})\b"),
    "personal-path": re.compile(rb"(?:[A-Z]:[\\/]Users[\\/]|/Users/|/home/)(?!<|example|user[\\/])[^\s/\\<>\"']+", re.I),
}


def git(*args: str, data: bytes | None = None) -> bytes:
    return subprocess.run(["git", *args], cwd=ROOT, input=data, capture_output=True,
                          check=True).stdout


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    paths = git("ls-files", "-z").decode().split("\0")
    paths = [name for name in paths if name]
    links = []
    working_findings = []
    for name in paths:
        data = (ROOT / name).read_bytes()
        for category, pattern in PATTERNS.items():
            for match in pattern.finditer(data):
                working_findings.append({"category": category, "path": name,
                                         "line": data[:match.start()].count(b"\n") + 1})
        if not name.endswith(".md"):
            continue
        path = ROOT / name
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(r"\[[^\]\n]*\]\(([^)\n]+)\)", text):
            target = match.group(1).strip().strip("<>")
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            target = target.split("#", 1)[0]
            if target and not (path.parent / target).exists():
                links.append({"file": name, "target": target})
    objects = {}
    for line in git("rev-list", "--objects", "origin/main", "--tags").decode().splitlines():
        oid, _, name = line.partition(" ")
        objects[oid] = name
    payload = git("cat-file", "--batch", data=("\n".join(objects) + "\n").encode())
    offset, blob_count, findings = 0, 0, []
    for oid, name in objects.items():
        end = payload.index(b"\n", offset)
        header = payload[offset:end].split()
        size = int(header[2])
        body = payload[end + 1:end + 1 + size]
        offset = end + size + 2
        if header[1] != b"blob":
            continue
        blob_count += 1
        for category, pattern in PATTERNS.items():
            for match in pattern.finditer(body):
                findings.append({"category": category, "object": oid, "path": name,
                                 "line": body[:match.start()].count(b"\n") + 1})
    artifacts = sorted({name for name in objects.values()
                        if name.lower().endswith((".pdf", ".zip", ".pem", ".p12", ".env"))})
    report = {"scope": "working tracked Markdown links; blobs reachable from origin/main and all tags",
              "tracked_files": len(paths), "historical_blobs": blob_count,
              "working_tree_findings": working_findings,
              "broken_local_links": links, "heuristic_findings": findings,
              "historical_binary_or_sensitive_paths": artifacts,
              "limits": "Pattern scan only; no guarantee of absence of secrets, personal data or copyright issues. Local-only branches and ignored inputs are excluded."}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return int(bool(links or any(item["category"] != "personal-path" for item in findings + working_findings)))


if __name__ == "__main__":
    raise SystemExit(main())
