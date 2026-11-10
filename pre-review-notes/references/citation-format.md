# Print-entry citations

LaTeX: `\sourceref{S001}{PDF p. 18}` for teaching content and
`\assessref{S004}{2023 final Q2(b)}` for assessment evidence.
Markdown: `[source:S001|PDF p. 18]` and `[assessment:S004|2023 final Q2(b)]`.
Use literal calls so `scripts/validate_citations.py` can check syntax and source IDs.
Semantic support still requires comparison with the actual source.

For an explicit request for citation-free body text, put source markers in `evidence.md`
alongside K/Q IDs and exact note locations. Run
`python scripts/validate_citations.py <note> --inventory <inventory.json> --evidence <evidence.md> --report <citation-report.json>`.
The report binds both files' hashes and checks references, while the second pass checks
that the companion supports the final note. Do not use `--allow-empty` as a substitute.
