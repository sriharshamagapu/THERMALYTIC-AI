from datetime import datetime, timedelta

import pandas as pd


def create_mock_temperature_data(
    location: str = "Phoenix",
    start_time: datetime | None = None,
) -> pd.DataFrame:
    """
    Create deterministic hourly temperature data for MVP testing.

    This is MOCK data and is not real FortyGuard data.
    """

    if start_time is None:
        start_time = datetime.now().replace(
            hour=7,
            minute=0,
            second=0,
            microsecond=0,
        )

    temperatures = [
        29.0,  # 07:00
        31.0,  # 08:00
        34.0,  # 09:00
        37.0,  # 10:00
        39.0,  # 11:00
        41.0,  # 12:00
        42.0,  # 13:00
        41.0,  # 14:00
        39.0,  # 15:00
        36.0,  # 16:00
        34.0,  # 17:00
        32.0,  # 18:00
    ]

    rows = []

    for index, temperature in enumerate(temperatures):
        timestamp = start_time + timedelta(hours=index)

        rows.append(
            {
                "timestamp": timestamp,
                "location": location,
                "temperature_c": temperature,
                "source": "Mock FortyGuard",
                "data_type": "mock",
            }
        )

    return pd.DataFrame(rows)