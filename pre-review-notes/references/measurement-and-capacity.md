# Token accounting, material capacity, and quality ceilings

Read this reference before substantial generation and again at delivery. The goal is an
auditable boundary, not a promise that a rough estimate equals provider billing or that a
large context window guarantees full comprehension.

## Capacity gate before generation

The inventory includes model-independent token ranges for extractable text. Run:

```text
python scripts/assess_capacity.py output/materials.json \
  --context-window <known-platform-limit> \
  --reserved-output-tokens <planned-output-and-reasoning-headroom> \
  --output output/capacity-report.json \
  --markdown output/capacity-report.md
```

Use a context limit only when the active platform/model exposes or documents it. Otherwise
omit it; the report must say `unknown` and the workflow must use incremental source subsets.
The estimate does not include image understanding, hidden system instructions, tool payloads,
or provider-specific tokenisation.

Treat the result as follows:

- `fits-estimate`: a full pass may fit, but citations and checkpoints remain mandatory;
- `near-limit`: use chapter subsets and keep output/reasoning headroom;
- `chunking-required`: never claim all sources were considered in one pass; inventory
  globally, retrieve relevant source IDs, and record uncovered material;
- `indeterminate` or `unknown`: resolve OCR/unreadable files or disclose that complete
  coverage cannot be verified.

The report also gives three separate ceilings:

1. **content coverage** — whether the supplied material could be inspected reliably;
2. **exam calibration** — whether assessment-bearing sources can support weighting claims;
3. **answer-depth calibration** — whether official solutions or marking guides exist.

Filename-derived source roles are preliminary routing hints. Verify them before converting a
ceiling into a final claim.

## Mandatory quality notice in every delivered generation

Do not use a generic disclaimer. State the concrete boundary for this artifact:

- selected and omitted source IDs;
- capacity status and whether chunking/retrieval was used;
- OCR, encryption, parsing, or missing-material failures;
- whether exam priority and answer depth are verified, limited, or unavailable;
- the next action that would raise the ceiling.

Passing `capacity_disclosure` QA means the check and disclosure exist; it does not mean the
materials fit or the quality ceiling is high.

## Per-generation token ledger

Immediately after each model-generated note, quiz bank, revision plan, or substantial rewrite,
append one ledger record.

If the platform exposes a response JSON with usage:

```text
python scripts/usage_ledger.py record --ledger output/usage-ledger.jsonl \
  --operation chapter-generation --provider openai --model <exact-model-id> \
  --usage-file output/response.json --artifact <generated-note-file>
```

If the platform exposes only visible files, create a partial estimate:

```text
python scripts/usage_ledger.py record --ledger output/usage-ledger.jsonl \
  --operation chapter-generation --input-file output/selected-source.txt \
  --output-file <generated-note-file>
```

If neither is possible, still record `--unavailable-reason`. Never substitute a character
estimate for provider-reported usage without labelling it `partial-estimate`. A partial input
estimate omits system instructions, conversation history, tools, images, and hidden reasoning.

Monetary cost is optional and requires an explicit, dated pricing profile based on
`assets/pricing-template.json`. Do not hardcode market prices into the skill. API token price,
subscription limits, credits, service tiers, long-context multipliers, and tool-call fees are
not interchangeable. The ledger calculation is an estimate, not an invoice.

Summarise a ledger with:

```text
python scripts/usage_ledger.py summary --ledger output/usage-ledger.jsonl
```

Passing `usage_accounting` QA means a record exists and its accuracy class is disclosed; it
does not imply exact provider usage or a complete monetary bill.
