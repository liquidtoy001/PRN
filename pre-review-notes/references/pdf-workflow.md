# LaTeX and PDF workflow

Use this workflow whenever a compiled PDF is requested. Keep the editable source beside the
PDF unless the learner explicitly asks for PDF only.

## 1. Compile deterministically

Run from the skill directory or pass an absolute script path:

```text
python scripts/build_note.py path/to/chapter.tex --output-dir output/pdf
```

The helper tries an explicitly requested engine first. In automatic mode it prefers XeLaTeX
for documents containing CJK text and otherwise tries Tectonic, `latexmk`, XeLaTeX, then
pdfLaTeX when available. It emits a machine-readable QA report and renders representative
pages when Poppler is available.

If the platform provides a dedicated LaTeX compiler, it may be used instead, but the checks
below still apply. Do not install a large TeX distribution without the learner's permission.

## 2. Structural and textual checks

Require all of the following before calling the build structurally valid:

- compiler exit code is zero and the expected PDF exists;
- the PDF reopens, is not encrypted, and contains at least one page;
- every page can be traversed without a fatal parser error;
- the source contains no unresolved template placeholders;
- the citation validator passes for required source references.

If a parser is unavailable, report `metadata_unavailable`; do not silently convert that into a
pass.

## 3. Visual inspection

The helper's PNG rendering is preparation for visual inspection, not the inspection itself.
Inspect at minimum the first page, a dense equation/table page, and the final page. Check:

- clipping, overlap, broken tables, and bad page breaks;
- missing CJK glyphs, tofu squares, and font substitution;
- blank or nearly blank pages;
- readable citations, links, headers, and footers;
- consistent margins, hierarchy, and colour contrast.

After any layout-affecting edit, compile and inspect again. Record the visual result in the QA
report or study state only after actually viewing the latest render.

## 4. Failure behavior

If compilation, parsing, rendering, or visual inspection is blocked, deliver the valid source
artifact and state the exact missing step. Never report a PDF as delivered merely because a
`.tex` file exists, and never claim visual QA from a successful compiler exit.
