# Source-grounded authoring

## Language

Keep every deliverable in the confirmed main language, including headings, figure captions,
assessment summaries, the course map, and progress report. A bilingual document is different
from a monolingual document with occasional glosses.

For Chinese notes, introduce specialised or difficult terms as
`中文（English, acronym）`, then use the English name or acronym consistently. Prefer the
canonical English term when it is the clearer search, code, implementation, or assessment
term. Do not translate identifiers, equations, bibliographic titles, or quoted wording merely
for visual uniformity.

## Chapter structure

Apply the confirmed purpose in `configuration.md`. Knowledge consolidation has no generated
question sections by default; retain source exercises as explained examples. Exam revision
uses assessment evidence and the selected companions. Omit inapplicable template blocks.

For informative source figures and tables, follow `source-visuals.md`: reuse them where useful,
place them beside the explanation, and explain how to read them and reach the stated conclusion.

Apply `coverage-and-depth.md` before using the template. The template is expandable:
repeat concept blocks for all ledger points, not just a few headline topics. Two to four
worked problems is a starting guideline, never a cap that drops source exercises. Retain
every exercise in the selected scope with a solution, a deferred solution locator, or an
explicit restriction for active graded work. Do not call deferred work fully explained.

For each concept, explain its purpose and intuition, formal content, notation and conditions,
then the steps or example needed to use it. A short factual remark need not become a full
essay. Add prerequisite bridges and justified derivations where slides skip reasoning.
Label original illustrative examples and supplementary explanations; do not attribute them
to the lecturer. External additions require their own sources when used. Do not expand into
unrelated advanced topics merely to increase length.

For mathematics, check dimensions, parameter domains, normalization, signs, equivalent
objective scaling, boundaries and tie cases. For diagrams, account for all regions and
transitions. Verify overlay page numbers against physical PDF pages. If a source is wrong,
preserve the locator and explain the discrepancy rather than copying or silently fixing it.
Record the actual independent calculation in `review.md`; a declaration of correctness is
not a calculation. Keep terse assessed answers separate from explanatory teaching prose.

Use `assets/template.tex` for quantitative material or
`assets/markdown-template.md` for prose-heavy material. Adapt the slots rather than forcing a
mathematical layout onto every discipline.

Each chapter should contain, when supported by the sources:

1. a header with the evidence boundary, capacity status, concrete quality ceiling, and
   supported priority statement;
2. concept sections using the course's notation and framing;
3. complete solutions or derivations for two to four high-value real problem types;
4. sourced misconception or trap boxes;
5. a compact quick-reference card;
6. an assessment mapping table with stable source IDs and locators;
7. a short practice-next list.

The quality ceiling is not a generic "AI may be wrong" disclaimer. State which source IDs were
used and omitted, whether OCR or chunking limited coverage, whether exam weighting is
supported, whether official solutions calibrated answer depth, and the next material or check
that would improve the result.

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
