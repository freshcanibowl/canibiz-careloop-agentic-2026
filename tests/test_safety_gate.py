from app.models.observation import StructuredObservation
from app.services.safety_gate import evaluate_observation

def test_normal_day_continues_monitoring():
    obs = StructuredObservation("pet-pika", 3, stool_score=5, appetite="normal", vomiting=False)
    decision = evaluate_observation(obs)
    assert decision.status == "CONTINUE_MONITORING"
    assert decision.reasons == ()

def test_reported_concerning_observations_require_professional_review():
    obs = StructuredObservation("pet-pika", 4, stool_score=7, appetite="low", vomiting=True)
    decision = evaluate_observation(obs)
    assert decision.status == "PROFESSIONAL_REVIEW_REQUIRED"
    assert set(decision.reasons) == {
        "vomiting_reported",
        "watery_stool_reported",
        "reduced_appetite_reported",
    }
