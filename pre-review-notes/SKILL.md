---
name: pre-review-notes
description: Build source-grounded, print-first course notes in PDF, editable LaTeX or Markdown, with optional revision plans and source-linked practice. Use with the learner's slides, exercises and assessment materials. For interactive HTML notes or collapsible answers use pre-review-notes-html instead; not for generic explanations without course material.
---

# Pre-Review Notes

Version: 0.2.10. Resolve this directory and read `VERSION`
before starting; disclose which copy is used when multiple installations exist.

Turn scattered course materials into maintainable revision notes whose priorities, worked
examples, and assessment claims can be traced to the course itself. The skill produces one
chapter at a time and can resume safely across sessions.

This is the print-first entry. Load only its local references and templates; do not import
another entry's rendering rules. Keep its output separate from other formats (recommended
`output/pdf/` for new projects; preserve existing project paths on resume). Reuse a verified
source/K/V ledger when both formats are requested, but do not overwrite configuration or
artifact state across entries. Browser print output is not a replacement for this workflow.

## Non-negotiable rules

**Coverage before compression.** Default to teaching notes that preserve every distinct
knowledge point in the selected scope, including qualifications, figure conclusions and
small remarks. Lightweight reduces the batch size, not explanation depth. A quick-reference
card is a companion, not a substitute for the chapter; explicit cheat-sheet requests may
use condensed output with omissions disclosed.

1. **Calibrate to evidence, not textbook convention.** Never call a topic important,
   frequent, or exam-style without a source that supports the claim. If assessment evidence
   is absent, label the result as lecture-driven rather than exam-calibrated.
2. **Keep user materials private by default.** Reading or downloading a source does not grant
   permission to commit, publish, redistribute, or place it in a release. Store third-party
   source files in a local ignored directory unless the user explicitly authorizes publishing
   them and the licence permits it.
3. **Use stable source identifiers.** Build a material inventory before making substantial
   claims. Cite source IDs and precise locators such as a PDF page, question number, section,
   or timestamp.
4. **Verify worked reasoning independently.** Do not copy a calculation or derivation on
   trust, even from an official solution. Mark unresolved uncertainty instead of smoothing it
   over.
5. **Do not treat current graded work as permission to complete it.** It may be used to map
   coverage and expected depth. Follow the user's institution rules before providing answers
   to an active assessment.
6. **Deliver incrementally.** Avoid a one-shot whole-course document. Establish the plan,
   complete one representative or highest-priority chapter, obtain useful feedback, then
   continue.
7. **Measure capacity and generation cost honestly.** Check the supplied material volume
   before substantial generation. After every model-generated artifact, append a token-usage
   record. Provider-reported usage, manual counts, partial estimates, and unavailable values
   must never be presented as equivalent.

## Start with the complete configuration intake

Read [references/configuration.md](references/configuration.md) before generation.
Present the complete configuration in the learner's language, showing already specified
values and recommended defaults. Ask once for all missing choices; allow a single reply
accepting defaults. Do not silently treat the recommendations as confirmed preferences.
If the user already specified everything or explicitly delegated choices, proceed without
another confirmation. Resume saved settings and ask only about unresolved or changed choices.

Purpose is independent of mode: `knowledge` (知识巩固版) teaches source knowledge with
proportionate expansion and no generated questions by default; `exam` (考试复习版) adds
evidence-based assessment preparation. Source examples remain in both. Purpose and explicit
companion choices override mode defaults, including full-mode learning-bank generation.

The complete intake includes purpose, mode, source scope, depth, language, deliverable set,
page size, layout density, paper enrichment, learning companions and relevant deadline/study time. Save the
resolved settings in study state even for a single chapter, following configuration.md.

### Existing preference semantics

Do not re-ask anything the learner has already specified. Resolve only what is missing:

- mode: **lightweight**, **full**, or **exam-cram**;
- main note language: **Chinese**, **English**, or **bilingual Chinese-English**;
- deliverable: Markdown, editable LaTeX, compiled PDF, or a combination;
- active-learning companion: none, flashcards, quiz, or both;
- deadline and available study time when they affect prioritisation.

Read [references/modes.md](references/modes.md) before choosing or applying a mode. If the
choice materially changes the result and cannot be inferred, ask one compact question that
bundles the missing preferences.

For Chinese notes, write specialised or easily confused terminology as
`中文（English, acronym）` on first use, then use the established English name or acronym
consistently. Examples include 普通最小二乘法（Ordinary Least Squares, OLS）、岭回归
（Ridge Regression）and 1-最近邻（1-Nearest Neighbour, 1-NN）. Keep mathematical
notation, code identifiers, bibliographic titles, and quoted source wording in their
canonical form.

## Workflow

Resolve every `assets/`, `references/`, and `scripts/` path relative to this skill directory,
not relative to the learner's course workspace. Pass explicit material and output paths to
scripts so generated files remain in the learner's project.

### 1. Inventory and establish the evidence boundary

When filesystem execution is available, run:

```text
python scripts/inventory_materials.py <materials-directory> --output output/materials.json
```

Use the resulting source IDs as the citation ledger. Inspect any `needs_ocr` or
`metadata_unavailable` warnings before drafting. Read
[references/evidence-workflow.md](references/evidence-workflow.md) for source roles,
assessment evidence, OCR handling, manifest downloads, and thin-sample rules.

