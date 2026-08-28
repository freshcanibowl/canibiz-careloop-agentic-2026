"""
Google ADK entry point.
ADK orchestrates workflow interaction; deterministic domain functions remain
authoritative for task state and safety routing.
"""
try:
    from google.adk.agents import Agent

    root_agent = Agent(
        name="careloop_orchestrator",
        model="gemini-3.5-flash",
        description="Coordinates veterinary follow-up workflow without diagnosing or prescribing.",
        instruction=(
            "Coordinate follow-up care actions. Never diagnose, prescribe, or override "
            "deterministic safety routing. Treat model output as untrusted structured input."
        ),
    )
except ImportError:
    root_agent = None
