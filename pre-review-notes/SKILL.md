---
name: pre-review-notes
description: Build source-grounded revision notes for a specific course from the learner's own slides, assignments, practice material, past assessments, and official solutions. Use when the learner wants assessment-calibrated study notes, a revision chapter, a cheat sheet, or an editable LaTeX and verified PDF deliverable. Do not use for a generic concept explanation with no course material.
---

# Pre-Review Notes

Turn scattered course materials into maintainable revision notes whose priorities, worked
examples, and assessment claims can be traced to the course itself. The skill produces one
chapter at a time and can resume safely across sessions.

## Non-negotiable rules

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

## Start by resolving four preferences

Do not re-ask anything the learner has already specified. Resolve only what is missing:

- mode: **lightweight**, **full**, or **exam-cram**;
- main note language: **Chinese**, **English**, or **bilingual Chinese-English**;
- deliverable: Markdown, editable LaTeX, compiled PDF, or a combination;
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

Retrieve the course's own theory, instructor examples, practice problems, assessed work,
past questions, and explicit guidance for the selected topic. Prefer real course problems to
invented textbook analogues. Use:

- `assets/template.tex` for quantitative courses;
- `assets/markdown-template.md` for prose-heavy courses.

Read [references/authoring.md](references/authoring.md) while drafting. Every assessment
claim and non-trivial sourced claim must carry a stable source ID and locator.

### 5. Validate evidence and reasoning

Run the citation validator when local files are available:

```text
python scripts/validate_citations.py <note-file> --inventory output/materials.json
```

Independently recompute or re-derive worked examples. Compare with official solutions only
after the independent attempt, then match their notation and rewarded depth without padding.

### 6. Build and inspect requested artifacts

For LaTeX/PDF delivery, read [references/pdf-workflow.md](references/pdf-workflow.md), run
`scripts/build_note.py`, and visually inspect its rendered representative pages. A successful
compiler exit and structural check do not by themselves prove the page layout is correct.

### 7. Deliver and update state

Deliver the chapter source and every requested rendered artifact. State the note language,
mode, source boundary, highest-value supported pattern, and any unresolved limitation.
Update `study_state.json` only after observable validation; then refresh `progress.md`.

## Included resources

- `references/modes.md` - scope and trade-offs for the three operating modes.
- `references/evidence-workflow.md` - inventory, OCR routing, evidence grading, and citations.
- `references/authoring.md` - chapter structure, language rules, and source-grounded writing.
- `references/pdf-workflow.md` - compilation, structural checks, rendering, and visual QA.
- `references/state-and-incremental.md` - resumable state and incremental rebuild behavior.
- `assets/` - LaTeX, Markdown, SVG, calendar, progress, and state templates.
- `scripts/` - deterministic inventory, download, citation, state, and PDF helpers.
