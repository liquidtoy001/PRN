# 0.2.5 local testing release

Use `dist/pre-review-notes-v0.2.5.zip` in a fresh skill folder and confirm its VERSION.
This release builds on PRN-repo 0.2.0; the other local checkout previously used for the
01--03 trial was 0.1.0. No old generated note is retroactively certified by this update.

Changes: small-batch lightweight teaching; page and knowledge-point coverage ledgers;
animation grouping with preserved intermediate changes; proportionate explanatory expansion;
length-triggered coverage review; separate semantic/reasoning/layout records; quieter
citations, heading orphan prevention, wider margins and readable body typography.

## Behavioral acceptance in another environment

Supply a deck and request lightweight Chinese teaching notes and PDF. Check actual outputs:

1. Each selected physical page is accounted for, with distinct small conditions and remarks
   traceable to note sections. Reconcile against the original, not just the generated ledger.
2. A five-frame diagram becomes a coherent explanation retaining each new step, without
   counting five duplicate frames as five independent topics.
3. Roughly 100 substantive slides producing under ten body pages triggers a documented
   coverage review; title pages and whitespace do not count toward the diagnostic.
4. Where formulas or figures are wrong, an independent derivation supports a cited correction.
   In the historical 01--03 trial, check 1-NN piecewise-constant predictions and ties, all
   decision-boundary regions, and SVM C scaling against the actual original pages.
5. Printed and physical page locators remain correct when overlays duplicate slide numbers.
6. Citations pass syntax checks AND support their claims. Layout has no orphan headings,
   tiny spillover pages or stale render evidence. Missing checks remain visibly incomplete.

These are manual acceptance cases, not claims that a fresh model run has passed them.
Existing automated unit tests cover script behavior; they do not establish teaching quality.
This package is for local testing, with no remote tag or public release implied.
