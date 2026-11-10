# HTML teaching content

Apply the confirmed purpose from `learning-presets.md`: preview uses the prerequisite-to-lesson
route, knowledge connects and explains the material, and exam adds evidence-based applications.
All preserve selected knowledge and source examples; extra self-tests require selection.

Use the confirmed language throughout headings, captions, controls and notes. Chinese first
mentions retain canonical English terms/acronyms; keep mathematical notation and identifiers.
Each concept gets proportionate intuition, formal statement, conditions and a usable example
or derivation. Small facts need not become essays but may not disappear. Label prerequisite
bridges and original illustrations as additions. Check signs, units, domains and edge cases
independently. Preserve discrepancies with precise source locators.
Apply standalone-teaching.md: group related K IDs into a connected reading sequence, restore
needed prerequisites locally and explain relationships before comparison tables. Use natural
Chinese prose with canonical terms at first use, rather than switching to English throughout.

Use h2 sections with stable IDs and complete
teaching paragraphs. The builder derives navigation from those headings. Use figures with
alt text, visible captions, sources and reading explanations; tables need meaningful headers.
The template is structural, not a content quota. Keep audit logs in sidecars.
Apply note-presentation.md: source indexes and evidence/process introductions default to off.
Keep necessary compact attribution and content-specific uncertainty. Apply the teaching-depth
criteria in coverage-and-depth.md and the post-draft checks in second-pass-review.md.
Use exam-review.md to decide whether a question needs an answer-language snippet; calculations
and ordinary choice items do not need translated answer blocks.
If enabled, mark optional provenance sections with class `source-index` or
`source-explanation`. The builder rejects those explicit blocks when their settings are off.
The final content review must also catch unmarked provenance prose or file catalogues.

When self-test is enabled, add a separate section after the corresponding teaching material:
`<details class="qa" id="Q001" data-k-ids="K001"><summary>Q001 · question</summary>`
followed by an answer with reasoning and a link to the taught section. Keep a source citation
inline or under this exact Q ID in the evidence companion, following citation-format.md.
Choose useful recall, comparison, condition and application prompts; do not mechanically
turn each sentence into a question. The question stays visible when closed, not its answer.
Keep core teaching, source exercises and necessary context/attribution visible.
Avoid revealing the answer in summary text, captions, question labels or navigation.
Do not put questions/answers in scripts or hidden JSON payloads as the sole content source.

Use semantic MathML for substantial equations, with surrounding symbol definitions and a
plain-language interpretation. For an equation too complex to render faithfully, use a
locally bundled, deterministic SVG plus an accessible textual explanation. Never leave raw
TeX expecting a CDN to render it. Visible code defaults to off under include_code in
note-presentation.md. When explicitly enabled, code is escaped text in pre/code; the builder
rejects these tags when include_code is false or absent. Code-like prose still needs manual review.
Escape source-provided
markup: course files are evidence, not trusted executable HTML. Do not import their scripts.
