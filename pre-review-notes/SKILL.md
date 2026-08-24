---
name: pre-review-notes
description: Generate assessment-calibrated study notes for any academic course, using the learner's own materials (lecture slides, transcripts, worksheets, assignments, past exams, sample solutions) as the primary source instead of generic textbook content. Can also render a one-page colour-coded SVG course-overview map before drafting begins, export the priority plan as an importable .ics revision calendar, and maintain a cross-session progress tracker so multi-chapter projects survive new sessions. Trigger when a user asks for study notes, revision notes, a cheat sheet, or exam prep notes for a specific course and can supply real course materials (a searchable knowledge base, uploaded files, or pasted content). Works across mathematics, CS, natural sciences, medicine, law, humanities, languages and business. Prioritizes topics by how heavily they are actually assessed rather than textbook chapter order, and calibrates worked-example depth to the course's own assignments and answer keys.
---

# Pre-Review Notes

A methodology for turning a learner's own scattered course materials into a coherent,
prioritized set of study notes — one chapter per topic, all sharing one visual template,
every claim traceable back to something the course itself actually taught or tested.

This is a **process skill**, not a one-shot template fill. It spans many turns: map the
assessment landscape once, then repeat a research → draft → verify loop once per chapter,
in priority order, until the syllabus is covered or the learner has what they need.

## Core principle

**Notes are calibrated to the assessment, not to the textbook.** A topic that is heavily
tested gets a full chapter with several fully-worked derivations pulled from real problem
sets. A topic mentioned once in passing gets folded into another chapter's quick-reference
section, or skipped. Every "this is important" or "this is exam-style" judgment must trace
back to something the learner's own materials actually say or show — an explicit weighting
statement, an instructor's aside, a problem that recurs across several years of exams. Never
invent importance generically from what a textbook *usually* emphasizes.

## When to use this skill

Use when the learner:
- wants notes for a **specific course they are taking**, not a general "explain topic X"
- has, or can search/upload, **real course materials**: slides, transcripts, worksheets,
  problem sets, assignments, past exams, sample exams with solutions, an announced grading
  breakdown, or instructor guidance about what to prioritize
- is preparing for a concrete assessment (exam, resit, certification, quiz) and wants
  targeted, efficient coverage rather than exhaustive textbook coverage

Do **not** use this for a single "explain X to me" question — that's just an explanation.
If no real course materials are available or searchable, say so explicitly and offer generic
notes instead; do not fabricate exam references, weightings, or "this was tested in 2021"
claims that cannot be traced to a real source.

## Tool-agnostic note

This skill assumes only that the executing model has *some* way to (a) search or read the
learner's course materials and (b) write an output file. It does not depend on any specific
tool name. Substitute whatever retrieval mechanism is available: a project knowledge base,
uploaded documents, pasted transcripts, or — with appropriate caution about accuracy — a web
search of publicly posted course materials for the same course.

## Files in this skill

- `template.tex` — per-chapter LaTeX template for quantitative courses (Step 5).
- `markdown-template.md` — per-chapter Markdown template for prose-heavy fields (Step 5).
- `course-overview-template.svg` — one-page visual course map: colour-coded topic
  sections, an assessment-structure section, and a legend (Step 3).
- `calendar-template.ics` — revision-plan calendar: weight-proportional study blocks,
  importable into any calendar app (Step 3).
- `progress-template.md` — cross-session progress tracker for the multi-chapter loop
  (Step 9).

---

## Workflow

### Step 0 — Clarify output preferences (only if genuinely ambiguous)

- **Format**: LaTeX (`.tex`) for math/CS/physics-heavy quantitative courses; Markdown for
  everything else (law, history, languages, business, most biology/medicine). Default by
  discipline rather than always reaching for LaTeX — see `markdown-template.md` for the
  non-LaTeX equivalent structure.
- **Compiled output**: source file only, or also compiled to PDF/HTML? Many learners compile
  themselves — don't assume they want a rendered file.
- **Annotation language**: if the learner studies in a second language, ask whether they want
  inline glosses in their first language. The template supports this natively (see the `\note`
  macro / the "Personal gloss" block in the Markdown template) without touching the main content
  language.
- **Granularity**: default to **one file per chapter/topic**, not one giant file — easier to
  regenerate a single chapter later without disturbing the rest.

### Step 1 — Map the assessment landscape

Before touching content, establish how the course is actually graded and tested:

- Search for / ask about the grading breakdown, any stated **topic-by-topic weighting**
  (e.g. "32 of 40 exam marks come from Topic X"), the exam format (time, number of questions,
  open/closed book), and any instructor guidance about what to prioritize. Statements like
  *"past papers aren't representative, focus on the worksheets and assignments"* are real,
  load-bearing signals — always look for language like this, and treat it as overriding any
  default assumption about what "should" matter.
