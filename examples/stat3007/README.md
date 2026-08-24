# STAT3007 example

This example exercises the `pre-review-notes` workflow on the public
[STAT3007/STAT7007 Deep Learning course page](https://yenan.github.io/teach/stat3007/index.html).

## Contents

- `slides/` — source metadata and `manifest.csv` for 33 unique slide URLs corresponding to 34 lecture rows. The original PDF files are intentionally not stored in Git.
- `notes/chapter-01-regression.tex` — English LaTeX source.
- `notes/chapter-01-regression-zh.tex` — Chinese LaTeX source. The first occurrence of specialised terms keeps the English name, such as `Ordinary Least Squares (OLS)` and `Ridge Regression`.
- `notes/pdf/` — compiled English and Chinese PDFs for direct viewing.
- `notes/progress.md` — evidence boundary and delivery status.
- `notes/topic-map.svg` — the course topic overview produced during planning.

## Evidence boundary

The public page supplied lecture slides but no grading breakdown, exam format,
past papers, or official answer keys. The example therefore demonstrates
source-grounded lecture-note production and does not claim an exam ranking or
assessment weight that was not available.

The slide PDFs are third-party local test inputs. Copyright remains with the
original course/source, and users should follow the source page's terms and
educational-use limits when obtaining them locally.

## Rechecking the slide set

`slides/README.md` contains the source page, expected unique-file count, and
page/byte totals. `slides/manifest.csv` records each original URL and SHA-256
hash so a local copy can be checked with a standard checksum tool.
