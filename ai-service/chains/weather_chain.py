from typing import Any, Dict

from agents.weather_agent import analyze_weather


def weather_chain(
    zone: Dict[str, Any],
    planned_datetime: str | None = None,
) -> Dict[str, Any]:
    """
    Execute the Weather reasoning chain for a single zone.

    The chain delegates weather analysis to the Weather Agent.
    All environmental values must come from the configured
    weather service/tool.
    """

    if not isinstance(zone, dict):
        raise ValueError("Zone must be a dictionary.")

    zone_id = zone.get("zoneId")

    if not zone_id:
        raise ValueError("zoneId is required for weather analysis.")

    latitude = zone.get("latitude")
    longitude = zone.get("longitude")

    if latitude is None or longitude is None:
        return {
            "zoneId": zone_id,
            "status": "missing",
            "summary": "Weather analysis unavailable because zone coordinates are missing.",
            "evidence": [],
            "missing_variables": [
                "latitude",
                "longitude",
            ],
            "data_completeness": 0.0,
            "source": None,
            "timestamp": None,
            "planned_datetime": planned_datetime,
            "error": {
                "type": "data",
                "component": "weather",
                "message": "Latitude and longitude are required for weather analysis.",
            },
        }

    try:
        result = analyze_weather(
            latitude=float(latitude),
            longitude=float(longitude),
            zone_id=zone_id,
            planned_datetime=planned_datetime,
        )

        if not isinstance(result, dict):
            raise ValueError("Weather agent returned an invalid result.")

        if result.get("zoneId") != zone_id:
            raise ValueError(
                f"Weather result zoneId mismatch. "
                f"Expected '{zone_id}', received '{result.get('zoneId')}'."
            )

        return result

    except Exception as exc:
        return {
            "zoneId": zone_id,
            "status": "error",
            "summary": "Weather analysis failed.",
            "evidence": [],
            "missing_variables": [],
            "data_completeness": 0.0,
            "source": None,
            "timestamp": None,
            "planned_datetime": planned_datetime,
            "error": {
                "type": "chain",
                "component": "weather",
                "message": str(exc),
            },
        }


# Alias for consistent chain naming.
run_weather_chain = weather_chain

