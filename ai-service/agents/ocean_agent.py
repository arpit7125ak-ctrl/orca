"""
AI-Service/agents/ocean_agent.py

Ocean Agent

Responsibilities:
- Interpret ocean/marine data supplied by Ocean Service.
- Identify relevant marine conditions.
- Preserve source, timestamp, units, and data status.
- Explicitly report missing or unavailable variables.
- Produce structured ocean assessment.

This agent must not:
- Invent ocean measurements.
- Call uncontrolled external APIs.
- Make final risk/route decisions.
- Hide missing data.
"""

from typing import Any, Dict, List, Optional

from models.schemas import (
    Evidence,
    QualityStatus,
)
from tools.ocean_tool import ocean_tool


OCEAN_VARIABLES = [
    "wave_height",
    "wave_period",
    "wave_direction",
    "current_speed",
    "current_direction",
    "tide_height",
    "tide",
    "sea_surface_temperature",
    "sst",
    "sea_state",
    "depth",
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
    Extract normalized ocean variables.
    """

    variables = result.get("variables", {})

    if not isinstance(variables, dict):
        return {}

    return variables


def _extract_status(result: Dict[str, Any]) -> str:
    """
    Extract overall ocean data status.
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
    Extract the timestamp associated with the ocean data.
    """

    timestamp = result.get("timestamp")

    if timestamp is None:
        timestamp = result.get("data_timestamp")

    return str(timestamp) if timestamp is not None else None


def _extract_unit(
    variable: str,
    result: Dict[str, Any],
) -> Optional[str]:
    """
    Extract unit information when supplied by the service.
    """

    units = result.get("units")

    if isinstance(units, dict):
        value = units.get(variable)

        if value is not None:
            return str(value)

    return None


def _map_evidence_status(status: str) -> str:
    """
    Map service status to the schema evidence status.
    """

    if status in {
        "forecast",
        "missing",
        "unavailable",
        "stale",
        "low_quality",
        "error",
        "observed",
    }:
        return status

    return "observed"


def _build_evidence(
    variable: str,
    value: Any,
    result: Dict[str, Any],
) -> Evidence:
    """
    Build provenance-preserving evidence.
    """

    status = _extract_status(result)

    return Evidence(
        variable=variable,
        value=value,
        unit=_extract_unit(variable, result),
        source=_extract_source(result),
        timestamp=_extract_timestamp(result),
        status=_map_evidence_status(status),
        quality=QualityStatus.UNKNOWN,
    )


def _build_missing_variables(
    variables: Dict[str, Any],
) -> List[str]:
    """
    Identify expected ocean variables that are unavailable.
    """

    missing: List[str] = []

    for variable in OCEAN_VARIABLES:
        if variable not in variables:
            missing.append(variable)
            continue

        if variables.get(variable) is None:
            missing.append(variable)

    return missing


def _build_summary(
    variables: Dict[str, Any],
    missing_variables: List[str],
) -> str:
    """
    Build a factual summary using only supplied values.
    """

    parts: List[str] = []

    wave_height = _safe_float(
        variables.get("wave_height")
    )

    if wave_height is not None:
        parts.append(
            f"wave height is {wave_height:g}"
        )

    wave_period = _safe_float(
        variables.get("wave_period")
    )

    if wave_period is not None:
        parts.append(
            f"wave period is {wave_period:g}"
        )

    wave_direction = _safe_float(
        variables.get("wave_direction")
    )

    if wave_direction is not None:
        parts.append(
            f"wave direction is {wave_direction:g}"
        )

    current_speed = _safe_float(
        variables.get("current_speed")
    )

    if current_speed is not None:
        parts.append(
            f"current speed is {current_speed:g}"
        )

    current_direction = _safe_float(
        variables.get("current_direction")
    )

    if current_direction is not None:
        parts.append(
            f"current direction is {current_direction:g}"
        )

    tide_height = _safe_float(
        variables.get("tide_height")
    )

    if tide_height is None:
        tide_height = _safe_float(
            variables.get("tide")
        )

    if tide_height is not None:
        parts.append(
            f"tide height is {tide_height:g}"
        )

    sst = _safe_float(
        variables.get("sea_surface_temperature")
    )

    if sst is None:
        sst = _safe_float(
            variables.get("sst")
        )

    if sst is not None:
        parts.append(
            f"sea-surface temperature is {sst:g}"
        )

    sea_state = variables.get("sea_state")

    if sea_state is not None:
        parts.append(
            f"sea state is {sea_state}"
        )

    depth = _safe_float(
        variables.get("depth")
    )

    if depth is not None:
        parts.append(
            f"depth is {depth:g}"
        )

    if parts:
        summary = (
            "Supplied ocean data indicates "
            + ", ".join(parts)
            + "."
        )
    else:
        summary = (
            "No usable ocean measurements were supplied."
        )

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
    Calculate simple field completeness.

    This is an evidence-availability measure, not
    statistical confidence.
    """

    if not OCEAN_VARIABLES:
        return 0.0

    available = 0

    for variable in OCEAN_VARIABLES:
        if variables.get(variable) is not None:
            available += 1

    return round(
        available / len(OCEAN_VARIABLES),
        2,
    )


def analyze_ocean(
    latitude: float,
    longitude: float,
    planned_datetime: Optional[str] = None,
    zone_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Run the Ocean Agent for a location.
    """

    result = ocean_tool(
        latitude=latitude,
        longitude=longitude,
        planned_datetime=planned_datetime,
    )

    if not isinstance(result, dict):
        return {
            "zoneId": zone_id,
            "status": "error",
            "summary": (
                "Ocean service returned an invalid response."
            ),
            "evidence": [],
            "missing_variables": OCEAN_VARIABLES,
            "data_completeness": 0.0,
            "error": {
                "type": "agent",
                "message": (
                    "Invalid ocean service response."
                ),
            },
        }

    variables = _extract_variables(result)
    status = _extract_status(result)

    missing_variables = _build_missing_variables(
        variables
    )

    evidence: List[Evidence] = []

    for variable in OCEAN_VARIABLES:
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


def ocean_agent(
    zone: Dict[str, Any],
    planned_datetime: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Zone-aware Ocean Agent entry point.

    The stable zoneId is carried through the complete result.
    """

    if not isinstance(zone, dict):
        return {
            "zoneId": None,
            "status": "error",
            "summary": "Invalid zone.",
            "evidence": [],
            "missing_variables": OCEAN_VARIABLES,
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
                "Ocean analysis could not run because "
                "zone coordinates are missing."
            ),
            "evidence": [],
            "missing_variables": OCEAN_VARIABLES,
            "data_completeness": 0.0,
            "error": {
                "type": "validation",
                "message": (
                    "Zone latitude and longitude are required."
                ),
            },
        }

    return analyze_ocean(
        latitude=latitude,
        longitude=longitude,
        planned_datetime=planned_datetime,
        zone_id=zone_id,
    )
