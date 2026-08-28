from datetime import date
from app.models.care_plan import CarePlan, TaskStatus
from app.storage import InMemoryTaskRepository
from app.use_cases import create_follow_up_plan

def test_vet_plan_creates_and_persists_follow_up_tasks():
    plan = CarePlan(
        "plan-pika-001", "pet-pika",
        "Transition food over 7 days. Record stool daily. Monitor appetite and vomiting. Review after 7 days.",
        date(2026, 8, 28), date(2026, 9, 4)
    )
    repo = InMemoryTaskRepository()
    persisted = create_follow_up_plan(plan, repo)
    kinds = [t["kind"] for t in persisted]
    assert "FEEDING_TRANSITION" in kinds
    assert kinds.count("STOOL_OBSERVATION") == 7
    assert "APPETITE_OBSERVATION" in kinds
    assert "VOMITING_OBSERVATION" in kinds
    assert "PROFESSIONAL_REVIEW" in kinds
    assert all(t["status"] == TaskStatus.PENDING for t in persisted)
    assert len(repo.list_for_plan("plan-pika-001")) == len(persisted)
