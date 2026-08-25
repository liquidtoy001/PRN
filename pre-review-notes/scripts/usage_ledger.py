#!/usr/bin/env python3
"""Record per-generation token usage and optional monetary estimates."""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from token_estimation import estimate_file_tokens


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON root must be an object")
    return raw


def nonnegative_integer(value: Any, name: str, *, allow_none: bool = False) -> int | None:
    if value is None and allow_none:
        return None
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a non-negative integer")
    try:
        integer = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a non-negative integer") from exc
    if integer < 0 or integer != value:
        raise ValueError(f"{name} must be a non-negative integer")
    return integer


def find_usage(raw: dict[str, Any]) -> dict[str, Any]:
    if isinstance(raw.get("usage"), dict):
        return raw["usage"]
    response = raw.get("response")
    if isinstance(response, dict) and isinstance(response.get("usage"), dict):
        return response["usage"]
    if "input_tokens" in raw or "output_tokens" in raw:
        return raw
    raise ValueError("usage JSON has no supported usage object")


def parse_provider_usage(path: Path) -> dict[str, int]:
    usage = find_usage(read_json(path))
    input_details = usage.get("input_tokens_details")
    if not isinstance(input_details, dict):
        input_details = {}
    output_details = usage.get("output_tokens_details")
    if not isinstance(output_details, dict):
        output_details = {}
    input_tokens = nonnegative_integer(usage.get("input_tokens"), "input_tokens")
    output_tokens = nonnegative_integer(usage.get("output_tokens"), "output_tokens")
    cached = nonnegative_integer(input_details.get("cached_tokens", 0), "cached_tokens")
    cache_write = nonnegative_integer(
        input_details.get("cache_write_tokens", 0), "cache_write_tokens"
    )
    reasoning = nonnegative_integer(
        output_details.get("reasoning_tokens", 0), "reasoning_tokens"
    )
    total = nonnegative_integer(
        usage.get("total_tokens", input_tokens + output_tokens), "total_tokens"
    )
    if total < input_tokens + output_tokens:
        raise ValueError("total_tokens cannot be smaller than input_tokens + output_tokens")
    if cached > input_tokens:
        raise ValueError("cached_tokens cannot exceed input_tokens")
    if reasoning > output_tokens:
        raise ValueError("reasoning_tokens cannot exceed output_tokens")
    return {
        "input_tokens": input_tokens,
        "cached_input_tokens": cached,
        "cache_write_tokens": cache_write,
        "output_tokens": output_tokens,
        "reasoning_tokens": reasoning,
        "total_tokens": total,
    }


def estimate_files(paths: list[Path], label: str) -> tuple[dict[str, int], list[dict[str, Any]]]:
    totals = {"lower": 0, "estimate": 0, "upper": 0}
    details: list[dict[str, Any]] = []
    for path in paths:
        result = estimate_file_tokens(path)
        detail = {"path": str(path.resolve()), "estimate": result}
        details.append(detail)
        if result.get("status") != "estimated":
            raise ValueError(f"cannot estimate {label} file {path}: {result.get('reason')}")
        totals["lower"] += int(result["lower_bound_tokens"])
        totals["estimate"] += int(result["estimated_tokens"])
        totals["upper"] += int(result["upper_bound_tokens"])
    return totals, details


def parse_manual_usage(args: argparse.Namespace) -> dict[str, int]:
    input_tokens = nonnegative_integer(args.input_tokens, "input_tokens")
    output_tokens = nonnegative_integer(args.output_tokens, "output_tokens")
    cached = nonnegative_integer(args.cached_input_tokens, "cached_input_tokens")
    cache_write = nonnegative_integer(args.cache_write_tokens, "cache_write_tokens")
    reasoning = nonnegative_integer(args.reasoning_tokens, "reasoning_tokens")
    total = nonnegative_integer(
        args.total_tokens if args.total_tokens is not None else input_tokens + output_tokens,
        "total_tokens",
    )
    if cached > input_tokens:
        raise ValueError("cached_input_tokens cannot exceed input_tokens")
    if reasoning > output_tokens:
        raise ValueError("reasoning_tokens cannot exceed output_tokens")
    return {
        "input_tokens": input_tokens,
        "cached_input_tokens": cached,
        "cache_write_tokens": cache_write,
        "output_tokens": output_tokens,
        "reasoning_tokens": reasoning,
        "total_tokens": total,
    }


