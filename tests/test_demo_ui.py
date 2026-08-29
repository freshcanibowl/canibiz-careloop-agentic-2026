from fastapi.testclient import TestClient

from app import api
from app.runtime import DeterministicObservationStructurer
from app.storage import InMemoryObservationRepository, InMemoryTaskRepository


app = api.app


def test_root_serves_the_careloop_workflow_ui():
    response = TestClient(app).get("/")

    assert response.status_code == 200
    assert "CaniBiz CareLoop" in response.text
    assert "Create follow-up plan" in response.text
    assert "Structure update" in response.text
    assert "VetBrief preview" in response.text
    assert "Download VetBrief" in response.text


def test_observation_response_returns_updated_timeline_tasks(monkeypatch):
    monkeypatch.setattr(api, "_task_repo", InMemoryTaskRepository())
    monkeypatch.setattr(api, "_observation_repo", InMemoryObservationRepository())
    monkeypatch.setattr(api, "_structurer", DeterministicObservationStructurer())
    client = TestClient(app)
    plan_id = "demo-ui-timeline"
    client.post("/plans", json={
        "plan_id": plan_id,
        "pet_id": "pet-pika",
        "instructions": "Record stool daily. Monitor appetite and vomiting. Review after 7 days.",
        "start_date": "2026-08-28",
        "review_date": "2026-09-04",
    })

    response = client.post("/observations", json={
        "plan_id": plan_id,
        "pet_id": "pet-pika",
        "day": 3,
        "message": "Stool was 5, appetite normal, no vomiting.",
    })

    completed = {
        task["kind"]
        for task in response.json()["tasks"]
        if task["due_day"] == 3 and task["status"] == "COMPLETED"
    }
    assert completed == {
        "STOOL_OBSERVATION",
        "APPETITE_OBSERVATION",
        "VOMITING_OBSERVATION",
    }
