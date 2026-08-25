# Evidence and material workflow

## 1. Keep source material outside publishable artifacts

Treat uploaded, downloaded, LMS, and third-party course files as local inputs by default.
Public accessibility is not evidence of a redistribution licence. Do not add them to Git,
skill ZIPs, release assets, or public examples unless the user explicitly authorises that
publication and the licence permits it.

For a reproducible local test, keep only a small manifest in the repository and download the
files into an ignored directory:

```text
python scripts/download_materials.py tests/fixtures/course/materials.csv \
  --output-dir test-data/course/materials
```

The downloader supports CSV or JSON manifests, verifies declared byte sizes and SHA-256
hashes, writes through `.part` files, and never treats a successful download as publication
permission.

## 2. Build a stable inventory

Run `inventory_materials.py` before substantial research. The inventory records a stable
source ID, relative path, byte size, SHA-256 digest, inferred role, and available PDF metadata.
Role inference is only a routing hint and must not be presented as a verified course fact.

Useful source roles include:

- syllabus or assessment specification;
- lecture slides, transcript, or required reading;
- worksheet, tutorial, lab, or practice set;
- assignment or other assessed work;
- past or sample assessment;
- official solution, marking guide, or examiner report.

If a PDF has little extractable text, the inventory marks it `needs_ocr`. Use an available
OCR/PDF tool to create a separate searchable derivative, retain the original unchanged, and
record the derivative path. A missing PDF parser is `metadata_unavailable`, not evidence that
the file is searchable.

## 3. Establish the assessment boundary

Prefer evidence in this order:

1. current official assessment specification or explicit instructor statement;
2. current marking guide and official sample solution;
3. repeated pattern across multiple comparable assessed items;
4. one or two historical items, clearly labelled as a thin sample;
5. lecture coverage or textbook convention, which supports content inclusion but not an exam
   probability claim.

Record whether each priority judgment is `verified`, `limited-inference`, or `unknown`.
Recency matters only when sources are comparable; a newer slide deck does not override an
explicit current assessment statement.

## 4. Citation identifiers and locators

Use the inventory ID, such as `S001`, together with the most precise locator available:

- PDF: physical PDF page and printed slide/page number when they differ;
- assessment: year, paper, question, and subpart;
- transcript or audio: timestamp;
- HTML/Markdown: heading or section anchor;
- code/notebook: filename plus cell or symbol.

LaTeX uses `\sourceref{S001}{PDF p. 18}` for teaching content and
`\assessref{S004}{2023 final Q2(b)}` for assessment evidence. Markdown uses
`[source:S001|PDF p. 18]` and `[assessment:S004|2023 final Q2(b)]`.

Do not cite a filename alone when a page, question, or section exists. If the source itself is
internally inconsistent, cite both locations and explain the discrepancy.

## 5. Source coverage before drafting

Before fixing the chapter order, report which evidence classes are present and missing. In
particular, explicitly say when there are no grading weights, past papers, official solutions,
or current-course confirmation. That boundary must survive into the note header, progress
report, and delivery summary.

Run the material-capacity report after inventory. Its filename-derived role counts are only a
preliminary signal; confirm whether apparent assessment files actually contain current
weights, questions, solutions, or marking guidance. The final quality ceiling must name both
evidence gaps and processing gaps such as OCR failures, encrypted files, or source IDs omitted
from the current chapter subset.