def resolve_measurement(args: argparse.Namespace) -> tuple[str, dict[str, Any], dict[str, Any]]:
    exact_sources = int(args.usage_file is not None) + int(
        args.input_tokens is not None or args.output_tokens is not None
    )
    estimated_sources = bool(args.input_file or args.output_file)
    unavailable = args.unavailable_reason is not None
    selected = exact_sources + int(estimated_sources) + int(unavailable)
    if selected != 1:
        raise ValueError(
            "choose exactly one measurement source: --usage-file, manual token counts, "
            "input/output files, or --unavailable-reason"
        )
    if args.usage_file:
        counts = parse_provider_usage(args.usage_file)
        return "provider-reported", counts, {"usage_file": str(args.usage_file.resolve())}
    if args.input_tokens is not None or args.output_tokens is not None:
        if args.input_tokens is None or args.output_tokens is None:
            raise ValueError("manual measurement requires both --input-tokens and --output-tokens")
        return "manually-reported", parse_manual_usage(args), {}
    if estimated_sources:
        input_totals, input_details = estimate_files(args.input_file, "input")
        output_totals, output_details = estimate_files(args.output_file, "output")
        counts = {
            "input_tokens": input_totals["estimate"],
            "cached_input_tokens": 0,
            "cache_write_tokens": 0,
            "output_tokens": output_totals["estimate"],
            "reasoning_tokens": 0,
            "total_tokens": input_totals["estimate"] + output_totals["estimate"],
            "lower_bound_tokens": input_totals["lower"] + output_totals["lower"],
            "upper_bound_tokens": input_totals["upper"] + output_totals["upper"],
        }
        details = {
            "input_files": input_details,
            "output_files": output_details,
            "scope_notice": (
                "Partial estimate covers only the listed files; system instructions, chat history, "
                "tool payloads, reasoning, images, and provider tokenisation may be absent."
            ),
        }
        return "partial-estimate", counts, details
    return (
        "unavailable",
        {
            "input_tokens": None,
            "cached_input_tokens": None,
            "cache_write_tokens": None,
            "output_tokens": None,
            "reasoning_tokens": None,
            "total_tokens": None,
        },
        {"reason": args.unavailable_reason},
    )


def decimal_rate(value: Any, name: str) -> Decimal | None:
    if value is None:
        return None
    try:
        rate = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"pricing field {name} must be numeric or null") from exc
    if rate < 0:
        raise ValueError(f"pricing field {name} must be non-negative")
    return rate


def load_pricing(path: Path | None, model: str | None) -> dict[str, Any] | None:
    if path is None:
        return None
    profile = read_json(path)
    models = profile.get("models")
    if not isinstance(models, dict):
        raise ValueError("pricing profile models must be an object")
    if not model:
        raise ValueError("--model is required with --pricing-file")
    rates = models.get(model)
    if not isinstance(rates, dict):
        raise ValueError(f"pricing profile has no exact model entry for {model}")
    return {
        "currency": str(profile.get("currency") or "USD"),
        "source": profile.get("source"),
        "as_of": profile.get("as_of"),
        "rates_per_million": {
            "input": decimal_rate(rates.get("input_per_million"), "input_per_million"),
            "cached_input": decimal_rate(
                rates.get("cached_input_per_million"), "cached_input_per_million"
            ),
            "cache_write": decimal_rate(
                rates.get("cache_write_per_million"), "cache_write_per_million"
            ),
            "output": decimal_rate(rates.get("output_per_million"), "output_per_million"),
        },
    }


