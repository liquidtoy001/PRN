# v0.3.0 validation

Local preparation was completed on 2026-11-10. This record separates engineering checks,
artifact inspection and learning-effectiveness evidence. The results below describe that
preparation run. Publication details and CI evidence for the published revision are recorded
on the [v0.3.0 Release](https://github.com/liquidtoy001/PRN/releases/tag/v0.3.0).

## Release scope

Both independently installable entries are version 0.3.0. The release includes the previously
unreleased teaching, exam-review and presentation improvements as well as the three-purpose
intake. Source material, private course outputs and local review records are excluded.

## Local preparation run

Environment: Windows, Python 3.10. The following checks were executed for the prepared 0.3.0
runtime. Remote CI had not run for that revision at the time of local preparation; it is a
separate publication check, linked from the Release.

- **37 unit/CLI tests passed.** The new release regression verifies that disabled or missing
  `include_code` rejects HTML pre/code before output, while an explicit true value builds.
  Earlier 36-test runs did not check this gap. The original HTML rendering fixture now opts
  into code deliberately; changing the fixture was not used to skip the new failure test.
- Both installable folders passed the external skill validator with UTF-8 enabled.
- Python compilation passed. Shared resources: **20 per entry, zero differences**.
- Packages were built from a `git -c core.autocrlf=false archive` export of the explicitly staged source, using
  canonical Git bytes instead of platform-specific working-copy line endings. Each package
  was built twice with identical bytes; every archive member matched the raw Git index blob.
  An earlier export inherited Windows autocrlf and failed this byte comparison. The final
  export explicitly disables that conversion, and both packages were rebuilt and rechecked.
- Both ZIPs are flattened, contain the expected VERSION/SKILL metadata and LICENSE, and
  exclude tests, private materials, generated PDFs, caches and local review files.
- The print package was extracted into a directory without its sibling/shared tree. Its
  real CLI saved and validated preview configuration, with extra learning outputs empty.
- The HTML package was extracted separately and built three original fixtures: knowledge /
  light / closed answers, exam / dark / open answers, and preview / no self-test. The outputs
  report version 0.3.0 and question counts 2, 2 and 0. Code and source-display settings were
  off for these three fixtures; their HTML, local image and citation checks passed.
- The publication heuristic scan covered **144 indexed paths and 184 historical blobs**:
  no matched credential/personal-path findings or broken local Markdown links. Its two
  historical PDF paths are the pre-existing published examples, not added source slides.
  `LOCAL-REVIEW.md` and the generated validation files stay ignored. This is a limited
  heuristic scan, not a comprehensive security or licensing certification.

## PDF smoke inspection

Two one-page, project-authored fixtures used the packaged template's preamble/macros, with
XeLaTeX and a locally available Chinese font. The source-index and source-explanation switches
were tested both off and on. Both compiled and passed structural traversal; extracted text
confirmed that the conditional sections appeared only when enabled.

Both complete pages were rendered and visually inspected. Chinese paragraphs, the equation,
condition table, chart labels and caption were readable, with no observed clipping or overlap.
After the canonical-byte rebuild, the final package compiled both fixtures again; the final
rendered PNGs matched the inspected pages byte-for-byte, and the text-switch checks passed again.
These small fixtures test rendering and switches, not a full course or extracted slide figures.
The build logs retain everypage compatibility and xeCJK monospace-family fallback warnings;
this is not a warning-free compilation claim.

## HTML browser acceptance remains pending

An attempt to open the generated local HTML in the browser tool was rejected by its URL
security policy: file URLs are not allowed. No server, alternate browser or automation route
was used to bypass that rejection. Therefore actual wide/narrow viewport appearance, keyboard
folding, browser MathML rendering and network-/JavaScript-disabled behavior remain unverified
for these artifacts. Static/CLI success is not a browser pass. Review the generated pages
manually before claiming browser acceptance.

## Prepared artifacts

| Package | Size (bytes) | Archive members | SHA-256 |
|---|---:|---:|---|
| pre-review-notes-v0.3.0.zip | 111340 | 44 | `78943ffa4ad159617ac821298cb09f5f35539b7684a4a0b6f7fd744d319ddabf` |
| pre-review-notes-html-v0.3.0.zip | 77868 | 36 | `7d9cd236a2498d7e647e96c9b8806c8717deb70f1e50f78d37e7526afcb6d14a` |

ZIPs and their individual `.zip.sha256` files are under ignored `dist/v0.3.0/`. Detailed local
build reports, extracted copies and rendering evidence are under `dist/v0.3.0-qa/`. The first
HTML candidate preceded the code-markup repair, and the next pair inherited CRLF conversion.
Both sets are superseded; their evidence is retained separately from
`package-verification-canonical.json` and `canonical-runtime-checks.json`. Existing published
v0.2.10 assets were not changed.

## Reproduction

From the repository root:

```text
python tools/sync_shared.py --check
python -m unittest discover -s tests/unit -v
python -m compileall -q pre-review-notes/scripts pre-review-notes-html/scripts shared/scripts tools tests/unit
python tools/package_skill.py --output-dir dist/v0.3.0
python tools/package_skill.py --skill-dir pre-review-notes-html --output-dir dist/v0.3.0
python tools/audit_publication.py --report dist/v0.3.0/publication-audit.json
```

Both skill folders also require the host's `skill-creator/scripts/quick_validate.py` with
UTF-8 enabled. This external validator is not bundled into the release.
For the exact release bytes, export the reviewed Git revision with
`git -c core.autocrlf=false archive` first and run the package
commands inside that export; a working copy with different line endings may produce different
ZIP bytes. Reverify package members against the final commit before attaching release assets.

## Evidence boundaries

- The three conversation examples in the maintainer chat were authored simulations, not
  independent model runs or fresh real-user tests.
- Earlier local teaching trials informed the changes and exposed errors that were repaired.
  Their private source files and output PDFs are not release fixtures, and their results
  are not presented as a clean v0.2.10-versus-v0.3.0 experiment.
- Unit tests exercise real CLI/state/build behavior, not prompt-wording matches. They cannot
  prove semantic coverage, connected teaching, accurate exam weighting or better exam scores.
- Exact-file duplicate groups identify identical bytes only. Scans and reformatted papers
  require full-content and provenance review before counting exam recurrence.
- Semantic and browser QA fields remain pending after a builder succeeds. They require
  actual review of the corresponding artifact; historical missing checks stay missing.
- Cross-platform CI for this release commit, systematic cross-discipline trials and learning
  gains are not established by a local Windows run.

The previous [v0.2.10 validation record](TESTING-0.2.10.md) is retained unchanged as historical
evidence, including its browser-access failure and pending checks.
