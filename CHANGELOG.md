# Changelog

## v0.3.0 — release preparation

Prepared 2026-11-10; not yet published. See [release notes](RELEASE-0.3.0.md) and
[validation](TESTING-0.3.0.md). Existing v0.2.10 artifacts remain unchanged.

Keep the PDF and HTML entries, with three explicit purpose presets: preview (new), knowledge
consolidation and exam revision. The first configuration exchange shows the entire active
entry's catalogue in four visible groups, including alternatives and inactive settings;
one reply can accept recommendations or customise them. Purpose is separate from work pace
(first chapter / whole course in chapters / time-limited scope). Saved and explicit choices
take precedence. All presets default to no extra practice; full/exam-cram no longer enable
a bank implicitly. Preview restores prerequisites and a lesson reading route while retaining
complete teaching within the agreed scope. Both configuration validators accept preview.

Teaching-depth acceptance for each knowledge point; exam configuration derived from supplied
papers, syllabus or topic checklist; exact-file duplicate groups plus full-content paper
identity review; automatic post-draft K/Q semantic review with a learner notification.
Source indexes and source/process explanations default to off in the note. Internal evidence
and necessary attribution remain available. Independent interactive HTML workbooks are deferred.

Follow-up from learner feedback: standalone reading paths, local prerequisite
bridges and explicit links between related concepts; connected templates instead of a box
per knowledge item; code shown only by explicit selection (`include_code=false` by default).
Answer-language snippets now depend on the requested response type, with no redundant
translations for calculations or ordinary choice items. Second-pass review also inspects
whole-chapter continuity, separately from per-item correctness and coverage.

Release preparation also found that HTML code markup could bypass a disabled code preference.
The builder now rejects pre/code unless include_code is explicitly true; the rendering fixture
opts into code deliberately, with a regression covering disabled and legacy configurations.

## Repository preparation — 2026-10-29

Beginner-oriented Chinese usage instructions and bilingual README; development commands moved
to DEVELOPMENT.md. Publication audit and CI added. Skill runtime remains v0.2.10.
Releases retain v0.2.10 (current dual entry) and v0.2.9 (last print-only rollback); older
Release pages/assets are locally archived, while their Git tags remain.

## Runtime versions

| Version | Changes |
|---|---|
| v0.3.0 (prepared) | Three purpose presets with one complete intake; standalone teaching, evidence-based exam configuration, paper identity review and automatic second-pass checks. |
| v0.2.10 | Independent offline HTML entry, optional folded questions, shared-resource drift checks and dual packages. |
| v0.2.9 | Separate image extraction and final-layout reviews, crop and render evidence. |
| v0.2.8 | Optional verified paper reading lists and integrated explanations. |
| v0.2.7 | Knowledge/exam purposes and persisted configuration; includes knowledge coverage and original-figure improvements from local 0.2.5/0.2.6 trials. |
| v0.2.0 | Learning banks, mastery/retests, capacity limits and honest usage accounting. |
| v0.1.0 | Inventory, citations, resumable state, PDF tooling and reproducible packaging. |
| v0.0.2 | Language choices, Chinese terminology and initial PDF workflow. |
| v0.0.1 | Initial instructions and templates. |
