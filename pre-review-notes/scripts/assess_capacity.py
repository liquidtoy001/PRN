#!/usr/bin/env python3
"""Assess material volume, context fit, and preliminary quality ceilings."""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ASSESSMENT_ROLES = {
    "assessment-specification",
    "past-assessment",
    "official-solution",
    "graded-work",
}

ZH_STRATEGIES = {
    "unknown": "平台上下文上限未知；在确认前使用分章材料子集。",
    "chunking-required": "不要一次载入全部材料；先全局盘点，再按章节检索并记录 source IDs。",
    "indeterminate": "先处理 OCR/不可读来源，或采用保守的增量检索。",
    "near-limit": "按章节选取材料，并为输出与推理保留余量。",
    "fits-estimate": "估算可能容纳全量材料，但仍需保留引用和增量检查点。",
}

ZH_NOTICE_MESSAGES = {
    "CONTEXT_LIMIT_UNKNOWN": "平台上下文上限未知，不能声称一次读取已覆盖全部资料。",
    "MATERIALS_EXCEED_SAFE_CONTEXT": "材料 token 上界超过安全输入容量；完整覆盖需要分块检索和检查点。",
    "UNSIZED_MATERIALS": "存在无法可靠估算 token 的来源文件。",
    "OCR_REQUIRED": "存在需要 OCR 后才能支持可靠覆盖声明的 PDF。",
    "ENCRYPTED_MATERIALS": "存在无法检查的加密 PDF。",
    "THIN_OR_INCOMPLETE_ASSESSMENT_EVIDENCE": "推测到的考核证据不完整；频率和权重结论仍受限。",
    "NO_ASSESSMENT_EVIDENCE": "未推测到考核类来源；成品只能声称课程材料驱动的内容覆盖。",
    "NO_OFFICIAL_SOLUTIONS": "缺少官方答案或评分标准，无法认证答题深度和得分步骤覆盖。",
    "ROLE_GUESSES_REQUIRE_VERIFICATION": "证据角色来自文件名推测，仅用于路由，不是已核实的课程事实。",
}


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


def add_notice(
    notices: list[dict[str, str]],
    code: str,
    severity: str,
    message: str,
) -> None:
    notices.append({"code": code, "severity": severity, "message": message})


def choose_materials(
    inventory: dict[str, Any], selected_ids: list[str]
) -> tuple[list[dict[str, Any]], list[str]]:
    materials = inventory.get("materials")
    if not isinstance(materials, list):
        raise ValueError("inventory.materials must be a list")
    invalid = [item for item in materials if not isinstance(item, dict)]
    if invalid:
        raise ValueError("every inventory material must be an object")
    if not selected_ids:
        return materials, []
    by_id = {str(item.get("id")): item for item in materials}
    missing = sorted(set(selected_ids) - set(by_id))
    if missing:
        raise ValueError(f"unknown source IDs: {', '.join(missing)}")
    selected = [by_id[identifier] for identifier in dict.fromkeys(selected_ids)]
    return selected, missing


def material_measurements(materials: list[dict[str, Any]]) -> dict[str, Any]:
    lower = 0
    estimate = 0
    upper = 0
    known_files = 0
    unknown_files: list[str] = []
    needs_ocr: list[str] = []
    encrypted: list[str] = []
    pdf_pages = 0
    total_bytes = 0
    roles: Counter[str] = Counter()

    for item in materials:
        identifier = str(item.get("id") or "unknown")
        path = str(item.get("path") or identifier)
        total_bytes += int(item.get("bytes") or 0)
        roles[str(item.get("role_guess") or "other")] += 1
        pdf = item.get("pdf") if isinstance(item.get("pdf"), dict) else {}
        pdf_pages += int(pdf.get("pages") or 0)
        if pdf.get("needs_ocr"):
            needs_ocr.append(f"{identifier}:{path}")
        if pdf.get("encrypted") or pdf.get("status") == "encrypted":
            encrypted.append(f"{identifier}:{path}")

        token_estimate = item.get("token_estimate")
        if not isinstance(token_estimate, dict) or token_estimate.get("status") not in {
            "estimated",
            "reported",
            "exact",
        }:
            unknown_files.append(f"{identifier}:{path}")
            continue
        try:
            lower_value = int(token_estimate.get("lower_bound_tokens", 0))
            estimate_value = int(token_estimate.get("estimated_tokens", 0))
            upper_value = int(token_estimate.get("upper_bound_tokens", 0))
        except (TypeError, ValueError):
            unknown_files.append(f"{identifier}:{path}")
            continue
        if min(lower_value, estimate_value, upper_value) < 0 or not (
            lower_value <= estimate_value <= upper_value
        ):
            unknown_files.append(f"{identifier}:{path}")
            continue
        lower += lower_value
        estimate += estimate_value
        upper += upper_value
        known_files += 1

    return {
        "files": len(materials),
        "total_bytes": total_bytes,
        "pdf_pages": pdf_pages,
        "token_estimate": {
            "status": "partial" if unknown_files else "estimated",
            "known_files": known_files,
            "unknown_files": unknown_files,
            "lower_bound_tokens": lower,
            "estimated_tokens": estimate,
            "upper_bound_tokens": upper,
            "method": "sum-of-inventory-estimates",
            "notice": "Bounds are model-independent estimates, not provider token counts.",
        },
        "needs_ocr_files": needs_ocr,
        "encrypted_files": encrypted,
        "role_guess_counts": dict(sorted(roles.items())),
    }


