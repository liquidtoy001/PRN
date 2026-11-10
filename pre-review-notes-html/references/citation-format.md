# HTML citations

Use compact literal markers in text: `[source:S001|PDF p. 18]` or
`[assessment:S004|2023 final Q2(b)]`. They may be inside a small span or a link but do not
split one marker across tags. With source indexes off, a plain citation span needs no
source-list section. If the index is enabled, a local source-list anchor can carry the full
title and locator. Remote reading links use verified HTTPS
URLs. A closed answer still contains visible citation text when opened.

The shared citation checker reads text nodes for HTML, excluding comments, scripts and
styles. It verifies source IDs and locator syntax, not semantic support or full coverage.
Use the HTML builder as well to check local anchors/assets; neither replaces source review.

If the user explicitly wants citation-free body text, supply `--evidence evidence.md` to the
builder and citation validator. This local companion has one `## <exact-anchor>` section per
mapped teaching section or question, with K IDs, the claim being supported and literal source
markers. For example, `## Q001` must carry citations supporting Q001's answer. Every uncited
folded answer requires its own mapped anchor. The builder checks anchors/source IDs, bundles
the companion without linking it in the teaching navigation, and records its hash. Manually
verify every claim-to-source association during the second pass. Retain necessary attribution.
