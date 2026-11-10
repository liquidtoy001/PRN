# Notes that can be read without the chat

Use this for ordinary teaching/revision chapters in either format. The default product is
a connected explanation that a learner can read independently. A condensed reference card
is a different, explicitly requested product. `extended` adds reasoning and connections;
it does not mean more isolated facts, code or repeated answer boxes.

## Plan the reading path, not one heading per ledger row

Before prose, sketch the chapter's central question, the concepts needed to answer it, and
their dependency order in the private coverage companion. Group related K IDs into coherent
teaching sections. A small condition usually belongs beside its rule, not in its own section.
The coverage ledger checks completeness; it is not the reader's table of contents.

Begin with a concrete situation and explain what the learner needs to decide or calculate.
Introduce the necessary objects and quantities before using them in a definition or formula.
Then develop the mechanism, work through an example, and explain what the result means.
Use natural paragraphs rather than repeating these as labelled boxes for every concept.
A transition must explain why the next idea is needed, not merely say "next we discuss X".

Keep a useful example running across related concepts where it reveals what changed.
Introduce another example when the original no longer serves the explanation. Place a
supporting calculation near the mechanism it explains. Put additional exam applications
after the relevant explanation reaches a natural stopping point; do not interrupt every
paragraph with a year/question label or answer-language sentence.

## Restore the prerequisites the chapter actually uses

Assume the learner may recognise a term without remembering its meaning. Before a concept's
first essential use, identify what the reader must already understand and supply a short
bridge: its meaning, a minimal example or interpretation, and why it matters here. A glossary
entry, acronym expansion, link to another chapter or "recall that" sentence alone is not a
bridge when the next argument depends on it.

For example, a value-learning chapter cannot rely on an unexplained "expected discounted
return" to define Q: first distinguish an immediate reward from a sequence's return and
explain discounting and averaging over uncertain outcomes. This illustrates the decision
rule; do not insert reinforcement-learning content into unrelated courses.

Read relevant earlier supplied course material when necessary and record its exact source.
Enrichment being off does not forbid explaining prerequisite reasoning from supplied sources.
Keep this bridge proportional to the selected topic. If a prerequisite needs its own chapter,
provide the minimum usable recap here and clearly locate the fuller treatment. Respect an
explicitly excluded topic; disclose the resulting reading dependency rather than silently
pretending the note is standalone. Do not reopen the entire course or invent an assessed topic.

Maintain a private prerequisite map: needed concept -> first use -> local explanation ->
course source or clearly identified supplementary reasoning. Recheck it after reordering.

## Connect nearby ideas before asking the learner to distinguish them

Explain the closest relevant prerequisite, alternative or special case, not every vaguely
related concept. State the shared problem, what is kept, what changes, and the consequence.
Define both sides enough for the comparison to be understood locally. A table is useful after
the explanation, but names and feature labels alone do not teach the relationship.

Use the same example/input for a consequential comparison when possible. Say whether one
concept is a prerequisite, a generalisation, a variant, an approximation, or an alternative;
do not leave that relationship implicit. Only claim course emphasis from inspected evidence.

## Keep the chosen language readable

In Chinese notes, give a canonical English term/acronym at its first useful appearance, then
use a stable Chinese term or familiar acronym naturally. Do not make the body drift into
English or code identifiers merely because the source does. Explain compact technical
phrases such as "bootstrap", "normalise" or "conditional expectation" when the argument
needs them. Formal precision and a plain-language interpretation should reinforce each other.

`exam_answer_language` selects the language of eligible model-answer snippets; it does not
require one after every example. Apply the question-type rules in `exam-review.md`.
Apply `include_code` from `note-presentation.md` before importing implementation material.

## Review the chapter as a reading experience

After checking the K/Q ledger, read the final body in order with the source and chat closed.
For each major transition, check whether the previous explanation gives the next section's
needed vocabulary, quantities and motivation. Trace the central example from setup to result.
Then reopen sources to resolve gaps. Inspect at least the opening and the most conceptually
demanding transition; a full-chapter readability claim requires reading the whole chapter.

Record concrete breakpoints and repairs in the second-pass companion: an undefined dependency,
an abrupt change of object/notation, a comparison with an unexplained side, a missing step,
or an exercise/answer/code block interrupting the argument. Several individually correct
sections can still fail this review. A word count, formula count or all-green K ledger is not
evidence of coherent teaching. `qa.teaching_depth` stays pending/fail until material reading
gaps are repaired; explicitly scoped refresher sheets retain their declared prerequisites.
