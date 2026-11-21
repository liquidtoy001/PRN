# Exam-specific configuration and paper identity

Read this when purpose is `exam`. Build the configuration from the learner's supplied
papers, current syllabus, instructor revision guidance or topic checklist before drafting.
The intake may proceed with any one of these. Record missing evidence in the delivery
message and internal plan. Ask only when a conflict changes the agreed scope or structure.

## Derive the plan from the supplied evidence

Save a local `exam-plan.md` with source IDs and exact locators for each decision:

| Available evidence | Supported use | Limit |
|---|---|---|
| Current syllabus, assessment specification or instructor checklist | Included/excluded topics, learning outcomes and explicit emphasis | Topic inclusion alone does not establish frequency or marks |
| Verified past paper or official sample | Section structure, assessed operations, answer language and observed depth | Historical marks and sections describe that paper until current applicability is verified |
| Marking guide or official solution | Rewarded steps, terminology and answer length | Independently check reasoning and retain withdrawn/ambiguous items |
| Lecture, lab, notebook or weekly quiz | Knowledge, prerequisites and practical mechanisms | Confirm whether a quiz is official before using it as assessment evidence |
| Learner corrections and attempted answers | Individual gaps and useful comparisons | Personal difficulty does not establish official frequency |

For `exam_organisation=source-led`, use verified current exam Sections when available.
Otherwise use the syllabus outcomes or checklist groups. If only historical papers are
available, label their structure provisional in the plan and reconcile it with current
course scope. Fall back to prerequisite-aware topic chapters when no supported structure
exists. Never invent Section numbers, marks or an institution's exam format.

Keep each knowledge topic together: definitions, mechanisms, comparisons, calculations and
diagrams may all test the same topic. Map every selected lecture/lab/checklist K ID into the
chosen structure, including knowledge absent from past papers. Give unmatched topics a
clearly named supplementary section rather than dropping them. Extract lab knowledge as
inputs, outputs, assumptions, implementation decisions and evaluation. Apply `include_code`
from `note-presentation.md`; selecting a lab for knowledge coverage does not opt into code.

Set `exam_basis_source_ids` to the inspected sources used to resolve the plan. Set
`exam_answer_language` from verified assessment instructions or the learner's preference;
otherwise leave it null and use the note language. This is a language preference, not an
instruction to translate every answer. Retain canonical terms alongside plain-language
explanations and select the response form below.

External papers and other courses enter only through the agreed scope/enrichment setting.
A request to use only supplied course material resolves enrichment to `off`. Show the resolved
structure, coverage boundary, language and priority basis together during intake; preserve
explicit user choices. `topic-led` remains available when the learner prefers topic chapters.

## Match answer form to the actual question

For each subpart, identify the deliverable, the given conditions it depends on and the
reasoning needed to obtain it. Similar stems may share an explanation of the principle.
Give each its own requested result or application. For instance, counting all terms of an
N-point direct DFT counts N samples for each of N coefficients. Counting all products of
a direct full linear convolution counts pairs from inputs of lengths N and M. Name the
operation and the two sets being counted before giving the cost. If an unspecified
convention changes the answer, state the assumption and illustrate the consequential
alternatives. Use a verified marking guide when available. Without one, describe a
concise prose answer as an example and avoid promises about marks.

Distinguish an explicitly excluded exam topic, a prerequisite still needed for an included
topic, and a topic whose assessment status is unknown. Record the source of the decision
in the exam plan. A long lab or a past appearance alone does not establish current scope.

Classify each question/subpart by the operation its stem requests, including mixed questions.
Keep the teaching in the note's language. A separate answer-language snippet is useful only
when the learner must compose assessed prose and its wording adds value:

| Required response | What belongs in the note | Separate answer-language snippet by default |
|---|---|---|
| Calculation, substitution, table update, numerical probability | Setup, steps, units/conditions, final value or table and interpretation | No; do not translate the result again |
| Choice, multiple choice, bare true/false | Selection and explanation of the relevant options/conditions in the note language | No; keep exact option labels when needed |
| Naming/listing a method or label | The requested canonical names and a useful local explanation | No; terminology is already the answer |
| Definition, explanation, comparison, justification, argument | Coherent teaching first; then a short, faithful model response when exam wording/language matters | Optional, only for the assessed prose requirement |
| Drawing or tracing a process | Labelled construction, intermediate states/arrows and result | No unless a separate prose justification is requested |
| Programming/code interpretation | Apply the confirmed code setting; otherwise teach the mechanism without a listing and flag any deferred code-dependent requirement | No automatic English paraphrase |

For "calculate and explain", keep the worked result once in the main answer. A useful
exam-language sentence starts at the reasoning the learner must express. For example,
after two update values, a prompt asking *when they agree* calls for the equality
condition. Repeating both values in English adds nothing to that condition. Include a
number in the snippet when it is evidence for the requested argument or the learner
explicitly asks for a complete model response.
For "true/false and justify", the justification may qualify; the bare selection does not.
This restriction removes redundant translated answers, not the reasoning needed to understand
a calculation or choice. If the main language already matches the exam language, do not repeat
the same answer in a second box. Explicit translation or language-practice requests override
this default. A broad saved preference for "English answers" should be presented using these
question-type semantics unless the learner explicitly wants every answer translated.

When an option mentions an unfamiliar neighbouring method, give the minimum local explanation
of what it does and which input/assumption decides the selection. A category label alone
does not explain the option. Keep this bridge proportional to the decision, not a new chapter.

Place eligible snippets after the corresponding complete teaching/application, not between
reasoning steps. Keep one useful response per distinct prose demand instead of repeating
equivalent answers for every reused paper. Record response type and inclusion/omission reason
in the private Q review; do not print an audit label for every decision.

## Identify papers before counting recurrence

`inventory_materials.py` reports byte-identical `duplicate_groups`. Retain every source ID
and filename; choose a canonical paper identity in the plan instead of deleting files.
Different hashes do not establish different papers. For scanned, annotated, re-exported or
renamed copies, compare all question stems, data, diagrams, subparts and order using complete
extraction/OCR and visual inspection. Filename years and sampled PDF text are insufficient.

Record a paper-identity table with source IDs, verified provenance/year/session, canonical
paper ID, relation (`same-paper`, `variant`, `distinct`, `unresolved`) and comparison evidence.
For partial overlaps, retain question/subpart identities and map each occurrence. An answer
book, student's filled copy and clean copy of one paper count as one assessment event.
A genuine new administration may reuse a question: retain both events and disclose reuse.
Preserve changes to numeric values/conditions as variants. Unresolved identity stays out of
recurrence counts until resolved.

Distinguish official papers/quizzes, instructor guidance, student writing, assistant answers
and generated mocks. Neither a filename containing `exam` nor an assistant's historical
claim proves official status. Mocks and answer paraphrases cannot increase official frequency.
Preserve official withdrawal/correction notices and avoid counting withdrawn items as a
current exam expectation.

## Use modest priority labels

Map canonical questions and subparts to K IDs, noting the tested operation and relevant
note section even when question text will not be printed. Use a simple star for a verified
instructor emphasis or recurrence in comparable, deduplicated official material. Record
which basis supports each star. With few papers, say "revision emphasis" or "repeated in
the supplied material". Provide no implied probability forecast.

Keep separate denominators for source knowledge, canonical question/subpart mapping, actual
explanations and learner attempts. A set of papers mapping to the notes does not establish
lecture completeness. A quiz score or exposure count cannot establish course mastery.
