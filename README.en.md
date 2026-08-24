# Pre-Review Notes · Evidence-Driven Course Revision

[中文](./README.md) | **English**

`pre-review-notes` is an Agent Skill that turns a learner's own slides, exercises,
assignments, past assessments, and official solutions into traceable, incrementally
maintainable revision chapters. It prioritises topics and calibrates answer depth only when
the course evidence supports those decisions.

The current source version is **v0.1.0**. It contains the first engineering phase and is
available from [GitHub Releases](https://github.com/liquidtoy001/PRN/releases/tag/v0.1.0).

## Capabilities

- Confirms `lightweight`, `full`, or `exam-cram` mode and Chinese, English, or bilingual output.
- Labels slides-only output as lecture-driven instead of inventing exam relevance.
- Retains canonical English technical terminology in Chinese notes.
- Uses stable source IDs, precise locators, and material hashes.
- Produces Markdown or editable LaTeX plus a structurally and visually checked PDF.
- Stores resumable machine state in `study_state.json` and renders a readable `progress.md`.

## Repository layout

```text
pre-review-notes/
├── pre-review-notes/                  installable skill
│   ├── SKILL.md                       concise entry point and routing
│   ├── VERSION
│   ├── assets/                        output templates
│   ├── references/                    mode-specific workflow guidance
│   └── scripts/                       deterministic workflow helpers
├── examples/stat3007/notes/           generated example output, no source slides
├── tests/fixtures/stat3007/materials.csv
├── test-data/                         ignored local third-party test inputs
├── tools/package_skill.py
├── dist/                              ignored local release artifacts
├── USAGE.md
├── TESTING.md
└── LICENSE
```

## Local source workflow

Create a citation-ready inventory:

```powershell
python pre-review-notes/scripts/inventory_materials.py `
  E:\path\to\course-materials `
  --output output/materials.json
```

Initialise resumable state:

```powershell
python pre-review-notes/scripts/manage_state.py init `
  --output output/study_state.json `
  --course-id STAT3007 `
  --course-title "Deep Learning" `
  --mode lightweight `
  --language zh `
  --format latex-pdf
```

See [USAGE.md](./USAGE.md) for installation and platform limitations.

## Local-only test materials

Third-party course PDFs are not project examples and must not enter new commits, skill ZIPs,
or release assets. The repository keeps only
[materials.csv](./tests/fixtures/stat3007/materials.csv). Reproduce the local fixture with:

```powershell
python pre-review-notes/scripts/download_materials.py `
  tests/fixtures/stat3007/materials.csv `
  --output-dir test-data/stat3007/slides
```

The downloader verifies declared sizes and SHA-256 hashes; it does not determine whether a
user is licensed to download or use the sources.

> Migration note: the new repository republishes a clean v0.0.1, v0.0.2, and v0.1.0 commit
> chain. The v0.0.2 feature snapshot and Release package are retained, but third-party slides
> and the old Git objects that contained them were not migrated.

## Phase-one changes

- Progressive disclosure through a concise `SKILL.md` and focused references.
- Three operating modes with explicit scope boundaries.
- Material inventory, stable source IDs, and scanned-PDF/OCR risk detection.
- CSV/JSON manifest downloads into ignored local directories.
- Machine-checkable LaTeX and Markdown citations.
- Resumable state, chapter input digests, and incremental rebuild decisions.
- LaTeX compilation, PDF traversal, representative rendering, and QA reports.
- Deterministic flattened ZIP packaging for GitHub Releases.

## Version history

| Version | Date | Changes |
|---|---|---|
| v0.1.0 | 2026-08-24 | Phase-one engineering: progressive skill, modes, local-only manifests, material/citation/state/PDF tools, incremental builds, and reproducible packaging. |
| v0.0.2 | 2026-08-13 | Language confirmation, English terminology in Chinese notes, LaTeX-to-PDF workflow, and a STAT3007 test; the migrated tag retains the feature snapshot but excludes third-party slides. |
| v0.0.1 | 2026-07 | Initial methodology, templates, and manual evaluation plan. |

Project code and original templates use the [MIT License](./LICENSE). Course materials are not
covered by that licence.
