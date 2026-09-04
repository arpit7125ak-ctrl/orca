"""
AI-Service/tools/gis_tool.py

Small tool wrapper for the GIS Service.

Responsibilities:
- Validate geographic coordinates.
- Fetch optional GIS/spatial information.
- Calculate distances between zones.
- Preserve missing/unavailable GIS data explicitly.
- Keep tool logic separate from agent reasoning.

This module must not:
- Call an LLM.
- Perform risk reasoning.
- Invent GIS values.
- Modify zone identity.
"""

from typing import Any, Dict, List, Optional

from services.gis_service import (
    calculate_distance,
    calculate_zone_distances,
    get_spatial_data,
)


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


def gis_tool(
    latitude: float,
    longitude: float,
    zone_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Fetch GIS/spatial information for a location.

    Parameters
    ----------
    latitude:
        Latitude of the requested location.

    longitude:
        Longitude of the requested location.

    zone_id:
        Stable zone identifier, when available.

    Returns
    -------
    Dict[str, Any]
        Structured GIS service response.
    """

    try:
        _validate_coordinates(latitude, longitude)

        result = get_spatial_data(
            latitude=float(latitude),
            longitude=float(longitude),
            zone_id=zone_id,
        )

        if not isinstance(result, dict):
            return {
                "status": "error",
                "variables": {},
                "error": {
                    "type": "tool",
                    "message": "GIS service returned an invalid response.",
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


def distance_tool(
    latitude1: float,
    longitude1: float,
    latitude2: float,
    longitude2: float,
) -> Dict[str, Any]:
    """
    Calculate geographic distance between two coordinates.

    Returns both kilometres and nautical miles.
    """

    try:
        _validate_coordinates(latitude1, longitude1)
        _validate_coordinates(latitude2, longitude2)

        return calculate_distance(
            latitude1=float(latitude1),
            longitude1=float(longitude1),
            latitude2=float(latitude2),
            longitude2=float(longitude2),
        )

    except ValueError as exc:
        return {
            "status": "error",
            "error": {
                "type": "validation",
                "message": str(exc),
            },
        }

    except Exception as exc:
        return {
            "status": "error",
            "error": {
                "type": "tool",
                "message": str(exc),
            },
        }


def zone_distance_tool(
    zones: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Calculate distances between supplied zones.

    Zone identity is always based on zoneId.
    Array position is never used as zone identity.
    """

    try:
        if not isinstance(zones, list):
            raise ValueError("zones must be a list.")

        if not zones:
            raise ValueError("At least one zone is required.")

        for zone in zones:
            if not isinstance(zone, dict):
                raise ValueError("Each zone must be an object.")

            if not zone.get("zoneId"):
                raise ValueError(
                    "Every zone must contain a stable zoneId."
                )

        result = calculate_zone_distances(zones)

        if not isinstance(result, dict):
            return {
                "status": "error",
                "distances": [],
                "error": {
                    "type": "tool",
                    "message": (
                        "GIS service returned an invalid distance response."
                    ),
                },
            }

        return result

    except ValueError as exc:
        return {
            "status": "error",
            "distances": [],
            "error": {
                "type": "validation",
                "message": str(exc),
            },
        }

    except Exception as exc:
        return {
            "status": "error",
            "distances": [],
            "error": {
                "type": "tool",
                "message": str(exc),
            },
        }


# Explicit aliases for callers.
get_gis_tool = gis_tool
get_distance_tool = distance_tool
get_zone_distance_tool = zone_distance_tool