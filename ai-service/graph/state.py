"""
AI-Service/graph/state.py

Shared state for the LangGraph analysis workflow.

Workflow:

START
  ↓
Weather
  ↓
Ocean
  ↓
Ecosystem
  ↓
Risk
  ↓
Decision
  ↓
END

Responsibilities:
- Maintain analysis-level state.
- Maintain multi-zone information.
- Preserve stable zoneId.
- Store domain-agent results.
- Store errors and partial failures.
- Prevent zone identity from depending on array position.

This module must not:
- Fetch external data.
- Call an LLM.
- Perform agent reasoning.
- Generate environmental measurements.
"""

from typing import Any, Dict, List, Optional, TypedDict


class AnalysisState(TypedDict, total=False):
    """
    Main state object passed between LangGraph nodes.
    """

    # ------------------------------------------------------------------
    # Analysis identity
    # ------------------------------------------------------------------

    analysis_id: str

    # ------------------------------------------------------------------
    # Original request
    # ------------------------------------------------------------------

    request: Dict[str, Any]

    # ------------------------------------------------------------------
    # Multi-zone input
    #
    # Every zone must contain a stable zoneId.
    # ------------------------------------------------------------------

    zones: List[Dict[str, Any]]

    # ------------------------------------------------------------------
    # Agent results
    #
    # Each dictionary is keyed by zoneId.
    # This avoids relying on array positions.
    # ------------------------------------------------------------------

    zone_results: Dict[str, Dict[str, Any]]

    weather_results: Dict[str, Dict[str, Any]]

    ocean_results: Dict[str, Dict[str, Any]]

    ecosystem_results: Dict[str, Dict[str, Any]]

    risk_results: Dict[str, Dict[str, Any]]

    decision_results: Dict[str, Dict[str, Any]]

    # ------------------------------------------------------------------
    # Final decision
    # ------------------------------------------------------------------

    decision: Optional[Dict[str, Any]]

    # ------------------------------------------------------------------
    # Errors
    # ------------------------------------------------------------------

    errors: List[Dict[str, Any]]

    # ------------------------------------------------------------------
    # Workflow status
    # ------------------------------------------------------------------

    success: bool

    partial: bool


def create_initial_state(
    request: Dict[str, Any],
) -> AnalysisState:
    """
    Create the initial state for a new analysis.

    Parameters
    ----------
    request:
        Validated analysis request.

    Returns
    -------
    AnalysisState
        Initial LangGraph state.
    """

    if not isinstance(request, dict):
        raise ValueError(
            "Analysis request must be a dictionary."
        )

    analysis_id = request.get("analysisId")

    if not analysis_id:
        raise ValueError(
            "Analysis request must contain analysisId."
        )

    zones = request.get("zones", [])

    if not isinstance(zones, list):
        raise ValueError(
            "Analysis request zones must be a list."
        )

    state: AnalysisState = {
        "analysis_id": str(analysis_id),
        "request": request,
        "zones": zones,
        "zone_results": {},
        "weather_results": {},
        "ocean_results": {},
        "ecosystem_results": {},
        "risk_results": {},
        "decision_results": {},
        "decision": None,
        "errors": [],
        "success": True,
        "partial": False,
    }

    return state


def get_zone_ids(
    state: AnalysisState,
) -> List[str]:
    """
    Return stable zoneIds from the current state.

    Raises
    ------
    ValueError
        If a zone does not have a zoneId or if duplicate
        zoneIds are detected.
    """

    zones = state.get("zones", [])

    if not isinstance(zones, list):
        raise ValueError(
            "State zones must be a list."
        )

    zone_ids: List[str] = []

    for zone in zones:
        if not isinstance(zone, dict):
            raise ValueError(
                "Every zone must be an object."
            )

        zone_id = zone.get("zoneId")

        if zone_id is None or str(zone_id).strip() == "":
            raise ValueError(
                "Every zone must contain a stable zoneId."
            )

        zone_id = str(zone_id)

        if zone_id in zone_ids:
            raise ValueError(
                f"Duplicate zoneId detected: {zone_id}"
            )

        zone_ids.append(zone_id)

    return zone_ids


def get_zone(
    state: AnalysisState,
    zone_id: str,
) -> Optional[Dict[str, Any]]:
    """
    Find a zone using its stable zoneId.

    Zone lookup never depends on array position.
    """

    if not zone_id:
        return None

    for zone in state.get("zones", []):
        if not isinstance(zone, dict):
            continue

        if str(zone.get("zoneId")) == str(zone_id):
            return zone

    return None


