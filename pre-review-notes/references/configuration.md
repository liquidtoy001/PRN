# Configuration intake (0.2.8)

## Ask once, then persist

Before drafting, inspect the request and any existing study state. Show this complete list
in the learner's language, marking values supplied by the learner as fixed and other values
as recommendations. Ask one bundled question covering unresolved choices. The user can
accept recommendations in one sentence or change specific rows. Do not ask ten serial
questions. Read-only inventory may proceed while awaiting the answer; substantive generation
waits for the response unless the user already delegated configuration choices. An unanswered
prompt is not confirmation. Skip redundant confirmation when all choices are known.

| Setting | Choices | Initial recommendation |
|---|---|---|
| Purpose | 知识巩固版 / 考试复习版 | knowledge |
| Mode | lightweight / full / exam-cram | lightweight |
| Source scope | all supplied / named files or page ranges | requested scope; otherwise all supplied in batches |
| Explanation depth | standard detailed / extended | standard detailed |
| Paper enrichment | 关闭 (off) / 推荐阅读 (reading-list) / 整合讲解 (integrated) | reading-list |
| Language | Chinese / English / bilingual | Chinese unless context indicates otherwise |
| Deliverables | PDF / Markdown / LaTeX / any combination | PDF |
| Page size | A4 / A5 / custom dimensions | A4; not applicable to Markdown-only |
| Layout density | comfortable / compact | comfortable |
| Companions | none / quiz / flashcards / both | none for knowledge; quiz suggested for exam |
| Time constraints | deadline and available study hours / none | none; ask for realistic time if exam-cram selected |

Explain that page count follows substantive content, and density/depth never permits silent
omission. Custom dimensions need explicit units. Do not invent a deadline or budget.

## Purpose behavior

Knowledge consolidation prioritises complete source extraction, small conditions, figures,
intuition, derivations, prerequisite bridges and proportionate expansion. Generate no new
self-tests, quizzes, question sections or flashcards unless explicitly requested, even in
full mode. Existing slide examples and exercises still contain knowledge: explain them as
worked examples, subject to active-assessment restrictions, rather than omitting them or
forcing an interactive quiz. Suggested next reading is allowed.

Exam revision retains coverage within the selected scope and adds evidence-backed assessment
mapping, solution methods, conditions and practice. Companion suggestions are not mandatory.
Without assessment sources, label priorities lecture-driven and exam frequency unknown.
Exam purpose does not imply exam-cram; time pressure is a separate choice. If knowledge plus
exam-cram is selected, explain the tension between exhaustive expansion and time triage and
resolve the intended scope before drafting, without silently changing either preference.

## State and continuation

Paper enrichment is independent of purpose, mode and depth. Both knowledge and exam notes
can use any setting. Read `paper-enrichment.md` before research/drafting when enabled.
Save `paper_enrichment` in note_configuration. For older state missing this key, ask only
about this unresolved preference; do not interpret its absence as permission for research.
Existing states without the key remain valid. Include its resolved value in input digests.

Persist the complete resolved intake in `preferences.note_configuration` using the object
shown in `assets/note-configuration.json`. Populate actual values; the asset is a recommendation,
not evidence of confirmation. `confirmed` becomes true only after a user response or explicit
delegation. Top-level mode/language/format/learning_outputs/date/hours remain the existing
fields; the nested configuration supplies purpose, scope, depth, exact deliverables and layout.

Use `manage_state.py init --note-configuration <resolved-json>` alongside existing flags.
For existing state, merge the configuration into preferences with a file edit and validate;
preserve all chapters and measurements. Do not reinitialise existing state. If legacy state
has no configuration, keep it valid and ask only for missing choices, without inventing past
confirmation. Include all content/layout preferences in chapter input digests.

For compatibility, choose top-level format `latex-pdf` for PDF with or without LaTeX,
`markdown-pdf` for Markdown plus PDF without LaTeX, `latex` for LaTeX without PDF, and
`markdown` for Markdown alone. The deliverables list is the authoritative delivery set,
including combinations the legacy format enum cannot express. PDF-only delivery may retain
internal build sources, but need not present them to the user.
