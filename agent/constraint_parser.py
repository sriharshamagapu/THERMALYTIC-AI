from dataclasses import dataclass
from datetime import time
import re


@dataclass
class JobConstraints:
    location: str
    work_duration_hours: float
    work_start: time
    work_end: time
    deadline: time
    work_type: str
    objective: str


def parse_time(value: str) -> time:
    """Convert a time string such as 7 AM or 5 PM into a time object."""

    value = value.strip().upper().replace(".", "")

    match = re.match(r"(\d{1,2})(?::(\d{2}))?\s*(AM|PM)?", value)

    if not match:
        raise ValueError(f"Invalid time format: {value}")

    hour = int(match.group(1))
    minute = int(match.group(2) or 0)
    period = match.group(3)

    if period == "PM" and hour != 12:
        hour += 12
    elif period == "AM" and hour == 12:
        hour = 0

    return time(hour, minute)


def parse_job_request(request: str) -> JobConstraints:
    """
    Parse the structured MVP request format.

    Example:
    Schedule 6 hours of outdoor maintenance in Phoenix today.
    We can work from 7 AM to 6 PM and need to finish by 5 PM.
    """

    text = " ".join(request.strip().split())

    # Work duration
    duration_match = re.search(
        r"(\d+(?:\.\d+)?)\s*hours?\s+of",
        text,
        re.IGNORECASE,
    )

    if not duration_match:
        raise ValueError("Could not identify work duration.")

    work_duration_hours = float(duration_match.group(1))

    # Location
    location_match = re.search(
        r"\bin\s+([A-Za-z][A-Za-z\s-]*?)(?:\s+today|\s+tomorrow|\.|,)",
        text,
        re.IGNORECASE,
    )

    if not location_match:
        raise ValueError("Could not identify location.")

    location = location_match.group(1).strip()

    # Work type
    work_type_match = re.search(
        r"hours?\s+of\s+(.+?)\s+in\s+",
        text,
        re.IGNORECASE,
    )

    if work_type_match:
        work_type = work_type_match.group(1).strip()
    else:
        work_type = "outdoor work"

    # Working window
    window_match = re.search(
        r"from\s+(.+?)\s+to\s+(.+?)\s+and",
        text,
        re.IGNORECASE,
    )

    if not window_match:
        raise ValueError("Could not identify working hours.")

    work_start = parse_time(window_match.group(1))
    work_end = parse_time(window_match.group(2))

    # Deadline
    deadline_match = re.search(
        r"finish\s+by\s+(.+?)(?:\.|$)",
        text,
        re.IGNORECASE,
    )

    if not deadline_match:
        raise ValueError("Could not identify deadline.")

    deadline = parse_time(deadline_match.group(1))

    return JobConstraints(
        location=location,
        work_duration_hours=work_duration_hours,
        work_start=work_start,
        work_end=work_end,
        deadline=deadline,
        work_type=work_type,
        objective="minimize heat exposure",
    )