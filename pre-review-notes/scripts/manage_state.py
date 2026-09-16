#!/usr/bin/env python3
"""Initialise, validate, and update resumable pre-review-notes state."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MODES = {"lightweight", "full", "exam-cram"}
LANGUAGES = {"zh", "en", "bilingual"}
FORMATS = {"markdown", "latex", "latex-pdf", "markdown-pdf"}
LEARNING_OUTPUTS = {"flashcards", "quiz"}
STATUSES = {"planned", "drafting", "verified", "delivered", "stale", "blocked"}
QA_VALUES = {"pending", "pass", "fail", "not-applicable", "unavailable"}
QA_FIELDS = {
    "citations",
    "reasoning",
    "pdf_structure",
    "visual",
    "capacity_disclosure",
    "usage_accounting",
    "learning_assets",
}
DIGEST_PATTERN = re.compile(r"[0-9a-f]{64}")
CURRENT_SCHEMA_VERSION = 2
SUPPORTED_SCHEMA_VERSIONS = {1, CURRENT_SCHEMA_VERSION}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def validate_note_configuration(configuration: Any) -> list[str]:
    """Validate optional 0.2.7 settings without invalidating legacy state."""
    if not isinstance(configuration, dict):
        return ["preferences.note_configuration must be an object"]
    errors: list[str] = []
    choices = {
        "purpose": {"knowledge", "exam"},
        "depth": {"standard-detailed", "extended"},
        "layout_density": {"comfortable", "compact"},
    }
    if "paper_enrichment" in configuration:
        choices["paper_enrichment"] = {"off", "reading-list", "integrated"}
    for key, allowed in choices.items():
        value = configuration.get(key)
        if not isinstance(value, str) or value not in allowed:
            errors.append(f"note_configuration.{key} must be one of {sorted(allowed)}")
    for key in ("scope", "page_size"):
        value = configuration.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"note_configuration.{key} must be a nonempty string")
    outputs = configuration.get("deliverables")
    if (not isinstance(outputs, list) or not outputs
            or not all(isinstance(value, str) and value in {"pdf", "latex", "markdown"}
                       for value in outputs)):
        errors.append("note_configuration.deliverables must contain pdf, latex or markdown")
    if not isinstance(configuration.get("confirmed"), bool):
        errors.append("note_configuration.confirmed must be boolean")
    return errors


def read_state(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("state root must be an object")
    return raw


def write_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def validate_state(state: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    schema_version = state.get("schema_version")
    if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        errors.append(f"schema_version must be one of {sorted(SUPPORTED_SCHEMA_VERSIONS)}")
    course = state.get("course")
    if (
        not isinstance(course, dict)
        or not str(course.get("id", "")).strip()
        or not str(course.get("title", "")).strip()
    ):
        errors.append("course.id and course.title are required")
    preferences = state.get("preferences")
    if not isinstance(preferences, dict):
        errors.append("preferences must be an object")
    else:
        if preferences.get("mode") not in MODES:
            errors.append(f"preferences.mode must be one of {sorted(MODES)}")
        if preferences.get("language") not in LANGUAGES:
            errors.append(f"preferences.language must be one of {sorted(LANGUAGES)}")
        if preferences.get("format") not in FORMATS:
            errors.append(f"preferences.format must be one of {sorted(FORMATS)}")
        study_hours = preferences.get("study_hours_available")
        configuration = preferences.get("note_configuration")
        if configuration is not None:
            errors.extend(validate_note_configuration(configuration))
        if study_hours is not None and (
            not isinstance(study_hours, (int, float))
            or isinstance(study_hours, bool)
            or study_hours < 0
        ):
            errors.append("preferences.study_hours_available must be a non-negative number or null")
        if schema_version == 2:
            learning_outputs = preferences.get("learning_outputs")
            if (
                not isinstance(learning_outputs, list)
                or not all(isinstance(value, str) for value in learning_outputs)
                or not set(learning_outputs).issubset(LEARNING_OUTPUTS)
            ):
                errors.append(
                    f"preferences.learning_outputs must be a list using {sorted(LEARNING_OUTPUTS)}"
                )
    materials_state = state.get("materials")
    if not isinstance(materials_state, dict):
        errors.append("materials must be an object")
    else:
        digest = materials_state.get("inventory_digest")
        if digest is not None and not DIGEST_PATTERN.fullmatch(str(digest)):
            errors.append("materials.inventory_digest must be a SHA-256 digest or null")
    if schema_version == 2:
        capacity = state.get("capacity")
        if not isinstance(capacity, dict):
            errors.append("capacity must be an object in schema_version 2")
        usage = state.get("usage")
        if not isinstance(usage, dict):
            errors.append("usage must be an object in schema_version 2")
        else:
            generation_count = usage.get("generation_count")
            if (
                not isinstance(generation_count, int)
                or isinstance(generation_count, bool)
                or generation_count < 0
            ):
                errors.append("usage.generation_count must be a non-negative integer")
        learning = state.get("learning")
        if not isinstance(learning, dict):
            errors.append("learning must be an object in schema_version 2")
    chapters = state.get("chapters")
    if not isinstance(chapters, list):
        errors.append("chapters must be a list")
        return errors
    seen: set[str] = set()
    for index, chapter in enumerate(chapters, 1):
        if not isinstance(chapter, dict):
            errors.append(f"chapter {index} must be an object")
            continue
        slug = str(chapter.get("slug", ""))
        if not slug:
            errors.append(f"chapter {index} has no slug")
        elif slug in seen:
            errors.append(f"duplicate chapter slug {slug}")
        seen.add(slug)
        if chapter.get("status") not in STATUSES:
            errors.append(f"chapter {slug or index} has invalid status")
        digest = chapter.get("input_digest")
        if digest is not None and not DIGEST_PATTERN.fullmatch(str(digest)):
            errors.append(f"chapter {slug or index} has invalid input_digest")
        qa = chapter.get("qa", {})
        if not isinstance(qa, dict):
            errors.append(f"chapter {slug or index} qa must be an object")
        else:
            for name, value in qa.items():
                if value not in QA_VALUES:
                    errors.append(f"chapter {slug or index} qa.{name} has invalid value {value}")
        if chapter.get("status") in {"verified", "delivered"}:
            if not DIGEST_PATTERN.fullmatch(str(chapter.get("input_digest") or "")):
                errors.append(f"chapter {slug or index} requires input_digest when verified or delivered")
            required = {"citations": "pass", "reasoning": "pass"}
            if isinstance(preferences, dict) and "pdf" in str(preferences.get("format", "")):
                required.update({"pdf_structure": "pass", "visual": "pass"})
            if schema_version == 2 and not chapter.get("legacy_generation", False):
                required.update(
                    {"capacity_disclosure": "pass", "usage_accounting": "pass"}
                )
                capacity_state = state.get("capacity")
                if not isinstance(capacity_state, dict) or not capacity_state.get("report_path"):
                    errors.append(
                        f"chapter {slug or index} requires a recorded capacity report"
                    )
                usage_state = state.get("usage")
                if (
                    not isinstance(usage_state, dict)
                    or not usage_state.get("ledger_path")
                    or not usage_state.get("last_generation_id")
                    or not isinstance(usage_state.get("generation_count"), int)
                    or usage_state.get("generation_count", 0) < 1
                ):
                    errors.append(
                        f"chapter {slug or index} requires at least one usage-ledger record"
                    )
            missing = [name for name, expected in required.items() if qa.get(name) != expected]
            if missing:
                errors.append(f"chapter {slug or index} required QA not passed: {', '.join(missing)}")
        if chapter.get("status") == "delivered" and not chapter.get("artifacts"):
            errors.append(f"chapter {slug or index} requires at least one delivered artifact")
    return errors


def find_chapter(state: dict[str, Any], slug: str) -> dict[str, Any] | None:
    return next((chapter for chapter in state.get("chapters", []) if chapter.get("slug") == slug), None)


def command_init(args: argparse.Namespace) -> int:
    if args.output.exists() and not args.force:
        print(f"state already exists: {args.output}; pass --force to replace it", file=sys.stderr)
        return 2
    state = {
        "schema_version": CURRENT_SCHEMA_VERSION,
        "course": {"id": args.course_id, "title": args.course_title},
        "preferences": {
            "mode": args.mode,
            "language": args.language,
            "format": args.format,
            "assessment_date": args.assessment_date,
            "study_hours_available": args.study_hours,
            "learning_outputs": sorted(set(args.learning_output)),
        },
        "materials": {"inventory_path": args.inventory, "inventory_digest": args.inventory_digest},
        "evidence_boundary": {
            "assessment_specification": "unknown",
            "past_assessments": "unknown",
            "official_solutions": "unknown",
            "notes": [],
        },
        "capacity": {
            "report_path": None,
            "status": "not-checked",
            "quality_ceiling": None,
            "last_checked_at": None,
        },
        "usage": {
            "ledger_path": None,
            "generation_count": 0,
            "last_generation_id": None,
            "last_measurement": None,
            "updated_at": None,
        },
        "learning": {
            "bank_paths": [],
            "state_path": None,
            "last_plan_path": None,
            "attempted_items": 0,
            "mastery_average": 0.0,
            "next_retest_at": None,
            "updated_at": None,
        },
        "chapters": [],
        "last_action": "Initialised study state",
        "next_action": "Inventory materials and establish the evidence boundary",
        "updated_at": utc_now(),
    }
    if args.note_configuration:
        try:
            state["preferences"]["note_configuration"] = json.loads(
                args.note_configuration.read_text(encoding="utf-8")
            )
        except (OSError, ValueError) as exc:
            print(f"configuration error: {exc}", file=sys.stderr)
            return 2
    errors = validate_state(state)
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 2
    write_state(args.output, state)
    print(f"state initialised: {args.output}")
    return 0


def migrate_v1_to_v2(state: dict[str, Any]) -> dict[str, Any]:
    if state.get("schema_version") != 1:
        raise ValueError("only schema_version 1 can be migrated")
    migrated = json.loads(json.dumps(state))
    migrated["schema_version"] = 2
    migrated.setdefault("preferences", {})["learning_outputs"] = []
    migrated["capacity"] = {
        "report_path": None,
        "status": "not-checked",
        "quality_ceiling": None,
        "last_checked_at": None,
    }
    migrated["usage"] = {
        "ledger_path": None,
        "generation_count": 0,
        "last_generation_id": None,
        "last_measurement": None,
        "updated_at": None,
    }
    migrated["learning"] = {
        "bank_paths": [],
        "state_path": None,
        "last_plan_path": None,
        "attempted_items": 0,
        "mastery_average": 0.0,
        "next_retest_at": None,
        "updated_at": None,
    }
    for chapter in migrated.get("chapters", []):
        if not isinstance(chapter, dict):
            continue
        chapter["legacy_generation"] = True
        qa = chapter.setdefault("qa", {})
        qa.setdefault("capacity_disclosure", "not-applicable")
        qa.setdefault("usage_accounting", "not-applicable")
        qa.setdefault("learning_assets", "not-applicable")
    migrated["last_action"] = "Migrated study state from schema 1 to schema 2"
    migrated["next_action"] = (
        "Run a capacity check before the next generation and start the usage ledger afterwards"
    )
    migrated["updated_at"] = utc_now()
    return migrated


def command_migrate(args: argparse.Namespace) -> int:
    try:
        state = read_state(args.state)
        if state.get("schema_version") == CURRENT_SCHEMA_VERSION:
            print(f"state is already schema_version {CURRENT_SCHEMA_VERSION}: {args.state}")
            return 0
        migrated = migrate_v1_to_v2(state)
        errors = validate_state(migrated)
        if errors:
            raise ValueError("; ".join(errors))
        output = args.output or args.state
        if output.exists() and output != args.state and not args.force:
            raise ValueError(f"output already exists: {output}; pass --force to replace it")
        write_state(output, migrated)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"state migration error: {exc}", file=sys.stderr)
        return 2
    print(f"state migrated: schema=2 output={output}")
    return 0


def command_validate(args: argparse.Namespace) -> int:
    try:
        state = read_state(args.state)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"state error: {exc}", file=sys.stderr)
        return 2
    errors = validate_state(state)
    for error in errors:
        print(f"ERROR {error}", file=sys.stderr)
    print(f"state validation: {'pass' if not errors else 'fail'}")
    return 1 if errors else 0


def command_update_chapter(args: argparse.Namespace) -> int:
    try:
        state = read_state(args.state)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"state error: {exc}", file=sys.stderr)
        return 2
    chapter = find_chapter(state, args.slug)
    if chapter is None:
        if not args.title:
            print("--title is required when creating a chapter", file=sys.stderr)
            return 2
        chapter = {
            "slug": args.slug,
            "title": args.title,
            "status": "planned",
            "legacy_generation": False,
            "priority_basis": None,
            "source_ids": [],
            "input_digest": None,
            "artifacts": [],
            "qa": {
                "citations": "pending",
                "reasoning": "pending",
                "pdf_structure": "not-applicable",
                "visual": "not-applicable",
                "capacity_disclosure": "pending",
                "usage_accounting": "pending",
                "learning_assets": "not-applicable",
            },
            "updated_at": utc_now(),
        }
        state.setdefault("chapters", []).append(chapter)

    if args.title:
        chapter["title"] = args.title
    if args.priority_basis is not None:
        chapter["priority_basis"] = args.priority_basis
    if args.input_digest:
        chapter["input_digest"] = args.input_digest
    if args.source_id:
        chapter["source_ids"] = sorted(set(chapter.get("source_ids", [])) | set(args.source_id))
    if args.artifact:
        chapter["artifacts"] = sorted(set(chapter.get("artifacts", [])) | set(args.artifact))

    qa = chapter.setdefault("qa", {})
    for field in sorted(QA_FIELDS):
        value = getattr(args, f"qa_{field}")
        if value is not None:
            qa[field] = value

    if args.status:
        if args.status in {"verified", "delivered"}:
            required = {"citations": "pass", "reasoning": "pass"}
            if "pdf" in state.get("preferences", {}).get("format", ""):
                required.update({"pdf_structure": "pass", "visual": "pass"})
            if state.get("schema_version") == 2 and not chapter.get("legacy_generation", False):
                required.update(
                    {"capacity_disclosure": "pass", "usage_accounting": "pass"}
                )
            missing = [name for name, expected in required.items() if qa.get(name) != expected]
            if missing:
                print(
                    f"cannot set {args.status}; required QA not passed: {', '.join(missing)}",
                    file=sys.stderr,
                )
                return 2
            if not DIGEST_PATTERN.fullmatch(str(chapter.get("input_digest") or "")):
                print(f"cannot set {args.status}; a valid --input-digest is required", file=sys.stderr)
                return 2
            if args.status == "delivered" and not chapter.get("artifacts"):
                print("cannot set delivered; at least one --artifact is required", file=sys.stderr)
                return 2
        chapter["status"] = args.status

    chapter["updated_at"] = utc_now()
    state["last_action"] = args.last_action or f"Updated chapter {args.slug}"
    if args.next_action is not None:
        state["next_action"] = args.next_action
    state["updated_at"] = utc_now()
    errors = validate_state(state)
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 2
    write_state(args.state, state)
    print(f"chapter updated: {args.slug} status={chapter['status']}")
    return 0


def command_needs_rebuild(args: argparse.Namespace) -> int:
    try:
        state = read_state(args.state)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"state error: {exc}", file=sys.stderr)
        return 2
    chapter = find_chapter(state, args.slug)
    reusable = bool(
        chapter
        and chapter.get("status") in {"verified", "delivered"}
        and chapter.get("input_digest") == args.input_digest
    )
    print("reuse" if reusable else "rebuild")
    return 0 if reusable else 3


def command_render_progress(args: argparse.Namespace) -> int:
    try:
        state = read_state(args.state)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"state error: {exc}", file=sys.stderr)
        return 2
    errors = validate_state(state)
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 2
    course = state["course"]
    pref = state["preferences"]
    materials = state.get("materials", {})
    capacity = state.get("capacity", {})
    usage = state.get("usage", {})
    learning = state.get("learning", {})
    lines = [
        f"# {course['id']} - {course['title']} Progress",
        "",
        f"- Mode: `{pref['mode']}`",
        f"- Note configuration: `{json.dumps(pref.get('note_configuration'), ensure_ascii=False)}`",
        f"- Language: `{pref['language']}`",
        f"- Format: `{pref['format']}`",
        f"- Assessment date: `{pref.get('assessment_date') or 'not provided'}`",
        f"- Material inventory: `{materials.get('inventory_path') or 'not generated'}`",
        f"- Inventory digest: `{materials.get('inventory_digest') or 'unknown'}`",
        f"- Capacity status: `{capacity.get('status') or 'legacy-not-checked'}`",
        f"- Capacity report: `{capacity.get('report_path') or 'not generated'}`",
        f"- Recorded generations: `{usage.get('generation_count', 0)}`",
        f"- Usage ledger: `{usage.get('ledger_path') or 'not generated'}`",
        f"- Learning outputs: `{', '.join(pref.get('learning_outputs', [])) or 'none'}`",
        f"- Attempted learning items: `{learning.get('attempted_items', 0)}`",
        f"- Average mastery: `{learning.get('mastery_average', 0.0)}`",
        f"- Next retest: `{learning.get('next_retest_at') or 'not scheduled'}`",
        "",
        "## Chapters",
        "",
        "| Chapter | Status | Priority evidence | Artifacts |",
        "|---|---|---|---|",
    ]
    for chapter in state.get("chapters", []):
        artifacts = ", ".join(f"`{path}`" for path in chapter.get("artifacts", [])) or "-"
        basis = str(chapter.get("priority_basis") or "unknown").replace("|", "\\|")
        lines.append(f"| {chapter['title']} | `{chapter['status']}` | {basis} | {artifacts} |")
    lines.extend(
        [
            "",
            "## Continuation",
            "",
            f"- Last action: {state.get('last_action') or 'none recorded'}",
            f"- Next action: {state.get('next_action') or 'none recorded'}",
            "",
            f"Updated: `{state.get('updated_at') or 'unknown'}`",
            "",
        ]
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"progress rendered: {args.output}")
    return 0


def add_qa_arguments(parser: argparse.ArgumentParser) -> None:
    for name in sorted(QA_FIELDS):
        parser.add_argument(f"--qa-{name.replace('_', '-')}", choices=sorted(QA_VALUES))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="create a new state file")
    init.add_argument("--output", type=Path, required=True)
    init.add_argument("--course-id", required=True)
    init.add_argument("--course-title", required=True)
    init.add_argument("--mode", choices=sorted(MODES), required=True)
    init.add_argument("--language", choices=sorted(LANGUAGES), required=True)
    init.add_argument("--format", choices=sorted(FORMATS), required=True)
    init.add_argument("--assessment-date")
    init.add_argument("--note-configuration", type=Path)
    init.add_argument("--study-hours", type=float)
    init.add_argument(
        "--learning-output",
        choices=sorted(LEARNING_OUTPUTS),
        action="append",
        default=[],
    )
    init.add_argument("--inventory")
    init.add_argument("--inventory-digest")
    init.add_argument("--force", action="store_true")
    init.set_defaults(handler=command_init)

    migrate = subparsers.add_parser("migrate", help="migrate schema_version 1 state to 2")
    migrate.add_argument("state", type=Path)
    migrate.add_argument("--output", type=Path)
    migrate.add_argument("--force", action="store_true")
    migrate.set_defaults(handler=command_migrate)

    validate = subparsers.add_parser("validate", help="validate an existing state file")
    validate.add_argument("state", type=Path)
    validate.set_defaults(handler=command_validate)

    update = subparsers.add_parser("update-chapter", help="create or update one chapter")
    update.add_argument("state", type=Path)
    update.add_argument("--slug", required=True)
    update.add_argument("--title")
    update.add_argument("--status", choices=sorted(STATUSES))
    update.add_argument("--priority-basis")
    update.add_argument("--input-digest")
    update.add_argument("--source-id", action="append")
    update.add_argument("--artifact", action="append")
    update.add_argument("--last-action")
    update.add_argument("--next-action")
    add_qa_arguments(update)
    update.set_defaults(handler=command_update_chapter)

    rebuild = subparsers.add_parser("needs-rebuild", help="check an incremental input digest")
    rebuild.add_argument("state", type=Path)
    rebuild.add_argument("--slug", required=True)
    rebuild.add_argument("--input-digest", required=True)
    rebuild.set_defaults(handler=command_needs_rebuild)

    render = subparsers.add_parser("render-progress", help="render progress.md from state")
    render.add_argument("state", type=Path)
    render.add_argument("--output", type=Path, required=True)
    render.set_defaults(handler=command_render_progress)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
