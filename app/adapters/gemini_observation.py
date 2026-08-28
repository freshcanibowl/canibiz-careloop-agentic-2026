import json
from app.models.observation import StructuredObservation

class GeminiObservationStructurer:
    """
    Production adapter boundary for Gemini.
    Imports Google SDK lazily so the deterministic domain test suite stays offline.
    """
    def __init__(self, model: str, project: str | None = None, location: str = "global"):
        self.model = model
        self.project = project
        self.location = location

    def structure(self, pet_id: str, day: int, message: str) -> StructuredObservation:
        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError("Install google-genai to use GeminiObservationStructurer") from exc

        client = genai.Client(
            vertexai=True,
            project=self.project,
            location=self.location,
        )
        prompt = f"""
Return JSON only.
Extract owner-reported follow-up observations.
Allowed stool_score: integer 1-7 or null.
Allowed appetite: low, normal, high, or null.
Allowed vomiting: true, false, or null.
Do not diagnose or recommend treatment.

pet_id={pet_id}
day={day}
message={message}
"""
        response = client.models.generate_content(model=self.model, contents=prompt)
        raw = response.text.strip().removeprefix("```json").removesuffix("```").strip()
        data = json.loads(raw)

        stool = data.get("stool_score")
        if stool is not None and (not isinstance(stool, int) or not 1 <= stool <= 7):
            raise ValueError("Invalid stool_score from model")
        appetite = data.get("appetite")
        if appetite not in (None, "low", "normal", "high"):
            raise ValueError("Invalid appetite from model")
        vomiting = data.get("vomiting")
        if vomiting not in (None, True, False):
            raise ValueError("Invalid vomiting value from model")

        return StructuredObservation(
            pet_id=pet_id, day=day, stool_score=stool,
            appetite=appetite, vomiting=vomiting, source="owner_report"
        )
