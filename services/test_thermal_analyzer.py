from services.fortyguard import FortyGuardClient
from services.thermal_analyzer import ThermalAnalyzer


def main():

    print("=" * 60)
    print("THERMALYTIC-AI")
    print("REAL FORTYGUARD THERMAL ANALYSIS")
    print("=" * 60)

    # ---------------------------------------------------------
    # FortyGuard client
    # ---------------------------------------------------------

    client = FortyGuardClient()

    # ---------------------------------------------------------
    # WORKING FORTYGUARD PAYLOAD
    # ---------------------------------------------------------

    payload = {
        "polygon_aoi": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-112.0800, 33.4400],
                            [-112.0700, 33.4400],
                            [-112.0700, 33.4500],
                            [-112.0800, 33.4500],
                            [-112.0800, 33.4400]
                        ]]
                    }
                }
            ]
        },

        "date_time": {
            "start_date": "2024-07-15",
            "start_time": "14:00",
            "filter_type": 1
        },

        "granularity": 100,

        "analytic_type": "tcm"
    }

    # ---------------------------------------------------------
    # Submit heatmap
    # ---------------------------------------------------------

    print("\nSubmitting real FortyGuard heatmap request...")

    submission = client.create_heatmap(payload)

    print("\n=== SUBMISSION ===")
    print(submission)

    # ---------------------------------------------------------
    # Activity ID
    # ---------------------------------------------------------

    activity_id = (
        submission
        .get("data", {})
        .get("activity_id")
    )

    if not activity_id:
        raise RuntimeError(
            "Activity ID was not returned by FortyGuard."
        )

    print(
        f"\nActivity ID: {activity_id}"
    )

    # ---------------------------------------------------------
    # Wait for completion
    # ---------------------------------------------------------

    print(
        "Waiting for FortyGuard to finish..."
    )

    result = client.wait_for_completion(
        activity_id
    )

    print(
        "\n=== FORTYGUARD RESULT RECEIVED ==="
    )

    # ---------------------------------------------------------
    # Thermal Analyzer
    # ---------------------------------------------------------

    analyzer = ThermalAnalyzer()

    analysis = analyzer.analyze(result)

    # ---------------------------------------------------------
    # Thermal Analysis
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("THERMAL ANALYSIS")
    print("=" * 60)

    print(
        f"\nTotal thermal cells: "
        f"{analysis['total_cells']}"
    )

    statistics = analysis["statistics"]

    print(
        f"Minimum temperature: "
        f"{statistics['minimum']} °C"
    )

    print(
        f"Maximum temperature: "
        f"{statistics['maximum']} °C"
    )

    print(
        f"Mean temperature: "
        f"{statistics['mean']} °C"
    )

    print(
        f"Temperature range: "
        f"{statistics['range']} °C"
    )

    # ---------------------------------------------------------
    # Overall risk
    # ---------------------------------------------------------

    print(
        f"\nOverall risk: "
        f"{analysis['overall_risk']}"
    )

    print(
        f"Hotspot cells: "
        f"{analysis['hotspot_count']}"
    )

    # ---------------------------------------------------------
    # Top hotspots
    # ---------------------------------------------------------

    print("\n=== TOP HOTSPOTS ===")

    hotspots = sorted(
        analysis["hotspots"],
        key=lambda x: x["temperature_c"],
        reverse=True,
    )

    if not hotspots:

        print("No hotspot cells found.")

    else:

        for cell in hotspots[:10]:

            print(
                f"Tile {cell['tile_id']} | "
                f"{cell['temperature_c']} °C | "
                f"{cell['risk_level']} | "
                f"Risk Score: {cell['risk_score']}"
            )

    # ---------------------------------------------------------
    # First thermal cell
    # ---------------------------------------------------------

    print("\n=== FIRST THERMAL CELL ===")

    cells = analysis["cells"]

    if cells:

        first_cell = cells[0]

        print(
            f"Tile ID: "
            f"{first_cell['tile_id']}"
        )

        print(
            f"Temperature: "
            f"{first_cell['temperature_c']} °C"
        )

        print(
            f"Risk level: "
            f"{first_cell['risk_level']}"
        )

        print(
            f"Risk score: "
            f"{first_cell['risk_score']}"
        )

    # ---------------------------------------------------------
    # Final status
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)

    print(
        "\n✅ Real FortyGuard data analyzed"
    )

    print(
        f"✅ {analysis['total_cells']} thermal cells processed"
    )

    print(
        f"✅ Overall risk: {analysis['overall_risk']}"
    )


if __name__ == "__main__":
    main()