# Pre-Review Notes · Evidence-Driven Course Revision

[中文](./README.md) | **English**

`pre-review-notes` is an Agent Skill that turns a learner's own slides, exercises,
assignments, past assessments, and official solutions into traceable, incrementally
maintainable revision chapters. It prioritises topics and calibrates answer depth only when
the course evidence supports those decisions.

The current source version is **v0.2.7**. It adds knowledge-consolidation and exam-revision
purposes, complete configuration intake and persisted settings, building on coverage and
source-visual improvements. Run `python tools/package_skill.py` for the current ZIP.
The earlier v0.2.0 release contains the second-phase learning loop and
resource measurement, and is available from
[GitHub Releases](https://github.com/liquidtoy001/PRN/releases/tag/v0.2.0).

## Capabilities

- Confirms `lightweight`, `full`, or `exam-cram` mode and Chinese, English, or bilingual output.
- Labels slides-only output as lecture-driven instead of inventing exam relevance.
- Retains canonical English technical terminology in Chinese notes.
- Uses stable source IDs, precise locators, and material hashes.
- Produces Markdown or editable LaTeX plus a structurally and visually checked PDF.
- Stores resumable machine state in `study_state.json` and renders a readable `progress.md`.
- Produces validated flashcards/quizzes, tracks errors, confidence and mastery, and schedules retests.
- Checks material capacity and quality ceilings before generation and records token usage afterwards.

## Repository layout

```text
pre-review-notes/
├── pre-review-notes/                  installable skill
│   ├── SKILL.md                       concise entry point and routing
│   ├── VERSION
│   ├── assets/                        output, learning-bank, state, and pricing templates
│   ├── references/                    evidence, authoring, learning, capacity, and usage rules
│   └── scripts/                       material, capacity, usage, learning, state, and PDF tools
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

Check safe context fit and the concrete product ceiling before drafting:

```powershell
python pre-review-notes/scripts/assess_capacity.py `
  output/materials.json `
  --context-window 128000 `
  --output output/capacity-report.json `
  --markdown output/capacity-report.md
```

`128000` is only a command example. Replace it with a confirmed active model/platform limit;
when unknown, omit it and use incremental retrieval instead of claiming full coverage.

Initialise resumable state:

```powershell
python pre-review-notes/scripts/manage_state.py init `
  --output output/study_state.json `
  --course-id STAT3007 `
  --course-title "Deep Learning" `
  --mode lightweight `
  --language zh `
  --format latex-pdf `
  --learning-output flashcards `
  --learning-output quiz
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

> Migration note: the new repository continues v0.2.0 from a clean v0.0.1, v0.0.2, and v0.1.0
> commit chain. The v0.0.2 feature snapshot and Release package are retained, but third-party slides
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

## Phase-two capabilities

- `manage_learning.py` validates source-linked flashcard/quiz banks, records correctness,
  confidence, mistake tags and mastery, and schedules staged retests.
- Retest plans use the assessment date, explicit assessment evidence, mastery, due state, and
  answer time. Items without assessment evidence remain labelled as learning priorities, not
  exam-frequency predictions.
- UTF-8 CSV and three-column Anki TSV export.
- Conservative material token ranges plus context-fit, OCR/encryption, content-coverage,
  exam-calibration, and answer-depth ceilings from `assess_capacity.py`.
- Per-generation `usage_ledger.py` records distinguish provider-reported, manually-reported,
  partial-estimate, and unavailable measurements. Monetary estimates require an explicit,
  dated pricing profile.
- Study-state schema 2 prevents new chapters from being verified/delivered without capacity
  disclosure and usage accounting, while retaining honest legacy migrations.

## Version history

| Version | Date | Changes |
|---|---|---|
| v0.2.0 | 2026-08-25 | Phase two: flashcards/quizzes, error/confidence/mastery tracking, dynamic retests, Anki/CSV, capacity and quality ceilings, and per-generation token/cost ledger. |
| v0.1.0 | 2026-08-24 | Phase-one engineering: progressive skill, modes, local-only manifests, material/citation/state/PDF tools, incremental builds, and reproducible packaging. |
| v0.0.2 | 2026-08-13 | Language confirmation, English terminology in Chinese notes, LaTeX-to-PDF workflow, and a STAT3007 test; the migrated tag retains the feature snapshot but excludes third-party slides. |
| v0.0.1 | 2026-07 | Initial methodology, templates, and manual evaluation plan. |

Project code and original templates use the [MIT License](./LICENSE). Course materials are not
covered by that licence.
