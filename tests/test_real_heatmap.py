from services.fortyguard import FortyGuardClient


client = FortyGuardClient()


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


print("Submitting real FortyGuard heatmap request...")

submission = client.create_heatmap(payload)

print()
print("=== SUBMISSION ===")
print(submission)


activity_id = submission["data"]["activity_id"]

print()
print("Activity ID:", activity_id)
print("Waiting for FortyGuard to finish...")


result = client.wait_for_completion(activity_id)


print()
print("=== HEATMAP RESULT ===")
print(result)


# --------------------------------------------------
# Extract heatmap data
# --------------------------------------------------

data = result.get("data", {})
result_data = data.get("result", {})

map_data = result_data.get("map_data", {})
stats_data = result_data.get("stats_data", {})

features = map_data.get("features", [])


# --------------------------------------------------
# Basic summary
# --------------------------------------------------

number_of_cells = len(features)

print()
print("=== HEATMAP SUMMARY ===")
print("Number of cells:", number_of_cells)
print("Number of features:", len(features))


# --------------------------------------------------
# Temperature statistics
# --------------------------------------------------

temperature_stats = stats_data.get("temperature_stats", {})

minimum_temperature = temperature_stats.get("minimum")
maximum_temperature = temperature_stats.get("maximum")
mean_temperature = temperature_stats.get("mean")
standard_deviation = temperature_stats.get("standard_deviation")


print()
print("=== TEMPERATURE STATISTICS ===")

if minimum_temperature is not None:
    print(f"Minimum temperature: {minimum_temperature:.2f} °C")
else:
    print("Minimum temperature: unavailable")

if maximum_temperature is not None:
    print(f"Maximum temperature: {maximum_temperature:.2f} °C")
else:
    print("Maximum temperature: unavailable")

if mean_temperature is not None:
    print(f"Mean temperature: {mean_temperature:.2f} °C")
else:
    print("Mean temperature: unavailable")

if standard_deviation is not None:
    print(f"Standard deviation: {standard_deviation:.4f} °C")
else:
    print("Standard deviation: unavailable")


# --------------------------------------------------
# First thermal cell
# --------------------------------------------------

if features:
    print()
    print("=== FIRST THERMAL CELL ===")

    first_feature = features[0]

    properties = first_feature.get("properties", {})

    print("Tile ID:", properties.get("tile_id"))

    average_temperature = properties.get("average_temperature")
    min_temperature = properties.get("min_temperature")
    max_temperature = properties.get("max_temperature")

    if average_temperature is not None:
        print(f"Average temperature: {average_temperature:.2f} °C")

    if min_temperature is not None:
        print(f"Minimum temperature: {min_temperature:.2f} °C")

    if max_temperature is not None:
        print(f"Maximum temperature: {max_temperature:.2f} °C")


# --------------------------------------------------
# Final validation
# --------------------------------------------------

print()

if features:
    print("✅ REAL FORTYGUARD HEATMAP DATA RECEIVED")
    print(f"✅ {number_of_cells} thermal cells available")
else:
    print("⚠️ Heatmap completed but returned no features.")