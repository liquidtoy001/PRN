# Configuration intake

Read [learning-presets.md](learning-presets.md) for the three presets, their defaults and
the first-use conversation. Show the preset comparison and **all four groups below in the
same first configuration exchange**, with alternatives, resolved values and their status.
Only the core choices normally need attention; the other groups stay visible and editable.
Do not hide advanced or exam-only rows. Ask once for unresolved choices, not once per group.

## Core choices

| Setting | Choices | Recommendation |
|---|---|---|
| Purpose preset | 课前预习 / 知识巩固 / 考试复习 | infer the request; otherwise knowledge |
| Source scope | named files/pages / supplied materials in batches | honour the request; otherwise suggest a concrete first chapter |
| Language | Chinese / English / bilingual | Chinese unless context indicates otherwise |
| Deliverables | PDF / Markdown / LaTeX / any combination | PDF |

## Learning options

| Setting | Choices | Recommendation |
|---|---|---|
| Work scope and pace | 先做一章 / 分章完成课程 / 限时冲刺 | first chapter (lightweight) |
| Explanation depth | 标准详细 / 扩展讲解 | standard detailed; neither omits selected knowledge |
| Paper enrichment | 关闭 / 推荐阅读 / 整合讲解 | off for preview/exam; reading-list for knowledge |
| Additional practice | none / quiz / flashcards / both | none in all presets; source exercises still explained |
| Time constraints | deadline and available study hours / none | none; actual date and hours required for exam-cram |

## Format and presentation defaults

| Setting | Choices | Recommendation |
|---|---|---|
| Page size | A4 / A5 / custom dimensions | A4; not applicable to Markdown-only |
| Layout density | comfortable / compact | comfortable |
| Visible code in notes | off / explicitly requested code | off; lab knowledge is still explained |
| Source index in notes | off / on | off |
| Source/process explanations in notes | off / on | off; disclose limitations in the delivery message |
| Second-pass review | 自动复核 / 本次暂缓复核 | automatic after drafting, with a notification |

## Exam-specific settings (show even when not applicable)

| Setting | Choices | Recommendation |
|---|---|---|
| Organisation and basis | follow supplied exam/syllabus/checklist structure / topic chapters | derive from inspected evidence; not applicable to preview/knowledge |
| Answer language | Chinese / English / bilingual / same as notes | verified instructions or learner preference; not applicable to preview/knowledge |

Explain that page count follows substantive content, and density/depth never permits silent
omission. Custom dimensions need explicit units. Do not invent a deadline or budget. For
Markdown-only, still show page size and density with their alternatives, marked not applicable.

## Applying the resolved preset

Use the purpose behaviour and precedence rules in `learning-presets.md`. `preview` and
`knowledge` organise teaching by prerequisite-aware topics; `exam` adds the course-specific
evidence workflow. All retain source examples and continuous explanations. Full and exam-cram
never turn an additional practice choice of none into a quiz or bank.

Map learner labels to existing fields: purpose `preview/knowledge/exam`; mode
`lightweight/full/exam-cram`; depth `standard-detailed/extended`; paper enrichment
`off/reading-list/integrated`; second pass `automatic/on-request`. Keep other existing enums.
Persist same-as-notes answer language as null. Do not expose these storage keys as additional
questions. If preview or knowledge is paired with exam-cram, agree what fits the actual time
and explicitly defer other scope rather than dropping details from every concept.

For exam purpose, read `exam-review.md`. Save `exam_organisation`, verified
`exam_basis_source_ids` and `exam_answer_language`; empty/null values mean unavailable or
not applicable, never fabricated exam facts. Present the derived course-specific choices
together in the first card where evidence is available. A syllabus or checklist is sufficient
when no paper exists; lectures alone cannot establish exam frequency. For a new non-exam
configuration retain storage defaults source-led / [] / null while marking these rows not
applicable. Preserve saved choices when switching purpose. A course-material-only request
resolves paper enrichment to off.

The default body is a standalone explanation with prerequisite bridges and connected prose;
see `standalone-teaching.md`. Depth is not a choice between readable and fragmented notes.
Describe the answer-language choice as applying to useful prose responses (definition,
explanation, comparison, justification), not translations after calculations and choice items.
Persist `include_code` as a boolean; see `note-presentation.md`. A coding source or extended
depth does not imply true. Missing include_code in legacy configurations defaults to false
for the next requested generation; preserve an explicit prior code request and leave old
artifacts/history intact. Include the resolved choice in content digests.

Read `note-presentation.md` for the two `show_source_*` booleans. The automatic second pass
is an execution default, not a separate consent gate. Read `second-pass-review.md`, announce
it after the draft, and continue. An explicit request to defer sets `second_pass_review` to
`on-request`; keep the output labelled as a draft awaiting that review.

## State and continuation

Paper enrichment can be customised independently of any preset, mode and depth. All three
purposes can use any setting. Read `paper-enrichment.md` before research/drafting when enabled.
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
Deliverables constrain the learner-facing notes. A request for "Markdown only" still uses
native JSON inventory/configuration/study state and JSONL usage records internally. Preserve
the tools' file formats and ordinary CLI entry points; do not wrap state in Markdown or
replace tool I/O to satisfy a note-format choice. If a user explicitly forbids internal file
types, explain the resulting persistence limitation rather than inventing compatible state.

Older configurations remain valid. On the next requested generation, resolve and persist
missing review/presentation preferences using these defaults while retaining explicit prior
choices. Do not backfill past semantic passes. Content/presentation changes invalidate the
affected chapter digest and require a new review. The state CLI accepts
`--qa-teaching-depth` and `--qa-second-pass`; they record observed review results only.
Each new/rebuilt chapter records its `second_pass_review` policy. A changed input digest resets
the two new QA results to pending. Existing delivered chapters retain their historical policy
until requested regeneration; missing review metadata never means they passed the new checks.
