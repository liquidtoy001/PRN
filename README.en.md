# Pre-Review Notes

[中文](./README.md) | **English**

Turn course slides, readings and exercises into study notes with source locators, explanations
and useful diagrams. This is an Agent Skill: instructions and supporting tools for a file-capable
AI agent, rather than a standalone application.

## Start here

1. Choose PDF for printing and annotation, or HTML for screen reading and optional folded answers.
2. Open the [latest Release](https://github.com/liquidtoy001/PRN/releases/latest) and download
   the appropriate ZIP under Assets. Follow the [installation guide](./USAGE.md).
3. Give your agent the course materials and start with one chapter.
4. Paste one of the requests below. The agent asks for missing preferences together.

| Goal | Download | Skill name |
|---|---|---|
| Printable PDF; optional Markdown / LaTeX | [pre-review-notes-v0.2.10.zip](https://github.com/liquidtoy001/PRN/releases/download/v0.2.10/pre-review-notes-v0.2.10.zip) | pre-review-notes |
| Offline HTML with optional folded answers | [pre-review-notes-html-v0.2.10.zip](https://github.com/liquidtoy001/PRN/releases/download/v0.2.10/pre-review-notes-html-v0.2.10.zip) | pre-review-notes-html |

Choose PDF if unsure. Either package can be installed alone or alongside the other.
Download the named ZIP, not GitHub's automatic Source code archive. The `.sha256` file is
an optional integrity check, not an installer.

**PDF request:**

```text
Use pre-review-notes with these course materials.
Choose knowledge consolidation, lightweight mode, English, and PDF output.
Start with chapter 1. Preserve small knowledge points and explain equations and useful figures.
Show all remaining configuration choices together before drafting.
```

**HTML request:**

```text
Use pre-review-notes-html with these course materials.
Choose knowledge consolidation, lightweight mode and English. Start with chapter 1.
Keep complete teaching explanations and add a self-test section with folded answers.
Deliver the entire offline HTML folder. Show remaining choices together first.
```

Replace chapter 1 with actual filenames or pages. Lightweight means smaller batches with
full teaching depth within the chosen scope. Knowledge mode defaults to no new questions;
the HTML example explicitly opts into self-tests.

## What to expect

The workflow accounts for selected pages and knowledge points, preserves conditions and
worked examples, and incorporates informative figures. It distinguishes course evidence,
supplementary explanations and optional verified paper enrichment. Exam-revision mode uses
assessment evidence when available.

PDF notes require compilation and page/figure inspection. HTML notes require browser layout,
math and interaction checks. PDF tooling also supports optional learning banks, Anki export and
retests; folded HTML questions do not track mastery. Progress is maintained by chapter.

PDF generation needs a working typesetting environment. If a required tool is missing, the
agent should identify the missing step and describe what it actually produced.

## Examples and limits

The [original HTML fixture](./tests/fixtures/html/) checks math, images and question structure.
The [older course example](./examples/stat3007/README.md) is a historical trial.

Actual course trials have concentrated on AI/ML. Cross-domain accuracy and learning gains have
not been systematically evaluated. There are 28 automated tests; they do not establish semantic
correctness or visual quality. Actual browser acceptance for v0.2.10 still has pending checks;
see [the validation record](./TESTING-0.2.10.md).

Keep private course materials local. Source slides are excluded from installation packages.
The [MIT License](./LICENSE) covers project code and original templates, not third-party material.

## Versions and development

The current install version is **v0.2.10**. Releases retain the latest dual-entry version and
**v0.2.9**, the last print-only version, as a rollback option. Older Git tags remain available
for historical inspection, rather than recommended installation.

See [development instructions](./DEVELOPMENT.md), [testing](./TESTING.md) and
[the changelog](./CHANGELOG.md). Canonical shared resources live in `shared/` and are
materialised into both independently installable packages.
