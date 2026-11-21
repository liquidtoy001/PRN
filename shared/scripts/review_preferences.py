"""Validate optional teaching/review preferences while accepting existing configurations."""
from __future__ import annotations

from datetime import date
import math


def validate_study_time(preferences: dict) -> list[str]:
    deadline = preferences.get("assessment_date")
    hours = preferences.get("study_hours_available")
    errors = []
    if deadline is not None:
        try:
            if date.fromisoformat(deadline).isoformat() != deadline:
                raise ValueError
        except (TypeError, ValueError):
            errors.append("assessment_date must be a calendar date in YYYY-MM-DD format")
    if hours is not None and (
        type(hours) not in (int, float) or hours <= 0
        or (isinstance(hours, float) and not math.isfinite(hours))
    ):
        errors.append("study_hours_available must be a positive finite number")
    if preferences.get("mode") == "exam-cram" and (deadline is None or hours is None):
        errors.append("exam-cram requires a deadline and study hours")
    return errors


FIELDS = {
    "exam_organisation", "exam_basis_source_ids", "exam_answer_language",
    "show_source_index", "show_source_explanations", "second_pass_review",
    "include_code",
}


def validate_review_preferences(config: dict) -> list[str]:
    errors = []
    choices = {
        "exam_organisation": {"source-led", "topic-led"},
        "second_pass_review": {"automatic", "on-request"},
    }
    for key, allowed in choices.items():
        if key in config and (not isinstance(config[key], str) or config[key] not in allowed):
            errors.append(f"{key} must be one of {sorted(allowed)}")
    for key in ("show_source_index", "show_source_explanations", "include_code"):
        if key in config and type(config[key]) is not bool:
            errors.append(f"{key} must be boolean")
    if "exam_answer_language" in config:
        language = config["exam_answer_language"]
        if language is not None and (not isinstance(language, str) or language not in {"zh", "en", "bilingual"}):
            errors.append("exam_answer_language must be zh, en, bilingual or null")
    if "exam_basis_source_ids" in config:
        sources = config["exam_basis_source_ids"]
        if not isinstance(sources, list) or any(not isinstance(item, str) or not item.strip() for item in sources):
            errors.append("exam_basis_source_ids must be a list of nonempty source IDs")
        elif len(sources) != len(set(sources)):
            errors.append("exam_basis_source_ids must be unique")
    return errors