def calculate_cost(
    counts: dict[str, Any], pricing: dict[str, Any] | None, measurement: str
) -> dict[str, Any]:
    if pricing is None:
        return {
            "status": "not-calculated",
            "reason": "No explicit pricing profile was supplied.",
        }
    if measurement == "unavailable":
        return {"status": "not-calculated", "reason": "Token counts are unavailable."}
    input_tokens = int(counts["input_tokens"])
    cached = int(counts["cached_input_tokens"])
    cache_write = int(counts["cache_write_tokens"])
    output_tokens = int(counts["output_tokens"])
    uncached = max(0, input_tokens - cached - cache_write)
    components = {
        "input": uncached,
        "cached_input": cached,
        "cache_write": cache_write,
        "output": output_tokens,
    }
    rates = pricing["rates_per_million"]
    missing = [name for name, tokens in components.items() if tokens and rates.get(name) is None]
    if missing:
        return {
            "status": "not-calculated",
            "reason": f"Pricing profile lacks rates for: {', '.join(missing)}",
        }
    costs: dict[str, str] = {}
    total = Decimal("0")
    for name, tokens in components.items():
        rate = rates.get(name)
        amount = Decimal("0") if not tokens else Decimal(tokens) * rate / Decimal(1_000_000)
        total += amount
        costs[name] = format(amount.quantize(Decimal("0.00000001")), "f")
    return {
        "status": "estimated" if measurement == "partial-estimate" else "calculated",
        "currency": pricing["currency"],
        "amount": format(total.quantize(Decimal("0.00000001")), "f"),
        "components": costs,
        "rates_per_million": {
            name: (str(value) if value is not None else None) for name, value in rates.items()
        },
        "pricing_source": pricing.get("source"),
        "pricing_as_of": pricing.get("as_of"),
        "billing_notice": (
            "This arithmetic estimate is not an invoice. Product plans, service tiers, tools, "
            "long-context multipliers, and provider billing rules may differ."
        ),
    }


def read_ledger(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid ledger JSON on line {line_number}: {exc}") from exc
        if not isinstance(record, dict):
            raise ValueError(f"ledger line {line_number} is not an object")
        records.append(record)
    return records


def write_ledger(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    payload = "".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records)
    temporary.write_text(payload, encoding="utf-8")
    temporary.replace(path)


def update_study_state(
    state_path: Path,
    ledger_path: Path,
    records: list[dict[str, Any]],
    record: dict[str, Any],
    chapter_slug: str | None,
) -> None:
    from manage_state import find_chapter, read_state, validate_state, write_state

    state = read_state(state_path)
    if state.get("schema_version") != 2:
        raise ValueError("study state must be migrated to schema_version 2")
    state["usage"] = {
        "ledger_path": str(ledger_path),
        "generation_count": len(records),
        "last_generation_id": record["generation_id"],
        "last_measurement": record["measurement"],
        "updated_at": record["recorded_at"],
    }
    if chapter_slug:
        chapter = find_chapter(state, chapter_slug)
        if chapter is None:
            raise ValueError(f"unknown chapter slug {chapter_slug}")
        chapter.setdefault("qa", {})["usage_accounting"] = "pass"
    state["updated_at"] = utc_now()
    errors = validate_state(state)
    if errors:
        raise ValueError("; ".join(errors))
    write_state(state_path, state)


def command_record(args: argparse.Namespace) -> int:
    if args.chapter_slug and not args.study_state:
        print("--chapter-slug requires --study-state", file=sys.stderr)
        return 2
    try:
        measurement, counts, measurement_details = resolve_measurement(args)
        pricing = load_pricing(args.pricing_file, args.model)
        generation_id = args.generation_id or f"gen-{uuid.uuid4().hex[:12]}"
        records = read_ledger(args.ledger)
        if any(record.get("generation_id") == generation_id for record in records):
            raise ValueError(f"duplicate generation_id {generation_id}")
        record = {
            "schema_version": 1,
            "generation_id": generation_id,
            "recorded_at": utc_now(),
            "operation": args.operation,
            "provider": args.provider,
            "model": args.model,
            "measurement": measurement,
            "token_usage": counts,
            "measurement_details": measurement_details,
            "cost": calculate_cost(counts, pricing, measurement),
            "artifacts": [str(path) for path in args.artifact],
            "notes": args.note,
        }
        records.append(record)
        write_ledger(args.ledger, records)
        if args.study_state:
            update_study_state(
                args.study_state,
                args.ledger,
                records,
                record,
                args.chapter_slug,
            )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"usage error: {exc}", file=sys.stderr)
        return 2
    print(
        f"usage recorded: id={generation_id} measurement={measurement} "
        f"total={counts.get('total_tokens')} ledger={args.ledger}"
    )
    return 0


