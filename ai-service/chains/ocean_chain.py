from typing import Any, Dict

from agents.ocean_agent import analyze_ocean


def ocean_chain(
    zone: Dict[str, Any],
    planned_datetime: str | None = None,
) -> Dict[str, Any]:
    """
    Execute the Ocean reasoning chain for a single zone.

    Ocean values are obtained only through the configured
    Ocean Agent/service. Missing variables remain explicit.
    """

    if not isinstance(zone, dict):
        raise ValueError("Zone must be a dictionary.")

    zone_id = zone.get("zoneId")

    if not zone_id:
        raise ValueError("zoneId is required for ocean analysis.")

    latitude = zone.get("latitude")
    longitude = zone.get("longitude")

    if latitude is None or longitude is None:
        return {
            "zoneId": zone_id,
            "status": "missing",
            "summary": (
                "Ocean analysis unavailable because "
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
                "component": "ocean",
                "message": (
                    "Latitude and longitude are required "
                    "for ocean analysis."
                ),
            },
        }

    try:
        result = analyze_ocean(
            latitude=float(latitude),
            longitude=float(longitude),
            zone_id=zone_id,
            planned_datetime=planned_datetime,
        )

        if not isinstance(result, dict):
            raise ValueError("Ocean agent returned an invalid result.")

        if result.get("zoneId") != zone_id:
            raise ValueError(
                f"Ocean result zoneId mismatch. "
                f"Expected '{zone_id}', "
                f"received '{result.get('zoneId')}'."
            )

        return result

    except Exception as exc:
        return {
            "zoneId": zone_id,
            "status": "error",
            "summary": "Ocean analysis failed.",
            "evidence": [],
            "missing_variables": [],
            "data_completeness": 0.0,
            "source": None,
            "timestamp": None,
            "planned_datetime": planned_datetime,
            "error": {
                "type": "chain",
                "component": "ocean",
                "message": str(exc),
            },
        }


run_ocean_chain = ocean_chain