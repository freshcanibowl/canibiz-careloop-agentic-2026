from app.models.vetbrief import VetBrief

def render_vetbrief(brief: VetBrief) -> str:
    outstanding = "\n".join(f"- {x}" for x in brief.outstanding_tasks) or "- None"
    timeline = "\n".join(f"- {x}" for x in brief.longitudinal_summary) or "- No observations recorded"
    reasons = ", ".join(brief.safety_reasons) or "none"

    return f"""VETBRIEF
Pet: {brief.pet_id}
Plan: {brief.plan_id}

FOLLOW-UP ADHERENCE
{brief.adherence_percent}% ({brief.completed_tasks}/{brief.expected_owner_tasks} expected owner tasks completed)

HOME OBSERVATION TIMELINE
{timeline}

OUTSTANDING
{outstanding}

WORKFLOW SAFETY STATUS
{brief.safety_status}
Routing reasons: {reasons}

Note: This brief summarizes owner-reported follow-up data. It does not diagnose or prescribe.
"""
