from dataclasses import asdict
from app.models.care_plan import TaskStatus
from app.models.observation import StructuredObservation


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


class FirestoreObservationRepository:
    def __init__(self, project: str | None = None):
        try:
            from google.cloud import firestore
        except ImportError as exc:
            raise RuntimeError(
                "Install google-cloud-firestore to use FirestoreObservationRepository"
            ) from exc
        self.db = firestore.Client(project=project)

    def save(self, plan_id: str, observation: StructuredObservation):
        payload = asdict(observation)
        payload["plan_id"] = plan_id
        document_id = f"{plan_id}:{observation.pet_id}:{observation.day}"
        self.db.collection("careloop_observations").document(document_id).set(payload)

    def list_for_plan(self, plan_id: str):
        docs = (
            self.db.collection("careloop_observations")
            .where("plan_id", "==", plan_id)
            .stream()
        )
        observations = []
        for doc in docs:
            payload = doc.to_dict()
            payload.pop("plan_id", None)
            observations.append(StructuredObservation(**payload))
        return sorted(observations, key=lambda observation: observation.day)
