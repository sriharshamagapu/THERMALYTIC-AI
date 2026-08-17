from datetime import datetime, timedelta

from agent.constraint_parser import JobConstraints


def validate_schedule(
    schedule: list[datetime],
    constraints: JobConstraints,
) -> dict:
    """
    Validate whether a candidate schedule satisfies
    the user's operational constraints.
    """

    if not schedule:
        return {
            "feasible": False,
            "reasons": ["Schedule is empty."],
        }

    required_hours = constraints.work_duration_hours

    # Check total work duration
    if len(schedule) < required_hours:
        return {
            "feasible": False,
            "reasons": [
                f"Required {required_hours} hours, "
                f"but schedule contains {len(schedule)} hours."
            ],
        }

    start_time = schedule[0]
    end_time = schedule[-1] + timedelta(hours=1)

    operating_start = datetime.combine(
        start_time.date(),
        constraints.work_start,
    )

    operating_end = datetime.combine(
        start_time.date(),
        constraints.work_end,
    )

    deadline = datetime.combine(
        start_time.date(),
        constraints.deadline,
    )

    reasons = []

    # Check operating window
    if start_time < operating_start:
        reasons.append("Schedule starts before the operating window.")

    if end_time > operating_end:
        reasons.append("Schedule ends after the operating window.")

    # Check deadline
    if end_time > deadline:
        reasons.append("Schedule finishes after the deadline.")

    # Check continuity
    for previous, current in zip(schedule, schedule[1:]):
        if current - previous != timedelta(hours=1):
            reasons.append("Schedule contains a gap.")

    return {
        "feasible": len(reasons) == 0,
        "reasons": reasons,
        "start": start_time,
        "end": end_time,
        "duration_hours": len(schedule),
    }