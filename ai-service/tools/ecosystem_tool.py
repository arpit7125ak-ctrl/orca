"""
AI-Service/tools/ecosystem_tool.py

Small tool wrapper for the Ecosystem Service.

Responsibilities:
- Validate latitude/longitude.
- Pass the request to the Ecosystem Service.
- Return structured ecosystem data.
- Preserve missing/unavailable data explicitly.
- Keep tool logic separate from agent reasoning.

This module must not:
- Call an LLM.
- Perform risk reasoning.
- Invent ecosystem values.
- Modify zone identity.
"""

from typing import Any, Dict, Optional

from services.ecosystem_service import get_ecosystem


def _validate_coordinates(
    latitude: float,
    longitude: float,
) -> None:
    """
    Validate geographic coordinates.
    """

    if latitude is None or longitude is None:
        raise ValueError("Latitude and longitude are required.")

    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "Latitude and longitude must be numeric."
        ) from exc

    if not -90.0 <= latitude <= 90.0:
        raise ValueError(
            f"Latitude must be between -90 and 90. Received: {latitude}"
        )

    if not -180.0 <= longitude <= 180.0:
        raise ValueError(
            f"Longitude must be between -180 and 180. Received: {longitude}"
        )


def ecosystem_tool(
    latitude: float,
    longitude: float,
    planned_datetime: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Fetch ecosystem/environmental data for a location.

    Parameters
    ----------
    latitude:
        Latitude of the requested location.

    longitude:
        Longitude of the requested location.

    planned_datetime:
        Planned activity/analysis datetime in ISO format.

    Returns
    -------
    Dict[str, Any]
        Structured ecosystem service response.
    """

    try:
        _validate_coordinates(latitude, longitude)

        result = get_ecosystem(
            latitude=float(latitude),
            longitude=float(longitude),
            planned_datetime=planned_datetime,
        )

        if not isinstance(result, dict):
            return {
                "status": "error",
                "variables": {},
                "error": {
                    "type": "tool",
                    "message": (
                        "Ecosystem service returned an invalid response."
                    ),
                },
            }

        return result

    except ValueError as exc:
        return {
            "status": "error",
            "variables": {},
            "error": {
                "type": "validation",
                "message": str(exc),
            },
        }

    except Exception as exc:
        return {
            "status": "error",
            "variables": {},
            "error": {
                "type": "tool",
                "message": str(exc),
            },
        }


# Alias for callers that prefer a *_tool naming convention.
get_ecosystem_tool = ecosystem_tool