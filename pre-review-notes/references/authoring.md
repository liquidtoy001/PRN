# Source-grounded authoring

## Language

Keep every deliverable in the confirmed main language, including headings, figure captions,
assessment summaries, the course map, and progress report. A bilingual document is different
from a monolingual document with occasional glosses.

For Chinese notes, introduce specialised or difficult terms as
`中文（English, acronym）`, then write naturally with stable Chinese terms or familiar acronyms.
Keep canonical English labels when needed for source/assessment recognition; do not replace
ordinary explanations with English phrases or implementation identifiers. Do not translate
equations, bibliographic titles or exact quoted wording merely for visual uniformity.

## Chapter structure

Apply `learning-presets.md` and the confirmed purpose in `configuration.md`. Preview builds
the prerequisite-to-lesson reading route; knowledge consolidation develops understanding;
exam revision adds assessment evidence and selected question applications. Additional practice
is opt-in for every preset. Retain source exercises as explained examples and omit inapplicable
template blocks.

For informative source figures and tables, follow `source-visuals.md`: reuse them where useful,
place them beside the explanation, and explain how to read them and reach the stated conclusion.

In a requested solution booklet, place each subpart beside its reasoning. Reflow text-heavy
stems and preserve the labels and values of any required figure. During print review, check
that a page turn has not separated a step from the only copy of its data. In a requested
practice copy, allow writing space proportional to the calculation or drawing.

Apply `coverage-and-depth.md` and `standalone-teaching.md` before using the template. Group
related ledger points into a connected explanation, rather than repeating a concept box per
K ID. Restore the actual prerequisites before first use and explain the relation to nearby
concepts. Choose worked applications to match the material and purpose. Retain
every exercise in the selected scope with a solution, a deferred solution locator, or an
explicit restriction for active graded work. Do not call deferred work fully explained.

For each concept, explain its purpose and intuition, formal content, notation and conditions,
then the steps or example needed to use it. A short factual remark need not become a full
essay. Add prerequisite bridges and justified derivations where slides skip reasoning.
Label original illustrative examples and supplementary explanations; do not attribute them
to the lecturer. External additions require their own sources when used. Do not expand into
unrelated advanced topics merely to increase length.
Use the teaching-depth criteria in coverage-and-depth.md before marking a K ID explained.
Bind plain-language synonyms to canonical course terminology. Compare mechanisms using a
shared minimal example and explain how a learner could reconstruct an essential diagram.

For mathematics, check dimensions, parameter domains, normalization, signs, equivalent
objective scaling, boundaries and tie cases. For diagrams, account for all regions and
transitions. Verify overlay page numbers against physical PDF pages. If a source is wrong,
preserve the locator and explain the discrepancy rather than copying or silently fixing it.
Record the actual independent calculation in `review.md`; a declaration of correctness is
not a calculation. Keep eligible terse assessed answers after complete explanations; apply
the question-type rules in exam-review.md instead of appending an English answer everywhere.
Apply include_code in note-presentation.md: a selected coding exercise teaches mechanisms
through prose, diagrams or trace tables unless visible code was explicitly requested.

Use `assets/template.tex` for quantitative material or
`assets/markdown-template.md` for prose-heavy material. Adapt the slots rather than forcing a
mathematical layout onto every discipline.

Start with the topic, then teach the selected material in a connected sequence. Explain
source problems where they advance the topic using as many steps as the reasoning needs.
For exam revision, select and justify problem types using the actual assessment evidence.
Place a sourced misconception beside the step it affects. Add a separate quick reference,
practice list or retest schedule only when requested. Include a source index or process
explanation only when its corresponding setting is enabled. See note-presentation.md.

The quality ceiling is not a generic "AI may be wrong" disclaimer. State which source IDs were
used and omitted, whether OCR or chunking limited coverage, whether exam weighting is
supported, whether official solutions calibrated answer depth, and the next material or check
that would improve the result. Keep this information in the review companion and delivery
message by default. Preserve content-specific qualifications in the teaching itself.

For prose fields, a worked derivation becomes a fully reasoned application to a real course
problem, case, passage, clinical vignette, or argument. Preserve the evidence structure even
when the visual form changes.

## Worked examples and official solutions

- Prefer the learner's own worksheet, assignment, sample-paper, or past-paper problem.
- Preserve the essential original wording privately when needed for practice, but avoid long
  third-party quotations in anything intended for public distribution.
- Solve independently first. Then compare with the official solution to calibrate notation,
  rewarded steps, and answer length.
- If the official answer appears wrong or outdated, show the independent check and flag the
  discrepancy; do not silently rewrite the source.
- Never pad a terse full-credit answer with unrelated theory.

## Claims and traps

A trap box requires evidence from instructor emphasis, an examiner report, repeated mistakes
the learner supplied, or a demonstrated pattern in assessed material. Generic subject-matter
advice may be labelled as general guidance, but it must not be disguised as a course-specific
warning.

Write `unknown` when the source set cannot support an exam claim. Sparse evidence can justify
a practice recommendation, but not a confident prediction.
