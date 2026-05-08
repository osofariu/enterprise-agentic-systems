"""Deterministic business logic for training recommendations.

Thresholds and prompt building live here — not in LLM instructions —
so numeric decisions are reliable. The LLM composes the natural-language
recommendation_basis, but this module decides IF a recommendation is made.
"""

from enum import Enum

from utils.models import MaintenanceDoc, MaintenancePersonnelBucket, TrainingRecommendation

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


# ── Labels ────────────────────────────────────────────────────────────────

_LEVEL_LABELS = {
    RecommendationLevel.SKIP: ("SKIP", "Insufficient data for recommendation"),
    RecommendationLevel.RECOMMEND: ("RECOMMENDED", "Pattern warrants training review"),
    RecommendationLevel.STRONGLY_RECOMMEND: (
        "STRONGLY RECOMMENDED",
        "Significant recurring pattern detected",
    ),
}


def build_recommendations(
    personnel_data: list[MaintenancePersonnelBucket],
    docs: list[MaintenanceDoc],
) -> list[TrainingRecommendation]:
    """Apply thresholds to personnel data and build recommendations.

    Args:
        personnel_data: Parsed results from the maintenance personnel-lookup
            endpoint — each bucket is one person plus the specific
            (machine_id, reason_code) issues they were present for.
        docs: Parsed results from the maintenance docs endpoint — used to
            attach human-readable description and training material to each
            recommendation.

    Returns:
        List of TrainingRecommendation objects, one per (personnel, issue) pair
        that meets the RECOMMEND threshold or higher.
    """
    # Index docs by reason_code and type for quick lookup
    docs_by_code: dict[str, dict[str, str]] = {}
    for doc in docs:
        docs_by_code.setdefault(doc.reason_code, {})[doc.reason_type] = doc.document

    recommendations: list[TrainingRecommendation] = []

    for person in personnel_data:
        for issue in person.issues:
            level = assess(
                average_duration_hours=issue.average_duration_hours,
                record_count=issue.record_count,
                total_duration_hours=issue.total_duration_hours,
            )

            if level == RecommendationLevel.SKIP:
                continue

            code_docs = docs_by_code.get(issue.reason_code, {})

            rec = TrainingRecommendation(
                personnel_id=person.personnel_id,
                personnel_name=person.personnel_name,
                machine_id=issue.machine_id,
                reason_code=issue.reason_code,
                level=level.value,
                record_count=issue.record_count,
                total_duration_hours=issue.total_duration_hours,
                average_duration_hours=issue.average_duration_hours,
                reason_description=code_docs.get("description"),
                training_doc=code_docs.get("training"),
            )
            recommendations.append(rec.model_copy(update={"approval_prompt": build_approval_prompt(rec)}))

    return recommendations


def build_approval_prompt(rec: TrainingRecommendation) -> str:
    """Build the rich approval prompt shown to the human reviewer."""
    level = RecommendationLevel(rec.level)
    label, explanation = _LEVEL_LABELS[level]

    # Visual bar: filled blocks proportional to avg hours (max ~10)
    filled = min(int(rec.average_duration_hours), 10)
    bar = "\u2593" * filled + "\u2591" * (10 - filled)

    lines = [
        "",
        f"  TRAINING {label}",
        f"  {explanation}",
        "",
        (
            f"  Personnel:  {rec.personnel_name} ({rec.personnel_id})"
            if rec.personnel_name
            else f"  Personnel:  {rec.personnel_id}"
        ),
        f"  Machine:    {rec.machine_id}",
        f"  Issue:      {rec.reason_code}",
    ]

    if rec.reason_description:
        lines.append(f"              {rec.reason_description}")

    lines += [
        "",
        f"  Events:     {rec.record_count}  {bar}",
        f"  Total hrs:  {rec.total_duration_hours:.1f}",
        f"  Avg hrs:    {rec.average_duration_hours:.1f}",
        "",
        f"  Thresholds (avg hrs): skip <={SKIP_THRESHOLD}  |  recommend >{RECOMMEND_THRESHOLD}  |  strongly >{STRONG_THRESHOLD}  (min {MIN_RECORD_COUNT} events)",
    ]

    if rec.training_doc:
        # Truncate long docs for display
        doc_display = rec.training_doc[:120] + "..." if len(rec.training_doc) > 120 else rec.training_doc
        lines += [
            "",
            f"  Training doc:",
            f'    "{doc_display}"',
        ]

    lines.append("")

    return "\n".join(lines)
