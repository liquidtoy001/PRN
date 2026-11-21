# Student-facing presentation

For new notes, `show_source_index=false` and `show_source_explanations=false`.
Keep these two choices in intake and save them with the other preferences.

`show_source_index` controls file catalogues, source-ID lists, question-to-source mapping
tables and audit-document links inside the note. `show_source_explanations` controls source
inventory narratives, evidence-grade/process explanations and lengthy quality-ceiling boxes
inside the note. Both default to off. Topic navigation and the teaching content are separate
and stay available. Put operational details in local inventory, coverage, exam-plan and review
companions; communicate omissions and unresolved errors in the delivery message.

Compact claim citations and required image/quotation attribution remain distinct from these
optional sections. Keep useful captions, symbol definitions and material caveats beside the
content they qualify. Honour an explicit request for citation-free body text by keeping
claim-to-source mappings in `evidence.md` with stable K/Q IDs, precise note locations and the
entry's citation syntax. Validate that companion against the inventory, then check the mapping
against the final note. Required attribution still accompanies reused licensed material.

Use the active entry's citation-format instructions. Never suppress uncertainty that changes
how a formula, explanation or answer should be interpreted. Avoid printing local filesystem
paths or an audit trail merely because the agent used them during production.

Existing confirmed preferences are retained. Missing new presentation keys mean the off
defaults for newly generated content; old files are revised only as part of requested work.
When either option is enabled, use concise relevant information and avoid repeated source
headers on every concept.

## Default handout layout

Use a single reading column, dark body text, a clear chapter title and bold numbered
sections. Reserve thin rules for major divisions and light shading for table headers or
an occasional result. Use paragraph spacing, heading weight and position to carry the
hierarchy in grayscale. Keep intact any source colors needed to interpret a figure.

In a teaching chapter, start the explanation on the opening page. Keep the symbol or
given value near its first use, set substantial equations on their own line and put
comparisons in a compact table when the columns help. In an exam section, keep the
question number, givens, labelled figure, subpart and its answer easy to find in order.
Use the same heading hierarchy across both treatments. Ordinary solutions need body-size
text and may continue across a page. Reserve writing space for a requested practice copy.

Use the learner's saved layout and density choices. A request for compact notes changes
spacing, while formulas and figure labels must remain legible at the selected page or
screen size. Printed pages use a simple page number; HTML retains screen navigation,
keyboard focus, theme selection and optional folded answers.

## Code in the learning artifact

`include_code=false` is the default. Preserve code as a source of knowledge without importing
its listings: explain inputs, outputs, state changes, control decisions and edge cases through
prose, equations, diagrams or hand-worked trace tables. A short numbered procedure is fine;
do not reintroduce a listing as a screenshot or disguise a program as pseudocode to bypass
this preference. Internal verification,
LaTeX/HTML authoring and build scripts are not code shown to the learner and remain available.

Set `include_code=true` only when the learner requests visible code or confirms it during
intake. Selecting a coding tutorial, extended depth or exam purpose alone is insufficient.
If an actual programming question requires code while the preference is off, explain the
mechanism and flag the code-dependent part as deferred; resolve that specific preference
before claiming to have completed it. With code enabled, use the smallest relevant snippet
after the conceptual explanation, or a separately requested appendix. No large implementation
block should be required to follow an otherwise conceptual revision chapter.
