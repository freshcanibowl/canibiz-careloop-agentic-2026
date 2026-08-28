from dataclasses import dataclass
from app.models.observation import StructuredObservation

@dataclass(frozen=True)
class SafetyDecision:
    status: str
    reasons: tuple[str, ...]

def evaluate_observation(observation: StructuredObservation) -> SafetyDecision:
    """
    Minimal deterministic demo gate.
    It does not diagnose. It decides whether the workflow needs professional review.
    Thresholds here are demo workflow rules, not veterinary diagnostic rules.
    """
    reasons = []

    if observation.vomiting is True:
        reasons.append("vomiting_reported")

    if observation.stool_score is not None and observation.stool_score >= 7:
        reasons.append("watery_stool_reported")

    if observation.appetite == "low":
        reasons.append("reduced_appetite_reported")

    if reasons:
        return SafetyDecision("PROFESSIONAL_REVIEW_REQUIRED", tuple(reasons))
    return SafetyDecision("CONTINUE_MONITORING", ())
