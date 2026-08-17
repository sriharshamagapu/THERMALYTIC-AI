from datetime import datetime, timedelta
from typing import Any

import pandas as pd


class MockFortyGuard:
    """
    Mock adapter for FortyGuard temperature intelligence.

    This is used during MVP development before the real
    FortyGuard API is connected.
    """

    def __init__(self) -> None:
        self.source = "Mock FortyGuard"

    def get_snapshot(self, location: str) -> dict[str, Any]:
        """Return current mock temperature intelligence."""
        return {
            "source": self.source,
            "location": location,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "temperature_c": 34.0,
            "status": "mock",
        }

    def get_forecast(
        self,
        location: str,
        start_time: datetime,
        hours: int = 12,
    ) -> pd.DataFrame:
        """
        Return mock hourly temperature intelligence.

        The real FortyGuard adapter will replace this method
        when API access is available.
        """

        temperatures = [
            29.0,
            31.0,
            34.0,
            37.0,
            39.0,
            41.0,
            42.0,
            41.0,
            39.0,
            36.0,
            34.0,
            32.0,
        ]

        rows = []

        for i in range(min(hours, len(temperatures))):
            rows.append(
                {
                    "timestamp": start_time + timedelta(hours=i),
                    "location": location,
                    "temperature_c": temperatures[i],
                    "source": self.source,
                    "data_type": "mock_forecast",
                }
            )

        return pd.DataFrame(rows)

    def get_exceedance(
        self,
        temperature_threshold: float = 38.0,
    ) -> dict[str, Any]:
        """Identify mock periods above a temperature threshold."""

        forecast = self.get_forecast(
            location="demo",
            start_time=datetime.now().replace(
                minute=0,
                second=0,
                microsecond=0,
            ),
            hours=12,
        )

        exceeded = forecast[
            forecast["temperature_c"] > temperature_threshold
        ]

        return {
            "threshold_c": temperature_threshold,
            "exceeded_periods": exceeded[
                ["timestamp", "temperature_c"]
            ].to_dict("records"),
            "count": len(exceeded),
            "source": self.source,
        }

    def get_persistence(
        self,
        temperature_threshold: float = 38.0,
    ) -> dict[str, Any]:
        """Calculate how long mock temperatures remain above a threshold."""

        forecast = self.get_forecast(
            location="demo",
            start_time=datetime.now().replace(
                minute=0,
                second=0,
                microsecond=0,
            ),
            hours=12,
        )

        above_threshold = forecast["temperature_c"] > temperature_threshold

        longest_run = 0
        current_run = 0

        for value in above_threshold:
            if value:
                current_run += 1
                longest_run = max(longest_run, current_run)
            else:
                current_run = 0

        return {
            "threshold_c": temperature_threshold,
            "longest_persistence_hours": longest_run,
            "source": self.source,
        }


def get_mock_fortyguard() -> MockFortyGuard:
    """Create a MockFortyGuard adapter."""
    return MockFortyGuard()