def context_fit(args: argparse.Namespace, measurements: dict[str, Any]) -> dict[str, Any]:
    estimate = measurements["token_estimate"]
    context_window = args.context_window
    if context_window is None:
        return {
            "status": "unknown",
            "context_window_tokens": None,
            "reserved_output_tokens": args.reserved_output_tokens,
            "overhead_tokens": args.overhead_tokens,
            "safety_margin": args.safety_margin,
            "usable_input_tokens": None,
            "upper_bound_ratio": None,
            "strategy": "Use incremental source selection until the platform context limit is known.",
        }

    pre_margin = context_window - args.reserved_output_tokens - args.overhead_tokens
    if pre_margin <= 0:
        raise ValueError("context window must exceed output and overhead reserves")
    usable = math.floor(pre_margin * (1.0 - args.safety_margin))
    upper = int(estimate["upper_bound_tokens"])
    ratio = upper / usable if usable else None
    unknown = bool(estimate["unknown_files"])
    if upper > usable:
        status = "chunking-required"
        strategy = "Do not load all materials at once; inventory globally and retrieve chapter subsets."
    elif unknown:
        status = "indeterminate"
        strategy = "Resolve unreadable/OCR sources or use conservative incremental retrieval."
    elif ratio is not None and ratio >= 0.85:
        status = "near-limit"
        strategy = "Use chapter subsets and preserve output/reasoning headroom."
    else:
        status = "fits-estimate"
        strategy = "A full pass may fit, but keep source IDs and incremental checkpoints."
    return {
        "status": status,
        "context_window_tokens": context_window,
        "reserved_output_tokens": args.reserved_output_tokens,
        "overhead_tokens": args.overhead_tokens,
        "safety_margin": args.safety_margin,
        "usable_input_tokens": usable,
        "upper_bound_ratio": round(ratio, 4) if ratio is not None else None,
        "strategy": strategy,
    }


