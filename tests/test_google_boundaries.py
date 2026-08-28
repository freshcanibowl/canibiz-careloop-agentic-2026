from app.agent import root_agent
from app.adapters.gemini_observation import GeminiObservationStructurer

def test_gemini_adapter_is_a_boundary_not_domain_authority():
    adapter = GeminiObservationStructurer("gemini-test")
    assert adapter.model == "gemini-test"

def test_adk_module_is_import_safe_without_cloud_dependencies():
    # In CI without ADK installed, root_agent is intentionally None.
    assert root_agent is None or getattr(root_agent, "name", None) == "careloop_orchestrator"


def test_gemini_adapter_uses_vertex_ai_adc(monkeypatch):
    from google import genai

    captured = {}

    class FakeModels:
        def generate_content(self, model, contents):
            captured["model"] = model
            return type("Response", (), {
                "text": '{"stool_score": 5, "appetite": "normal", "vomiting": false}'
            })()

    class FakeClient:
        models = FakeModels()

    def client_factory(**kwargs):
        captured["client"] = kwargs
        return FakeClient()

    monkeypatch.setattr(genai, "Client", client_factory)
    adapter = GeminiObservationStructurer(
        "gemini-3.5-flash", project="ai-malaysia", location="global"
    )

    observation = adapter.structure("pet-pika", 3, "stool 5, eating, no vomiting")

    assert captured["client"] == {
        "vertexai": True,
        "project": "ai-malaysia",
        "location": "global",
    }
    assert captured["model"] == "gemini-3.5-flash"
    assert (observation.stool_score, observation.appetite, observation.vomiting) == (
        5, "normal", False
    )
