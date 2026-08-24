# STAT3007 local test fixture

This fixture stores metadata only. It does not contain or redistribute the course slide PDFs.

- Course page: <https://yenan.github.io/teach/stat3007/index.html>
- Manifest: `materials.csv`
- Unique files: 33 for 34 lecture rows; Lectures 32 and 33 share one PDF
- Expected total size: 85,660,004 bytes
- Expected physical PDF pages: 869

Download into the ignored local test-data directory:

```powershell
python pre-review-notes/scripts/download_materials.py `
  tests/fixtures/stat3007/materials.csv `
  --output-dir test-data/stat3007/slides
```

Verify an existing local copy without network access:

```powershell
python pre-review-notes/scripts/download_materials.py `
  tests/fixtures/stat3007/materials.csv `
  --output-dir test-data/stat3007/slides `
  --verify-only
```

The manifest records source URLs, expected page counts, byte sizes, and SHA-256 hashes. Page
counts are reference metadata; the downloader verifies bytes, hashes, and PDF headers. A
successful download or checksum match does not establish redistribution rights.
