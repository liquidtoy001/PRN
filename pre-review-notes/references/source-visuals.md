# Source figures, charts and tables

## Select for teaching value

Inspect the visuals on every selected page, including vector diagrams and tables that are
not embedded bitmap images. Prefer incorporating an existing informative visual over merely
summarising it or inventing a substitute. Typical candidates include algorithm steps, model
architectures, geometric explanations, decision boundaries, experimental comparisons and
worked-example figures. Judge the visual's teaching role, not just its size or colour.

Record each candidate with a stable V ID, source ID, physical page and printed slide locator,
linked K IDs, intended note section, asset path and disposition in `coverage.md`. Dispositions
are reused, cropped, redrawn, keyframes, omitted or pending. Give reasons for omissions such
as decoration, true duplication or information completely conveyed elsewhere. Do not omit a
useful figure solely to keep the note short. Unreadable essential visuals remain pending.

## Preserve and prepare

- Reuse a clear original figure. Extract it where reliable; otherwise render the PDF page
  with an available PDF tool and crop a separate derivative. Composite/vector diagrams may
  need page rendering to preserve arrows, labels and overlays. Inspect the actual result.
- Crop irrelevant margins or slide chrome, retaining axes, units, legends, annotations,
  panel labels, captions and source credits needed to interpret the figure. Keep aspect ratio.
  Retain the original file unchanged; store derivatives in the learner's local output assets.
- For dense figures, use a wider placement or meaningful labelled panels instead of shrinking
  everything to illegibility. Prefer vector output where supported, or enough raster resolution
  for labels to remain readable at final PDF size. Upscaling cannot recover missing detail.
- Redraw only when it improves readability or the original cannot be reused suitably. Mark
  the result as redrawn/adapted and compare it against the original: values, axis scales,
  units, arrow direction, topology, proportions and class boundaries must remain faithful.
  Never invent values from a low-resolution chart. State when a reconstruction is schematic.
- For animation sequences, select the frames needed to explain each substantive change.
  Use a labelled sequence or composite with accompanying steps. Do not keep only the final
  frame if intermediate states carry knowledge, or repeat unchanged frames unnecessarily.
- Tables may be faithfully typeset for readability. Preserve headers, units, footnotes,
  numeric precision and meaningful emphasis; verify every transcribed cell against the source.

Use deterministic extraction, cropping or drawing tools for scientific evidence. Do not use
generative image reconstruction to reproduce exact source charts, numerical tables or labels.
If required tools or source resolution are insufficient, disclose the specific limitation.

## Explain and attribute

Place the visual near the concept or example it supports. Give a caption in the note language,
a stable source ID and precise physical page locator using the normal citation syntax, and
state whether it is original, cropped, redrawn or assembled from keyframes. Keep original
labels readable; add a translated legend beside the figure if useful, without obscuring it.

Explain what the axes, legend and symbols represent, what to observe or compare, and how
that observation supports the conclusion. For an example, connect the visual to the solution
steps. Use proportionate detail: a simple diagram needs less explanation than a multi-panel
experiment. Mark added highlights and supplementary interpretation so they are not mistaken
for instructor annotations. If the original is inconsistent, cite and explain the discrepancy.

Source attribution does not grant redistribution rights. Apply the skill's existing private
material boundary to both originals and crops; do not include course images in the skill ZIP.

## Verify the rendered result

### Gate 1: extraction completeness

Before insertion, compare the derivative with the original page. Check all four edges,
axes, tick labels, units, legends, arrows, panel labels and relevant footnotes. Leave a
small visible safety margin appropriate to the figure instead of cropping tightly against
marks. For composite diagrams, render the full page and crop if object extraction loses
text or vector layers. Never call a partial bitmap extraction the complete figure.

Record V ID, source physical page, extraction method, derivative path, and crop rectangle
with units, coordinate origin and page dimensions (or full-page/no crop). Include rotation
or scaling when relevant. Keep original inputs intact. Mark the gate pass/fail/pending with
actual observations; repair or disclose incomplete essential figures before delivery.

### Gate 2: final-page layout

Default to a standalone image block in normal document flow, with caption and source kept
together. Reserve the entire block height. Avoid text wrapping, absolute positioning,
negative spacing and overlays for ordinary teaching figures. Custom layouts require explicit
inspection for collisions. Do not add translated labels over original content.

In LaTeX, use a normal `figure` with `[htbp]`, `\centering` and `\includegraphics`.
Bound width by `\linewidth`, retain aspect ratio, and budget height for the image PLUS
caption, source and spacing. Avoid forced `[H]` placement into insufficient space. Do not
apply a second `trim`/`clip` unless intentional and separately verified. In HTML/PDF use
normal-flow image blocks with proportional sizing; avoid fixed-height clipped containers.

Move oversized blocks to a figure page, use landscape, or split into labelled panels with
shared legends preserved. Do not shrink dense labels until unreadable. If an image already
includes its caption, avoid duplicate captions while retaining source attribution.

Render and inspect EVERY final page containing a figure at normal reading size and zoom in
to verify edges and labels. Check body text, captions, headers and footers do not cover the
figure; verify its correct explanation and caption are adjacent. Record final PDF page,
PDF hash/build and fresh render path per V ID. After edits, rebuild and recheck all affected
pages, including pages shifted by reflow. Old renders cannot certify a new PDF.

Geometry/text-overlap detection may flag candidates, but labels inside a figure are valid
overlaps and cannot be treated as automatic failures. Compiler success and automated bounds
checks cannot replace visual review. Both gates must pass before declaring a visual complete;
unresolved clipping, obstruction or unreadability stays fail/pending, with the specific limit
disclosed. These are manual review requirements, not new automated guarantees.

Compare source and derivative, then inspect the final PDF pages containing reused or adapted
visuals at readable size. Check legibility, clipping, aspect ratio, values, labels, placement,
caption association and source locator. Check the explanation against what the figure actually
shows. Record V IDs and observations in `review.md`. A successfully embedded file does not
prove visual fidelity. Report pending essential visuals as incomplete coverage even when all
surrounding text has been drafted.
