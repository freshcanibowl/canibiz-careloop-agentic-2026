from datetime import date
from app.models.care_plan import CarePlan, TaskStatus
from app.models.observation import StructuredObservation
from app.storage import InMemoryTaskRepository
from app.use_cases import create_follow_up_plan
from app.services.task_state import apply_observation
from app.services.followup_engine import detect_missing_actions
from app.services.vetbrief_builder import build_vetbrief
from app.services.vetbrief_renderer import render_vetbrief

def test_state_becomes_auditable_vetbrief():
    plan = CarePlan(
        "plan-pika-003", "pet-pika",
        "Transition food over 7 days. Record stool daily. Monitor appetite and vomiting. Review after 7 days.",
        date(2026,8,28), date(2026,9,4)
    )
    tasks = create_follow_up_plan(plan, InMemoryTaskRepository())

    day3 = StructuredObservation("pet-pika", 3, stool_score=5, appetite="normal", vomiting=False)
    day7 = StructuredObservation("pet-pika", 7, stool_score=4, appetite=None, vomiting=None)
    apply_observation(tasks, day3)
    apply_observation(tasks, day7)

    # Simulate completed transition at day 7.
    for task in tasks:
        if task["kind"] == "FEEDING_TRANSITION":
            task["status"] = TaskStatus.COMPLETED

    detect_missing_actions(tasks, current_day=8)

    brief = build_vetbrief(
        plan.plan_id, plan.pet_id, tasks, [day3, day7], through_day=7
    )

    assert brief.pet_id == "pet-pika"
    assert brief.expected_owner_tasks == 10
    assert brief.completed_tasks == 5
    assert brief.adherence_percent == 50
    assert brief.safety_status == "CONTINUE_MONITORING"
    assert "Day 3: stool 5, appetite normal, no vomiting reported" in brief.longitudinal_summary
    assert "Day 7: stool 4" in brief.longitudinal_summary
    assert any("STOOL_OBSERVATION day 1" == x for x in brief.outstanding_tasks)

    rendered = render_vetbrief(brief)
    assert "FOLLOW-UP ADHERENCE" in rendered
    assert "50% (5/10 expected owner tasks completed)" in rendered
    assert "It does not diagnose or prescribe." in rendered

def test_vetbrief_routes_concerning_owner_report_to_professional_review():
    plan = CarePlan(
        "plan-pika-004", "pet-pika",
        "Record stool daily. Monitor appetite and vomiting. Review after 7 days.",
        date(2026,8,28), date(2026,9,4)
    )
    tasks = create_follow_up_plan(plan, InMemoryTaskRepository())
    obs = StructuredObservation("pet-pika", 3, stool_score=7, appetite="low", vomiting=True)
    apply_observation(tasks, obs)

    brief = build_vetbrief(plan.plan_id, plan.pet_id, tasks, [obs], through_day=3)

    assert brief.safety_status == "PROFESSIONAL_REVIEW_REQUIRED"
    assert set(brief.safety_reasons) == {
        "vomiting_reported",
        "watery_stool_reported",
        "reduced_appetite_reported",
    }
