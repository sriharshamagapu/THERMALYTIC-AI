from datetime import datetime

from agent.constraint_parser import parse_job_request
from optimizer.scheduler import generate_candidate_schedules
from optimizer.constraints import validate_schedule
from optimizer.scoring import select_best_schedule
from optimizer.heat_budget import calculate_heat_budget
from services.mock_temperature_data import create_mock_temperature_data


class ThermalyticAgent:
    """
    Core THERMALYTIC AI orchestration layer.

    Current version uses deterministic Python tools and
    mock FortyGuard temperature intelligence.
    """

    def __init__(self):
        self.name = "THERMALYTIC AI"
        self.data_source = "Mock FortyGuard"

    def create_plan(self, user_request: str) -> dict:
        """
        Convert a natural-language operational request into
        an evidence-backed heat-aware work plan.
        """

        # 1. Understand and extract constraints
        constraints = parse_job_request(user_request)

        # 2. Get temperature intelligence
        temperature_data = create_mock_temperature_data(
            location=constraints.location,
            start_time=datetime.combine(
                datetime.today(),
                constraints.work_start,
            ),
        )

        # 3. Generate candidate schedules
        candidates = generate_candidate_schedules(
            constraints
        )

        # 4. Validate candidates
        feasible_candidates = []

        for candidate in candidates:
            validation = validate_schedule(
                candidate,
                constraints,
            )

            if validation["feasible"]:
                feasible_candidates.append(candidate)

        # 5. Optimize
        best = select_best_schedule(
            feasible_candidates,
            temperature_data,
        )

        # 6. Handle impossible requests
        if best is None:
            return {
                "success": False,
                "message": "No feasible schedule exists under the current constraints.",
                "constraints": constraints,
            }

        # 7. Calculate Heat Budget
        heat_budget = calculate_heat_budget(
            best["schedule"],
            temperature_data,
        )

        # 8. Build final result
        return {
            "success": True,
            "agent": self.name,
            "data_source": self.data_source,
            "constraints": constraints,
            "temperature_data": temperature_data,
            "candidate_count": len(candidates),
            "feasible_candidate_count": len(
                feasible_candidates
            ),
            "schedule": best["schedule"],
            "optimization": best,
            "heat_budget": heat_budget,
        }