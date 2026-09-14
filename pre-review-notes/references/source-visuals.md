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

Compare source and derivative, then inspect the final PDF pages containing reused or adapted
visuals at readable size. Check legibility, clipping, aspect ratio, values, labels, placement,
caption association and source locator. Check the explanation against what the figure actually
shows. Record V IDs and observations in `review.md`. A successfully embedded file does not
prove visual fidelity. Report pending essential visuals as incomplete coverage even when all
surrounding text has been drafted.