def quality_ceiling(
    measurements: dict[str, Any], fit: dict[str, Any]
) -> dict[str, Any]:
    notices: list[dict[str, str]] = []
    roles = measurements["role_guess_counts"]
    unknown_files = measurements["token_estimate"]["unknown_files"]

    if fit["status"] == "unknown":
        content_coverage = "unverified"
        add_notice(
            notices,
            "CONTEXT_LIMIT_UNKNOWN",
            "warning",
            "The platform context limit is unknown, so one-pass coverage cannot be claimed.",
        )
    elif fit["status"] == "chunking-required":
        content_coverage = "incremental-only"
        add_notice(
            notices,
            "MATERIALS_EXCEED_SAFE_CONTEXT",
            "warning",
            (
                "The material upper estimate exceeds safe input capacity; full coverage "
                "requires chunked retrieval and checkpoints."
            ),
        )
    elif fit["status"] in {"indeterminate", "near-limit"}:
        content_coverage = "limited-or-incremental"
    else:
        content_coverage = "full-pass-possible"

    if unknown_files:
        content_coverage = "limited-or-incremental"
        add_notice(
            notices,
            "UNSIZED_MATERIALS",
            "warning",
            f"{len(unknown_files)} source file(s) have no usable token estimate.",
        )
    if measurements["needs_ocr_files"]:
        add_notice(
            notices,
            "OCR_REQUIRED",
            "warning",
            f"{len(measurements['needs_ocr_files'])} PDF(s) need OCR before reliable coverage claims.",
        )
    if measurements["encrypted_files"]:
        add_notice(
            notices,
            "ENCRYPTED_MATERIALS",
            "warning",
            f"{len(measurements['encrypted_files'])} encrypted PDF(s) could not be inspected.",
        )

    specification_count = int(roles.get("assessment-specification", 0))
    past_count = int(roles.get("past-assessment", 0))
    solution_count = int(roles.get("official-solution", 0))
    assessment_signal_count = sum(int(roles.get(role, 0)) for role in ASSESSMENT_ROLES)

    if specification_count and past_count >= 2 and solution_count:
        exam_calibration = "potentially-strong-after-verification"
    elif assessment_signal_count:
        exam_calibration = "limited-until-verified"
        add_notice(
            notices,
            "THIN_OR_INCOMPLETE_ASSESSMENT_EVIDENCE",
            "warning",
            "The inferred assessment evidence set is incomplete; frequency and weighting claims remain limited.",
        )
    else:
        exam_calibration = "unavailable"
        add_notice(
            notices,
            "NO_ASSESSMENT_EVIDENCE",
            "warning",
            "No assessment-bearing source was inferred; the product can only claim source-grounded course coverage.",
        )

    if solution_count:
        answer_depth = "potentially-calibrated-after-verification"
    else:
        answer_depth = "not-calibrated-to-official-solutions"
        add_notice(
            notices,
            "NO_OFFICIAL_SOLUTIONS",
            "warning",
            "Without official solutions or marking guides, answer depth and awarded-step coverage cannot be certified.",
        )

    add_notice(
        notices,
        "ROLE_GUESSES_REQUIRE_VERIFICATION",
        "info",
        "Evidence-role counts come from filenames and are routing hints, not verified course facts.",
    )
    return {
        "status": "preliminary",
        "content_coverage": content_coverage,
        "exam_calibration": exam_calibration,
        "answer_depth": answer_depth,
        "mandatory_notices": notices,
    }


def render_markdown(report: dict[str, Any], language: str) -> str:
    volume = report["material_volume"]
    estimate = volume["token_estimate"]
    fit = report["context_fit"]
    ceiling = report["quality_ceiling"]
    if language == "zh":
        heading = "# 材料容量与成品质量上限"
        labels = {
            "scope": "检查范围",
            "volume": "材料容量",
            "fit": "上下文适配",
            "quality": "质量上限（初步）",
            "limits": "必须披露的限制",
        }
        lines = [
            heading,
            "",
            f"- {labels['scope']}：{report['scope']['selected_files']} 个文件",
            f"- {labels['volume']}：{volume['total_bytes']} bytes，PDF 共 {volume['pdf_pages']} 页",
            (
                f"- Token 估算：{estimate['lower_bound_tokens']}–"
                f"{estimate['upper_bound_tokens']}（中值 {estimate['estimated_tokens']}）"
            ),
            f"- {labels['fit']}：`{fit['status']}`；安全输入容量：`{fit['usable_input_tokens'] or 'unknown'}`",
            f"- 处理策略：{ZH_STRATEGIES.get(fit['status'], fit['strategy'])}",
            "",
            f"## {labels['quality']}",
            "",
            f"- 内容覆盖：`{ceiling['content_coverage']}`",
            f"- 考试校准：`{ceiling['exam_calibration']}`",
            f"- 答题深度校准：`{ceiling['answer_depth']}`",
            "",
            f"## {labels['limits']}",
            "",
        ]
    else:
        lines = [
            "# Material Capacity and Product Quality Ceiling",
            "",
            f"- Scope: {report['scope']['selected_files']} files",
            f"- Volume: {volume['total_bytes']} bytes and {volume['pdf_pages']} PDF pages",
            (
                f"- Token estimate: {estimate['lower_bound_tokens']}–"
                f"{estimate['upper_bound_tokens']} (midpoint {estimate['estimated_tokens']})"
            ),
            f"- Context fit: `{fit['status']}`; safe input capacity: `{fit['usable_input_tokens'] or 'unknown'}`",
            f"- Processing strategy: {fit['strategy']}",
            "",
            "## Preliminary quality ceiling",
            "",
            f"- Content coverage: `{ceiling['content_coverage']}`",
            f"- Exam calibration: `{ceiling['exam_calibration']}`",
            f"- Answer-depth calibration: `{ceiling['answer_depth']}`",
            "",
            "## Mandatory limitations",
            "",
        ]
    for notice in ceiling["mandatory_notices"]:
        message = (
            ZH_NOTICE_MESSAGES.get(notice["code"], notice["message"])
            if language == "zh"
            else notice["message"]
        )
        lines.append(f"- **{notice['code']}** ({notice['severity']}): {message}")
    lines.extend(["", f"Generated: `{report['generated_at']}`", ""])
    return "\n".join(lines)


