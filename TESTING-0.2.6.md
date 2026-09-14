# 0.2.6 local testing release

Builds on 0.2.5 with source-visual reuse rules. Install the new ZIP in a fresh skill folder
and confirm VERSION is 0.2.6. Existing coverage, depth, measurement and privacy rules remain.

Manual acceptance cases for the next real generation:

- A dense, readable original chart is included beside its explanation with axes, units,
  legend and exact source locator preserved, and a meaningful reading guide.
- A composite/vector diagram survives extraction or page cropping with arrows and labels
  intact; merely extracting one bitmap layer is insufficient.
- A multi-frame animation retains every informative transition in selected keyframes.
- A redrawn diagram is labelled and compared against the source; a retyped table preserves
  every value, header and footnote. Unreadable values are not invented.
- Decorative and truly redundant figures have explicit omission reasons. Essential unreadable
  visuals remain pending rather than being counted as covered by surrounding prose.
- Final PDF inspection covers all reused/adapted visual pages at readable size. Course images
  remain in local learner output assets and never enter the distributable skill ZIP.

These are behavioral acceptance cases, not claims of a completed teaching-generation test.
