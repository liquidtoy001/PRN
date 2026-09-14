# Active learning and staged retesting

Respect `configuration.md` first: knowledge consolidation and an explicit `none` companion
choice suppress automatic question/bank generation in every mode. Existing source exercises
may still be explained as examples. Never infer a quiz request merely from full mode.

Use this workflow when the learner requests flashcards or quizzes, or when `full` or
`exam-cram` mode includes active-learning outputs. Notes remain the source-grounded teaching
artifact; a learning bank is a separate, machine-checkable practice layer.

## Build a learning bank only from verified chapter content

Start from `assets/learning-bank-template.json`. Each item needs:

- a stable item ID and one of `flashcard`, `multiple-choice`, `short-answer`, or
  `worked-problem`;
- a prompt that does not reveal the answer;
- an answer and concise rationale;
- at least one stable source ID with a precise locator;
- a difficulty and realistic answer time;
- `assessment_weight` only when `priority_evidence` directly supports that value.

Do not turn a generic textbook fact into a course-specific exam claim. Distractors should
represent sourced or observed misconceptions when possible; label generic diagnostic
distractors as general guidance. Avoid long copyrighted question reproduction in any public
export.

Validate before use:

```text
python scripts/manage_learning.py validate-bank output/learning-bank.json \
  --inventory output/materials.json
```

## Record attempts, confidence, and mistakes

Initialise a local learner state, then record every attempted item. Confidence is 1–5 and is
recorded before answer feedback where the interface allows it.

```text
python scripts/manage_learning.py init --bank output/learning-bank.json \
  --output output/learning_state.json --assessment-date 2026-11-10
python scripts/manage_learning.py record-attempt --bank output/learning-bank.json \
  --state output/learning_state.json --item-id regression-Q001 \
  --correct no --confidence 5 --mistake-tag sign-error
```

The deterministic scheduler gives wrong answers a next-day retest, expands intervals after
consecutive correct answers, and penalises high-confidence errors in the mastery estimate.
Mastery is a scheduling signal over recent attempts, not proof that the learner will answer a
novel exam question correctly.

## Reprioritise against the assessment date

Generate a time-bounded plan from due state, mastery gap, error history, answer time, and only
explicit assessment evidence:

```text
python scripts/manage_learning.py plan --bank output/learning-bank.json \
  --state output/learning_state.json --available-minutes 45 \
  --output output/retest-plan.json
```

Near the assessment date, explicitly evidenced items receive more weight. Items without an
assessment source are labelled `learning priority; exam relevance unknown`; the score is not
an exam-probability forecast. Always deliver the plan's uncovered list so a short time budget
is not mistaken for complete preparation.

## Export

```text
python scripts/manage_learning.py export --bank output/learning-bank.json \
  --format csv --output output/learning-bank.csv
python scripts/manage_learning.py export --bank output/learning-bank.json \
  --format anki --output output/learning-bank-anki.tsv
```

Anki output is a three-column UTF-8 TSV: front, back, and tags. Exported answers include the
source locator. Keep learner attempts and confidence data local unless the learner explicitly
asks to publish them.
