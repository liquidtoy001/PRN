# Final print-page visual layout


Default to a standalone image block in normal document flow, with caption and source kept
together. Reserve the entire block height. Avoid text wrapping, absolute positioning,
negative spacing and overlays for ordinary teaching figures. Custom layouts require explicit
inspection for collisions. Do not add translated labels over original content.

In LaTeX, use a normal `figure` with `[htbp]`, `\centering` and `\includegraphics`.
Bound width by `\linewidth`, retain aspect ratio, and budget height for the image PLUS
caption, source and spacing. Avoid forced `[H]` placement into insufficient space. Do not
apply a second `trim`/`clip` unless intentional and separately verified.

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
