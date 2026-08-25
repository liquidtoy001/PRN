#!/usr/bin/env python3
"""Validate learning banks, track attempts, schedule retests, and export cards."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import math
import re
import sys
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any


ITEM_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}")
SOURCE_ID_PATTERN = re.compile(r"S\d+")
KINDS = {"flashcard", "multiple-choice", "short-answer", "worked-problem"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON root must be an object")
    return raw


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def bank_digest(bank: dict[str, Any]) -> str:
    payload = json.dumps(bank, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def inventory_ids(path: Path | None) -> set[str] | None:
    if path is None:
        return None
    inventory = read_json(path)
    materials = inventory.get("materials")
    if not isinstance(materials, list):
        raise ValueError("inventory.materials must be a list")
    return {
        str(item.get("id"))
        for item in materials
        if isinstance(item, dict) and item.get("id")
    }


def validate_reference(
    reference: Any,
    item_id: str,
    field: str,
    known_sources: set[str] | None,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(reference, dict):
        return [f"item {item_id} {field} entries must be objects"]
    source_id = str(reference.get("source_id") or "")
    locator = str(reference.get("locator") or "").strip()
    if not SOURCE_ID_PATTERN.fullmatch(source_id):
        errors.append(f"item {item_id} {field} has invalid source_id {source_id!r}")
    elif known_sources is not None and source_id not in known_sources:
        errors.append(f"item {item_id} {field} references unknown source {source_id}")
    if not locator:
        errors.append(f"item {item_id} {field} requires a precise locator")
    reference_type = reference.get("type", "source")
    if reference_type not in {"source", "assessment"}:
        errors.append(f"item {item_id} {field} type must be source or assessment")
    return errors


def validate_bank(bank: dict[str, Any], known_sources: set[str] | None = None) -> list[str]:
    errors: list[str] = []
    if bank.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if not str(bank.get("course_id") or "").strip():
        errors.append("course_id is required")
    items = bank.get("items")
    if not isinstance(items, list) or not items:
        errors.append("items must be a non-empty list")
        return errors
    seen: set[str] = set()
    for index, item in enumerate(items, 1):
        if not isinstance(item, dict):
            errors.append(f"item {index} must be an object")
            continue
        identifier = str(item.get("id") or "")
        if not ITEM_ID_PATTERN.fullmatch(identifier):
            errors.append(f"item {index} has invalid id {identifier!r}")
        elif identifier in seen:
            errors.append(f"duplicate item id {identifier}")
        seen.add(identifier)
        kind = item.get("kind")
        if kind not in KINDS:
            errors.append(f"item {identifier or index} kind must be one of {sorted(KINDS)}")
        if not str(item.get("prompt") or "").strip():
            errors.append(f"item {identifier or index} prompt is required")
        if not str(item.get("answer") or "").strip():
            errors.append(f"item {identifier or index} answer is required")
        if kind == "multiple-choice":
            choices = item.get("choices")
            if not isinstance(choices, list) or len(choices) < 2:
                errors.append(f"item {identifier or index} multiple-choice requires at least 2 choices")
        difficulty = item.get("difficulty", 3)
        if not isinstance(difficulty, int) or not 1 <= difficulty <= 5:
            errors.append(f"item {identifier or index} difficulty must be an integer from 1 to 5")
        minutes = item.get("estimated_minutes", 3)
        if not isinstance(minutes, (int, float)) or isinstance(minutes, bool) or minutes <= 0:
            errors.append(f"item {identifier or index} estimated_minutes must be positive")
        tags = item.get("tags", [])
        if not isinstance(tags, list) or not all(isinstance(value, str) for value in tags):
            errors.append(f"item {identifier or index} tags must be a list of strings")
        references = item.get("source_refs")
        if not isinstance(references, list) or not references:
            errors.append(f"item {identifier or index} source_refs must be non-empty")
        else:
            for reference in references:
                errors.extend(
                    validate_reference(reference, identifier or str(index), "source_refs", known_sources)
                )
        weight = item.get("assessment_weight")
        priority_refs = item.get("priority_evidence", [])
        if weight is not None:
            if (
                not isinstance(weight, (int, float))
                or isinstance(weight, bool)
                or not 0 <= float(weight) <= 1
            ):
                errors.append(f"item {identifier or index} assessment_weight must be in [0, 1]")
            if not isinstance(priority_refs, list) or not priority_refs:
                errors.append(
                    f"item {identifier or index} assessment_weight requires priority_evidence"
                )
        if priority_refs:
            if not isinstance(priority_refs, list):
                errors.append(f"item {identifier or index} priority_evidence must be a list")
            else:
                for reference in priority_refs:
                    errors.extend(
                        validate_reference(
                            reference,
                            identifier or str(index),
                            "priority_evidence",
                            known_sources,
                        )
                    )
    return errors


def item_map(bank: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item["id"]): item for item in bank["items"]}


def parse_date(value: str | None, name: str) -> date | None:
    if value is None:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be YYYY-MM-DD") from exc


def parse_datetime(value: str | None) -> datetime:
    if value is None:
        return datetime.now(timezone.utc)
    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError("--attempted-at must be an ISO-8601 date or timestamp") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def validate_learning_state(state: dict[str, Any], bank: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if state.get("schema_version") != 1:
        errors.append("learning state schema_version must be 1")
    if state.get("bank_digest") != bank_digest(bank):
        errors.append("learning state bank_digest does not match the bank")
    states = state.get("items")
    if not isinstance(states, dict):
        errors.append("learning state items must be an object")
        return errors
    expected = set(item_map(bank))
    actual = set(states)
    if expected != actual:
        errors.append("learning state item IDs do not match the bank")
    for identifier, item_state in states.items():
        if not isinstance(item_state, dict):
            errors.append(f"learning state item {identifier} must be an object")
            continue
        mastery = item_state.get("mastery")
        if not isinstance(mastery, (int, float)) or not 0 <= float(mastery) <= 1:
            errors.append(f"learning state item {identifier} mastery must be in [0, 1]")
        attempts = item_state.get("attempts")
        if not isinstance(attempts, list):
            errors.append(f"learning state item {identifier} attempts must be a list")
    return errors


def initialise_learning_state(bank: dict[str, Any], assessment_date: str | None) -> dict[str, Any]:
    now = utc_now()
    return {
        "schema_version": 1,
        "course_id": bank["course_id"],
        "bank_digest": bank_digest(bank),
        "assessment_date": assessment_date,
        "items": {
            str(item["id"]): {
                "mastery": 0.0,
                "status": "new",
                "consecutive_correct": 0,
                "lapses": 0,
                "due_at": None,
                "attempts": [],
            }
            for item in bank["items"]
        },
        "updated_at": now,
    }


def mastery_from_attempts(attempts: list[dict[str, Any]]) -> tuple[float, float]:
    recent = attempts[-5:]
    if not recent:
        return 0.0, 0.0
    weighted = 0.0
    weights = 0.0
    calibration_total = 0.0
    for index, attempt in enumerate(recent, 1):
        score = float(attempt["score"])
        confidence = (int(attempt["confidence"]) - 1) / 4
        adjusted = score
        if score < 0.6 and confidence >= 0.75:
            adjusted = max(0.0, score - 0.15)
        weighted += index * adjusted
        weights += index
        calibration_total += abs(confidence - score)
    mastery = max(0.0, min(1.0, weighted / weights))
    calibration_error = calibration_total / len(recent)
    return round(mastery, 4), round(calibration_error, 4)


def next_interval_days(consecutive_correct: int) -> int:
    schedule = (1, 3, 7, 14, 30, 60)
    return schedule[min(max(consecutive_correct - 1, 0), len(schedule) - 1)]


def update_main_study_state(
    state_path: Path,
    *,
    bank_path: Path,
    learning_state_path: Path,
    learning_state: dict[str, Any],
    plan_path: Path | None = None,
) -> None:
    from manage_state import read_state, validate_state, write_state

    study_state = read_state(state_path)
    if study_state.get("schema_version") != 2:
        raise ValueError("study state must be migrated to schema_version 2")
    item_states = learning_state["items"].values()
    attempted = [item for item in item_states if item.get("attempts")]
    mastery_average = (
        round(sum(float(item["mastery"]) for item in attempted) / len(attempted), 4)
        if attempted
        else 0.0
    )
    due_values = sorted(
        str(item["due_at"]) for item in item_states if item.get("due_at") is not None
    )
    study_state["learning"] = {
        "bank_paths": sorted(
            set(study_state.get("learning", {}).get("bank_paths", [])) | {str(bank_path)}
        ),
        "state_path": str(learning_state_path),
        "last_plan_path": str(plan_path) if plan_path else study_state.get("learning", {}).get("last_plan_path"),
        "attempted_items": len(attempted),
        "mastery_average": mastery_average,
        "next_retest_at": due_values[0] if due_values else None,
        "updated_at": utc_now(),
    }
    study_state["updated_at"] = utc_now()
    errors = validate_state(study_state)
    if errors:
        raise ValueError("; ".join(errors))
    write_state(state_path, study_state)


def command_validate_bank(args: argparse.Namespace) -> int:
    try:
        bank = read_json(args.bank)
        errors = validate_bank(bank, inventory_ids(args.inventory))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"learning bank error: {exc}", file=sys.stderr)
        return 2
    for error in errors:
        print(f"ERROR {error}", file=sys.stderr)
    print(f"learning bank validation: {'pass' if not errors else 'fail'} items={len(bank.get('items', []))}")
    return 1 if errors else 0


def command_init(args: argparse.Namespace) -> int:
    if args.output.exists() and not args.force:
        print(f"learning state already exists: {args.output}; pass --force to replace", file=sys.stderr)
        return 2
    try:
        bank = read_json(args.bank)
        errors = validate_bank(bank, inventory_ids(args.inventory))
        if errors:
            raise ValueError("; ".join(errors))
        assessment = parse_date(args.assessment_date, "--assessment-date")
        state = initialise_learning_state(bank, assessment.isoformat() if assessment else None)
        write_json(args.output, state)
        if args.study_state:
            update_main_study_state(
                args.study_state,
                bank_path=args.bank,
                learning_state_path=args.output,
                learning_state=state,
            )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"learning state error: {exc}", file=sys.stderr)
        return 2
    print(f"learning state initialised: items={len(state['items'])} output={args.output}")
    return 0


def command_record_attempt(args: argparse.Namespace) -> int:
    try:
        bank = read_json(args.bank)
        state = read_json(args.state)
        errors = validate_bank(bank)
        errors.extend(validate_learning_state(state, bank))
        if errors:
            raise ValueError("; ".join(errors))
        if args.item_id not in state["items"]:
            raise ValueError(f"unknown item id {args.item_id}")
        attempted_at = parse_datetime(args.attempted_at)
        score = args.score if args.score is not None else (1.0 if args.correct == "yes" else 0.0)
        if not 0 <= score <= 1:
            raise ValueError("--score must be in [0, 1]")
        correct = score >= 0.6
        if args.score is not None and correct != (args.correct == "yes"):
            raise ValueError("--correct and --score disagree at the 0.6 correctness threshold")
        item_state = state["items"][args.item_id]
        attempt = {
            "attempted_at": attempted_at.isoformat().replace("+00:00", "Z"),
            "score": round(float(score), 4),
            "correct": correct,
            "confidence": args.confidence,
            "mistake_tags": sorted(set(args.mistake_tag)),
            "note": args.note,
        }
        item_state["attempts"].append(attempt)
        if correct:
            item_state["consecutive_correct"] = int(item_state.get("consecutive_correct", 0)) + 1
            interval = next_interval_days(item_state["consecutive_correct"])
        else:
            item_state["consecutive_correct"] = 0
            item_state["lapses"] = int(item_state.get("lapses", 0)) + 1
            interval = 1
        due_date = attempted_at.date() + timedelta(days=interval)
        assessment = parse_date(state.get("assessment_date"), "assessment_date")
        if assessment and assessment > attempted_at.date():
            due_date = min(due_date, assessment - timedelta(days=1))
        elif assessment and assessment <= attempted_at.date():
            due_date = attempted_at.date()
        mastery, calibration_error = mastery_from_attempts(item_state["attempts"])
        item_state["mastery"] = mastery
        item_state["confidence_calibration_error"] = calibration_error
        item_state["due_at"] = due_date.isoformat()
        if not correct:
            item_state["status"] = "relearn"
        elif mastery >= 0.80 and item_state["consecutive_correct"] >= 2:
            item_state["status"] = "mastered"
        else:
            item_state["status"] = "learning"
        state["updated_at"] = utc_now()
        write_json(args.state, state)
        if args.study_state:
            update_main_study_state(
                args.study_state,
                bank_path=args.bank,
                learning_state_path=args.state,
                learning_state=state,
            )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"learning attempt error: {exc}", file=sys.stderr)
        return 2
    print(
        f"attempt recorded: item={args.item_id} correct={correct} mastery={mastery:.4f} "
        f"due={item_state['due_at']}"
    )
    return 0


def source_reference_text(references: list[dict[str, Any]]) -> str:
    parts = []
    for reference in references:
        prefix = "assessment" if reference.get("type") == "assessment" else "source"
        parts.append(f"[{prefix}:{reference['source_id']}|{reference['locator']}]")
    return " ".join(parts)


def item_priority(
    item: dict[str, Any], item_state: dict[str, Any], as_of: date, exam: date | None
) -> tuple[float, dict[str, Any]]:
    mastery_gap = 1.0 - float(item_state.get("mastery", 0.0))
    due_value = parse_date(item_state.get("due_at"), "due_at")
    due = due_value is None or due_value <= as_of
    due_factor = 1.5 if due else 0.75
    weight = item.get("assessment_weight")
    evidence_backed = weight is not None and bool(item.get("priority_evidence"))
    evidence_weight = float(weight) if evidence_backed else 0.5
    days_to_exam = (exam - as_of).days if exam else None
    if days_to_exam is None:
        evidence_factor = 1.0
    elif days_to_exam <= 7:
        evidence_factor = 0.5 + 1.5 * evidence_weight
    elif days_to_exam <= 30:
        evidence_factor = 0.65 + 1.2 * evidence_weight
    else:
        evidence_factor = 0.8 + 0.8 * evidence_weight
    lapse_factor = 1.0 + min(1.0, int(item_state.get("lapses", 0)) * 0.15)
    minutes = float(item.get("estimated_minutes", 3))
    score = (0.25 + mastery_gap) * due_factor * evidence_factor * lapse_factor / math.sqrt(minutes)
    return round(score, 6), {
        "due": due,
        "mastery_gap": round(mastery_gap, 4),
        "assessment_weight": weight,
        "evidence_backed": evidence_backed,
        "days_to_exam": days_to_exam,
        "estimated_minutes": minutes,
    }


def command_plan(args: argparse.Namespace) -> int:
    try:
        bank = read_json(args.bank)
        state = read_json(args.state)
        errors = validate_bank(bank)
        errors.extend(validate_learning_state(state, bank))
        if errors:
            raise ValueError("; ".join(errors))
        as_of = parse_date(args.as_of, "--as-of") or datetime.now(timezone.utc).date()
        exam = parse_date(args.assessment_date or state.get("assessment_date"), "assessment_date")
        if exam and exam < as_of:
            raise ValueError("assessment date cannot be before --as-of")
        if args.available_minutes <= 0:
            raise ValueError("--available-minutes must be positive")
        by_id = item_map(bank)
        ranked: list[dict[str, Any]] = []
        for identifier, item in by_id.items():
            score, basis = item_priority(item, state["items"][identifier], as_of, exam)
            ranked.append(
                {
                    "item_id": identifier,
                    "kind": item["kind"],
                    "prompt": item["prompt"],
                    "priority_score": score,
                    "priority_basis": basis,
                    "priority_label": (
                        "assessment-supported learning priority"
                        if basis["evidence_backed"]
                        else "learning priority; exam relevance unknown"
                    ),
                    "source_refs": item["source_refs"],
                }
            )
        ranked.sort(key=lambda value: (-value["priority_score"], value["item_id"]))
        selected: list[dict[str, Any]] = []
        used_minutes = 0.0
        for item in ranked:
            minutes = float(item["priority_basis"]["estimated_minutes"])
            if used_minutes + minutes <= args.available_minutes or not selected:
                selected.append(item)
                used_minutes += minutes
        selected_ids = {item["item_id"] for item in selected}
        uncovered = [item for item in ranked if item["item_id"] not in selected_ids]
        plan = {
            "schema_version": 1,
            "generated_at": utc_now(),
            "as_of": as_of.isoformat(),
            "assessment_date": exam.isoformat() if exam else None,
            "available_minutes": args.available_minutes,
            "scheduled_minutes": round(used_minutes, 2),
            "selected": selected,
            "uncovered": uncovered,
            "scoring_notice": (
                "Scores schedule review from mastery, due state, time cost, and only explicit "
                "assessment_weight evidence; they are not exam-probability predictions."
            ),
        }
        write_json(args.output, plan)
        if args.study_state:
            update_main_study_state(
                args.study_state,
                bank_path=args.bank,
                learning_state_path=args.state,
                learning_state=state,
                plan_path=args.output,
            )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"learning plan error: {exc}", file=sys.stderr)
        return 2
    print(
        f"learning plan: selected={len(selected)} uncovered={len(uncovered)} "
        f"minutes={used_minutes:.2f} output={args.output}"
    )
    return 0


def export_front(item: dict[str, Any]) -> str:
    prompt = str(item["prompt"])
    choices = item.get("choices")
    if isinstance(choices, list) and choices:
        prompt += "\n" + "\n".join(f"{index + 1}. {value}" for index, value in enumerate(choices))
    return prompt


def export_back(item: dict[str, Any]) -> str:
    parts = [str(item["answer"])]
    if item.get("rationale"):
        parts.append(str(item["rationale"]))
    parts.append(source_reference_text(item["source_refs"]))
    return "\n\n".join(part for part in parts if part)


def command_export(args: argparse.Namespace) -> int:
    try:
        bank = read_json(args.bank)
        errors = validate_bank(bank, inventory_ids(args.inventory))
        if errors:
            raise ValueError("; ".join(errors))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8", newline="") as handle:
            if args.format == "csv":
                writer = csv.writer(handle)
                writer.writerow(["id", "kind", "front", "back", "tags", "source_refs"])
                for item in bank["items"]:
                    writer.writerow(
                        [
                            item["id"],
                            item["kind"],
                            export_front(item),
                            export_back(item),
                            " ".join(sorted(set(item.get("tags", [])))),
                            source_reference_text(item["source_refs"]),
                        ]
                    )
            else:
                writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
                for item in bank["items"]:
                    source_tags = [reference["source_id"] for reference in item["source_refs"]]
                    tags = " ".join(sorted(set(item.get("tags", [])) | set(source_tags)))
                    front = html.escape(export_front(item)).replace("\n", "<br>")
                    back = html.escape(export_back(item)).replace("\n", "<br>")
                    writer.writerow([front, back, tags])
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"learning export error: {exc}", file=sys.stderr)
        return 2
    print(f"learning export: format={args.format} items={len(bank['items'])} output={args.output}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate-bank", help="validate a generated learning bank")
    validate.add_argument("bank", type=Path)
    validate.add_argument("--inventory", type=Path)
    validate.set_defaults(handler=command_validate_bank)

    initialise = subparsers.add_parser("init", help="initialise learner state from a bank")
    initialise.add_argument("--bank", type=Path, required=True)
    initialise.add_argument("--output", type=Path, required=True)
    initialise.add_argument("--inventory", type=Path)
    initialise.add_argument("--assessment-date")
    initialise.add_argument("--study-state", type=Path)
    initialise.add_argument("--force", action="store_true")
    initialise.set_defaults(handler=command_init)

    attempt = subparsers.add_parser("record-attempt", help="record one quiz/card attempt")
    attempt.add_argument("--bank", type=Path, required=True)
    attempt.add_argument("--state", type=Path, required=True)
    attempt.add_argument("--item-id", required=True)
    attempt.add_argument("--correct", choices=("yes", "no"), required=True)
    attempt.add_argument("--score", type=float)
    attempt.add_argument("--confidence", type=int, choices=range(1, 6), required=True)
    attempt.add_argument("--attempted-at")
    attempt.add_argument("--mistake-tag", action="append", default=[])
    attempt.add_argument("--note")
    attempt.add_argument("--study-state", type=Path)
    attempt.set_defaults(handler=command_record_attempt)

    plan = subparsers.add_parser("plan", help="build a time-bounded staged-retest plan")
    plan.add_argument("--bank", type=Path, required=True)
    plan.add_argument("--state", type=Path, required=True)
    plan.add_argument("--output", type=Path, required=True)
    plan.add_argument("--as-of")
    plan.add_argument("--assessment-date")
    plan.add_argument("--available-minutes", type=float, default=60)
    plan.add_argument("--study-state", type=Path)
    plan.set_defaults(handler=command_plan)

    export = subparsers.add_parser("export", help="export a learning bank to CSV or Anki TSV")
    export.add_argument("--bank", type=Path, required=True)
    export.add_argument("--format", choices=("csv", "anki"), required=True)
    export.add_argument("--output", type=Path, required=True)
    export.add_argument("--inventory", type=Path)
    export.set_defaults(handler=command_export)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
