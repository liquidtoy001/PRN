# Pre-Review Notes · Exam-Calibrated Course Revision Notes

[中文](./README.md) | **English**

A cross-platform **Agent Skill** that turns a learner's own course materials—slides, worksheets, assignments, past papers, and official solutions—into revision notes ordered by real assessment evidence. It works across maths, CS, natural sciences, medicine, law, languages, and business.

> Core principle: calibrate notes to the course's actual assessment evidence, not to textbook order. Never invent an exam weighting or a “frequently tested” claim when the supplied materials do not support it.

See [USAGE.md](./USAGE.md) for installation and platform usage (Chinese), and [TESTING.md](./TESTING.md) for the manual evaluation plan.

## Repository structure

```text
pre-review-notes/
├── pre-review-notes/                 Installable skill source (runtime files only)
│   ├── SKILL.md
│   ├── template.tex                  LaTeX chapter template for maths/CS
│   ├── markdown-template.md          Markdown chapter template for prose fields
│   ├── course-overview-template.svg  One-page course overview template
│   ├── calendar-template.ics         Revision calendar template
│   └── progress-template.md          Cross-session progress template
├── examples/stat3007/                Reproducible STAT3007 example and source set
│   ├── slides/                       source metadata and manifest.csv only; no source PDFs
│   └── notes/                        English/Chinese LaTeX, PDFs, and progress.md
├── GitHub Release                    Uploadable v0.0.2 skill ZIP
├── README.md / README.en.md          Bilingual project documentation
├── USAGE.md                          Installation and usage
├── TESTING.md                        Manual evaluation plan
└── LICENSE                           MIT license
```

`pre-review-notes/` is the install boundary. Course PDFs, example notes, and LaTeX build intermediates remain outside the skill package. Historical installation archives belong in GitHub Releases rather than Git history.

## What changed in v0.0.2

- Step 0 now confirms the main note language—Chinese, English, or bilingual—and keeps the `.tex`, PDF, course map, and `progress.md` consistent.
- Chinese notes retain English for specialised or easily confused terms. On first use, write `中文（English, acronym）`, for example 普通最小二乘法 (Ordinary Least Squares, OLS), 岭回归 (Ridge Regression), and 1 近邻回归 (1-Nearest-Neighbour Regression, 1-NN).
- Step 8 compiles LaTeX, validates PDF structure and text extraction, and renders representative pages with Poppler to catch clipping, overlap, missing glyphs, and blank pages. On Windows, MiKTeX `latexmk` failures fall back to `pdflatex`/`xelatex`.
- `examples/stat3007/` records 33 unique slide sources for 34 lecture rows in a manifest (Lectures 32 and 33 share `32-rl2.pdf`) and provides English/Chinese generated Regression notes. The original slides are local test inputs only.

## Workflow at a glance (Steps 0–10)

1. **Step 0** — Confirm output format, PDF requirement, main note language, annotation language, and chapter granularity.
2. **Step 1** — Map the real grading structure, exam format, and instructor priorities.
3. **Step 2** — Inventory slides, exercises, assignments, past papers, and official solutions.
4. **Step 3** — Order chapters by assessment weight and prerequisites; optionally render an SVG overview and `.ics` calendar.
5. **Step 4** — Retrieve course-specific examples, worksheets, assignments, and exam questions for each chapter.
6. **Step 5** — Draft concepts, complete derivations, trap boxes, quick-reference cards, and an assessment map from the shared template.
7. **Step 6** — Calibrate answer depth against official solutions.
8. **Step 7** — Independently re-derive numerical, algebraic, and logical work.
9. **Step 8** — Compile LaTeX and complete PDF structural, textual, and visual QA.
10. **Step 9** — Deliver one chapter with its evidence boundary, language, and output files.
11. **Step 10** — Iterate through the remaining chapters in priority order and update `progress.md`.

## Example: STAT3007

The example uses the public course page [STAT3007/STAT7007 Deep Learning](https://yenan.github.io/teach/stat3007/index.html). `examples/stat3007/slides/README.md` and the manifest record source URLs, page counts, byte sizes, and SHA-256 hashes, but the repository does not contain the original slide PDFs. Users who obtain them locally must follow the source's copyright and educational-use conditions.

Open the generated artifacts directly:

- [Chinese Regression PDF](./examples/stat3007/notes/pdf/stat3007-regression-notes-zh.pdf)
- [English Regression PDF](./examples/stat3007/notes/pdf/stat3007-regression-notes-en.pdf)
- [Chinese LaTeX source](./examples/stat3007/notes/chapter-01-regression-zh.tex)
- [English LaTeX source](./examples/stat3007/notes/chapter-01-regression.tex)

Only lecture slides were available for this example, so no exam weighting, question format, or official solution was fabricated; the boundary is recorded in `progress.md`.

## License

The skill code and templates are licensed under [MIT](./LICENSE). Third-party course materials are outside this licence and are not distributed in the repository or Releases.

## Version history

| Version | Date | Changes |
|---|---|---|
| v0.0.2 | 2026-08-13 | Separated installable skill from examples; added language confirmation, English terminology convention for Chinese notes, LaTeX-to-PDF compilation and visual QA; added the reproducible STAT3007 example, 33-slide manifest, and a new skill zip. |
| v0.0.1 | 2026-07 | Initial public release with the core methodology, LaTeX/Markdown/SVG/ICS/progress templates, and manual evaluation plan. |
