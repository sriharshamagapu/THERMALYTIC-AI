import os
import time
from datetime import datetime, timedelta
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv


load_dotenv()


class FortyGuardClient:
    """Client for the real FortyGuard Temperature API."""

    BASE_URL = "https://api.fortyguard.com"

    def __init__(self) -> None:
        self.api_key = os.getenv("FORTYGUARD_API_KEY")

        if not self.api_key:
            raise RuntimeError(
                "FORTYGUARD_API_KEY not found in .env"
            )

        self.headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json",
        }

    def create_heatmap(self, payload: dict) -> dict:
        """Submit a heatmap analysis request."""

        response = requests.post(
            f"{self.BASE_URL}/v1/heatmap",
            headers=self.headers,
            json=payload,
            timeout=60,
        )

        response.raise_for_status()

        return response.json()

    def get_status(self, activity_id: str) -> dict:
        """Check the status of a FortyGuard task."""

        response = requests.get(
            f"{self.BASE_URL}/v1/status/{activity_id}",
            headers=self.headers,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def wait_for_completion(
        self,
        activity_id: str,
        timeout_seconds: int = 600,
        poll_seconds: int = 5,
    ) -> dict:
        """
        Wait for an asynchronous FortyGuard task to complete.

        The method tolerates temporary API/network errors such as
        502/503/504 responses and continues polling until the
        overall timeout is reached.
        """

        start_time = time.time()
        attempt = 0

        while time.time() - start_time < timeout_seconds:

            attempt += 1

            elapsed = int(
                time.time() - start_time
            )

            remaining = max(
                timeout_seconds - elapsed,
                0
            )

            try:

                result = self.get_status(
                    activity_id
                )

                status = str(
                    result.get("status")
                    or result.get("data", {}).get(
                        "status",
                        ""
                    )
                ).strip().lower()

                print(
                    f"FortyGuard status: {status} "
                    f"| elapsed: {elapsed}s "
                    f"| remaining: {remaining}s"
                )

                # ------------------------------------------------
                # COMPLETED
                # ------------------------------------------------

                if status in {
                    "completed",
                    "complete",
                    "success",
                    "succeeded",
                    "done",
                }:

                    return result

                # ------------------------------------------------
                # FAILED
                # ------------------------------------------------

                if status in {
                    "failed",
                    "failure",
                    "error",
                    "cancelled",
                    "canceled",
                }:

                    raise RuntimeError(
                        "FortyGuard task failed: "
                        f"{result}"
                    )

                # ------------------------------------------------
                # PROCESSING / QUEUED / PENDING
                # ------------------------------------------------

                if status in {
                    "processing",
                    "queued",
                    "pending",
                    "submitted",
                    "running",
                    "in_progress",
                    "in-progress",
                    "started",
                    "",
                }:

                    time.sleep(
                        min(
                            poll_seconds,
                            remaining,
                        )
                    )

                    continue

                # ------------------------------------------------
                # UNKNOWN STATUS
                # ------------------------------------------------

                print(
                    "FortyGuard returned an unknown "
                    f"status: {status}"
                )

                time.sleep(
                    min(
                        poll_seconds,
                        remaining,
                    )
                )

            except requests.exceptions.HTTPError as error:

                response = getattr(
                    error,
                    "response",
                    None
                )

                status_code = (
                    response.status_code
                    if response is not None
                    else None
                )

                # Temporary gateway/server problems should
                # not immediately kill the analysis.

                if status_code in {
                    429,
                    500,
                    502,
                    503,
                    504,
                }:

                    print(
                        "Temporary FortyGuard API error "
                        f"{status_code}. "
                        f"Retrying in {poll_seconds}s..."
                    )

                    time.sleep(
                        min(
                            poll_seconds,
                            remaining,
                        )
                    )

                    continue

                raise RuntimeError(
                    "FortyGuard status request failed: "
                    f"{error}"
                ) from error

            except (
                requests.exceptions.Timeout,
                requests.exceptions.ConnectionError,
            ) as error:

                print(
                    "Temporary FortyGuard network error: "
                    f"{error}. "
                    f"Retrying in {poll_seconds}s..."
                )

                time.sleep(
                    min(
                        poll_seconds,
                        remaining,
                    )
                )

                continue

        raise TimeoutError(
            "FortyGuard task did not complete within "
            f"{timeout_seconds} seconds."
        )


# ============================================================
# MOCK FORTYGUARD
# ============================================================


class MockFortyGuard:
    """
    Mock adapter for FortyGuard temperature intelligence.

    This is used during MVP development before the real
    FortyGuard API is connected.
    """

    def __init__(self) -> None:
        self.source = "Mock FortyGuard"

    def get_snapshot(
        self,
        location: str
    ) -> dict[str, Any]:
        """Return current mock temperature intelligence."""

        return {
            "source": self.source,
            "location": location,
            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),
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

        for i in range(
            min(
                hours,
                len(temperatures)
            )
        ):

            rows.append(
                {
                    "timestamp": (
                        start_time
                        + timedelta(hours=i)
                    ),
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
            forecast["temperature_c"]
            > temperature_threshold
        ]

        return {
            "threshold_c": temperature_threshold,
            "exceeded_periods": exceeded[
                [
                    "timestamp",
                    "temperature_c",
                ]
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

        above_threshold = (
            forecast["temperature_c"]
            > temperature_threshold
        )

        longest_run = 0
        current_run = 0

        for value in above_threshold:

            if value:

                current_run += 1

                longest_run = max(
                    longest_run,
                    current_run
                )

            else:

                current_run = 0

        return {
            "threshold_c": temperature_threshold,
            "longest_persistence_hours": (
                longest_run
            ),
            "source": self.source,
        }


def get_mock_fortyguard() -> MockFortyGuard:
    """Create a MockFortyGuard adapter."""

    return MockFortyGuard()