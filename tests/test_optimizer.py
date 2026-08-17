from datetime import datetime

from agent.constraint_parser import parse_job_request
from optimizer.scheduler import generate_candidate_schedules
from optimizer.constraints import validate_schedule
from optimizer.scoring import select_best_schedule
from services.mock_temperature_data import create_mock_temperature_data


REQUEST = (
    "Schedule 6 hours of outdoor maintenance in Phoenix today. "
    "We can work from 7 AM to 6 PM and need to finish by 5 PM."
)


def main():
    # 1. Parse the user's request
    constraints = parse_job_request(REQUEST)

    print("\n=== CONSTRAINTS ===")
    print("Location:", constraints.location)
    print("Duration:", constraints.work_duration_hours, "hours")
    print("Operating window:", constraints.work_start, "-", constraints.work_end)
    print("Deadline:", constraints.deadline)

    # 2. Create mock temperature intelligence
    temperature_data = create_mock_temperature_data(
        location=constraints.location,
        start_time=datetime.combine(
            datetime.today(),
            constraints.work_start,
        ),
    )

    print("\n=== MOCK TEMPERATURE DATA ===")
    print(temperature_data.to_string(index=False))

    # 3. Generate candidate schedules
    candidates = generate_candidate_schedules(constraints)

    print("\n=== CANDIDATES ===")
    print("Generated:", len(candidates))

    # 4. Validate candidates
    feasible_candidates = []

    for candidate in candidates:
        validation = validate_schedule(
            candidate,
            constraints,
        )

        if validation["feasible"]:
            feasible_candidates.append(candidate)

    print("Feasible:", len(feasible_candidates))

    # 5. Score feasible candidates
    best = select_best_schedule(
        feasible_candidates,
        temperature_data,
    )

    print("\n=== BEST SCHEDULE ===")

    if best is None:
        print("No feasible schedule found.")
        return

    for start_time in best["schedule"]:
        print(
            start_time.strftime("%H:%M"),
            "→",
            (start_time.hour + 1) % 24,
            ":00",
        )

    print("\nAverage temperature:", best["average_temperature_c"], "°C")
    print("Maximum temperature:", best["maximum_temperature_c"], "°C")
    print("Total temperature score:", best["total_temperature_c"])


if __name__ == "__main__":
    main()