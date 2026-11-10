# Pre-Review Notes

[中文](./README.md) | **English**

Turn course slides, readings and exercises into standalone notes for preview, knowledge
consolidation or exam revision, with explanations, useful diagrams and source mappings in
companion records. This is an Agent Skill: instructions and supporting tools for a file-capable
AI agent, rather than a standalone application.

**Version status: v0.3.0 is being prepared for release.** This page describes v0.3.0. The
currently published version is still [v0.2.10](https://github.com/liquidtoy001/PRN/releases/tag/v0.2.10),
which does not contain the new workflow.

## Start here

1. Choose PDF for printing and annotation, or HTML for screen reading and optional folded answers.
2. Open the [latest Release](https://github.com/liquidtoy001/PRN/releases/latest) and download
   the appropriate ZIP under Assets. Follow the [installation guide](./USAGE.md).
3. Give your agent the course materials and start with one chapter.
4. Paste one of the requests below. The agent shows all choices and recommendations together;
   accept them in one reply or customise them together.

| Goal | Download | Skill name |
|---|---|---|
| Printable PDF; optional Markdown / LaTeX | pre-review-notes-v0.3.0.zip (pending release) | pre-review-notes |
| Offline HTML with optional folded answers | pre-review-notes-html-v0.3.0.zip (pending release) | pre-review-notes-html |

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

## Three presets, one complete intake

| Preset | Teaching focus | Recommended paper enrichment | Extra practice |
|---|---|---|---|
| Preview | Prerequisites, intuition and the lesson's reading route | Off | None |
| Knowledge consolidation | Definitions, mechanisms, derivations and related concepts | Reading list | None |
| Exam revision | Applications grounded in supplied papers, syllabus or checklist | Off | None |

Purpose is separate from pace: first chapter, a course delivered in chapters, or time-limited
scope. The first conversation shows all settings and alternatives in four visible groups,
including advanced and currently inactive settings. One reply can accept recommendations.
Explicit and saved choices take precedence; practice, papers and code remain customisable.
See the [complete Chinese intake examples](./examples/intake/README.md).

## What to expect

The workflow accounts for selected pages and knowledge points, preserves conditions and
worked examples, and incorporates informative figures. It distinguishes course evidence,
supplementary explanations and optional verified paper enrichment. Exam-revision mode uses
assessment evidence when available. It checks paper identities before counting recurrence.
Standalone teaching restores prerequisites and connects related concepts. Code, source indexes
and process explanations default to off in the body; evidence records remain available.
Answer-language snippets depend on question type, avoiding repeated translations after
calculations and ordinary choice items. After drafting, the agent announces and performs a
second pass over knowledge and questions, then checks whole-chapter continuity.

PDF notes require compilation and page/figure inspection. HTML notes require browser layout,
math and interaction checks. PDF tooling also supports optional learning banks, Anki export and
retests; folded HTML questions do not track mastery. Progress is maintained by chapter.

PDF generation needs a working typesetting environment. If a required tool is missing, the
agent should identify the missing step and describe what it actually produced.

## Examples and limits

The [original HTML fixture](./tests/fixtures/html/) checks math, images and question structure.
The [older course example](./examples/stat3007/README.md) is a historical trial.

Actual course trials have concentrated on AI/ML. Cross-domain accuracy and learning gains have
not been systematically evaluated. See [v0.3.0 validation](./TESTING-0.3.0.md) for the actual
engineering and visual checks. Passing automated tests does not establish teaching quality
or error-free content; compare generated notes with their sources.

Keep private course materials local. Source slides are excluded from installation packages.
The [MIT License](./LICENSE) covers project code and original templates, not third-party material.

## Versions and development

The prepared version is **v0.3.0**; see [release notes and upgrade guidance](./RELEASE-0.3.0.md).
Both v0.2.10 entries keep their names and accept existing knowledge/exam configurations.
Preserve old outputs and progress before using the new workflow for subsequent chapters.
Historical chapters are never automatically credited with passing the new review.

See [development instructions](./DEVELOPMENT.md), [testing](./TESTING.md) and
[the changelog](./CHANGELOG.md). Canonical shared resources live in `shared/` and are
materialised into both independently installable packages.
