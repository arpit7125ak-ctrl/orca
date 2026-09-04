from __future__ import annotations

from typing import Any, Dict, Optional

from services.weather_service import get_weather


def weather_tool(
    latitude: float,
    longitude: float,
    planned_datetime: Optional[str] = None,
) -> Dict[str, Any]:
    """
    AI-callable weather retrieval tool.

    This tool is intentionally small:
        Tool -> Weather Service

    Weather interpretation belongs to weather_agent.py.

    No environmental values are generated or inferred here.
    """

    if not isinstance(latitude, (int, float)):
        return {
            "success": False,
            "data": None,
            "error": "latitude must be a number",
        }

    if not isinstance(longitude, (int, float)):
        return {
            "success": False,
            "data": None,
            "error": "longitude must be a number",
        }

    if not -90 <= latitude <= 90:
        return {
            "success": False,
            "data": None,
            "error": "latitude must be between -90 and 90",
        }

    if not -180 <= longitude <= 180:
        return {
            "success": False,
            "data": None,
            "error": "longitude must be between -180 and 180",
        }

    try:
        result = get_weather(
            latitude=float(latitude),
            longitude=float(longitude),
            planned_datetime=planned_datetime,
        )

        return result

    except Exception as exc:
        return {
            "success": False,
            "data": None,
            "error": f"Weather tool execution failed: {exc}",
        }
    