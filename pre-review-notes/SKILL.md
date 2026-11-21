---
name: pre-review-notes
description: Build source-grounded, print-first course notes for preview, knowledge consolidation or exam revision in PDF, editable LaTeX or Markdown. Use with the learner's slides, exercises and assessment materials. For interactive HTML notes or collapsible answers use pre-review-notes-html instead; not for generic explanations without course material.
---

# Pre-Review Notes

Version: 0.3.5. Resolve this directory and read `VERSION`
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

**Standalone reading.** Build a connected explanation with the prerequisites available
before they are used. Read [references/standalone-teaching.md](references/standalone-teaching.md)
when planning and drafting; a correct inventory of separate points is not a readable chapter.

1. **Calibrate to evidence, not textbook convention.** Never call a topic important,
   frequent, or exam-style without a source that supports the claim. If assessment evidence
   is absent, label the result as lecture-driven rather than exam-calibrated.
2. **Keep user materials private by default.** Reading or downloading a source does not grant
   permission to commit, publish, redistribute, or place it in a release. Store third-party
   source files in a local ignored directory unless the user explicitly authorizes publishing
   them and the licence permits it.
3. **Use stable source identifiers.** Build a material inventory before making substantial
   claims. Record source IDs and precise locators such as a PDF page, question number,
   section or timestamp in the note or its mapped evidence companion.
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

## Start with presets and a complete configuration card

Follow the [first-use conversation](references/learning-presets.md) using every row and
alternative in the [configuration card](references/configuration.md). Show the whole card
once, including inactive rows. On resume, ask only about missing or changed choices.

Purpose selects the teaching route. Mode selects scope/time: 先做一章 (`lightweight`), 分章完成课程
(`full`), 限时冲刺 (`exam-cram`). Read [references/modes.md](references/modes.md). All presets
retain source examples, full within-scope teaching and review; additional practice defaults
to none. Full mode and exam purpose never silently enable a quiz or bank.
For exam purpose, read [references/exam-review.md](references/exam-review.md) and derive
structure, scope and answer language from the supplied papers, syllabus or topic checklist.
Read [references/note-presentation.md](references/note-presentation.md): source indexes and
source/process explanations default to off in the student note; keep the evidence companions.
Visible code also defaults to off (`include_code=false`). Answer-language snippets follow
the actual question type in exam-review.md, not every formula, calculation or choice item.

For Chinese notes, write specialised or easily confused terminology as
`中文（English, acronym）` on first use, then use stable Chinese terminology or familiar acronyms
naturally in the confirmed note language. Examples include 普通最小二乘法（Ordinary Least Squares, OLS）、岭回归
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

### 2. Plan topics for the selected purpose

For preview and knowledge, follow the course sequence and prerequisite dependencies from
learning-presets.md. Do not require an exam map or past-paper search to start a preview.
For exam, identify grading structure, format, instructor guidance, assessed items and
official solutions. Resolve paper identities and question overlaps using exam-review.md
before counting recurrence. Build chapters at an assessable topic grain. Order them by supported
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

Retrieve the course's own theory, instructor examples and exercises for the selected topic;
use assessment sources when the confirmed purpose/scope calls for them. Prefer real course problems to
invented textbook analogues. Use:

- `assets/template.tex` for quantitative courses;
- `assets/markdown-template.md` for prose-heavy courses.

Read [references/authoring.md](references/authoring.md) while drafting. Every assessment
claim and non-trivial sourced claim must carry a stable source ID and locator.
When the learner requests citation-free body text, put those mappings in evidence.md using
references/citation-format.md and pass it to the citation validator.

When flashcards or quizzes are selected in the confirmed configuration, read
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

After the draft exists, read [references/second-pass-review.md](references/second-pass-review.md).
Notify the learner that the automatic second pass is starting, then check every in-scope K ID
and question/subpart against the final note. Use `assets/second-pass-template.md`, repair
omissions and non-responsive explanations, read the chapter continuously for prerequisite
gaps and broken transitions, try a consequential next step with its result covered,
and check similar questions against their distinct demands. Rebuild affected outputs. Explicitly deferred
reviews remain pending. Question checking does not require printing questions in the note.

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
For automatic second-pass configurations, `teaching_depth` and `second_pass` must also pass.
Remind the learner of the completed K/Q counts, corrections and unresolved items in delivery,
with a link to the private review companion. Keep that audit trail out of the note by default.

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
