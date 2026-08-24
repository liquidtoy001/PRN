# Pre-Review Notes · Exam-Calibrated Course Revision Notes

[中文](./README.md) | **English**

A cross-platform **Agent Skill**: turns your own scattered course materials (lecture slides, worksheets, assignments, past exams, official answer keys) into a set of revision notes ordered by **assessment weight**, with every claim **traceable to a real source**. Works for any discipline (maths / CS / law / medicine / humanities, etc.).

> Core principle: notes are calibrated to the exam, not to the textbook. Heavily-assessed topics get full chapters with real-exam derivations; topics only mentioned in passing get merged or skipped. Every "this is frequently tested" claim must be traceable to real evidence in the course materials.

👉 **Installation and usage for each platform: see [USAGE.md](./USAGE.md)** (in Chinese)

## Repository structure

```
pre-review-notes/                      Skill source directory (usable as-is)
├── SKILL.md                           Main skill file: methodology + anti-pattern list
├── template.tex                       Chapter-notes LaTeX template (maths/CS)
├── markdown-template.md               Chapter-notes Markdown template (humanities)
├── course-overview-template.svg       One-page course overview map template
├── calendar-template.ics              Revision calendar template (importable into any calendar app)
└── progress-template.md               Cross-session progress tracker template
pre-review-notes-v0.0.1.zip            Release package (SKILL.md at zip root; upload directly to claude.ai / Qoder, etc.)
USAGE.md                               Installation and usage per platform
TESTING.md                             Manual evaluation plan (validates skill effectiveness)
README.en.md                           This file
LICENSE                                MIT license
```

## Files in the skill

| File | Purpose | Workflow step |
|---|---|---|
| `SKILL.md` | Main skill file: 9-step methodology + anti-pattern list | All steps |
| `template.tex` | Chapter-notes LaTeX template (maths/CS courses) | Step 5 |
| `markdown-template.md` | Chapter-notes Markdown template (law/history/languages) | Step 5 |
| `course-overview-template.svg` | One-page course overview map (colour-coded topic sections + assessment section) | Step 3 |
| `calendar-template.ics` | Revision calendar: study blocks allocated by assessment weight, importable anywhere | Step 3 |
| `progress-template.md` | Cross-session progress tracker — resume in a new session at zero cost | Step 9 |

## Workflow at a glance (9 steps)

1. **Step 0** Confirm output preferences (LaTeX / Markdown, bilingual annotations, one file per chapter)
2. **Step 1** Map the assessment structure: mark weightings, exam format, teacher-flagged priorities
3. **Step 2** Inventory all available materials
4. **Step 3** Order chapters by assessment weight + prerequisite dependencies; optionally render an SVG overview map to confirm the plan, and export a .ics revision calendar (working backward from the exam date, blocks allocated by weight)
5. **Step 4** Per chapter, retrieve the course's own worked examples, exercises and past-exam questions
6. **Step 5** Draft against the shared template: concepts → full real-exam derivations → pitfall boxes → quick-reference card → assessment map
7. **Step 6** Calibrate answer depth against official answer keys (no more, no less)
8. **Step 7** Independently re-derive everything — trust no source blindly
9. **Steps 8–9** Deliver one chapter per turn, iterating by priority; progress recorded in `progress.md` so a new session or a different tool can pick up seamlessly

## Model suggestions by discipline (reference)

| Discipline | Suggestion | Why |
|---|---|---|
| Maths / CS | DeepSeek-R1, GLM + Claude Code | Most reliable for Step 7 re-derivation; can compile LaTeX locally |
| Law / History / Languages | Kimi | Long context, good for large prose-material inventories |
| Medicine | Qwen family, Tencent Yuanbao | Handles mixed Chinese-English guidelines; bilingual annotations |

## FAQ

- **No real course materials?** The skill explicitly refuses to fabricate citations like "this appeared in year X"; it will only produce generic notes and state that calibration sources are missing.
- **Chinese support?** Native: the SVG ships a CJK font stack, `template.tex` reserves CJK macros, and the Markdown template includes bilingual annotation blocks.
- **Can it generate the whole notebook in one go?** Not recommended (see the "one-shot mega-files" anti-pattern): the default is one chapter per turn, with the priority plan confirmed before drafting.
- **Will it quiz me?** No. The skill has no quiz/testing feature; past-exam questions go into the notes verbatim, in the "full derivations" section, with step-by-step model-answer-style solutions.

## Effectiveness validation

The skill ships with a reproducible manual evaluation plan (A/B comparison + blind scoring, 5 falsifiable hypotheses, 5 test cases, a 6-dimension rubric, and a hard "fabrication rate = 0" veto criterion).

👉 **Full plan: see [TESTING.md](./TESTING.md)** (in Chinese)

## Version history

| Version | Date | Changes |
|---|---|---|
| v0.0.1 | 2026-07 | First public release: SKILL.md 9-step methodology + 5 templates (LaTeX / Markdown / SVG overview map / .ics calendar / progress tracker), bilingual README, standalone USAGE / TESTING docs, installable skill zip attached to the GitHub Release |

## License

[MIT](./LICENSE)
