# Development

Python 3.10+ is required for the included CLI tools. Most checks use the standard library.
PDF metadata and traversal require `pypdf`; PDF compilation requires an available LaTeX engine,
and representative rendering requires Poppler. These are optional for HTML-only generation.
Read [USAGE.md](./USAGE.md) for the learner workflow.

On Windows, `PRN` is a reserved device name. Choose a normal local clone directory:

```text
git clone https://github.com/liquidtoy001/PRN.git pre-review-notes-dev
cd pre-review-notes-dev
```

CI downloads the tested commit's source archive into a non-reserved directory under the
runner's temporary directory; even GitHub's default workspace parents contain `PRN`.

## Shared resources

Edit canonical files in `shared/`, then materialise and check the copies:

```text
python tools/sync_shared.py
python tools/sync_shared.py --check
python -m unittest discover -s tests/unit -v
python -m compileall -q pre-review-notes/scripts pre-review-notes-html/scripts shared/scripts tools
```

Both installable folders contain complete copies, so neither needs its sibling at runtime.
Keep format-specific configuration, templates and layout rules in the relevant skill.
Use UTF-8 when running external skill validators on Windows.

## Build installation packages

```text
python tools/package_skill.py
python tools/package_skill.py --skill-dir pre-review-notes-html
```

Both flattened ZIPs and SHA-256 files are written to ignored `dist/`.
Never place the output directory inside a skill. A versioned Release asset must not be silently
replaced with different bytes; publish a new version when runtime files change.

## Reproduce a local course fixture

```text
python pre-review-notes/scripts/download_materials.py tests/fixtures/stat3007/materials.csv --output-dir test-data/stat3007/slides
```

Downloads are local third-party inputs. The manifest specifies expected sizes and SHA-256 hashes;
it does not grant redistribution rights. Never commit those PDFs or private learner state.
The original HTML fixture in `tests/fixtures/html/` can be used without third-party course data;
its build command is documented in [TESTING-0.2.10.md](./TESTING-0.2.10.md).

## Publication checks

```text
python tools/audit_publication.py --report dist/publication-audit.json
```

The audit checks tracked Markdown links and scans blobs reachable from origin/main and tags
for a limited set of credential/path patterns. It reports locations without printing secret
values. It is a heuristic check, not a security certification. Recheck the remote repository,
release attachments and intended public branches before changing visibility.

See [TESTING.md](./TESTING.md) for test scope and the manual teaching-quality evaluation plan.
