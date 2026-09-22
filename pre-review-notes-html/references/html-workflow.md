# Offline HTML build and handoff

Keep the authored body fragment and its `assets/` in a local chapter source directory. Reuse
`assets/chapter-fragment.html` structurally; do not ship its sample content as a real chapter.
The bundled builder accepts a restricted, non-executable HTML/MathML fragment. It escapes
titles/navigation and rejects scripts, event handlers, inline CSS, embedded documents,
remote assets, missing images, escaping paths, duplicate IDs and broken local anchors.
This is a controlled authoring subset, not a general-purpose hostile-HTML sanitizer.

```text
python scripts/build_html.py --content <chapter-body.html> \
  --configuration <confirmed-html-configuration.json> --inventory <materials.json> \
  --title <chapter-title> --output-dir output/html/chapter-01/build-001
```

Use a new nonexistent output directory per build; the helper refuses existing paths
to prevent overwriting a print artifact or stale assets. It emits index.html (inline CSS and
optional progressive-enhancement JS), referenced local images, configuration.json and a
build-report.json binding hashes to the build inputs. It performs no network requests.
Move/zip the whole generated folder for handoff; external reading links are optional, not
rendering dependencies. Do not copy original slide decks into the deliverable automatically.

Native folding works with JavaScript disabled. Enhancement buttons expand/collapse all
answers when JavaScript is available. They do not record attempts or mastery. Native MathML
needs a browser supporting its used constructs: inspect the actual browser, particularly
fractions, matrices and CJK labels. Unsupported math stays a disclosed limitation until a
verified local fallback is supplied. All instructional content and figures must be local.

Browser print styling is only a convenience. It is not the verified print-first PDF product;
do not promise printed answer visibility across viewers. Use the separate print entry for
a printable deliverable. Hosting/sharing requires its own explicit user request.

Record semantic, coverage and browser findings in review.md. The build report deliberately
leaves browser and semantic review pending. Source inventory/configuration/artifact hashes
must change the chapter state on rebuild; an old screenshot cannot verify a new build.

The shared capacity/usage tools' optional `--study-state` integration is print-entry-only
and fails before writes in this package. Run them without that flag; record their report/
ledger paths and actual QA findings in the HTML state manually. No print helper is needed.

For each entry in `study-state-template.json`'s chapters list, record a stable slug, selected
source IDs/ranges, inventory/configuration/build-report hashes, output/coverage/review paths,
pending K/V IDs, and `qa` values for coverage, reasoning, citations, extraction, browser,
capacity disclosure and usage accounting. Use pending/pass/fail/not-applicable honestly.
Only mark the chapter delivered after requested artifacts exist and all applicable checks
pass; otherwise record a partial handoff with its remaining checks. State is agent-maintained,
not a claim of automated HTML workflow enforcement or stored quiz attempts.
