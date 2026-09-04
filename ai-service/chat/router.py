from typing import Any, Dict


# Supported chat routes.
ROUTES = {
    "weather": "weather",
    "ocean": "ocean",
    "ecosystem": "ecosystem",
    "risk": "risk",
    "decision": "decision",
    "comparison": "comparison",
    "general": "general",
}


def _normalize_question(question: str) -> str:
    """
    Normalize user text for simple route detection.
    """

    if not isinstance(question, str):
        return ""

    return " ".join(question.lower().strip().split())


def _contains_any(text: str, keywords: list[str]) -> bool:
    """
    Check whether any keyword occurs in the normalized question.
    """

    return any(keyword in text for keyword in keywords)


def route_question(
    user_question: str,
    current_zone: str | None = None,
) -> Dict[str, Any]:
    """
    Route a user question to the relevant ORCA context.

    This router only determines which existing analysis context
    should be used. It does not fetch environmental data and
    does not generate the final answer.
    """

    question = _normalize_question(user_question)

    if not question:
        return {
            "route": ROUTES["general"],
            "zoneId": current_zone,
            "reason": "No user question was provided.",
        }

    # Comparison questions should be checked first because they
    # can also contain weather/ocean/risk terminology.
    comparison_keywords = [
        "compare",
        "comparison",
        "which zone",
        "which area",
        "better zone",
        "safer zone",
        "best zone",
        "difference between zones",
        "between the zones",
    ]

    if _contains_any(question, comparison_keywords):
        return {
            "route": ROUTES["comparison"],
            "zoneId": None,
            "reason": "Question requests comparison across zones.",
        }

    decision_keywords = [
        "should i",
        "should we",
        "recommend",
        "recommendation",
        "suitable",
        "suitability",
        "can i go",
        "can we go",
        "is it safe",
        "safe to",
        "what should",
        "decision",
        "advise",
    ]

    if _contains_any(question, decision_keywords):
        return {
            "route": ROUTES["decision"],
            "zoneId": current_zone,
            "reason": "Question requests an operational recommendation.",
        }

    risk_keywords = [
        "risk",
        "danger",
        "hazard",
        "hazards",
        "unsafe",
        "threat",
        "warning",
        "critical",
        "high risk",
    ]

    if _contains_any(question, risk_keywords):
        return {
            "route": ROUTES["risk"],
            "zoneId": current_zone,
            "reason": "Question asks about risk or hazards.",
        }

    weather_keywords = [
        "weather",
        "temperature",
        "rain",
        "rainfall",
        "precipitation",
        "wind",
        "wind speed",
        "wind direction",
        "gust",
        "visibility",
        "pressure",
        "forecast",
        "weather condition",
    ]

    if _contains_any(question, weather_keywords):
        return {
            "route": ROUTES["weather"],
            "zoneId": current_zone,
            "reason": "Question relates to weather conditions.",
        }

    ocean_keywords = [
        "wave",
        "waves",
        "wave height",
        "wave period",
        "swell",
        "current",
        "current speed",
        "current direction",
        "tide",
        "tides",
        "sea surface temperature",
        "sst",
        "sea state",
        "ocean",
        "marine condition",
        "depth",
        "water condition",
    ]

    if _contains_any(question, ocean_keywords):
        return {
            "route": ROUTES["ocean"],
            "zoneId": current_zone,
            "reason": "Question relates to ocean or marine conditions.",
        }

    ecosystem_keywords = [
        "ecosystem",
        "ecology",
        "biodiversity",
        "habitat",
        "chlorophyll",
        "productivity",
        "protected area",
        "protected",
        "sensitive area",
        "sensitive habitat",
        "marine life",
        "ecological",
        "conservation",
    ]

    if _contains_any(question, ecosystem_keywords):
        return {
            "route": ROUTES["ecosystem"],
            "zoneId": current_zone,
            "reason": "Question relates to ecosystem conditions.",
        }

    return {
        "route": ROUTES["general"],
        "zoneId": current_zone,
        "reason": "No specific domain was identified.",
    }


def route_chat(
    user_question: str,
    current_zone: str | None = None,
) -> str:
    """
    Convenience function returning only the selected route.
    """

    result = route_question(
        user_question=user_question,
        current_zone=current_zone,
    )

    return result["route"]


def is_supported_route(route: str) -> bool:
    """
    Check whether a route is supported.
    """

    return route in ROUTES.values()
