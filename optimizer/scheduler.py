from datetime import datetime, timedelta
from typing import List

from agent.constraint_parser import JobConstraints


def generate_candidate_schedules(
    constraints: JobConstraints,
) -> List[list[datetime]]:
    """
    Generate candidate hourly schedules within the allowed
    operating window and before the deadline.

    Each candidate is a list of hourly start times.
    """

    required_hours = int(constraints.work_duration_hours)

    start_datetime = datetime.combine(
        datetime.today(),
        constraints.work_start,
    )

    end_datetime = datetime.combine(
        datetime.today(),
        constraints.work_end,
    )

    deadline_datetime = datetime.combine(
        datetime.today(),
        constraints.deadline,
    )

    latest_allowed_end = min(end_datetime, deadline_datetime)

    candidates = []

    current_start = start_datetime

    while current_start + timedelta(hours=required_hours) <= latest_allowed_end:

        candidate = [
            current_start + timedelta(hours=i)
            for i in range(required_hours)
        ]

        candidates.append(candidate)

        current_start += timedelta(hours=1)

    return candidates