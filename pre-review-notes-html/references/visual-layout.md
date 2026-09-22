# Browser layout and interaction gate

Use normal-flow figure/caption/source blocks, proportional images, no cropped fixed-height
containers, absolute overlays or text wrapping over diagrams. Dense originals need a readable
local full-size image link or meaningful labelled panels, not only a tiny responsive thumbnail.
Keep axes, legends and annotations intact; explain any scrollable table region. Dark themes
must not invert scientific-image colours. Preserve a neutral backing for transparent diagrams.

Open the actual generated index.html in an available browser. Inspect desktop width and a
narrow phone-sized viewport (about 375 CSS pixels), and zoom text to check reflow. Verify:

- complete Chinese glyphs, MathML notation, code and long-source-link wrapping;
- every V ID at normal reading size and full image size, all edges/labels and adjacent captions;
- headings/anchors, local images and optional external reading links correctly identified;
- Tab focus and Enter/Space on summaries, answer visibility before/after folding;
- all-answer controls when enabled, and native answers without JavaScript;
- content/figures/math with network unavailable; no required CDN fonts or renderers;
- chosen theme, contrast and focus indicators, with no page-wide horizontal overflow.

Record the artifact hash, browser/version, actual viewport and screenshot/observations per
visual and interaction checked. Browser access, network blocking or scripting toggles may be
unavailable; mark the unperformed check pending, not pass. Geometry checks and static asset
checks are useful evidence with narrower scope than visual inspection. Recheck changed
sections and all affected assets after each build.
