from datetime import datetime

from agent.constraint_parser import parse_job_request
from optimizer.scheduler import generate_candidate_schedules
from optimizer.constraints import validate_schedule
from optimizer.scoring import select_best_schedule
from optimizer.heat_budget import calculate_heat_budget
from services.mock_temperature_data import create_mock_temperature_data


REQUEST = (
    "Schedule 6 hours of outdoor maintenance in Phoenix today. "
    "We can work from 7 AM to 6 PM and need to finish by 5 PM."
)


def main():
    # Parse request
    constraints = parse_job_request(REQUEST)

    # Create mock temperature data
    temperature_data = create_mock_temperature_data(
        location=constraints.location,
        start_time=datetime.combine(
            datetime.today(),
            constraints.work_start,
        ),
    )

    # Generate candidates
    candidates = generate_candidate_schedules(constraints)

    # Keep only feasible candidates
    feasible_candidates = []

    for candidate in candidates:
        validation = validate_schedule(
            candidate,
            constraints,
        )

        if validation["feasible"]:
            feasible_candidates.append(candidate)

    # Select best schedule
    best = select_best_schedule(
        feasible_candidates,
        temperature_data,
    )

    if best is None:
        print("No feasible schedule found.")
        return

    # Calculate Heat Budget
    heat_budget = calculate_heat_budget(
        best["schedule"],
        temperature_data,
    )

    print("\n=== HEAT BUDGET ===")
    print(
        "Total temperature score:",
        heat_budget["total_temperature_score"],
    )
    print(
        "Average temperature:",
        heat_budget["average_temperature_c"],
        "°C",
    )
    print(
        "Maximum temperature:",
        heat_budget["maximum_temperature_c"],
        "°C",
    )
    print(
        "Hours above 38°C:",
        heat_budget["hours_above_38c"],
    )


if __name__ == "__main__":
    main()