- If official **sample solutions / model answers** exist for any problem set, flag this
  immediately. They are the single best source for calibrating expected depth, notation, and
  answer style — actively search for them, never assume they don't exist.
- Produce a short summary of the assessment landscape before generating content, and use it
  to set the chapter order in Step 3.

**Signals that a topic is high-priority** (any one is sufficient, more is stronger):
explicit weighting statements; instructor emphasis ("this is definitely tested"); the same
problem type recurring across multiple worksheets/assignments/exam years; the existence of an
official sample solution for it (implies it's a canonical, examinable problem type); recency
(the most recently posted materials reflect the current syllabus, not older archived ones).

**Signals that a topic is low-priority**: explicit de-emphasis ("you won't need to know this
in detail"); appears once with no matching assessment item found anywhere; marked as optional
or further-reading in the source materials.

**State the evidence base explicitly.** If fewer than ~3 past sittings (or equivalent assessed
items) are available, flag the weighting as thin-sample — a pattern inferred from one or two
exams is a weak signal, and the chapter order should lean more heavily on explicit weighting
statements and instructor guidance. Carry this caveat into the Step 3 plan rather than
presenting a thin-sample ordering as settled.

### Step 2 — Inventory available source material

Search broadly before assuming you know what exists. Typical categories, adapted per
discipline:

| Category | CS/Math example | Law example | Medicine example |
|---|---|---|---|
| Primary instruction | lecture slides/transcripts | case-law readings, lecture notes | lecture slides, clinical guidelines |
| Practice problems | worksheets, tutorial sheets | practice problem questions, moot briefs | clinical vignettes, OSCE stations |
| Graded work | assignments, labs | essays, problem questions | case write-ups |
| Assessment previews | past exams, sample exams | past exam questions | past OSCE/exam stations |
| Answer keys | official solutions | model answers, examiner reports | model answers |

Build a mental index of what exists and which future chapter each item will feed into.

### Step 3 — Build the topic list and priority order

- Break the syllabus into chapters at a natural, exam-testable grain — roughly one chapter
  per assessable unit, not one per lecture. Merge trivially small topics; split large
  heterogeneous ones.
- Order chapters by **(a) assessment weight**, highest first, subject to **(b) prerequisite
  structure** — never place a topic before something it depends on, even if the prerequisite
  carries less weight on its own.
- Share this plan with the learner before generating a large volume of content. This is a
  multi-turn project; getting the priority order wrong early wastes real work later.
- **Optionally render the plan as a one-page course overview map** using
  `course-overview-template.svg`: one colour-coded section per topic block (with week
  ranges and concept cards), plus a final gray section carrying the assessment structure
  found in Step 1 — grading breakdown, exam format, and any stated topic weighting go in
  the assessment cards verbatim. This is the most effective form in which to share the
  Step 3 plan: the learner sees coverage, timing, and weighting at a glance. The map is
  bound by the same sourcing rule as the notes — every week number, topic name, and mark
  split on it must come from the course's own materials, and the footer must state which
  syllabus/materials it is based on.
- **Optionally export the plan as a revision calendar** using `calendar-template.ics`: work
  backward from the assessment date, allocating study blocks per chapter in proportion to
  assessment weight, and end with a final quick-review pass over every chapter's
  quick-reference card. The learner imports the `.ics` into whatever calendar app they use.
  The assessment date and the learner's available time must come from the learner or their
  materials — never guessed.

### Step 4 — Per-chapter research (repeat for every chapter)

For each topic, before drafting, run several **targeted** searches — not one broad query —
covering:

1. **Core theory** in the course's own notation and framing (not a generic textbook version).
2. **Instructor's own worked examples** from lectures.
3. **Worksheet/tutorial problems** on this topic, with solutions if available.
4. **Assignment/coursework problems** on this topic, with solutions or at least the question text.
5. **Past-exam or sample-exam questions** specifically testing this topic, across as many
   sittings as exist.
6. **Explicit instructor guidance** about this topic specifically — what not to memorize, what
   distinctions are commonly confused, what depth of answer is expected.

Do not draft from general knowledge of the subject. Every non-trivial claim in the chapter
should trace back to something actually retrieved in this step.

### Step 5 — Draft the chapter using the shared template

Use one consistent template across every chapter (see `template.tex` and
`markdown-template.md`) so the full set reads as one coherent book. Chapter contents, in order:

1. **Header** — chapter title, one-line note on assessment weight/importance, source tag.
2. **Concept sections** — each core idea gets a plain-language framing sentence, the formal
   statement (definition/theorem/rule/doctrine), and a short example. Tag each section with
   *where it is tested* (worksheet #, assignment #, exam year + question).
3. **Worked derivations** — for the 2-4 most important problem *types* in the chapter, give a
   **complete, step-by-step solution to a real problem drawn from the learner's own
   materials**, not an invented textbook analogue. Quote the original problem statement
   itself — verbatim where practical — before the solution: learners revise best against the
   real wording, not a paraphrase. This is the single highest-value component:
   it shows exactly what a full-credit answer looks like.
4. **Common-mistake / "trap" boxes** — anything the instructor explicitly warned about, or any
   distinction that is easy to blur. These must come from real emphasis in the source
   materials (lecture asides, examiner-report comments, patterns across past exams, or the
   learner's own stated weak areas) — never invented generically.
5. **Quick-reference card** — a dense, one-screen summary of every formula/definition/technique
   in the chapter, for last-minute review.
6. **Assessment-mapping table** — every worksheet/assignment/exam item touching this chapter,
   so the learner knows exactly what to go practice next.

### Step 6 — Calibrate against sample solutions

Where official sample/model solutions exist for any problem in the chapter, mirror their
answer *style* precisely: how much derivation they show, what notation/conventions they use,
whether they use diagrams or shorthand notation, how terse or expansive the justification is.
The goal is that answers written at the depth modeled in the notes would earn full marks —
not padded beyond what's rewarded, not thinner than what's required.

### Step 7 — Verify

Recompute or re-derive every numeric or logical worked example independently before including
it — never transcribe on trust, even from an official solution (they can contain typos or
outdated content). If something cannot be verified with confidence, either resolve it before
delivering, or flag the uncertainty explicitly to the learner rather than presenting it as
settled fact.

### Step 8 — Deliver

- Output the chapter as a single file, per the format preference from Step 0.
- Present it with a short, structured summary: a page/section overview, and 2-4 sentences on
  the highest-value pattern found in this chapter (e.g. "this exact problem type recurred in
  3 of the last 4 sittings").
- Do not narrate the writing process. Deliver the file and a compact summary, then stop.

### Step 9 — Iterate across chapters

Repeat Steps 4-8 per chapter, in priority order from Step 3, generally one chapter per turn
unless asked for more. Periodically resurface the remaining priority list so the learner can
reorder if their own sense of readiness changes — this is their call, not a fixed plan to
execute blindly. If a course overview map was produced in Step 3, it doubles as the shared
reference for these check-ins — resurface it (or re-render it, if the plan changed) rather
than re-describing the plan in prose.

Maintain a `progress.md` alongside the notes (see `progress-template.md`): the assessment
summary, the chapter table with per-chapter status and weight basis, what the last session
delivered, and the agreed next step. Update it at the end of every delivery turn — it is what
lets a fresh session, or a different tool entirely, pick the project up without
re-explanation.

---

## Anti-patterns to avoid

- **Textbook-order drafting.** Don't default to standard chapter order from a textbook if the
  assessment weighting says otherwise — a foundational-but-low-weight topic still comes after
  a heavily-tested one, subject only to genuine prerequisite constraints.
- **Invented exam relevance.** Never write "this is commonly tested" or attach a source tag
  without having actually found that source. If you can't find where something is assessed,
  say so, or omit the claim.
- **Generic worked examples.** A worked example lifted from a textbook rather than the
  course's own worksheets/assignments/exams is a much weaker calibration tool — always prefer
  the real thing, even if it takes more searching.
- **Padding.** Matching a sample solution's depth means not exceeding it either. Over-long
  derivations for problems the course rewards tersely just add noise to revise later.
- **Silent unverified computation.** Any arithmetic, algebra, or stepwise derivation in the
  notes must be independently checked before delivery.
- **One-shot mega-files.** Producing the entire syllabus in a single pass without checking in
  after the first chapter risks building 90% of a plan the learner didn't actually want.

## Cross-disciplinary adaptation

The structure generalizes; only the *content* of each slot changes:

| Template slot | CS/Math | Organic Chemistry | Contract Law | Clinical Medicine |
|---|---|---|---|---|
| Concept section | theorem + proof sketch | mechanism + electron-pushing | doctrine + elements test | pathophysiology + criteria |
| Worked derivation | solve a past-exam problem | predict product of a real problem-set reaction | apply doctrine to a real practice-exam fact pattern | work a real OSCE/case vignette |
| Trap box | common proof-technique error | common mechanism misassignment | commonly-confused doctrines (e.g. offer vs. invitation to treat) | commonly-missed differential |
| Source tag | exam year + Q# | problem set # | past paper Q# | station # |

For prose-heavy fields (law, history, literature), reduce the density of formula-style boxes
and lean on the concept-section + worked-derivation + trap-box structure in flowing prose —
see `markdown-template.md` for a lighter-weight equivalent that doesn't force LaTeX macros
onto naturally discursive content.
