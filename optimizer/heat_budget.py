import pandas as pd


def calculate_heat_budget(
    schedule,
    temperature_data: pd.DataFrame,
) -> dict:
    """
    Calculate an operational heat-exposure budget for a schedule.

    This is an optimization metric based on temperature data.
    It is NOT a medical or worker-safety formula.
    """

    schedule_timestamps = set(schedule)

    selected = temperature_data[
        temperature_data["timestamp"].isin(schedule_timestamps)
    ].copy()

    if selected.empty:
        return {
            "total_temperature_score": None,
            "average_temperature_c": None,
            "maximum_temperature_c": None,
            "hours_above_38c": 0,
        }

    return {
        "total_temperature_score": float(
            selected["temperature_c"].sum()
        ),
        "average_temperature_c": float(
            selected["temperature_c"].mean()
        ),
        "maximum_temperature_c": float(
            selected["temperature_c"].max()
        ),
        "hours_above_38c": int(
            (selected["temperature_c"] > 38).sum()
        ),
    }