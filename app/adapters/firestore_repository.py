from dataclasses import asdict
from app.models.care_plan import TaskStatus


class FirestoreTaskRepository:
    def __init__(self, project: str | None = None):
        try:
            from google.cloud import firestore
        except ImportError as exc:
            raise RuntimeError("Install google-cloud-firestore to use FirestoreTaskRepository") from exc
        self.db = firestore.Client(project=project)

    @staticmethod
    def _serialize(payload: dict) -> dict:
        out = dict(payload)
        status = out.get("status")
        if isinstance(status, TaskStatus):
            out["status"] = status.value
        return out

    @staticmethod
    def _hydrate(payload: dict) -> dict:
        out = dict(payload)
        status = out.get("status")
        if isinstance(status, str):
            try:
                out["status"] = TaskStatus(status)
            except ValueError:
                pass
        return out

    def save_many(self, tasks):
        self.save_dicts([asdict(task) for task in tasks])

    def save_dicts(self, tasks):
        batch = self.db.batch()
        for task in tasks:
            payload = self._serialize(task)
            ref = self.db.collection("careloop_tasks").document(payload["task_id"])
            batch.set(ref, payload)
        batch.commit()

    def list_for_plan(self, plan_id: str):
        docs = (
            self.db.collection("careloop_tasks")
            .where("plan_id", "==", plan_id)
            .stream()
        )
        return [self._hydrate(doc.to_dict()) for doc in docs]
