import os
from app.storage import InMemoryObservationRepository, InMemoryTaskRepository
from app.adapters.firestore_repository import (
    FirestoreObservationRepository,
    FirestoreTaskRepository,
)
from app.adapters.gemini_observation import GeminiObservationStructurer
from app.services.observation_parser import parse_owner_observation


class DeterministicObservationStructurer:
    def structure(self, pet_id: str, day: int, message: str):
        return parse_owner_observation(pet_id, day, message)


def build_task_repository():
    backend = os.getenv("CARELOOP_STORAGE_BACKEND", "memory").lower()
    if backend == "firestore":
        return FirestoreTaskRepository(project=os.getenv("GOOGLE_CLOUD_PROJECT") or None)
    if backend == "memory":
        return InMemoryTaskRepository()
    raise ValueError(f"Unsupported CARELOOP_STORAGE_BACKEND={backend}")


def build_observation_repository():
    backend = os.getenv("CARELOOP_STORAGE_BACKEND", "memory").lower()
    if backend == "firestore":
        return FirestoreObservationRepository(
            project=os.getenv("GOOGLE_CLOUD_PROJECT") or None
        )
    if backend == "memory":
        return InMemoryObservationRepository()
    raise ValueError(f"Unsupported CARELOOP_STORAGE_BACKEND={backend}")


def build_observation_structurer():
    backend = os.getenv("CARELOOP_AI_BACKEND", "deterministic").lower()
    if backend == "gemini":
        return GeminiObservationStructurer(
            os.getenv("GEMINI_MODEL", "gemini-3.5-flash"),
            project=os.getenv("GOOGLE_CLOUD_PROJECT") or None,
            location=os.getenv("GOOGLE_CLOUD_LOCATION", "global"),
        )
    if backend == "deterministic":
        return DeterministicObservationStructurer()
    raise ValueError(f"Unsupported CARELOOP_AI_BACKEND={backend}")
