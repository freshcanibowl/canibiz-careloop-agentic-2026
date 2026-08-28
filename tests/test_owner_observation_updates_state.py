from datetime import date
from app.models.care_plan import CarePlan, TaskStatus
from app.storage import InMemoryTaskRepository
from app.use_cases import create_follow_up_plan
from app.services.observation_parser import parse_owner_observation
from app.services.task_state import apply_observation

def test_owner_message_changes_workflow_state():
    plan = CarePlan("plan-pika-001","pet-pika",
        "Transition food over 7 days. Record stool daily. Monitor appetite and vomiting. Review after 7 days.",
        date(2026,8,28), date(2026,9,4))
    tasks = create_follow_up_plan(plan, InMemoryTaskRepository())
    obs = parse_owner_observation("pet-pika", 3,
        "Pika's poop was softer today, maybe around 5. She finished her food and hasn't vomited.")
    assert (obs.stool_score, obs.appetite, obs.vomiting) == (5, "normal", False)
    updated = apply_observation(tasks, obs)
    statuses = {t["kind"]:t["status"] for t in updated if t["due_day"] == 3}
    assert statuses["STOOL_OBSERVATION"] == TaskStatus.COMPLETED
    assert statuses["APPETITE_OBSERVATION"] == TaskStatus.COMPLETED
    assert statuses["VOMITING_OBSERVATION"] == TaskStatus.COMPLETED
