from typing import Any, Dict

from agents.ecosystem_agent import analyze_ecosystem


def ecosystem_chain(
    zone: Dict[str, Any],
    planned_datetime: str | None = None,
) -> Dict[str, Any]:
    """
    Execute the Ecosystem reasoning chain for a single zone.

    Ecosystem values are obtained only through the configured
    Ecosystem Agent/service. Missing variables remain explicit.
    """

    if not isinstance(zone, dict):
        raise ValueError("Zone must be a dictionary.")

    zone_id = zone.get("zoneId")

    if not zone_id:
        raise ValueError("zoneId is required for ecosystem analysis.")

    latitude = zone.get("latitude")
    longitude = zone.get("longitude")

    if latitude is None or longitude is None:
        return {
            "zoneId": zone_id,
            "status": "missing",
            "summary": (
                "Ecosystem analysis unavailable because "
                "zone coordinates are missing."
            ),
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
                "component": "ecosystem",
                "message": (
                    "Latitude and longitude are required "
                    "for ecosystem analysis."
                ),
            },
        }

    try:
        result = analyze_ecosystem(
            latitude=float(latitude),
            longitude=float(longitude),
            zone_id=zone_id,
            planned_datetime=planned_datetime,
        )

        if not isinstance(result, dict):
            raise ValueError(
                "Ecosystem agent returned an invalid result."
            )

        if result.get("zoneId") != zone_id:
            raise ValueError(
                f"Ecosystem result zoneId mismatch. "
                f"Expected '{zone_id}', "
                f"received '{result.get('zoneId')}'."
            )

        return result

    except Exception as exc:
        return {
            "zoneId": zone_id,
            "status": "error",
            "summary": "Ecosystem analysis failed.",
            "evidence": [],
            "missing_variables": [],
            "data_completeness": 0.0,
            "source": None,
            "timestamp": None,
            "planned_datetime": planned_datetime,
            "error": {
                "type": "chain",
                "component": "ecosystem",
                "message": str(exc),
            },
        }


run_ecosystem_chain = ecosystem_chain