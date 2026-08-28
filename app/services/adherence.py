from app.models.care_plan import TaskStatus

OWNER_TASKS = {
    "FEEDING_TRANSITION",
    "STOOL_OBSERVATION",
    "APPETITE_OBSERVATION",
    "VOMITING_OBSERVATION",
}

def calculate_adherence(tasks: list[dict], through_day: int) -> tuple[int, int, int]:
    expected = [
        t for t in tasks
        if t["kind"] in OWNER_TASKS and t["due_day"] <= through_day
    ]
    completed = [t for t in expected if t["status"] == TaskStatus.COMPLETED]
    pct = round((len(completed) / len(expected)) * 100) if expected else 100
    return pct, len(completed), len(expected)
