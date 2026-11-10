# Work pace and scope

Apply `learning-presets.md` and the confirmed configuration first. Purpose controls the
teaching route; mode controls scope and time. Neither relaxes depth, citation, uncertainty,
privacy or verification. Present the plain labels below, keeping the stored values compatible.

| Learner label (stored mode) | Choose when | Required output | Scope boundary |
|---|---|---|---|
| 先做一章 (`lightweight`) | A first trial or one bounded chapter is wanted. | Material inventory, capacity/quality boundary, provisional topic route, one complete chapter, review and token record. | No claim of whole-course coverage. |
| 分章完成课程 (`full`) | The learner wants a maintainable multi-chapter set and sources are available. | Course topic plan for the selected purpose, resumable state, chapter loop, citation validation, reviews, usage ledger and requested artifacts. | Deliver incrementally; disclose sources or chapters still pending. |
| 限时冲刺 (`exam-cram`) | The learner provides a deadline and available study time and accepts a narrower scope. | Supported priorities, a bounded reading/action plan, complete teaching within selected topics, deferred-topic list, review and usage ledger. | Explicitly identify omitted scope; do not imply that it is safe to skip. |

## Selection rules

- All purposes and modes default to no additional practice. Generate a bank, quiz or cards
  only when selected in the confirmed configuration. Preserve original course exercises as
  explained examples; their presence is not consent to generate more questions.

- Default to `lightweight` for an initial trial or slides-only source set.
- Recommend `full` only when the learner wants sustained multi-chapter work and source access
  is sufficient.
- Use `exam-cram` only with a known deadline and available study time. Ask for a realistic
  study budget if allocating hours would otherwise require guessing. Preview and knowledge can
  also be time-limited; use their reading goals without inventing assessment priorities.
- Run the capacity gate in every mode. A mode changes scope, not the obligation to disclose
  unreadable, unprocessed, or out-of-context materials.
- If the learner explicitly chooses a mode, follow it unless a missing prerequisite makes the
  requested result impossible; explain the consequence rather than silently switching modes.

## Mode-specific planning

### Lightweight

This is a small-batch teaching mode, not a compression mode. Within the selected pages,
preserve all distinct knowledge points and explain them at a usable learning depth. Split
large selections into smaller chapters rather than shortening every concept to a sentence.
Read `coverage-and-depth.md`; produce a coverage ledger and review record for each batch.
An explicit request for a concise cheat sheet overrides the default teaching format, but
must disclose omissions and must not claim to replace complete notes.

Inventory all supplied files, but deeply inspect only the sources needed for the chosen
chapter. Keep the source-coverage table in the coverage companion by default. If assessment evidence is absent, call the
output `source-grounded course notes`, not `exam-calibrated notes`. Do not create a learning
bank unless the learner asks for it.

### Full

Plan the course sequence and prerequisites for preview/knowledge. For exam purpose, inspect
the supplied assessment-bearing sources before fixing the evidence-based chapter order;
follow `exam-review.md` when evidence is missing. Initialise
`study_state.json`, compute an inventory digest, and use per-chapter input digests so unchanged
chapters are not regenerated. Stop after the first completed chapter for learner feedback
unless the learner explicitly requested a larger batch. Produce a validated learning bank
and learner state only when additional practice was selected.

### Exam-cram

Allocate time by the selected purpose, prerequisites, observed gaps and realistic reading
cost. For exam purpose, use supported assessment value too. Each selected topic needs a
concrete next action such as reading a named explanation or tracing a source example. Add
practice/retests only when selected, and use actual attempt history rather than invented
mastery or due state. Finish with an explicit `not covered` list. Narrow the agreed scope
instead of reducing every concept to a sentence. Never turn a sparse past-paper sample or a
scheduler score into confident probability predictions.
