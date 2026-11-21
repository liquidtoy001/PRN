# Automatic second pass after drafting

Apply to every generated or substantially revised note, for all three purposes and both formats.
`second_pass_review=automatic` is the default for new work. Once a complete batch draft
exists, notify the learner in their language, for example:

> 笔记初稿已生成，接下来会逐知识点、逐题检查讲解是否完整、解析是否直接回答题目，并修正发现的问题。

Continue the review in the same task without asking for another approval. This is a fresh
source-to-note reading pass. Reopen the final text and original material instead of accepting
the drafting agent's completion statements. If independent reviewers are available and
permitted, they can help; the workflow must also work in a single-agent environment.

## Review every selected knowledge point

Start from the inspected source pages and outcomes, then reconcile the K ledger so omissions
from the ledger itself can be found. Read the note section assigned to each K ID in context.
Use the teaching-depth criteria in `coverage-and-depth.md`. For each point, record the actual
definition/mechanism/example/symbol/boundary check, a precise note location, findings and
`pass`, `fail`, `pending` or a justified `not-applicable` for individual criteria.

Check prerequisites and nearby terminology. Independently calculate worked values and trace
diagram arrows, axes, branches and labels against the prose. For comparisons, verify that
both sides use the same comparison axis and, where helpful, the same small example.
Fix a missing explanation at its teaching location, not solely in a separate audit report.

## Review the continuous reading path

Apply `standalone-teaching.md` in addition to the per-K checks. Read the body in order without
depending on the chat, ledger or original slides. Inspect the opening, every major transition,
the prerequisite map and the central worked example. Can the learner tell why a concept is
introduced, what earlier idea it uses, and how it differs from the nearby alternatives?
Record the actual locations checked and any repaired breakpoints. A sampled reading is
partial, even when all isolated K/Q checks pass. Do not backfill a readability pass for an
older artifact whose review did not inspect continuity.

At a consequential worked step, cover the next line and attempt it using only the preceding
text or figure. Record the input you could locate, the operation you chose, the result
and where an extra hint was needed. For a qualitative section, trace the evidence for the
next inference instead. If it breaks, repair the preceding explanation and retry. This is
an author's reading check; record learner performance only when a learner actually tries it.
On revision, reconcile removed examples, conditions and useful shortcuts with the selected
sources and K IDs. Restore a lost detail where the reader would use it.

Check that source code has not leaked into a code-off chapter, including implementation
identifiers and code-like pseudocode that replace an explanation. Keep mathematical notation
and genuinely needed canonical labels. Check that question/answer blocks sit after their
teaching and do not repeatedly interrupt it. `qa.teaching_depth` requires both local depth
and this continuous-reading check, with unresolved prerequisite gaps recorded explicitly.

## Review every included question and explanation

Use stable Q IDs for source questions/subparts and any explicitly requested generated
questions. Review the question even when only its knowledge is included in the student note:
read the actual stem, identify its requested operation, then attempt an answer using the
mapped note. Record the needed reasoning privately. Do not add a question bank to the note
merely to conduct this check. Restricted active-assessment answers stay pending with a reason.

For each Q ID, check the whole unit: stem/conditions -> requested response type -> answer ->
direct reasoning -> option reasons when present -> eligible answer-language snippet, if any.
Apply the question-type table in `exam-review.md`; record why a separate snippet was included
or omitted. Calculations and ordinary choice items still need reasoning, not an English
restatement of the result. For mixed questions, assess each required operation separately.
Read each second-language snippet on its own. Cut any clause that only translates an
already visible result, while retaining the assessed explanation and any evidence it needs.
Honour a learner's explicit request for full translation.
The explanation must
answer every part of this stem. A correct general paragraph on the same subject is insufficient.
An explanation of an algorithm's process may still fail a question asking what one cell stores.
Review shared concept anchors independently for each different question.

When two in-scope subparts share a topic but ask for different results, swap the draft
answers and identify which requested step or condition is lost. Repair generic answers
that conceal a difference. An identical demand can legitimately reuse its answer.

When the learner requested paired practice and solution copies, match the final rendered
subparts in order by stable ID, including shared stems, diagrams, given values, prefilled
cells and corrections. Attempt each item from the practice view alone, check for exposed
answers, then locate its corresponding solution and verify that it uses the same data.
For folded HTML practice, do this with answers closed and then open the matching answer.
Use this check only for the requested practice format.

For multiple-choice material, establish a unique best answer under the stated conditions.
Verify each All/None component and distinguish a true but incomplete selection from a false
statement. Check length, detail, grammatical fit, unique terminology/formulas, absolute words
and answer-position patterns for accidental clues. Record suspect items and fix substance;
do not force equal lengths or a fixed answer-letter quota. Preserve stable option identities
and existing attempts when correcting only explanations. Flag changes that affect scoring
before attributing an error to the learner.

## Repair, bind the review and report

Use `assets/second-pass-template.md` as a private companion. List every in-scope K/Q ID and
its result, pending items, independent reasoning evidence, and before/after corrections.
Record denominators, not only percentages. With no included questions, record Q review as
not applicable with the reason; still review all K IDs. A sampled check must be labelled partial.

After changing a stem, answer, definition, formula or diagram, recheck all dependent K/Q IDs.
Rebuild requested outputs after corrections and inspect the affected rendered pages/views.
Bind the final review to the final source and artifact SHA-256 values. A later content change
invalidates the affected results; a later render requires renewed layout checks.

Keep coverage, teaching depth, question semantics, citation syntax, visual layout and program
behavior as separate results. Engineering checks cannot supply a semantic pass. Record
`qa.teaching_depth` and `qa.second_pass` only after observed checks, with the companion path.
Do not mark a new automatically reviewed chapter verified/delivered while either is pending.

In the delivery message, remind the learner that the second pass ran, give actual K/Q counts,
summarise substantive repairs and remaining uncertainty, and link the review companion. If
capacity/tool access prevents completion, deliver an explicitly partial draft with the
unreviewed IDs and next action. An explicit request to defer uses `on-request`; retain pending
review results and label the draft accordingly. Never claim automatic semantic correctness.
