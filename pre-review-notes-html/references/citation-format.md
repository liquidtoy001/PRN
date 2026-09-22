# HTML citations

Keep visible literal markers in text: `[source:S001|PDF p. 18]` or
`[assessment:S004|2023 final Q2(b)]`. They may be inside a small span or a link but do not
split one marker across tags. Link to a local source-list anchor such as `#source-S001` and
give the source title and precise locator there. Remote reading links use verified HTTPS
URLs. A closed answer still contains visible citation text when opened.

The shared citation checker reads text nodes for HTML, excluding comments, scripts and
styles. It verifies source IDs and locator syntax, not semantic support or full coverage.
Use the HTML builder as well to check local anchors/assets; neither replaces source review.
