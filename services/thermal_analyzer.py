from typing import Any


class ThermalAnalyzer:
    """
    Analyze real FortyGuard thermal heatmap data.

    Input:
        FortyGuard GeoJSON FeatureCollection

    Output:
        Temperature statistics
        Risk classification
        Hotspot information
        Priority score
    """

    def __init__(
        self,
        low_threshold: float = 35.0,
        moderate_threshold: float = 38.0,
        high_threshold: float = 40.0,
        extreme_threshold: float = 45.0,
    ) -> None:

        self.low_threshold = low_threshold
        self.moderate_threshold = moderate_threshold
        self.high_threshold = high_threshold
        self.extreme_threshold = extreme_threshold

    # ---------------------------------------------------------
    # Extract thermal cells
    # ---------------------------------------------------------

    def extract_cells(self, heatmap_result: dict) -> list[dict[str, Any]]:
        """
        Extract thermal cells from FortyGuard response.
        """

        try:
            features = (
                heatmap_result
                .get("data", {})
                .get("result", {})
                .get("map_data", {})
                .get("features", [])
            )

            return features

        except AttributeError:
            return []

    # ---------------------------------------------------------
    # Extract temperatures
    # ---------------------------------------------------------

    def extract_temperatures(
        self,
        features: list[dict[str, Any]],
    ) -> list[float]:

        temperatures = []

        for feature in features:

            properties = feature.get("properties", {})

            temperature = properties.get("average_temperature")

            if temperature is not None:
                try:
                    temperatures.append(float(temperature))
                except (TypeError, ValueError):
                    pass

        return temperatures

    # ---------------------------------------------------------
    # Temperature statistics
    # ---------------------------------------------------------

    def calculate_statistics(
        self,
        temperatures: list[float],
    ) -> dict[str, float]:

        if not temperatures:
            return {
                "minimum": 0.0,
                "maximum": 0.0,
                "mean": 0.0,
                "range": 0.0,
            }

        minimum = min(temperatures)
        maximum = max(temperatures)
        mean = sum(temperatures) / len(temperatures)
        temperature_range = maximum - minimum

        return {
            "minimum": round(minimum, 2),
            "maximum": round(maximum, 2),
            "mean": round(mean, 2),
            "range": round(temperature_range, 2),
        }

    # ---------------------------------------------------------
    # Classify temperature
    # ---------------------------------------------------------

    def classify_temperature(
        self,
        temperature: float,
    ) -> str:

        if temperature >= self.extreme_threshold:
            return "EXTREME"

        if temperature >= self.high_threshold:
            return "HIGH"

        if temperature >= self.moderate_threshold:
            return "MODERATE"

        if temperature >= self.low_threshold:
            return "LOW"

        return "SAFE"

    # ---------------------------------------------------------
    # Calculate risk score
    # ---------------------------------------------------------

    def calculate_risk_score(
        self,
        temperature: float,
    ) -> float:

        """
        Convert temperature into a 0-100 risk score.

        35°C  -> 0
        38°C  -> 30
        40°C  -> 60
        45°C+ -> 100
        """

        if temperature < self.low_threshold:
            return 0.0

        if temperature >= self.extreme_threshold:
            return 100.0

        if temperature <= self.moderate_threshold:

            score = (
                (temperature - self.low_threshold)
                / (
                    self.moderate_threshold
                    - self.low_threshold
                )
            ) * 30

            return round(score, 2)

        if temperature <= self.high_threshold:

            score = 30 + (
                (temperature - self.moderate_threshold)
                / (
                    self.high_threshold
                    - self.moderate_threshold
                )
            ) * 30

            return round(score, 2)

        score = 60 + (
            (temperature - self.high_threshold)
            / (
                self.extreme_threshold
                - self.high_threshold
            )
        ) * 40

        return round(score, 2)

    # ---------------------------------------------------------
    # Analyze individual cells
    # ---------------------------------------------------------

    def analyze_cells(
        self,
        features: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:

        analyzed_cells = []

        for feature in features:

            properties = feature.get("properties", {})

            temperature = properties.get(
                "average_temperature"
            )

            if temperature is None:
                continue

            temperature = float(temperature)

            risk_level = self.classify_temperature(
                temperature
            )

            risk_score = self.calculate_risk_score(
                temperature
            )

            analyzed_cells.append(
                {
                    "tile_id": properties.get(
                        "tile_id",
                        feature.get("id"),
                    ),
                    "temperature_c": round(
                        temperature,
                        2,
                    ),
                    "risk_level": risk_level,
                    "risk_score": risk_score,
                    "geometry": feature.get(
                        "geometry"
                    ),
                }
            )

        return analyzed_cells

    # ---------------------------------------------------------
    # Find hotspots
    # ---------------------------------------------------------

    def find_hotspots(
        self,
        analyzed_cells: list[dict[str, Any]],
        threshold: float | None = None,
    ) -> list[dict[str, Any]]:

        if threshold is None:
            threshold = self.high_threshold

        hotspots = [
            cell
            for cell in analyzed_cells
            if cell["temperature_c"] >= threshold
        ]

        return hotspots

    # ---------------------------------------------------------
    # Overall risk
    # ---------------------------------------------------------

    def calculate_overall_risk(
        self,
        analyzed_cells: list[dict[str, Any]],
    ) -> str:

        if not analyzed_cells:
            return "UNKNOWN"

        scores = [
            cell["risk_score"]
            for cell in analyzed_cells
        ]

        average_score = sum(scores) / len(scores)

        if average_score >= 80:
            return "EXTREME"

        if average_score >= 60:
            return "HIGH"

        if average_score >= 30:
            return "MODERATE"

        if average_score > 0:
            return "LOW"

        return "SAFE"

    # ---------------------------------------------------------
    # Full analysis
    # ---------------------------------------------------------

    def analyze(
        self,
        heatmap_result: dict,
    ) -> dict[str, Any]:

        features = self.extract_cells(
            heatmap_result
        )

        temperatures = self.extract_temperatures(
            features
        )

        statistics = self.calculate_statistics(
            temperatures
        )

        analyzed_cells = self.analyze_cells(
            features
        )

        hotspots = self.find_hotspots(
            analyzed_cells
        )

        overall_risk = self.calculate_overall_risk(
            analyzed_cells
        )

        return {
            "total_cells": len(analyzed_cells),
            "statistics": statistics,
            "overall_risk": overall_risk,
            "hotspot_count": len(hotspots),
            "hotspots": hotspots,
            "cells": analyzed_cells,
        }


def get_thermal_analyzer() -> ThermalAnalyzer:
    """
    Create ThermalAnalyzer instance.
    """

    return ThermalAnalyzer()