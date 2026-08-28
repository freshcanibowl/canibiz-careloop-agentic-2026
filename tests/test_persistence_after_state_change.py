from datetime import date
from app.models.care_plan import CarePlan, TaskStatus
from app.models.observation import StructuredObservation
from app.storage import InMemoryTaskRepository
from app.use_cases import create_follow_up_plan
from app.services.task_state import apply_observation


def test_state_change_is_persistable_across_repository_read():
    repo = InMemoryTaskRepository()
    plan = CarePlan(
        "plan-persist-1", "pet-pika",
        "Record stool daily. Review after 7 days.",
        date(2026,8,28), date(2026,9,4)
    )
    tasks = create_follow_up_plan(plan, repo)
    obs = StructuredObservation("pet-pika", 3, stool_score=5)
    apply_observation(tasks, obs)
    repo.save_dicts(tasks)

    reread = repo.list_for_plan(plan.plan_id)
    day3 = [t for t in reread if t["kind"] == "STOOL_OBSERVATION" and t["due_day"] == 3][0]
    assert day3["status"] == TaskStatus.COMPLETED
