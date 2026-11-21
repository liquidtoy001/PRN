# v0.2.10 release validation

Date: 2026-09-22. Windows / Python 3.10. This report distinguishes executable checks from
browser acceptance and teaching effectiveness. No third-party slide files are included.

## Executed

- `python -m unittest discover -s tests/unit -v`: 28 tests passed (15 existing, 13 added).
- `python -m compileall -q pre-review-notes/scripts pre-review-notes-html/scripts shared/scripts tools tests/unit`: passed.
- Both Skill directories passed `quick_validate.py` with UTF-8 enabled.
- `python tools/sync_shared.py --check`: 13 shared resources per entry, zero drift.
- Both ZIPs were built twice in temporary directories and compared byte-for-byte.
- The HTML ZIP was extracted into an isolated directory with no sibling or shared source tree;
  its actual CLI successfully built the original HTML fixture and copied the referenced image.
- Automated checks cover initial answer states, no-question full/knowledge mode, invalid/mixed
  configuration rejection, per-answer citations, missing/remote/escaping assets, active SVG,
  duplicate IDs, unbalanced markup, bad anchors, existing-output preservation and honest QA flags.
- Shared-resource drift blocks packaging without silently repairing the edited copy.
- Print-only `--study-state` flags fail before writes in HTML; standalone capacity/usage still run.
- Legitimate `Example 3.2`/Chinese example locators pass; unresolved TODO/TBD/unknown slots fail.
- Absolute and parent-escaping inventory paths fail `--materials-root`; packaging rejects an
  output directory inside either skill or shared sources before writing anything.

The project-authored fixture at `tests/fixtures/html/` includes Chinese, a MathML fraction,
an SVG with labels, a table, long code, source anchors and two optional questions. Its
`configuration.json` explicitly enables questions for this engineering fixture; it is not the
new-user default. Its content is not a real course or a cross-domain evaluation.

Reproduce a build into a fresh directory:

```powershell
python pre-review-notes-html/scripts/build_html.py --content tests/fixtures/html/chapter.html --configuration tests/fixtures/html/configuration.json --inventory tests/fixtures/html/inventory.json --title "HTML acceptance fixture" --output-dir dist/html-acceptance-001
```

## Independent forward test

A separate agent read the HTML skill for a realistic Chinese, lightweight, knowledge-mode
request with missing configuration and papers disabled. It showed a bundled intake, retained
explicit choices on continuation and did not generate questions by default. This was a
read-only simulation, not a real material-to-note execution. It found that optional shared
state flags depended on the absent print helper. The flags now reject that path before any
write, with a regression test and explicit HTML state-maintenance instructions.

A separate read-only code review reproduced locator false positives, material-root escape and
in-skill packaging contamination. All three were fixed and covered by executable regressions.
Its documentation-link finding was resolved by adding this report before publication.

## Not completed

The available browser tool rejected local-file navigation under its URL security policy.
No alternate browser, server or automation route was used to circumvent the block. Therefore
desktop/phone visual layout, actual keyboard interaction, JavaScript-disabled behavior,
network-disabled rendering, MathML appearance and per-figure final browser review are pending.
Native HTML structure and local dependency checks support a narrower claim, not browser QA.
The generated build report correctly leaves browser and semantic review pending.

The print template/compiler was not changed and was not recompiled in this release; existing
state/QA regressions passed. Neither this release nor its tests prove exhaustive knowledge
coverage, cross-domain correctness, learning gains or browser compatibility in all targets.

## Maintainer workflow

Edit canonical shared files in `shared/`, run `python tools/sync_shared.py`, inspect the
resulting copies and rerun tests. The copies are intentionally committed so both repository
directories and release ZIPs are independently installable. Do not edit generated copies alone.
Format-specific citation syntax, length diagnostics and visual layout live only in each entry.
