from agent.constraint_parser import parse_job_request


request = (
    "Schedule 6 hours of outdoor maintenance in Phoenix today. "
    "We can work from 7 AM to 6 PM and need to finish by 5 PM."
)

job = parse_job_request(request)

print("Location:", job.location)
print("Work duration:", job.work_duration_hours, "hours")
print("Work start:", job.work_start)
print("Work end:", job.work_end)
print("Deadline:", job.deadline)
print("Work type:", job.work_type)
print("Objective:", job.objective)