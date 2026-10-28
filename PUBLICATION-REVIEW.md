# Public repository preparation — 2026-10-29

Review target: `liquidtoy001/PRN`, based on main `fbf4ac8` plus the documentation/audit changes
in this preparation commit. Repository visibility is intentionally unchanged (private).

## Checks performed

- Reviewed tracked file inventory, default branch, tags and GitHub Release metadata.
- Scanned 168 historical blobs reachable from origin/main and the eight version tags for a
  limited set of private-key/provider/GitHub credential patterns and concrete personal paths.
  No matches were found. This is a heuristic scan, not a comprehensive secret audit.
- Inspected all nine release ZIPs: no nested PDF, cache or ZIP artifacts, escaping paths or
  matches from the credential patterns used in the attachment check. Downloaded all 16 assets
  and verified their hashes against GitHub's metadata.
- Confirmed original course slide PDFs do not occur in the reachable history. Two historical
  generated note PDF paths do occur; they are early course-derived examples, not source slides.
  The current Chinese example has three pages, no attached files and no author field in its
  PDF metadata. Its editable source uses typeset content and diagrams rather than slide images.
- 28 unit tests passed. Both Skill frontmatter validators and the 13-file shared-resource
  consistency check passed. Local Markdown link checks passed.

## Changes for public readers

- Rewrote both READMEs around choosing a package and starting one chapter.
- Rewrote the Chinese usage guide around download, install, materials, example requests,
  configuration, results and common problems. Development commands moved to DEVELOPMENT.md.
- Added a changelog, a repeatable heuristic publication audit, and a Windows/Linux CI matrix
  for Python 3.10/3.12. The remote CI result must be checked separately after push.
  Initial Windows checkout exposed the reserved device name `PRN`; checkout and run paths
  now use `repository/`. Local clone instructions also specify a non-reserved directory.
- Kept v0.2.10 as recommended current release and v0.2.9 as the last print-only rollback.
  Removed redundant Release pages/assets for v0.0.1, v0.0.2, v0.1.0, v0.2.0, v0.2.7 and v0.2.8
  after a verified local backup. All Git version tags remain; no history rewrite is involved.
  Retained package bytes and checksums are unchanged.

## Limits

This preparation does not establish cross-domain learning effectiveness or semantic accuracy
of generated notes. The prior HTML browser acceptance gaps remain documented. Course-derived
examples are historical trials and must not be presented as guaranteed current quality.
Code/template licensing does not grant rights to redistribute third-party course sources.
