from services.operations_recommender import OperationsRecommender


analysis = {
    "overall_risk": "MODERATE",

    "statistics": {
        "minimum": 39.71,
        "maximum": 39.75,
        "mean": 39.73,
        "range": 0.04,
    },

    "hotspot_count": 0,
}


recommender = OperationsRecommender()

recommendation = recommender.recommend(
    analysis
)


print("=" * 60)
print("THERMALYTIC AI")
print("OPERATIONAL RECOMMENDATION TEST")
print("=" * 60)

print()

print("Priority:")
print(recommendation["priority"])

print()

print("Recommendation:")
print(recommendation["recommendation"])

print()

print("Reason:")
print(recommendation["reason"])

print()

print("Action:")
print(recommendation["action"])

print()
print("=" * 60)
print("TEST COMPLETE")
print("=" * 60)