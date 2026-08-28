from app.services.task_builder import build_follow_up_tasks

def create_follow_up_plan(plan, repository):
    tasks = build_follow_up_tasks(plan)
    if not tasks:
        raise ValueError("Care plan produced no actionable follow-up tasks")
    repository.save_many(tasks)
    return repository.list_for_plan(plan.plan_id)