def update_study_state(
    state_path: Path,
    report_path: Path,
    report: dict[str, Any],
    chapter_slug: str | None,
) -> None:
    from manage_state import find_chapter, read_state, validate_state, write_state

    state = read_state(state_path)
    if state.get("schema_version") != 2:
        raise ValueError("study state must be migrated to schema_version 2")
    state["capacity"] = {
        "report_path": str(report_path),
        "status": report["context_fit"]["status"],
        "quality_ceiling": report["quality_ceiling"],
        "last_checked_at": report["generated_at"],
    }
    if chapter_slug:
        chapter = find_chapter(state, chapter_slug)
        if chapter is None:
            raise ValueError(f"unknown chapter slug {chapter_slug}")
        chapter.setdefault("qa", {})["capacity_disclosure"] = "pass"
    state["updated_at"] = utc_now()
    errors = validate_state(state)
    if errors:
        raise ValueError("; ".join(errors))
    write_state(state_path, state)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventory", type=Path)
    parser.add_argument("--output", type=Path, required=True, help="capacity report JSON")
    parser.add_argument("--markdown", type=Path, help="optional human-readable report")
    parser.add_argument("--language", choices=("en", "zh"), default="en")
    parser.add_argument("--source-id", action="append", default=[])
    parser.add_argument("--context-window", type=int)
    parser.add_argument("--reserved-output-tokens", type=int, default=8192)
    parser.add_argument("--overhead-tokens", type=int, default=8192)
    parser.add_argument("--safety-margin", type=float, default=0.15)
    parser.add_argument("--study-state", type=Path)
    parser.add_argument("--chapter-slug")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.context_window is not None and args.context_window <= 0:
        print("--context-window must be positive", file=sys.stderr)
        return 2
    if args.reserved_output_tokens < 0 or args.overhead_tokens < 0:
        print("token reserves must be non-negative", file=sys.stderr)
        return 2
    if not 0 <= args.safety_margin < 1:
        print("--safety-margin must be in [0, 1)", file=sys.stderr)
        return 2
    if args.chapter_slug and not args.study_state:
        print("--chapter-slug requires --study-state", file=sys.stderr)
        return 2
    try:
        inventory = read_json(args.inventory)
        materials, _ = choose_materials(inventory, args.source_id)
        measurements = material_measurements(materials)
        fit = context_fit(args, measurements)
        report = {
            "schema_version": 1,
            "generated_at": utc_now(),
            "inventory_path": str(args.inventory.resolve()),
            "inventory_digest": inventory.get("inventory_digest"),
            "scope": {
                "selected_source_ids": args.source_id or "all",
                "selected_files": len(materials),
            },
            "material_volume": measurements,
            "context_fit": fit,
            "quality_ceiling": quality_ceiling(measurements, fit),
        }
        write_json(args.output, report)
        if args.markdown:
            args.markdown.parent.mkdir(parents=True, exist_ok=True)
            args.markdown.write_text(render_markdown(report, args.language), encoding="utf-8")
        if args.study_state:
            update_study_state(args.study_state, args.output, report, args.chapter_slug)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"capacity error: {exc}", file=sys.stderr)
        return 2
    estimate = report["material_volume"]["token_estimate"]
    print(
        "capacity: "
        f"status={fit['status']} files={len(materials)} "
        f"estimated={estimate['estimated_tokens']} upper={estimate['upper_bound_tokens']} "
        f"report={args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
