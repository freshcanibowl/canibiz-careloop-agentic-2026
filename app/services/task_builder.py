import re
from uuid import uuid4
from app.models.care_plan import CarePlan, FollowUpTask

def _task(plan, kind, instruction, due_day):
    return FollowUpTask(str(uuid4()), plan.plan_id, plan.pet_id, kind, instruction, due_day)

def build_follow_up_tasks(plan: CarePlan):
    text = plan.instructions.lower()
    tasks = []
    transition = re.search(r"(transition|switch).{0,40}?([0-9]+)[ -]?day", text)
    days = int(transition.group(2)) if transition else 7
    if transition:
        tasks.append(_task(plan, "FEEDING_TRANSITION", f"Complete {days}-day feeding transition", days))
    if "stool" in text:
        for day in range(1, days + 1):
            tasks.append(_task(plan, "STOOL_OBSERVATION", "Record stool observation", day))
    if "appetite" in text:
        tasks.append(_task(plan, "APPETITE_OBSERVATION", "Record appetite observation", 3))
    if "vomit" in text:
        tasks.append(_task(plan, "VOMITING_OBSERVATION", "Record vomiting observation", 3))
    review = re.search(r"(review|follow.?up).{0,20}?([0-9]+)[ -]?day", text)
    review_day = int(review.group(2)) if review else days
    tasks.append(_task(plan, "PROFESSIONAL_REVIEW", "Professional follow-up review due", review_day))
    return tasks
