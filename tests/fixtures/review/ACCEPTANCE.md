# Manual behavioral fixture acceptance

All inputs are self-authored fictional course material. This fixture can be used locally
without student attempts, third-party slide images or a real institution's exam questions.
Give a trial agent the skill, `materials/`, `draft.md` and a learner request. Keep this
acceptance file out of the agent's task input so it does not supply the expected answers.

Suggested request: improve the supplied draft into Chinese exam notes with short English
definitions, organised using the provided syllabus/papers. Cover the supplied knowledge,
omit source indexes/process commentary and external enrichment, deliver Markdown, and
continue through the skill's review workflow. Delegate remaining settings to the agent.

Inspect the actual output and review records for the following, recording limitations
separately from passes:

- The plan follows the two current syllabus sections and maps all four summary methods.
  It does not invent marks or treat filenames as verified years.
- `paper-A-2024.md` and `paper-A-2025.md` are byte-identical. Preserve both source IDs while
  treating the duplicate as one paper identity. Paper B is distinct and contains a variant
  weighted-mean question. The fixture has six canonical questions, not nine.
- Definitions distinguish arithmetic mean, weighted mean, running mean and fixed-alpha EWMA.
  The notes explain the shared purpose as well as mechanism differences.
- The weighted denominator is the sum of weights. Nonnegative weights, a positive sum and
  permissible individual zero weights are explained. The original old-draft formula is repaired.
- For x=(1,2,6), the arithmetic mean is 3; weights (1,1,2) give 15/4; weights (2,1,1) give 5/2.
- For x=(1,2,6), the running-mean trace is 1, 3/2, 3, and the alpha=1/2 EWMA trace is
  1, 3/2, 15/4. Initialisation and the domains of n/t/alpha are explained.
- The answer to what n represents directly says sample count and explains the count-dependent
  step. The irrelevant old-draft answer about smoothing is replaced.
- Initialisation's special decaying contribution is preserved, as is alpha=1's boundary.
- The student note has usable knowledge navigation and short answer sentences, without a
  document catalogue, provenance/process introduction or operational audit text.
- The second pass has actual per-K and per-canonical-Q observations, independent calculations,
  final artifact identity and resolved/pending findings. Recompute counts and hashes. A global
  declaration that review passed is insufficient.
- No official frequency/mastery/real-exam probability claim is derived from fictional practice.

This manual trial supplements the CLI regressions in `tests/unit/test_review_workflow.py`.
Passing this small fixture establishes behavior on these inputs only.