def get_zone_result(
    state: AnalysisState,
    zone_id: str,
) -> Dict[str, Any]:
    """
    Get or create the aggregate result for a zone.
    """

    zone_id = str(zone_id)

    results = state.setdefault(
        "zone_results",
        {},
    )

    if zone_id not in results:
        results[zone_id] = {
            "analysisId": state.get(
                "analysis_id"
            ),
            "zoneId": zone_id,
            "weather": None,
            "ocean": None,
            "ecosystem": None,
            "risk": None,
            "decision": None,
            "errors": [],
            "partial": False,
        }

    return results[zone_id]


def update_zone_result(
    state: AnalysisState,
    zone_id: str,
    component: str,
    result: Optional[Dict[str, Any]],
) -> None:
    """
    Store a component result against a specific zone.

    Parameters
    ----------
    zone_id:
        Stable zone identifier.

    component:
        One of:
        weather
        ocean
        ecosystem
        risk
        decision

    result:
        Agent output.
    """

    allowed_components = {
        "weather",
        "ocean",
        "ecosystem",
        "risk",
        "decision",
    }

    if component not in allowed_components:
        raise ValueError(
            f"Unsupported zone result component: {component}"
        )

    zone_id = str(zone_id)

    zone_result = get_zone_result(
        state,
        zone_id,
    )

    zone_result[component] = result

    if isinstance(result, dict):
        result_zone_id = result.get("zoneId")

        # Never silently associate a result with the wrong zone.
        if (
            result_zone_id is not None
            and str(result_zone_id) != zone_id
        ):
            raise ValueError(
                "Zone identity mismatch: "
                f"expected {zone_id}, "
                f"received {result_zone_id}."
            )

        if result.get("error"):
            zone_result["errors"].append(
                result["error"]
            )
            zone_result["partial"] = True

        status = str(
            result.get("status", "")
        ).lower()

        if status in {
            "error",
            "missing",
            "unavailable",
        }:
            zone_result["partial"] = True

    if zone_result.get("partial"):
        state["partial"] = True


def add_error(
    state: AnalysisState,
    error: Dict[str, Any],
    zone_id: Optional[str] = None,
) -> None:
    """
    Add a structured workflow error.

    If zoneId is supplied, the error is also attached
    to that zone.
    """

    if not isinstance(error, dict):
        error = {
            "type": "unknown",
            "message": str(error),
        }

    error_copy = dict(error)

    if zone_id is not None:
        error_copy["zoneId"] = str(zone_id)

    state.setdefault(
        "errors",
        [],
    ).append(error_copy)

    state["partial"] = True

    if zone_id is not None:
        zone_result = get_zone_result(
            state,
            str(zone_id),
        )

        zone_result.setdefault(
            "errors",
            [],
        ).append(error_copy)

        zone_result["partial"] = True


def mark_partial(
    state: AnalysisState,
    zone_id: Optional[str] = None,
) -> None:
    """
    Mark the analysis or a specific zone as partial.
    """

    state["partial"] = True

    if zone_id is not None:
        zone_result = get_zone_result(
            state,
            str(zone_id),
        )

        zone_result["partial"] = True


def validate_state_zone_identity(
    state: AnalysisState,
) -> None:
    """
    Validate that all stored results correspond to known zones.

    This protects against accidental cross-zone mixing.
    """

    known_zone_ids = set(
        get_zone_ids(state)
    )

    result_maps = [
        state.get("weather_results", {}),
        state.get("ocean_results", {}),
        state.get("ecosystem_results", {}),
        state.get("risk_results", {}),
        state.get("decision_results", {}),
        state.get("zone_results", {}),
    ]

    for result_map in result_maps:
        if not isinstance(result_map, dict):
            continue

        for zone_id, result in result_map.items():

            zone_id = str(zone_id)

            if zone_id not in known_zone_ids:
                raise ValueError(
                    "Result contains unknown zoneId: "
                    f"{zone_id}"
                )

            if not isinstance(result, dict):
                continue

            result_zone_id = result.get("zoneId")

            if (
                result_zone_id is not None
                and str(result_zone_id) != zone_id
            ):
                raise ValueError(
                    "Stored result zoneId does not match "
                    f"its map key: {zone_id}"
                )


def finalize_state(
    state: AnalysisState,
) -> AnalysisState:
    """
    Mark the state as successfully completed or partial.

    A partial analysis is not reported as fully successful.
    """

    validate_state_zone_identity(state)

    state["success"] = not bool(
        state.get("partial", False)
    )

    return state
