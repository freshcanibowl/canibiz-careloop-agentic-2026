from datetime import date
from app.models.care_plan import CarePlan, TaskStatus
from app.storage import InMemoryTaskRepository
from app.use_cases import create_follow_up_plan
from app.services.followup_engine import detect_missing_actions

def test_overdue_observation_changes_state_and_creates_agent_action():
    plan = CarePlan(
        "plan-pika-002", "pet-pika",
        "Transition food over 7 days. Record stool daily. Review after 7 days.",
        date(2026,8,28), date(2026,9,4)
    )
    tasks = create_follow_up_plan(plan, InMemoryTaskRepository())

    actions = detect_missing_actions(tasks, current_day=3)

    overdue_stool = [
        t for t in tasks
        if t["kind"] == "STOOL_OBSERVATION" and t["due_day"] in (1,2)
    ]
    assert len(overdue_stool) == 2
    assert all(t["status"] == TaskStatus.FOLLOW_UP_REQUIRED for t in overdue_stool)
    assert len(actions) == 2
    assert all(a.action_type == "REQUEST_OWNER_FOLLOW_UP" for a in actions)
