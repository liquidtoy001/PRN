# Pre-Review Notes · Source-Grounded Learning and Revision

[中文](./README.md) | **English**

`pre-review-notes` is an Agent Skill that turns a learner's own slides, exercises,
assignments, past assessments, and official solutions into traceable, incrementally
maintainable revision chapters. It prioritises topics and calibrates answer depth only when
the course evidence supports those decisions.

Version **v0.2.10** provides two independently installable entries in this repository:

| Skill | Purpose | Format-specific features |
|---|---|---|
| `pre-review-notes` | Print-first notes | PDF / LaTeX / Markdown, page layout and per-figure review |
| `pre-review-notes-html` | Screen reading | Offline HTML, navigation, optional folded answers, reading width/density/theme |

They share coverage, evidence, paper enrichment and image-extraction rules, with separate
configuration, templates, state and layout reviews. Knowledge mode still defaults to no new
questions. Explicit self-test selection adds a companion, not a replacement for teaching prose.
Browser print is not the verified print-first PDF product.

Download both ZIPs and their SHA-256 files from the
[v0.2.10 Release](https://github.com/liquidtoy001/PRN/releases/tag/v0.2.10).
The original install name is unchanged; either package can be installed alone or alongside the other.
CLI behavior, configuration isolation and standalone ZIP builds were tested. Browser local-file
access was blocked by the runtime security policy, so viewport, keyboard and visual math
acceptance remain pending. Engineering checks do not establish HTML teaching efficacy.

## Capabilities

- Collects purpose, mode, scope, depth, language, deliverables, page size, density, paper
  enrichment, companions and time constraints in one intake and persists resolved choices.
- Knowledge consolidation defaults to no generated questions; source examples remain explained.
- Tracks page-level knowledge coverage and source visuals; lightweight reduces batch size,
  not teaching depth. Optional paper enrichment requires verified sources.

- Confirms `lightweight`, `full`, or `exam-cram` mode and Chinese, English, or bilingual output.
- Labels slides-only output as lecture-driven instead of inventing exam relevance.
- Retains canonical English technical terminology in Chinese notes.
- Uses stable source IDs, precise locators, and material hashes.
- Produces Markdown or editable LaTeX plus a structurally and visually checked PDF.
- Stores resumable machine state in `study_state.json` and renders a readable `progress.md`.
- When selected, produces validated flashcards/quizzes, tracks errors, confidence and mastery, and schedules retests.
- Checks material capacity and quality ceilings before generation and records token usage afterwards.

## Intended domains and validation limits

The material-based workflow is not AI-specific, but actual generation experience has been
concentrated in AI/ML coursework and the repository course fixture is STAT3007. Even these
trials exposed content and layout defects. Cross-domain teaching quality is not established.
Script tests verify tool behavior, not factual correctness or learning outcomes. Course samples
are evaluation/iteration inputs; editing this skill does not train or fine-tune the base model.

Math, statistics, algorithms and other CS courses are plausible nearby applications, requiring
checks of assumptions, proofs, notation and code. Physics/engineering need unit, approximation
and diagram checks. Biology and other visual subjects need detailed label/process review.
Prose-heavy humanities/social sciences have a Markdown template but need argument, attribution,
context and assessment-rubric evaluation. These are design assessments, not tested guarantees.
Medical/legal course notes need domain review and are not professional decision guidance.

Before broadening support claims, evaluate a small chapter from each material type: mathematical
derivation, code/algorithm, layered diagram and extended argument. Compare with the original
for omissions, errors, supplementary-source quality and readability.

## Repository layout

```text
pre-review-notes/
├── pre-review-notes/                  installable skill
│   ├── SKILL.md                       concise entry point and routing
│   ├── VERSION
│   ├── assets/                        output, learning-bank, state, and pricing templates
│   ├── references/                    evidence, authoring, learning, capacity, and usage rules
│   └── scripts/                       material, capacity, usage, learning, state, and PDF tools
├── pre-review-notes-html/             independently installable HTML entry
├── shared/                            canonical format-neutral development resources
├── tools/sync_shared.py               materialise shared copies; --check detects drift
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

For HTML, request `pre-review-notes-html`, specify your material scope, and confirm the bundled
intake. The output is an offline folder with index.html and local assets. Edit shared resources
only under `shared/`, then run `python tools/sync_shared.py`. Committed copies keep each skill
self-contained. Packaging rejects drift:

```powershell
python tools/sync_shared.py --check
python tools/package_skill.py
python tools/package_skill.py --skill-dir pre-review-notes-html
```

The commands below are for the print entry; do not pass its state configuration to the HTML entry.

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
| v0.2.10 | 2026-09-22 | Independent offline HTML entry with optional folded answers; shared-resource drift checks and two release packages. |
| v0.2.9 | 2026-09-19 | Separate figure extraction and final-layout reviews; crop and per-figure render evidence. |
| v0.2.8 | 2026-09-16 | Paper-enrichment configuration and verified paper/figure integration. |
| v0.2.7 | 2026-09-15 | Note purposes and persisted complete intake; includes 0.2.5 coverage and 0.2.6 source-visual improvements. |
| v0.2.0 | 2026-08-25 | Phase two: flashcards/quizzes, error/confidence/mastery tracking, dynamic retests, Anki/CSV, capacity and quality ceilings, and per-generation token/cost ledger. |
| v0.1.0 | 2026-08-24 | Phase-one engineering: progressive skill, modes, local-only manifests, material/citation/state/PDF tools, incremental builds, and reproducible packaging. |
| v0.0.2 | 2026-08-13 | Language confirmation, English terminology in Chinese notes, LaTeX-to-PDF workflow, and a STAT3007 test; the migrated tag retains the feature snapshot but excludes third-party slides. |
| v0.0.1 | 2026-07 | Initial methodology, templates, and manual evaluation plan. |

Project code and original templates use the [MIT License](./LICENSE). Course materials are not
covered by that licence.
