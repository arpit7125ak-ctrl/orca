"""
AI-Service/agents/weather_agent.py

Weather Agent

Responsibilities:
- Interpret weather data supplied by Weather Service.
- Identify relevant weather conditions.
- Preserve source, timestamp, unit, forecast/observation status,
  and quality information.
- Explicitly report missing or unavailable variables.
- Produce structured weather assessment.

This agent must not:
- Invent weather measurements.
- Call uncontrolled external APIs.
- Make final risk/route decisions.
- Hide missing data.
"""

from typing import Any, Dict, List, Optional

from models.schemas import (
    Evidence,
    QualityStatus,
    WeatherAssessment,
)
from tools.weather_tool import weather_tool


WEATHER_VARIABLES = [
    "temperature_2m",
    "precipitation",
    "visibility",
    "pressure_msl",
    "wind_speed_10m",
    "wind_direction_10m",
    "wind_gusts_10m",
    "weather_code",
]


def _safe_float(value: Any) -> Optional[float]:
    """
    Convert a value to float when possible.
    """

    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _extract_variables(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract normalized weather variables from the service response.
    """

    variables = result.get("variables", {})

    if not isinstance(variables, dict):
        return {}

    return variables


def _extract_status(result: Dict[str, Any]) -> str:
    """
    Extract overall data status.
    """

    status = result.get("status")

    if status is None:
        return "unknown"

    return str(status).lower()


def _extract_source(result: Dict[str, Any]) -> Optional[str]:
    """
    Extract provider/source information.
    """

    source = result.get("source")

    if source is None:
        source = result.get("provider")

    return str(source) if source is not None else None


def _extract_timestamp(result: Dict[str, Any]) -> Optional[str]:
    """
    Extract the timestamp associated with the weather data.
    """

    timestamp = result.get("timestamp")

    if timestamp is None:
        timestamp = result.get("data_timestamp")

    return str(timestamp) if timestamp is not None else None


def _build_evidence(
    variable: str,
    value: Any,
    result: Dict[str, Any],
) -> Evidence:
    """
    Build provenance-preserving evidence for one weather variable.
    """

    source = _extract_source(result)
    timestamp = _extract_timestamp(result)

    unit = None

    units = result.get("units")

    if isinstance(units, dict):
        unit = units.get(variable)

    status = _extract_status(result)

    if status == "forecast":
        evidence_status = "forecast"
    elif status in {
        "missing",
        "unavailable",
        "stale",
        "low_quality",
        "error",
    }:
        evidence_status = status
    else:
        evidence_status = "observed"

    return Evidence(
        variable=variable,
        value=value,
        unit=unit,
        source=source,
        timestamp=timestamp,
        status=evidence_status,
        quality=QualityStatus.UNKNOWN,
    )


def _build_missing_variables(
    variables: Dict[str, Any],
) -> List[str]:
    """
    Identify expected weather variables that were not supplied.
    """

    missing = []

    for variable in WEATHER_VARIABLES:
        if variable not in variables:
            missing.append(variable)
            continue

        value = variables.get(variable)

        if value is None:
            missing.append(variable)

    return missing


def _build_summary(
    variables: Dict[str, Any],
    missing_variables: List[str],
) -> str:
    """
    Build a concise factual weather summary.

    Only supplied measurements are mentioned.
    """

    parts: List[str] = []

    temperature = _safe_float(
        variables.get("temperature_2m")
    )

    if temperature is not None:
        parts.append(
            f"temperature is {temperature:g}"
        )

    precipitation = _safe_float(
        variables.get("precipitation")
    )

    if precipitation is not None:
        parts.append(
            f"precipitation is {precipitation:g}"
        )

    wind_speed = _safe_float(
        variables.get("wind_speed_10m")
    )

    if wind_speed is not None:
        parts.append(
            f"wind speed is {wind_speed:g}"
        )

    wind_direction = _safe_float(
        variables.get("wind_direction_10m")
    )

    if wind_direction is not None:
        parts.append(
            f"wind direction is {wind_direction:g}"
        )

    visibility = _safe_float(
        variables.get("visibility")
    )

    if visibility is not None:
        parts.append(
            f"visibility is {visibility:g}"
        )

    pressure = _safe_float(
        variables.get("pressure_msl")
    )

    if pressure is not None:
        parts.append(
            f"pressure is {pressure:g}"
        )

    if not parts:
        summary = "No usable weather measurements were supplied."
    else:
        summary = "Supplied weather data indicates " + ", ".join(parts) + "."

    if missing_variables:
        summary += (
            " Missing or unavailable variables: "
            + ", ".join(missing_variables)
            + "."
        )

    return summary


def _calculate_data_completeness(
    variables: Dict[str, Any],
) -> float:
    """
    Calculate simple evidence completeness.

    This is NOT a statistical forecast confidence.
    It only measures how many expected fields are available.
    """

    if not WEATHER_VARIABLES:
        return 0.0

    available = 0

    for variable in WEATHER_VARIABLES:
        if variables.get(variable) is not None:
            available += 1

    return round(
        available / len(WEATHER_VARIABLES),
        2,
    )


def analyze_weather(
    latitude: float,
    longitude: float,
    planned_datetime: Optional[str] = None,
    zone_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Run the Weather Agent for a location.

    Parameters
    ----------
    latitude:
        Latitude of the zone.

    longitude:
        Longitude of the zone.

    planned_datetime:
        Planned activity datetime.

    zone_id:
        Stable zone identifier.

    Returns
    -------
    Dict[str, Any]
        Structured weather assessment.
    """

    result = weather_tool(
        latitude=latitude,
        longitude=longitude,
        planned_datetime=planned_datetime,
    )

    if not isinstance(result, dict):
        return {
            "zoneId": zone_id,
            "status": "error",
            "summary": "Weather service returned an invalid response.",
            "evidence": [],
            "missing_variables": WEATHER_VARIABLES,
            "data_completeness": 0.0,
            "error": {
                "type": "agent",
                "message": "Invalid weather service response.",
            },
        }

    variables = _extract_variables(result)
    status = _extract_status(result)

    missing_variables = _build_missing_variables(
        variables
    )

    evidence: List[Evidence] = []

    for variable in WEATHER_VARIABLES:
        if variable not in variables:
            continue

        value = variables.get(variable)

        if value is None:
            continue

        evidence.append(
            _build_evidence(
                variable=variable,
                value=value,
                result=result,
            )
        )

    completeness = _calculate_data_completeness(
        variables
    )

    summary = _build_summary(
        variables=variables,
        missing_variables=missing_variables,
    )

    assessment: Dict[str, Any] = {
        "zoneId": zone_id,
        "status": status,
        "summary": summary,
        "evidence": evidence,
        "missing_variables": missing_variables,
        "data_completeness": completeness,
        "source": _extract_source(result),
        "timestamp": _extract_timestamp(result),
        "planned_datetime": planned_datetime,
    }

    if "error" in result:
        assessment["error"] = result["error"]

    return assessment


def weather_agent(
    zone: Dict[str, Any],
    planned_datetime: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Zone-aware Weather Agent entry point.

    The stable zoneId is carried through every result.
    """

    if not isinstance(zone, dict):
        return {
            "zoneId": None,
            "status": "error",
            "summary": "Invalid zone.",
            "evidence": [],
            "missing_variables": WEATHER_VARIABLES,
            "data_completeness": 0.0,
            "error": {
                "type": "validation",
                "message": "Zone must be an object.",
            },
        }

    zone_id = zone.get("zoneId")

    latitude = zone.get("latitude")
    longitude = zone.get("longitude")

    if latitude is None or longitude is None:
        return {
            "zoneId": zone_id,
            "status": "error",
            "summary": (
                "Weather analysis could not run because "
                "zone coordinates are missing."
            ),
            "evidence": [],
            "missing_variables": WEATHER_VARIABLES,
            "data_completeness": 0.0,
            "error": {
                "type": "validation",
                "message": (
                    "Zone latitude and longitude are required."
                ),
            },
        }

    return analyze_weather(
        latitude=latitude,
        longitude=longitude,
        planned_datetime=planned_datetime,
        zone_id=zone_id,
    )
