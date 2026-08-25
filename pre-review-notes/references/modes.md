# Operating modes

Select the smallest mode that satisfies the learner's goal. A mode controls scope and time;
it never relaxes citation, uncertainty, privacy, or verification rules.

| Mode | Choose when | Required output | Deliberately omitted |
|---|---|---|---|
| `lightweight` | The learner wants one chapter, is evaluating the skill, or has slides but little assessment evidence. | Material inventory, capacity/quality boundary, provisional topic map, one representative chapter, and token record. Active-learning output only when requested. | Whole-course coverage, calendar, and exhaustive cross-assessment analysis. |
| `full` | Several source categories and enough time are available for a maintainable course set. | Complete assessment map, topic plan, resumable state, chapter loop, citation validation, flashcard/quiz bank, learner state, token ledger, and requested compiled artifacts. | Nothing required by the agreed scope, but chapters are still delivered incrementally. |
| `exam-cram` | The assessment is close and the learner provides a deadline or time budget. | Evidence-ranked triage plan, highest-yield chapters/cards, timed quiz/retest plan, explicit uncovered-risk list, token ledger, and a final review block. | Low-value completeness and decorative outputs that consume the remaining study time. |

## Selection rules

- Default to `lightweight` for an initial trial or slides-only source set.
- Recommend `full` only when the learner wants sustained multi-chapter work and source access
  is sufficient.
- Use `exam-cram` only with a known deadline and realistic available time. Do not invent
  study hours or imply that omitted material is safe.
- Run the capacity gate in every mode. A mode changes scope, not the obligation to disclose
  unreadable, unprocessed, or out-of-context materials.
- If the learner explicitly chooses a mode, follow it unless a missing prerequisite makes the
  requested result impossible; explain the consequence rather than silently switching modes.

## Mode-specific planning

### Lightweight

Inventory all supplied files, but deeply inspect only the sources needed for the chosen
chapter. Produce a short source-coverage table. If assessment evidence is absent, call the
output `source-grounded course notes`, not `exam-calibrated notes`. Do not create a learning
bank unless the learner asks for it.

### Full

Inspect all assessment-bearing sources before fixing the chapter order. Initialise
`study_state.json`, compute an inventory digest, and use per-chapter input digests so unchanged
chapters are not regenerated. Stop after the first completed chapter for learner feedback
unless the learner explicitly requested a larger batch. Produce a validated learning bank and
initial learner state for the delivered chapter unless the learner opts out.

### Exam-cram

Allocate time by supported assessment value, prerequisites, learner weakness, and practice
cost. Each selected topic must have a next action: read a card, redo a named problem, or check
a named misconception. Build a time-bounded retest plan from mastery and due state. Finish
with an explicit `not covered` list. Never turn a sparse past-paper sample or a scheduler score
into confident probability predictions.
