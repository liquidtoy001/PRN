# Learning presets and first-use intake

Read this before either format's configuration intake. A preset is the initial value of
`note_configuration.purpose`, not a third skill, a rendering format or a quality level.
Use the active entry's configuration catalogue; keep PDF and HTML settings separate.

## Three purposes

| Learner-facing preset | Stored purpose | Reading goal | Recommended paper enrichment | Additional practice |
|---|---|---|---|---|
| 课前预习 | preview | Prepare to follow the lesson: restore prerequisites, introduce its central problem and build intuition through small examples | off | none |
| 知识巩固 | knowledge | Understand and connect the supplied knowledge, including conditions, derivations and source examples | reading-list | none |
| 考试复习 | exam | Understand the selected knowledge and apply it to the supplied syllabus, checklist and actual assessment tasks | off | none; offer optional practice in the complete catalogue |

All three recommend `lightweight`, `standard-detailed`, the learner's language (Chinese when
no other context exists), comfortable layout and automatic second-pass review. Visible code,
source indexes and source/process explanations default to off. The print default is PDF/A4;
HTML defaults to standard width, light theme, `self_test=none`, `answers_initial=null`.
An already stated preference overrides these recommendations. A preset does not silently
enable a quiz, folded questions, flashcards, code or external reading.

Infer purpose from the request when clear: preparing for a first encounter suggests preview;
understanding or consolidating material suggests knowledge; preparing for an assessment
suggests exam. When unclear, recommend knowledge and make it editable. Merely supplying a
past paper or a programming lab does not determine purpose, practice or code preferences.

### Preview changes the teaching route, not the coverage requirement

Build the chapter around prerequisites -> the lesson's motivating problem -> core concepts
and a small running example -> how the ideas connect -> points to notice during the lesson.
Explain unfamiliar vocabulary before it carries an argument. State lesson watch-points as
brief observations, not a compulsory self-test or a new set of questions. If no slides are
available, name the narrower syllabus/reading boundary and do not invent the lecturer's content.

Recommend a concrete first chapter or page range when the learner has not chosen scope.
Within the agreed scope, retain distinct knowledge, source figures, conditions and worked
exercises at usable depth. Preview is not permission to mark unexamined details explained.
If the available time calls for only an orientation, agree that narrower scope and record
deferred material; do not call an overview complete coverage. Keep the same reasoning,
source, visual and continuous-reading checks as the other purposes.

Knowledge also defaults to no generated questions. Exam adds evidence-based organisation,
selected question explanations and answer-form rules from `exam-review.md`; an additional
practice bank is separate and optional. Source exercises remain explained examples in all
three, subject to active-assessment restrictions. Selecting exam does not select exam-cram.

## First interaction: one complete, grouped configuration card

Before asking the first configuration question for a new course/output setup, show all of
the following together in the learner's language. A quick read-only inventory may precede
the card so filenames and evidence-based suggestions are concrete.

1. A short comparison of the three presets and the selected/recommended one.
2. The active format's **entire** settings catalogue, grouped as core choices, learning
   options, format/presentation defaults and exam-specific settings. Each row shows the
   available alternatives and current value. Label values `已指定`, `已保存`, `推荐`,
   `依据资料` or `本次不适用` as appropriate; use equivalent labels in other languages.
3. One invitation to accept the displayed recommendations or change any rows together.
   For example: “可以回复‘用预习预设，其余按推荐’，也可以一次列出要改的设置。”

All settings must be visible in that first configuration exchange, including advanced and
currently inapplicable rows. Do not hide them behind an advanced-settings link, collapsed
section, another message or a prior preset-selection question. Inapplicable exam settings
still show their alternatives and state that they become active for exam purpose. HTML
answer-open/closed options remain visible when self-test is off, marked not applicable.
The list is comprehensive for the chosen entry, not a mixture of PDF and HTML controls.

Simplification means fewer decisions, not fewer visible settings. Focus the learner on
purpose, concrete scope, language and the entry's deliverable. Recommend or derive the rest.
Use plain labels: `先做一章 (lightweight)`, `分章完成课程 (full)`, `限时冲刺 (exam-cram)`;
`标准详细 / 扩展讲解`; `自动复核 / 本次暂缓复核`.
Keep implementation-only keys, validators, compiler choices and internal file formats out
of the user-facing card. The format-specific tables map those labels to stored values.

Do not re-ask supplied choices. If all values are specified or the learner delegated the
remaining choices, show the resolved card and continue without another confirmation.
Otherwise wait for the answer before substantive generation; an unanswered question is not
acceptance. Read-only inventory can continue. Only ask a follow-up for a genuinely unresolved
scope, missing required time budget or material conflict that cannot be resolved from files.

Selecting one preset alone is not acceptance of unseen options. If all alternatives and
defaults were already displayed, “use this preset, the rest as recommended” accepts them.
External enrichment follows its displayed, accepted setting and prior scope restrictions.
Automatic second-pass review is the normal workflow, not a new permission gate.

## Persistence and continuation

Save the purpose as `preview`, `knowledge` or `exam` in the existing configuration, together
with all resolved values. Do not introduce a separate preset field with competing semantics.
The shipped assets remain unconfirmed knowledge recommendations, not evidence of consent.
Set `confirmed=true` only after an actual reply or explicit delegation.

Priority is current explicit choices -> saved choices -> preset recommendations. On resume,
read the saved configuration, preserve customisation and ask only unresolved/changed items;
do not show the whole first-use questionnaire again unless requested. A purpose change alone
does not reset language, scope, code, practice or layout. Show proposed changes together if
the learner explicitly asks to reset to a preset's defaults. Existing knowledge/exam states
remain valid; never relabel past notes as preview or backfill quality passes.

Purpose and other content/layout changes must enter input digests and trigger the ordinary
affected-chapter rebuild/review rules. Purpose-independent quality checks always remain active.