def command_summary(args: argparse.Namespace) -> int:
    try:
        records = read_ledger(args.ledger)
    except (OSError, ValueError) as exc:
        print(f"usage error: {exc}", file=sys.stderr)
        return 2
    measurement_counts = Counter(str(record.get("measurement")) for record in records)
    token_totals: defaultdict[str, int] = defaultdict(int)
    cost_totals: defaultdict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    cost_records = 0
    for record in records:
        usage = record.get("token_usage")
        if isinstance(usage, dict):
            for name in ("input_tokens", "cached_input_tokens", "output_tokens", "total_tokens"):
                value = usage.get(name)
                if isinstance(value, int):
                    token_totals[name] += value
        cost = record.get("cost")
        if isinstance(cost, dict) and cost.get("status") in {"calculated", "estimated"}:
            try:
                cost_totals[str(cost.get("currency") or "unknown")] += Decimal(str(cost["amount"]))
                cost_records += 1
            except (InvalidOperation, KeyError):
                pass
    summary = {
        "schema_version": 1,
        "ledger": str(args.ledger),
        "generation_count": len(records),
        "measurement_counts": dict(sorted(measurement_counts.items())),
        "token_totals_mixed_accuracy": dict(sorted(token_totals.items())),
        "cost_totals": {currency: str(value) for currency, value in sorted(cost_totals.items())},
        "costed_generation_count": cost_records,
        "notice": "Totals may mix exact, reported, partial-estimate, and unavailable records.",
    }
    payload = json.dumps(summary, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    record = subparsers.add_parser("record", help="append one generation measurement")
    record.add_argument("--ledger", type=Path, required=True)
    record.add_argument("--generation-id")
    record.add_argument("--operation", required=True)
    record.add_argument("--provider")
    record.add_argument("--model")
    record.add_argument("--usage-file", type=Path)
    record.add_argument("--input-tokens", type=int)
    record.add_argument("--output-tokens", type=int)
    record.add_argument("--cached-input-tokens", type=int, default=0)
    record.add_argument("--cache-write-tokens", type=int, default=0)
    record.add_argument("--reasoning-tokens", type=int, default=0)
    record.add_argument("--total-tokens", type=int)
    record.add_argument("--input-file", type=Path, action="append", default=[])
    record.add_argument("--output-file", type=Path, action="append", default=[])
    record.add_argument("--unavailable-reason")
    record.add_argument("--pricing-file", type=Path)
    record.add_argument("--artifact", type=Path, action="append", default=[])
    record.add_argument("--note", action="append", default=[])
    record.add_argument("--study-state", type=Path)
    record.add_argument("--chapter-slug")
    record.set_defaults(handler=command_record)

    summary = subparsers.add_parser("summary", help="summarise a usage ledger")
    summary.add_argument("--ledger", type=Path, required=True)
    summary.add_argument("--output", type=Path)
    summary.set_defaults(handler=command_summary)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
