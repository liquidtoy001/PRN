# Print-entry citations

LaTeX: `\sourceref{S001}{PDF p. 18}` for teaching content and
`\assessref{S004}{2023 final Q2(b)}` for assessment evidence.
Markdown: `[source:S001|PDF p. 18]` and `[assessment:S004|2023 final Q2(b)]`.
Use literal calls so `scripts/validate_citations.py` can check syntax and source IDs.
Semantic support still requires comparison with the actual source.
