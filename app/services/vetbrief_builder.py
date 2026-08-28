from app.models.care_plan import TaskStatus
from app.models.vetbrief import VetBrief
from app.services.adherence import calculate_adherence
from app.services.safety_gate import evaluate_observation

def build_vetbrief(plan_id: str, pet_id: str, tasks: list[dict], observations: list, through_day: int) -> VetBrief:
    adherence, completed, expected = calculate_adherence(tasks, through_day)

    outstanding = tuple(
        f"{t['kind']} day {t['due_day']}"
        for t in tasks
        if t["due_day"] <= through_day
        and t["kind"] != "PROFESSIONAL_REVIEW"
        and t["status"] != TaskStatus.COMPLETED
    )

    safety_reasons = []
    summary = []
    for obs in sorted(observations, key=lambda o: o.day):
        decision = evaluate_observation(obs)
        safety_reasons.extend(decision.reasons)
        parts = [f"Day {obs.day}"]
        if obs.stool_score is not None:
            parts.append(f"stool {obs.stool_score}")
        if obs.appetite is not None:
            parts.append(f"appetite {obs.appetite}")
        if obs.vomiting is not None:
            parts.append("vomiting reported" if obs.vomiting else "no vomiting reported")
        summary.append(": ".join([parts[0], ", ".join(parts[1:])]))

    unique_reasons = tuple(dict.fromkeys(safety_reasons))
    safety_status = "PROFESSIONAL_REVIEW_REQUIRED" if unique_reasons else "CONTINUE_MONITORING"

    return VetBrief(
        pet_id=pet_id,
        plan_id=plan_id,
        adherence_percent=adherence,
        completed_tasks=completed,
        expected_owner_tasks=expected,
        outstanding_tasks=outstanding,
        safety_status=safety_status,
        safety_reasons=unique_reasons,
        longitudinal_summary=tuple(summary),
    )
