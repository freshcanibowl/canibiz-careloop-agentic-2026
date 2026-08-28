from dataclasses import asdict
from app.models.care_plan import TaskStatus


class InMemoryTaskRepository:
    def __init__(self):
        self._tasks = {}

    def save_many(self, tasks):
        for task in tasks:
            self._tasks[task.task_id] = asdict(task)

    def save_dicts(self, tasks):
        for task in tasks:
            payload = dict(task)
            status = payload.get("status")
            if isinstance(status, TaskStatus):
                payload["status"] = status
            self._tasks[payload["task_id"]] = payload

    def list_for_plan(self, plan_id):
        return [dict(t) for t in self._tasks.values() if t["plan_id"] == plan_id]
