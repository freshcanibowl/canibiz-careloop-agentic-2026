from app.models.care_plan import TaskStatus

def apply_observation(tasks, observation):
    for task in tasks:
        if task["pet_id"] != observation.pet_id or task["due_day"] != observation.day:
            continue
        if task["kind"] == "STOOL_OBSERVATION" and observation.stool_score is not None:
            task["status"] = TaskStatus.COMPLETED
        elif task["kind"] == "APPETITE_OBSERVATION" and observation.appetite is not None:
            task["status"] = TaskStatus.COMPLETED
        elif task["kind"] == "VOMITING_OBSERVATION" and observation.vomiting is not None:
            task["status"] = TaskStatus.COMPLETED
    return tasks
