# Learning presets and first-use intake

A preset determines the teaching purpose. Use the active entry's configuration catalogue.

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

Use the learner's language. A read-only inventory may inform the suggested scope and exam basis.

1. Show **one card in the first reply about configuration**. In its purpose row, compare
   preview, knowledge and exam in one phrase each. Use all four tables from this entry's
   `configuration.md`, in order. Show **every row, all alternatives and its current value**
   including advanced and inactive settings. Mark values 已指定 / 已保存 / 推荐 / 依据资料 /
   本次不适用. For an inactive row, give its activation condition (e.g. answers open/closed
   applies when HTML self-test is enabled). Keep the full card visible in this message.
2. Highlight only the choices needing attention, usually purpose, scope, language and output.
   Use the catalogue's plain labels; keep storage keys internal. End with one invitation:
   “回复‘按推荐’，或一次告诉我想改的项。” A prior choice of preset fills that row only.
3. An explicit delegation or fully specified request lets work proceed after showing the
   resolved card. Otherwise wait for a reply. Ask together for any essential missing facts,
   such as the two time constraints for a sprint. Respect source-only restrictions when
   proposing enrichment. Automatic review proceeds after notifying the learner.

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