Before substantial generation, read
[references/measurement-and-capacity.md](references/measurement-and-capacity.md) and run
`scripts/assess_capacity.py`. Share the capacity status, source coverage, and preliminary
quality ceiling. If material does not safely fit, switch to cited chapter subsets and retain
an explicit uncovered-source list; a large upload must not silently become partial coverage.

### 2. Map assessment and topic priority

Identify the grading structure, exam format, explicit instructor guidance, assessed items,
and official solutions. Build chapters at an assessable topic grain. Order them by supported
assessment weight subject to genuine prerequisites. Where evidence is thin, use transparent
labels such as `verified`, `inferred from limited evidence`, and `unknown`; do not fabricate a
numerical ranking.

Share the proposed order before producing a large volume. A course overview SVG and revision
calendar are optional assets, not substitutes for evidence.

### 3. Initialise resumable state

For multi-chapter work, initialise `study_state.json` from
`assets/study-state-template.json` or with `scripts/manage_state.py`. Treat JSON as the
machine-readable source of truth and render `progress.md` as its human-readable companion.
Read [references/state-and-incremental.md](references/state-and-incremental.md) for statuses,
input digests, and rebuild rules.

### 4. Research and draft one chapter

Before research, apply the confirmed paper-enrichment setting using
[references/paper-enrichment.md](references/paper-enrichment.md) when enabled.

First read [references/coverage-and-depth.md](references/coverage-and-depth.md).
Inspect every selected physical page, group true duplicate/animation pages, and create
`coverage.md` using `assets/coverage-template.md`. Map each distinct point to a note section.
If the selected scope is too large, split it into chapters and keep remaining points pending.

For source figures, charts and tables, read
[references/source-visuals.md](references/source-visuals.md). Prefer reusing informative
original visuals near their explanation; record their disposition in the coverage ledger.
Text coverage alone is insufficient when a figure carries essential relationships or examples.

Retrieve the course's own theory, instructor examples, practice problems, assessed work,
past questions, and explicit guidance for the selected topic. Prefer real course problems to
invented textbook analogues. Use:

- `assets/template.tex` for quantitative courses;
- `assets/markdown-template.md` for prose-heavy courses.

Read [references/authoring.md](references/authoring.md) while drafting. Every assessment
claim and non-trivial sourced claim must carry a stable source ID and locator.

When flashcards or quizzes are requested, or included by the selected mode, read
[references/active-learning.md](references/active-learning.md). Generate a separate learning
bank from verified chapter content, validate it with `scripts/manage_learning.py`, and record
attempts, confidence, mistakes, mastery, and staged retests in local learner state. Do not
assign an assessment weight without direct priority evidence.

### 5. Validate evidence and reasoning

When paper enrichment is `reading-list` or `integrated`, read
[references/paper-enrichment.md](references/paper-enrichment.md). Verify papers before
recommending or incorporating them; record access limitations and precise source locators.

Reconcile the coverage ledger against the original pages and the final note, then write
`review.md` using `assets/review-template.md`. Citation syntax, semantic support, coverage,
independent reasoning and visual layout are separate checks. Automated citation validation
does not certify correctness or completeness. Unresolved substantive points prevent a claim
of complete coverage; report partial delivery explicitly.

Run the citation validator when local files are available:

```text
python scripts/validate_citations.py <note-file> --inventory output/materials.json
```

Independently recompute or re-derive worked examples. Compare with official solutions only
after the independent attempt, then match their notation and rewarded depth without padding.

### 6. Build and inspect requested artifacts

For each included visual, pass extraction-completeness and final-page-layout reviews
separately using `references/source-visuals.md`. A complete image file does not prove
the final PDF displays it without obstruction. Record both checks by V ID in review.md.

For LaTeX/PDF delivery, read [references/pdf-workflow.md](references/pdf-workflow.md), run
`scripts/build_note.py`, and visually inspect its rendered representative pages. A successful
compiler exit and structural check do not by themselves prove the page layout is correct.

### 7. Deliver and update state

Deliver the chapter source and every requested rendered artifact. State the note language,
mode, source boundary, highest-value supported pattern, capacity status, and the concrete
quality ceiling for this artifact. Immediately append one record to `usage-ledger.jsonl` with
`scripts/usage_ledger.py`: prefer provider-reported usage; otherwise record a labelled partial
estimate or an explicit unavailable reason. Monetary cost requires a dated user/provider
pricing profile and remains an estimate rather than an invoice.

For schema-version 2 state, do not mark a newly generated chapter verified or delivered until
`capacity_disclosure` and `usage_accounting` QA pass. Update `study_state.json` only after
observable validation; then refresh `progress.md` and any requested retest plan.

## Included resources

- `references/modes.md` - scope and trade-offs for the three operating modes.
- `references/evidence-workflow.md` - inventory, OCR routing, evidence grading, and citations.
- `references/authoring.md` - chapter structure, language rules, and source-grounded writing.
- `references/pdf-workflow.md` - compilation, structural checks, rendering, and visual QA.
- `references/state-and-incremental.md` - resumable state and incremental rebuild behavior.
- `references/active-learning.md` - flashcards, quizzes, mastery, dynamic plans, and exports.
- `references/measurement-and-capacity.md` - context fit, quality ceilings, and usage ledger.
- `assets/` - LaTeX, Markdown, SVG, calendar, progress, and state templates.
- `scripts/` - deterministic inventory, capacity, usage, learning, citation, state, and PDF helpers.
