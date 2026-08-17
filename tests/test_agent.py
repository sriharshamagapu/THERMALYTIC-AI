from agent.orchestrator import ThermalyticAgent


request = (
    "Schedule 6 hours of outdoor maintenance in Phoenix today. "
    "We can work from 7 AM to 6 PM and need to finish by 5 PM."
)


agent = ThermalyticAgent()

result = agent.create_plan(request)

print("\n=== THERMALYTIC AI ===")

print("Success:", result["success"])
print("Agent:", result["agent"])
print("Data source:", result["data_source"])

print("\n=== PLAN ===")
print("Location:", result["constraints"].location)
print("Duration:", result["constraints"].work_duration_hours, "hours")
print("Deadline:", result["constraints"].deadline)

print("\n=== OPTIMIZATION ===")
print(
    "Candidates:",
    result["candidate_count"],
)
print(
    "Feasible:",
    result["feasible_candidate_count"],
)

print("\n=== HEAT BUDGET ===")
print(
    "Total score:",
    result["heat_budget"]["total_temperature_score"],
)
print(
    "Average temperature:",
    result["heat_budget"]["average_temperature_c"],
)
print(
    "Maximum temperature:",
    result["heat_budget"]["maximum_temperature_c"],
)