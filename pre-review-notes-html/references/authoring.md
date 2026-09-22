# HTML teaching content

Use the confirmed language throughout headings, captions, controls and notes. Chinese first
mentions retain canonical English terms/acronyms; keep mathematical notation and identifiers.
Each concept gets proportionate intuition, formal statement, conditions and a usable example
or derivation. Small facts need not become essays but may not disappear. Label prerequisite
bridges and original illustrations as additions. Check signs, units, domains and edge cases
independently. Preserve discrepancies with precise source locators.

Use a short evidence-boundary introduction, then h2 sections with stable IDs and complete
teaching paragraphs. The builder derives navigation from those headings. Use figures with
alt text, visible captions, sources and reading explanations; tables need meaningful headers.
The template is structural, not a content quota. Keep audit logs in sidecars.

When self-test is enabled, add a separate section after the corresponding teaching material:
`<details class="qa" id="Q001" data-k-ids="K001"><summary>Q001 · question</summary>`
followed by an answer with reasoning, a source citation and a link to the taught section.
Choose useful recall, comparison, condition and application prompts; do not mechanically
turn each sentence into a question. The question stays visible when closed, not its answer.
Do not hide core teaching, source exercises or citations needed to understand the body.
Avoid revealing the answer in summary text, captions, question labels or navigation.
Do not put questions/answers in scripts or hidden JSON payloads as the sole content source.

Use semantic MathML for substantial equations, with surrounding symbol definitions and a
plain-language interpretation. For an equation too complex to render faithfully, use a
locally bundled, deterministic SVG plus an accessible textual explanation. Never leave raw
TeX expecting a CDN to render it. Code is escaped text in pre/code. Escape source-provided
markup: course files are evidence, not trusted executable HTML. Do not import their scripts.
