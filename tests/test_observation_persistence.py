from app.models.observation import StructuredObservation
from app import storage
from fastapi.testclient import TestClient

from app import api
from app.runtime import DeterministicObservationStructurer
from app.storage import InMemoryTaskRepository
from app.adapters.firestore_repository import FirestoreObservationRepository


def test_observation_history_survives_repository_reread():
    assert hasattr(storage, "InMemoryObservationRepository"), (
        "observation repository is required for persistent VetBrief history"
    )
    repo = storage.InMemoryObservationRepository()
    first = StructuredObservation(
        pet_id="pet-pika",
        day=3,
        stool_score=5,
        appetite="normal",
        vomiting=False,
    )

    repo.save("plan-persist-observations", first)

    assert repo.list_for_plan("plan-persist-observations") == [first]


def test_same_day_observation_update_replaces_previous_value():
    repo = storage.InMemoryObservationRepository()
    repo.save(
        "plan-observation-update",
        StructuredObservation("pet-pika", 3, stool_score=6),
    )

    latest = StructuredObservation("pet-pika", 3, stool_score=4)
    repo.save("plan-observation-update", latest)

    assert repo.list_for_plan("plan-observation-update") == [latest]


def test_vetbrief_reads_observations_from_repository(monkeypatch):
    monkeypatch.setattr(api, "_task_repo", InMemoryTaskRepository())
    monkeypatch.setattr(api, "_structurer", DeterministicObservationStructurer())
    monkeypatch.setattr(
        api, "_observation_repo", storage.InMemoryObservationRepository(), raising=False
    )
    client = TestClient(api.app)

    plan_id = "plan-api-observation-persistence"
    assert client.post(
        "/plans",
        json={
            "plan_id": plan_id,
            "pet_id": "pet-pika",
            "instructions": "Record stool daily. Review after 7 days.",
            "start_date": "2026-08-28",
            "review_date": "2026-09-04",
        },
    ).status_code == 200
    assert client.post(
        "/observations",
        json={
            "plan_id": plan_id,
            "pet_id": "pet-pika",
            "day": 3,
            "message": "Stool was 5, appetite normal, no vomiting.",
        },
    ).status_code == 200

    response = client.post(
        "/vetbrief",
        json={"plan_id": plan_id, "pet_id": "pet-pika", "through_day": 3},
    )

    assert response.status_code == 200
    assert response.json()["brief"]["longitudinal_summary"] == [
        "Day 3: stool 5, appetite normal, no vomiting reported"
    ]


def test_firestore_observation_repository_round_trip(monkeypatch):
    stored = {}

    class FakeDocument:
        def __init__(self, document_id):
            self.document_id = document_id

        def set(self, payload):
            stored[self.document_id] = dict(payload)

    class FakeSnapshot:
        def __init__(self, payload):
            self.payload = payload

        def to_dict(self):
            return dict(self.payload)

    class FakeQuery:
        def __init__(self, plan_id):
            self.plan_id = plan_id

        def stream(self):
            return [
                FakeSnapshot(payload)
                for payload in stored.values()
                if payload["plan_id"] == self.plan_id
            ]

    class FakeCollection:
        def document(self, document_id):
            return FakeDocument(document_id)

        def where(self, field, operator, value):
            assert (field, operator) == ("plan_id", "==")
            return FakeQuery(value)

    class FakeClient:
        def collection(self, name):
            assert name == "careloop_observations"
            return FakeCollection()

    from google.cloud import firestore

    monkeypatch.setattr(firestore, "Client", lambda project=None: FakeClient())
    repo = FirestoreObservationRepository()
    assert hasattr(repo, "save"), "Firestore observation persistence is missing"
    observation = StructuredObservation("pet-pika", 4, stool_score=4)

    repo.save("plan-firestore-observations", observation)

    assert repo.list_for_plan("plan-firestore-observations") == [observation]
