# Pre-Review Notes

[中文](./README.md) | **English**

Turn course slides, readings and exercises into standalone study notes. Choose **preview,
knowledge consolidation or exam revision**, then choose printable PDF or screen-friendly HTML.

This is an Agent Skill: instructions and supporting tools for an AI agent that can read files
and create artifacts. It is not a standalone application.

**Current version: [v0.3.5](https://github.com/liquidtoy001/PRN/releases/tag/v0.3.5).**
v0.3.5 checks whether a reader can work out the next step from the chapter. For example, an attention explanation identifies the query and its source vectors and works one dot product so the reader can calculate the next score. [Release notes](./RELEASE-0.3.5.md)

The layout defaults to a course handout with a single reading column, bold headings,
displayed equations and lightly shaded table headers. Each worked subpart keeps its solution
nearby. HTML uses the same hierarchy with optional folded answers and a dark theme.

## Choose a purpose: which preset fits?

| Preset | Your situation | How the notes teach | Useful inputs |
|---|---|---|---|
| **Preview** | A new chapter, unfamiliar prerequisites, or preparation before class | Restore prerequisites, introduce concepts through a concrete problem and small examples, then connect the lesson and identify points to notice in class | Upcoming slides, lecture notes or assigned reading |
| **Knowledge consolidation** | You attended the lecture but understanding is fragmented; you remember a formula without knowing why; you want to relearn after a gap | Explain definitions, mechanisms, derivations and conditions, and use examples to connect related concepts | Studied slides, notes and exercises; optionally describe what confuses you |
| **Exam revision** | You want to follow an exam outline, apply knowledge to questions or build a standalone revision guide | Organise knowledge using actual assessment evidence, explain selected questions and subparts, and tailor answer wording to the response type | Course material plus any available past paper, syllabus or topic checklist; solutions or marking guides help when available |

For the same chapter on conditional probability, preview would establish events and what
"given" means; consolidation would connect conditional and joint probability and the derivation;
exam revision would also use supplied questions to explain how to interpret the task, set up
the calculation and explain the result.

**All presets retain the distinct knowledge, conditions, source examples and useful figures
within the agreed scope, with the same coverage and review requirements.** Preview introduces
prerequisites earlier. When time is limited, agree a smaller scope and identify deferred content.

Defaults and customisation:

- **Extra practice defaults to none.** Source exercises and selected past-paper questions
  still receive explanations. Quizzes, flashcards or folded HTML questions can be added.
- **Paper enrichment:** off for preview/exam; a reading list is recommended for consolidation.
  The confirmed setting controls execution. Request "paper enrichment off" to use only supplied material.
- **Code, source indexes and process explanations default to off in the body.** Explain lab
  mechanisms in the notes, retain necessary citations/figure attribution, and keep full mappings in companions.
- **Existing choices take precedence.** Changing purpose preserves your language, layout and
  practice choices. Explicitly request a reset when you want the new preset's defaults.

If unsure, describe your situation and the agent will recommend a preset alongside the other
choices. Slides alone can support exam-oriented study notes, but cannot establish exam
structure, question frequency or this year's emphasis.

## Choose an output: PDF or HTML

| Reading context | v0.3.5 package | Skill name |
|---|---|---|
| Printable PDF; optional Markdown / LaTeX | [pre-review-notes-v0.3.5.zip](https://github.com/liquidtoy001/PRN/releases/download/v0.3.5/pre-review-notes-v0.3.5.zip) | pre-review-notes |
| Offline HTML with optional folded answers | [pre-review-notes-html-v0.3.5.zip](https://github.com/liquidtoy001/PRN/releases/download/v0.3.5/pre-review-notes-html-v0.3.5.zip) | pre-review-notes-html |

**All three presets work with either entry.** Preview can use PDF; exam revision can use HTML.
Install either package or both. When requesting both outputs, each keeps its own configuration
and artifacts.

Use the download links above, or select the appropriate ZIP under Assets on the
[v0.3.5 Release page](https://github.com/liquidtoy001/PRN/releases/tag/v0.3.5).
Follow the [beginner installation guide](./USAGE.md).
The `.sha256` file checks integrity; GitHub's automatic Source code download is the repository
archive. Neither is the named skill installation ZIP.

## Choose the scope and pace

| Choice | When it fits | What happens |
|---|---|---|
| **First chapter** (lightweight, default) | An initial trial or one bounded chapter | Complete the selected files/pages with full teaching depth |
| **Course in chapters** (full) | Building a maintainable set over time | Plan the course, then generate chapters incrementally with saved progress |
| **Time-limited revision** (exam-cram) | A known deadline and available study hours | Prioritise using evidence and prerequisite dependencies; state scope trade-offs and deferred content |

Purpose and pace are independent. Exam revision can start weeks ahead and proceed chapter by
chapter; preview can focus on the section you plan to study in one hour. Choosing exam revision
still allows a normal, systematic study pace.

## Start with a request you can copy

Attach your materials or provide their local directory. Replace the filenames, chapters and
page ranges below with the actual scope; no internal configuration keys need to be memorised.

**Preview · printed notes**

```text
Use pre-review-notes with the preview preset, English notes and PDF output.
This chapter is new to me. Start with [filename / chapter / page range].
Restore the prerequisites and explain concepts through examples while retaining the selected details and source exercises.
Show all settings and recommendations together for confirmation.
```

**Knowledge consolidation · screen reading**

```text
Use pre-review-notes-html with the knowledge consolidation preset and English notes.
Start with [filename / chapter / page range]. I am confused about [concept or specific difficulty].
Explain mechanisms, derivations and connections between related concepts. Deliver the entire offline HTML folder.
Show all settings and recommendations together for confirmation.
```

To add self-tests, append: "Add folded questions with answers initially closed."

**Exam revision · organised around course requirements**

```text
Use pre-review-notes with the exam revision preset, English explanations and PDF output.
Use my supplied syllabus, topic checklist or past papers to organise [chapter / scope].
Teach the knowledge needed for the selected questions and follow any evidenced assessment-language requirements.
Show the complete configuration together and use the recommendations for remaining settings.
```

For a time-limited plan, add the actual deadline and available study hours. Answer-language
snippets follow the question type and assessment requirements. Calculations and ordinary choice items retain reasoning
and results in the note language without an extra translation by default.

## What the first configuration exchange shows

The agent displays **every setting, alternative and recommendation** for the selected entry
in four visible groups:

1. **Core choices:** purpose, material scope, note language and deliverables.
2. **Learning options:** pace, depth, papers, practice and time.
3. **Layout and presentation:** paper size or webpage appearance, density, code, source displays and review.
4. **Exam settings:** organisational evidence and answer language, visible but inactive for other purposes.

Advanced options remain visible. Accept with "Use this preset and the other recommendations",
or change several together: "Papers off, A5, the rest as recommended" for PDF, or
"Dark theme and folded questions" for HTML. If your initial
request already delegates the remaining choices, the agent shows the resolved settings and
continues. Saved settings carry forward on resume. See the [complete Chinese intake examples](./examples/intake/README.md).

## What you receive

- **PDF entry:** the requested PDF and any selected editable sources. Check equations, figures
  and pagination before printing.
- **HTML entry:** a complete folder; open `index.html` and retain its images and other assets.
  Answers can be expanded when self-tests were selected.
- **Companion records and progress:** source mappings, coverage and review records that support
  continuation and later chapter revisions.

After drafting, the agent announces and performs a second pass over knowledge and questions,
then reads the whole chapter for prerequisite gaps and continuity. Corrections are rebuilt and
inspected; unresolved or unprocessed material is disclosed at delivery. Past papers are checked
for duplicates before question frequency is counted; copies count once, while variants and
uncertain cases are recorded separately.

The PDF entry also offers optional learning banks, Anki export and retests. Folded HTML
questions currently do not track mastery.

PDF generation needs a working typesetting environment. If a required tool is missing, the
agent should identify the missing step and describe what it actually produced.

## Examples and limits

The [original HTML fixture](./tests/fixtures/html/) checks math, images and question structure.
The [older course example](./examples/stat3007/README.md) is a historical trial.

Actual course trials have concentrated on AI/ML. Cross-domain accuracy and learning gains have
not been systematically evaluated. All 45 local regression tests passed. Both pages of a Chinese PDF handout were inspected.
The offline HTML fixture built successfully. Narrow-screen and keyboard checks ran on an earlier candidate.
See [v0.3.5 validation](./TESTING-0.3.5.md) for the exact scope. Passing automated tests does not
establish teaching quality or error-free content; compare generated notes with their sources.

Keep private course materials local. Source slides are excluded from installation packages.
The [MIT License](./LICENSE) covers project code and original templates, not third-party material.

## Versions and development

The current version is **v0.3.5**; see [release notes and upgrade guidance](./RELEASE-0.3.5.md).
Use the same skill names when upgrading. Existing course progress remains readable.
Preserve old outputs and progress before using the new workflow for subsequent chapters.
Historical chapters are never automatically credited with passing the new review.

See [development instructions](./DEVELOPMENT.md), [testing](./TESTING.md) and
[the changelog](./CHANGELOG.md). Canonical shared resources live in `shared/` and are
materialised into both independently installable packages.
