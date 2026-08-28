import os
from app.runtime import build_task_repository, build_observation_structurer
from app.storage import InMemoryTaskRepository
from app.runtime import DeterministicObservationStructurer
from app.adapters.gemini_observation import GeminiObservationStructurer


def test_default_runtime_is_offline_and_reproducible(monkeypatch):
    monkeypatch.delenv("CARELOOP_STORAGE_BACKEND", raising=False)
    monkeypatch.delenv("CARELOOP_AI_BACKEND", raising=False)
    assert isinstance(build_task_repository(), InMemoryTaskRepository)
    assert isinstance(build_observation_structurer(), DeterministicObservationStructurer)


def test_gemini_runtime_uses_required_3_5_default(monkeypatch):
    monkeypatch.setenv("CARELOOP_AI_BACKEND", "gemini")
    monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", "careloop-project")
    monkeypatch.setenv("GOOGLE_CLOUD_LOCATION", "global")
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    adapter = build_observation_structurer()
    assert isinstance(adapter, GeminiObservationStructurer)
    assert adapter.model == "gemini-3.5-flash"
    assert adapter.project == "careloop-project"
    assert adapter.location == "global"
