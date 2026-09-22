# HTML configuration intake

Show the entire table in the learner's language, distinguish supplied/saved values from
recommendations, and ask once for unresolved settings. Do not draft while an unanswered
intake is outstanding unless the learner delegated choices. Save the complete object from
`assets/note-configuration.json` after confirmation, not merely the changed fields.

| Setting | Choices | Recommendation |
|---|---|---|
| Purpose | knowledge / exam | knowledge (知识巩固版) |
| Mode | lightweight / full / exam-cram | lightweight |
| Scope | selected files/pages / supplied materials in batches | honour the request |
| Depth | standard-detailed / extended | standard-detailed |
| Language | zh / en / bilingual | zh unless context indicates otherwise |
| Output | HTML folder (fixed for this entry) | offline folder, index.html plus assets |
| Reading width | standard / wide | standard |
| Density | comfortable / compact | comfortable |
| Theme | light / dark / auto | light |
| Self-test | none / folded-qa | none for knowledge; suggest folded-qa for exam |
| Initial answers | closed / open | closed when folded-qa is selected; otherwise not applicable |
| Paper enrichment | off / reading-list / integrated | reading-list |
| Time | date and available hours / none | none; both required for exam-cram |

Do not ask for A4/A5, print margins, LaTeX engine or PDF compilation. Folded questions are
not a separate export type. Knowledge plus folded-qa is valid only with explicit selection;
it adds a companion section, not question-shaped replacement prose. Full does not override
`self_test=none`. Existing source exercises stay explained even when self-test is disabled.
Do not invent mastery tracking, spaced repetition, Anki exports or their persistence; those
are not implemented by this HTML entry. Honour a narrower explicit request or explain a gap.

Lightweight delivers one representative chapter with complete within-scope coverage. Full
plans the course and proceeds by chapter with resumable state. Exam-cram requires a real
deadline and hours; agree a smaller scope and disclose omissions, not silent compression.
Knowledge plus exam-cram needs an agreed trade-off between scope and available time.

The HTML configuration has `schema_version=1`, `format=html`, and `preferences` containing
mode, language, date/hours and `note_configuration`. `confirmed=true` requires a user reply
or explicit delegation. `answers_initial=null` when self-test is none. Paper enrichment is
stored in `preferences.note_configuration.paper_enrichment` as in the shared evidence rules.
Never pass this configuration to the print entry's `manage_state.py` or merge states by name.
On resume, read saved configuration and ask only unresolved/changed choices. Imported PDF
preferences may be shown as candidates, never silently relabelled as confirmed HTML choices.
