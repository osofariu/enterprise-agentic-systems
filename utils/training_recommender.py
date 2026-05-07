"""Deterministic business logic for training recommendations.

Thresholds and prompt building live here — not in LLM instructions —
so numeric decisions are reliable. The LLM composes the natural-language
recommendation_basis, but this module decides IF a recommendation is made.
"""

from dataclasses import dataclass
from enum import Enum


# ── Thresholds ────────────────────────────────────────────────────────────

# These drive the three-tier recommendation logic based on average
# maintenance duration (hours per event). Higher averages indicate
# personnel spending more time per issue — a signal for training need.
#
#   avg_hours <= SKIP_THRESHOLD       → normal, skip
#   avg_hours > RECOMMEND_THRESHOLD   → recommend training
#   avg_hours > STRONG_THRESHOLD      → strongly recommend training
SKIP_THRESHOLD = 2.0
RECOMMEND_THRESHOLD = 3.0
STRONG_THRESHOLD = 4.0

# Minimum events required before we assess — avoids recommending
# training based on a single outlier event.
MIN_RECORD_COUNT = 2


class RecommendationLevel(str, Enum):
    SKIP = "skip"
    RECOMMEND = "recommend"
    STRONGLY_RECOMMEND = "strongly_recommend"


def assess(
    *,
    average_duration_hours: float,
    record_count: int,
    total_duration_hours: float,
) -> RecommendationLevel:
    """Determine recommendation level from maintenance stats.

    Uses average_duration_hours as the primary signal, with a minimum
    record_count gate to avoid noise from single events.
    """
    if record_count < MIN_RECORD_COUNT:
        return RecommendationLevel.SKIP
    if average_duration_hours > STRONG_THRESHOLD:
        return RecommendationLevel.STRONGLY_RECOMMEND
    if average_duration_hours > RECOMMEND_THRESHOLD:
        return RecommendationLevel.RECOMMEND
    return RecommendationLevel.SKIP


# ── Recommendation data ──────────────────────────────────────────────────


@dataclass
class Recommendation:
    """A single training recommendation with all context for approval."""

    personnel_id: str
    personnel_name: str | None
    machine_id: str
    reason_code: str
    level: RecommendationLevel
    record_count: int
    total_duration_hours: float
    average_duration_hours: float
    training_doc: str | None
    reason_description: str | None
    approval_prompt: str


# ── Labels ────────────────────────────────────────────────────────────────

_LEVEL_LABELS = {
    RecommendationLevel.SKIP: ("SKIP", "Insufficient data for recommendation"),
    RecommendationLevel.RECOMMEND: ("RECOMMENDED", "Pattern warrants training review"),
    RecommendationLevel.STRONGLY_RECOMMEND: (
        "STRONGLY RECOMMENDED",
        "Significant recurring pattern detected",
    ),
}


# ── Prompt builder ────────────────────────────────────────────────────────


def build_approval_prompt(
    *,
    personnel_id: str,
    personnel_name: str | None = None,
    machine_id: str,
    reason_code: str,
    level: RecommendationLevel,
    record_count: int,
    total_duration_hours: float,
    average_duration_hours: float,
    reason_description: str | None = None,
    training_doc: str | None = None,
) -> str:
    """Build the rich approval prompt shown to the human reviewer."""
    label, explanation = _LEVEL_LABELS[level]

    # Visual bar: filled blocks proportional to avg hours (max ~10)
    filled = min(int(average_duration_hours), 10)
    bar = "\u2593" * filled + "\u2591" * (10 - filled)

    lines = [
        "",
        f"  TRAINING {label}",
        f"  {explanation}",
        "",
        f"  Personnel:  {personnel_name} ({personnel_id})" if personnel_name else f"  Personnel:  {personnel_id}",
        f"  Machine:    {machine_id}",
        f"  Issue:      {reason_code}",
    ]

    if reason_description:
        lines.append(f"              {reason_description}")

    lines += [
        "",
        f"  Events:     {record_count}  {bar}",
        f"  Total hrs:  {total_duration_hours:.1f}",
        f"  Avg hrs:    {average_duration_hours:.1f}",
        "",
        f"  Thresholds (avg hrs): skip <={SKIP_THRESHOLD}  |  recommend >{RECOMMEND_THRESHOLD}  |  strongly >{STRONG_THRESHOLD}  (min {MIN_RECORD_COUNT} events)",
    ]

    if training_doc:
        # Truncate long docs for display
        doc_display = (
            training_doc[:120] + "..." if len(training_doc) > 120 else training_doc
        )
        lines += [
            "",
            f"  Training doc:",
            f'    "{doc_display}"',
        ]

    lines.append("")

    return "\n".join(lines)


def build_recommendations(
    personnel_data: list[dict],
    docs: list[dict],
) -> list[Recommendation]:
    """Apply thresholds to personnel data and build recommendations.

    Args:
        personnel_data: Results from maintenance_personnel API call.
            Each entry has personnel_id, record_count, total_duration_hours,
            average_duration_hours, and issues (list of machine_id/reason_code).
        docs: Results from maintenance_docs API call.
            Each entry has reason_code, reason_type, document.

    Returns:
        List of Recommendation objects, one per (personnel, issue) pair
        that meets the RECOMMEND threshold or higher.
    """
    # Index docs by reason_code and type for quick lookup
    docs_by_code: dict[str, dict[str, str]] = {}
    for doc in docs:
        code = doc["reason_code"]
        if code not in docs_by_code:
            docs_by_code[code] = {}
        docs_by_code[code][doc["reason_type"]] = doc["document"]

    recommendations: list[Recommendation] = []

    for person in personnel_data:
        for issue in person["issues"]:
            rc_count = issue["record_count"]
            rc_total = issue["total_duration_hours"]
            rc_avg = issue["average_duration_hours"]
            level = assess(
                average_duration_hours=rc_avg,
                record_count=rc_count,
                total_duration_hours=rc_total,
            )

            if level == RecommendationLevel.SKIP:
                continue

            rc = issue["reason_code"]
            reason_desc = docs_by_code.get(rc, {}).get("description")
            training_doc = docs_by_code.get(rc, {}).get("training")

            person_name = person.get("personnel_name")

            prompt = build_approval_prompt(
                personnel_id=person["personnel_id"],
                personnel_name=person_name,
                machine_id=issue["machine_id"],
                reason_code=rc,
                level=level,
                record_count=rc_count,
                total_duration_hours=rc_total,
                average_duration_hours=rc_avg,
                reason_description=reason_desc,
                training_doc=training_doc,
            )

            recommendations.append(
                Recommendation(
                    personnel_id=person["personnel_id"],
                    personnel_name=person_name,
                    machine_id=issue["machine_id"],
                    reason_code=rc,
                    level=level,
                    record_count=rc_count,
                    total_duration_hours=rc_total,
                    average_duration_hours=rc_avg,
                    training_doc=training_doc,
                    reason_description=reason_desc,
                    approval_prompt=prompt,
                )
            )

    return recommendations
