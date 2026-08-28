from app.models.care_plan import TaskStatus
from app.models.action import AgentAction

def detect_missing_actions(tasks: list[dict], current_day: int) -> list[AgentAction]:
    """Mark overdue owner-observation tasks and emit auditable next actions."""
    actions = []
    owner_task_kinds = {
        "STOOL_OBSERVATION",
        "APPETITE_OBSERVATION",
        "VOMITING_OBSERVATION",
        "FEEDING_TRANSITION",
    }
    for task in tasks:
        if (
            task["kind"] in owner_task_kinds
            and task["status"] == TaskStatus.PENDING
            and task["due_day"] < current_day
        ):
            task["status"] = TaskStatus.FOLLOW_UP_REQUIRED
            actions.append(
                AgentAction(
                    action_type="REQUEST_OWNER_FOLLOW_UP",
                    pet_id=task["pet_id"],
                    day=current_day,
                    reason=f"Overdue {task['kind']} from day {task['due_day']}",
                    target_task_id=task["task_id"],
                )
            )
    return actions
