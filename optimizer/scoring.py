import pandas as pd


def score_schedule(
    schedule,
    temperature_data: pd.DataFrame,
) -> dict:
    """
    Score a schedule based on temperature exposure.

    Lower score = lower total temperature exposure.
    This is an operational optimization score, NOT a
    medical or worker-safety formula.
    """

    schedule_timestamps = set(schedule)

    selected = temperature_data[
        temperature_data["timestamp"].isin(schedule_timestamps)
    ].copy()

    if selected.empty:
        return {
            "score": float("inf"),
            "average_temperature_c": None,
            "maximum_temperature_c": None,
            "total_temperature_c": None,
        }

    total_temperature = selected["temperature_c"].sum()
    average_temperature = selected["temperature_c"].mean()
    maximum_temperature = selected["temperature_c"].max()

    return {
        "score": float(total_temperature),
        "average_temperature_c": float(average_temperature),
        "maximum_temperature_c": float(maximum_temperature),
        "total_temperature_c": float(total_temperature),
    }


def select_best_schedule(
    candidates,
    temperature_data: pd.DataFrame,
):
    """
    Select the candidate schedule with the lowest
    temperature exposure score.
    """

    results = []

    for schedule in candidates:
        score = score_schedule(
            schedule,
            temperature_data,
        )

        results.append(
            {
                "schedule": schedule,
                **score,
            }
        )

    if not results:
        return None

    return min(
        results,
        key=lambda result: result["score"],
    )