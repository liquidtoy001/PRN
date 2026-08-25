# State and incremental builds

Use `study_state.json` for multi-chapter work. It is the machine-readable source of truth;
`progress.md` is a human-readable projection and must not silently disagree with it.

## State model

The template is `assets/study-state-template.json`. Important fields are:

- `mode`, `language`, `format`, assessment date, and study-time constraints;
- `materials_inventory` and its deterministic digest;
- an explicit assessment evidence boundary;
- chapters with statuses, selected source IDs, an `input_digest`, artifacts, and QA results;
- a capacity/quality-ceiling report and a per-generation usage ledger;
- links to active-learning banks, learner state, and staged-retest plans;
- the last completed action and agreed next action.

Allowed chapter statuses are `planned`, `drafting`, `verified`, `delivered`, `stale`, and
`blocked`. Use `verified` only after citation and reasoning checks. Use `delivered` only after
every requested artifact has passed its applicable checks.

Schema version 2 requires `capacity_disclosure=pass` and `usage_accounting=pass` for every new
verified/delivered generation. These values mean the report or ledger entry exists and its
accuracy is disclosed; they do not mean the context fit was good or the token count was exact.
Use `manage_state.py migrate` for a schema-version 1 file. Migrated historical chapters are
marked `legacy_generation` rather than retroactively inventing measurements.

## Commands

Initialise and validate state:

```text
python scripts/manage_state.py init --output output/study_state.json \
  --course-id COURSE --course-title "Course title" --mode lightweight \
  --language zh --format latex-pdf
python scripts/manage_state.py validate output/study_state.json
python scripts/manage_state.py migrate output/legacy-study_state.json
```

Update one chapter after observable work:

```text
python scripts/manage_state.py update-chapter output/study_state.json \
  --slug regression --title Regression --status verified \
  --input-digest <sha256> --source-id S002 --artifact output/regression.tex \
  --qa-citations pass --qa-reasoning pass \
  --qa-capacity-disclosure pass --qa-usage-accounting pass
```

Check whether an unchanged chapter can be reused:

```text
python scripts/manage_state.py needs-rebuild output/study_state.json \
  --slug regression --input-digest <sha256>
```

Exit code `0` means the recorded verified/delivered chapter can be reused; exit code `3`
means rebuild it.

## Computing an input digest

Hash the canonical combination of:

- selected source IDs and their current SHA-256 values;
- mode and output language;
- authoring template version or digest;
- chapter-specific learner preferences.

When the material inventory changes, do not automatically invalidate every chapter. Mark only
chapters whose selected sources or relevant configuration changed as `stale`. Rebuild into a
temporary output path and replace the delivered artifact only after validation succeeds.
