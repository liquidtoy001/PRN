# STAT3007/STAT7007 Deep Learning slides

Source: <https://yenan.github.io/teach/stat3007/index.html>
Course page: Semester 1, 2022, Nan Ye, The University of Queensland
Downloaded: 2026-08-10 (Australia/Brisbane)

## Coverage

- The course page contains 34 lecture rows with a `slides` link.
- Lecture 32 and Lecture 33 both point to `32-rl2.pdf`.
- `manifest.csv` records all 33 unique PDF files referenced by the page; the PDF binaries are intentionally omitted from Git and Releases.
- Total size: 85,660,004 bytes.
- Total physical PDF pages: 869. Beamer overlays mean this can exceed the logical
  slide number printed in some decks.

See `manifest.csv` for the lecture-to-file mapping, source URLs, page counts,
file sizes, and SHA-256 checksums.

## Verification

During the original local test, the 33 files were reopened with `pypdf` in non-strict mode and every physical
page was traversed for text extraction. All files:

- begin with a PDF header and end with an EOF marker;
- are unencrypted;
- have at least one page and extractable text on every page;
- completed traversal without a fatal parser or extraction error.

Some source decks contain duplicate `/ToUnicode` entries in embedded font
dictionaries. `pypdf` reports these as non-fatal warnings; they did not prevent
page traversal, text extraction, or Poppler rendering.

For visual QA, page 1 of every deck was rendered with Poppler, along with
representative internal pages containing equations, diagrams, and dense text.
No clipping, blank rendering, missing glyph blocks, or obvious corruption was
observed in that sample.
