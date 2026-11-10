# HTML configuration intake

Read [learning-presets.md](learning-presets.md). Show the three presets and **all four groups
below in the same first configuration exchange**, in the learner's language. Include every
row's alternatives, resolved value and status, even when not applicable. Recommend the
non-core settings so one reply can accept or adjust them; do not hide an advanced section or
ask for a preset before displaying the rest. Preserve supplied/saved choices. Save the complete
object from `assets/note-configuration.json` after confirmation, not merely changed fields.

## Core choices

| Setting | Choices | Recommendation |
|---|---|---|
| Purpose preset | 课前预习 / 知识巩固 / 考试复习 | infer the request; otherwise knowledge |
| Scope | selected files/pages / supplied materials in batches | honour the request; otherwise suggest a concrete first chapter |
| Language | zh / en / bilingual | zh unless context indicates otherwise |
| Output | HTML folder (fixed for this entry) | offline folder, index.html plus assets |

## Learning options

| Setting | Choices | Recommendation |
|---|---|---|
| Work scope and pace | 先做一章 / 分章完成课程 / 限时冲刺 | first chapter (lightweight) |
| Depth | 标准详细 / 扩展讲解 | standard-detailed; complete within the selected scope |
| Paper enrichment | 关闭 / 推荐阅读 / 整合讲解 | off for preview/exam; reading-list for knowledge |
| Additional self-test | none / folded questions and answers | none in all presets; source examples stay visible |
| Initial answers | closed / open | closed when self-test selected; otherwise not applicable (null) |
| Time | date and available hours / none | none; both required for exam-cram |

## Format and presentation defaults

| Setting | Choices | Recommendation |
|---|---|---|
| Reading width | standard / wide | standard |
| Density | comfortable / compact | comfortable |
| Theme | light / dark / auto | light |
| Visible code | off / explicitly requested code | off; source mechanisms remain explained |
| Source index | off / on | off |
| Source/process explanations | off / on | off; limitations go in the delivery message |
| Second-pass review | 自动复核 / 本次暂缓复核 | automatic after drafting, with a notification |

## Exam-specific settings (show even when not applicable)

| Setting | Choices | Recommendation |
|---|---|---|
| Organisation and basis | follow supplied exam/syllabus/checklist structure / topic chapters | derive from inspected evidence; not applicable to preview/knowledge |
| Answer language | Chinese / English / bilingual / same as notes | verified instructions or learner preference; not applicable to preview/knowledge |

## Applying the resolved preset

Use `learning-presets.md` for purpose behaviour, first-use confirmation and continuation.
Map purpose to `preview/knowledge/exam`, pace to `lightweight/full/exam-cram`, depth to
`standard-detailed/extended`, paper to `off/reading-list/integrated`, self-test to
`none/folded-qa`, and review to `automatic/on-request`. Keep storage keys out of the card.
For same-as-notes answer language store null. On a new non-exam setup, keep source-led / [] /
null for the inactive exam fields, and preserve saved custom values when purpose changes.

Do not ask for A4/A5, print margins, LaTeX engine or PDF compilation. Folded questions are
not a separate export type. All presets can add folded-qa through an explicit selection;
it adds a companion section, not question-shaped replacement prose. Full does not override
`self_test=none`. Existing source exercises stay explained even when self-test is disabled.
Do not invent mastery tracking, spaced repetition, Anki exports or their persistence; those
are not implemented by this HTML entry. Honour a narrower explicit request or explain a gap.

Lightweight delivers one representative chapter with complete within-scope coverage. Full
plans the course and proceeds by chapter with resumable state. Exam-cram requires a real
deadline and hours; agree a smaller scope and disclose omissions, not silent compression.
Preview or knowledge plus exam-cram needs an agreed trade-off between scope and available time.

Ordinary notes default to standalone reading, with local prerequisite bridges and connected
sections; follow `standalone-teaching.md`. Explain that answer-language snippets are selected
by the requested response type, not added to every calculation or choice item. Persist the
boolean `include_code` from note-presentation.md. Missing keys in older configurations mean
false for new generation; retain explicit prior code requests and old artifacts/history.

The HTML configuration has `schema_version=1`, `format=html`, and `preferences` containing
mode, language, date/hours and `note_configuration`. `confirmed=true` requires a user reply
or explicit delegation. `answers_initial=null` when self-test is none. Paper enrichment is
stored in `preferences.note_configuration.paper_enrichment` as in the shared evidence rules.
Never pass this configuration to the print entry's `manage_state.py` or merge states by name.
On resume, read saved configuration and ask only unresolved/changed choices. Imported PDF
preferences may be shown as candidates, never silently relabelled as confirmed HTML choices.
The output choice describes learner-facing notes; internal inventory/configuration/review
data retain their documented native formats. Use the included CLI interfaces without I/O
wrappers that change state encodings or claim unsupported continuation compatibility.

Read `exam-review.md` to set `exam_organisation`, `exam_basis_source_ids` and
`exam_answer_language` from actual evidence. Read `note-presentation.md` for the two
`show_source_*` booleans and `second-pass-review.md` for automatic review. The builder accepts
these optional fields in schema 1. Legacy files remain valid; apply the new defaults to the
next requested generation and retain explicitly saved choices. Missing keys do not certify
an earlier review. Content/configuration changes require renewed artifact-bound checks.
