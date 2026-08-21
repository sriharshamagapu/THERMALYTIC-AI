# ============================================================
# THERMALYTIC AI
# Operations Recommender
# ============================================================


class OperationsRecommender:
    """
    Converts thermal analysis and operation type
    into an operational recommendation.
    """
    def recommend(
        self,
        analysis,
        operation_type="General Outdoor Operations",
   ):

        overall_risk = str(
            analysis.get(
                "overall_risk",
                "UNKNOWN"
            )
        ).upper()

        operation_type = str(
            operation_type
        ).strip()

        statistics = analysis.get(
            "statistics",
            {}
        )

        minimum = float(
            statistics.get(
                "minimum",
                0
            )
        )

        maximum = float(
            statistics.get(
                "maximum",
                0
            )
        )

        mean = float(
            statistics.get(
                "mean",
                0
            )
        )

        hotspot_count = int(
            analysis.get(
                "hotspot_count",
                0
            )
        )

        temperature_range = float(
            statistics.get(
                "range",
                maximum - minimum
            )
        )

        # ====================================================
        # OPERATION-SPECIFIC GUIDANCE
        # ====================================================

        operation_guidance = {

            "Outdoor Construction": {
                "HIGH": (
                    "Delay heat-intensive construction activities "
                    "until thermal exposure decreases."
                ),
                "MODERATE": (
                    "Plan construction activities with "
                    "work-rest cycles and prioritize cooler areas."
                ),
                "LOW": (
                    "Construction activities may proceed "
                    "under normal thermal monitoring."
                ),
            },

            "Agricultural Work": {
                "HIGH": (
                    "Delay high-exertion agricultural work "
                    "until thermal conditions improve."
                ),
                "MODERATE": (
                    "Schedule demanding field activities "
                    "during cooler periods and use work-rest planning."
                ),
                "LOW": (
                    "Agricultural activities may proceed "
                    "with normal thermal monitoring."
                ),
            },

            "Road Maintenance": {
                "HIGH": (
                    "Postpone heat-intensive road maintenance "
                    "when operationally possible."
                ),
                "MODERATE": (
                    "Limit prolonged exposure during road maintenance "
                    "and prioritize cooler operational periods."
                ),
                "LOW": (
                    "Road maintenance may proceed with "
                    "normal thermal monitoring."
                ),
            },

            "Industrial Inspection": {
                "HIGH": (
                    "Delay non-critical outdoor industrial inspections "
                    "until thermal exposure decreases."
                ),
                "MODERATE": (
                    "Conduct inspections with controlled exposure "
                    "and appropriate work-rest planning."
                ),
                "LOW": (
                    "Industrial inspection may proceed "
                    "with normal thermal monitoring."
                ),
            },

            "Solar Field Maintenance": {
                "HIGH": (
                    "Avoid prolonged solar-field maintenance "
                    "during elevated thermal conditions."
                ),
                "MODERATE": (
                    "Schedule maintenance during cooler periods "
                    "and limit prolonged exposure."
                ),
                "LOW": (
                    "Solar-field maintenance may proceed "
                    "with normal thermal monitoring."
                ),
            },

            "Emergency Response": {
                "HIGH": (
                    "Minimize unnecessary personnel exposure "
                    "while maintaining emergency readiness."
                ),
                "MODERATE": (
                    "Maintain emergency readiness while "
                    "rotating personnel to control thermal exposure."
                ),
                "LOW": (
                    "Emergency operations may proceed "
                    "with normal thermal monitoring."
                ),
            },

            "General Outdoor Operations": {
                "HIGH": (
                    "Delay heat-sensitive outdoor operations "
                    "until thermal exposure decreases."
                ),
                "MODERATE": (
                    "Proceed with caution using appropriate "
                    "thermal exposure controls."
                ),
                "LOW": (
                    "Outdoor operations may proceed "
                    "with normal thermal monitoring."
                ),
            },
        }

        # ====================================================
        # SELECT OPERATION PROFILE
        # ====================================================

        profile = operation_guidance.get(
            operation_type,
            operation_guidance[
                "General Outdoor Operations"
            ],
        )

        # ====================================================
        # HIGH RISK
        # ====================================================

        if overall_risk == "HIGH":

            return {
                "priority": "HIGH",

                "recommendation": profile["HIGH"],

                "reason": (
                    f"Mean temperature is "
                    f"{mean:.2f}°C with a maximum of "
                    f"{maximum:.2f}°C. The thermal assessment "
                    "indicates high operational risk."
                ),

                "action": (
                    "Reduce exposure duration, use suitable "
                    "work-rest planning and reassess conditions "
                    "before continuing heat-intensive activities."
                ),

                "operation_type": operation_type,
            }

        # ====================================================
        # MODERATE RISK
        # ====================================================

        if overall_risk == "MODERATE":

            if hotspot_count > 0:

                return {
                    "priority": "MEDIUM",

                    "recommendation": profile["MODERATE"],

                    "reason": (
                        f"The analyzed area contains "
                        f"{hotspot_count} thermal hotspot cell(s), "
                        f"with a mean temperature of "
                        f"{mean:.2f}°C."
                    ),

                    "action": (
                        "Avoid identified hotspot areas where "
                        "possible, rotate exposed personnel and "
                        "monitor thermal conditions."
                    ),

                    "operation_type": operation_type,
                }

            return {
                "priority": "MEDIUM",

                "recommendation": profile["MODERATE"],

                "reason": (
                    f"Mean temperature is "
                    f"{mean:.2f}°C with moderate overall "
                    "thermal risk and no significant hotspot "
                    "concentration."
                ),

                "action": (
                    "Use suitable work-rest planning and "
                    "continue monitoring thermal conditions "
                    "during operations."
                ),

                "operation_type": operation_type,
            }

        # ====================================================
        # LOW RISK
        # ====================================================

        if overall_risk == "LOW":

            return {
                "priority": "LOW",

                "recommendation": profile["LOW"],

                "reason": (
                    f"Mean temperature is "
                    f"{mean:.2f}°C and overall thermal "
                    "risk is low."
                ),

                "action": (
                    "Proceed while continuing normal "
                    "thermal monitoring."
                ),

                "operation_type": operation_type,
            }

        # ====================================================
        # UNKNOWN / FALLBACK
        # ====================================================

        return {
            "priority": "UNKNOWN",

            "recommendation": (
                "Thermal conditions require further "
                "assessment before operational planning."
            ),

            "reason": (
                "The thermal risk classification "
                "could not be determined."
            ),

            "action": (
                "Review the thermal dataset before proceeding."
            ),

            "operation_type": operation_type,
        }