"""
AI-Service/agents/ecosystem_agent.py

Ecosystem Agent

Responsibilities:
- Interpret ecosystem/environmental data supplied by Ecosystem Service.
- Identify ecological conditions and constraints.
- Preserve source, timestamp, units, and data status.
- Explicitly report missing or unavailable variables.
- Produce structured ecosystem assessment.

This agent must not:
- Invent ecological measurements.
- Call uncontrolled external APIs.
- Make final risk/route decisions.
- Hide missing data.
"""

from typing import Any, Dict, List, Optional

from models.schemas import (
    EcosystemAssessment,
    Evidence,
    QualityStatus,
)
from tools.ecosystem_tool import ecosystem_tool


ECOSYSTEM_VARIABLES = [
    "ecosystem_condition",
    "sensitivity",
    "biodiversity",
    "biodiversity_index",
    "chlorophyll",
    "chlorophyll_a",
    "productivity",
    "primary_productivity",
    "habitat",
    "habitat_type",
    "protected_area",
    "protected_area_status",
    "sensitive_area",
    "ecological_constraint",
    "ecological_constraints",
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


def _extract_variables(
    result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Extract normalized ecosystem variables.
    """

    variables = result.get("variables", {})

    if not isinstance(variables, dict):
        return {}

    return variables


def _extract_status(
    result: Dict[str, Any],
) -> str:
    """
    Extract overall ecosystem data status.
    """

    status = result.get("status")

    if status is None:
        return "unknown"

    return str(status).lower()


def _extract_source(
    result: Dict[str, Any],
) -> Optional[str]:
    """
    Extract provider/source information.
    """

    source = result.get("source")

    if source is None:
        source = result.get("provider")

    return str(source) if source is not None else None


def _extract_timestamp(
    result: Dict[str, Any],
) -> Optional[str]:
    """
    Extract the timestamp associated with ecosystem data.
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
    Extract unit information when supplied.
    """

    units = result.get("units")

    if isinstance(units, dict):
        value = units.get(variable)

        if value is not None:
            return str(value)

    return None


def _map_evidence_status(
    status: str,
) -> str:
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
    Identify expected ecosystem variables that are unavailable.
    """

    missing: List[str] = []

    for variable in ECOSYSTEM_VARIABLES:
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
    Build a factual ecosystem summary.

    Only supplied information is included.
    """

    parts: List[str] = []

    ecosystem_condition = variables.get(
        "ecosystem_condition"
    )

    if ecosystem_condition is not None:
        parts.append(
            f"ecosystem condition is {ecosystem_condition}"
        )

    sensitivity = variables.get("sensitivity")

    if sensitivity is not None:
        parts.append(
            f"sensitivity is {sensitivity}"
        )

    biodiversity = variables.get("biodiversity")

    if biodiversity is None:
        biodiversity = variables.get(
            "biodiversity_index"
        )

    if biodiversity is not None:
        numeric_biodiversity = _safe_float(
            biodiversity
        )

        if numeric_biodiversity is not None:
            parts.append(
                f"biodiversity indicator is "
                f"{numeric_biodiversity:g}"
            )
        else:
            parts.append(
                f"biodiversity information is {biodiversity}"
            )

    chlorophyll = variables.get("chlorophyll")

    if chlorophyll is None:
        chlorophyll = variables.get(
            "chlorophyll_a"
        )

    if chlorophyll is not None:
        numeric_chlorophyll = _safe_float(
            chlorophyll
        )

        if numeric_chlorophyll is not None:
            parts.append(
                f"chlorophyll indicator is "
                f"{numeric_chlorophyll:g}"
            )
        else:
            parts.append(
                f"chlorophyll information is {chlorophyll}"
            )

    productivity = variables.get("productivity")

    if productivity is None:
        productivity = variables.get(
            "primary_productivity"
        )

    if productivity is not None:
        numeric_productivity = _safe_float(
            productivity
        )

        if numeric_productivity is not None:
            parts.append(
                f"productivity indicator is "
                f"{numeric_productivity:g}"
            )
        else:
            parts.append(
                f"productivity information is {productivity}"
            )

    habitat = variables.get("habitat")

    if habitat is None:
        habitat = variables.get("habitat_type")

    if habitat is not None:
        parts.append(
            f"habitat information is {habitat}"
        )

    protected_area = variables.get(
        "protected_area"
    )

    if protected_area is None:
        protected_area = variables.get(
            "protected_area_status"
        )

    if protected_area is not None:
        parts.append(
            f"protected-area status is {protected_area}"
        )

    sensitive_area = variables.get(
        "sensitive_area"
    )

    if sensitive_area is not None:
        parts.append(
            f"sensitive-area status is {sensitive_area}"
        )

    ecological_constraint = variables.get(
        "ecological_constraint"
    )

    if ecological_constraint is None:
        ecological_constraint = variables.get(
            "ecological_constraints"
        )

    if ecological_constraint is not None:
        parts.append(
            f"ecological constraints are "
            f"{ecological_constraint}"
        )

    if parts:
        summary = (
            "Supplied ecosystem data indicates "
            + ", ".join(parts)
            + "."
        )
    else:
        summary = (
            "No usable ecosystem information was supplied."
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

    This is an evidence-availability measure,
    not ecological confidence.
    """

    if not ECOSYSTEM_VARIABLES:
        return 0.0

    available = 0

    for variable in ECOSYSTEM_VARIABLES:
        if variables.get(variable) is not None:
            available += 1

    return round(
        available / len(ECOSYSTEM_VARIABLES),
        2,
    )


def analyze_ecosystem(
    latitude: float,
    longitude: float,
    planned_datetime: Optional[str] = None,
    zone_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Run the Ecosystem Agent for a location.
    """

    result = ecosystem_tool(
        latitude=latitude,
        longitude=longitude,
        planned_datetime=planned_datetime,
    )

    if not isinstance(result, dict):
        return {
            "zoneId": zone_id,
            "status": "error",
            "summary": (
                "Ecosystem service returned "
                "an invalid response."
            ),
            "evidence": [],
            "missing_variables": ECOSYSTEM_VARIABLES,
            "data_completeness": 0.0,
            "error": {
                "type": "agent",
                "message": (
                    "Invalid ecosystem service response."
                ),
            },
        }

    variables = _extract_variables(result)
    status = _extract_status(result)

    missing_variables = _build_missing_variables(
        variables
    )

    evidence: List[Evidence] = []

    for variable in ECOSYSTEM_VARIABLES:
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


def ecosystem_agent(
    zone: Dict[str, Any],
    planned_datetime: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Zone-aware Ecosystem Agent entry point.

    Stable zoneId is carried through the complete result.
    """

    if not isinstance(zone, dict):
        return {
            "zoneId": None,
            "status": "error",
            "summary": "Invalid zone.",
            "evidence": [],
            "missing_variables": ECOSYSTEM_VARIABLES,
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
                "Ecosystem analysis could not run "
                "because zone coordinates are missing."
            ),
            "evidence": [],
            "missing_variables": ECOSYSTEM_VARIABLES,
            "data_completeness": 0.0,
            "error": {
                "type": "validation",
                "message": (
                    "Zone latitude and longitude are required."
                ),
            },
        }

    return analyze_ecosystem(
        latitude=latitude,
        longitude=longitude,
        planned_datetime=planned_datetime,
        zone_id=zone_id,
    )