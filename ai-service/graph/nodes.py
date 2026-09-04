from typing import Any, Dict

from agents.weather_agent import weather_agent
from agents.ocean_agent import ocean_agent
from agents.ecosystem_agent import ecosystem_agent
from agents.risk_agent import risk_agent
from agents.decision_agent import decision_agent, compare_zone_decisions

from graph.state import (
    AnalysisState,
    get_zone_ids,
    get_zone,
    update_zone_result,
    add_error,
    mark_partial,
    validate_state_zone_identity,
)


def _get_planned_datetime(state: AnalysisState) -> str | None:
    """
    Extract planned datetime from the original request.
    """
    request = state.get("request", {})

    if not isinstance(request, dict):
        return None

    return request.get("planned_datetime")


def _safe_zone(state: AnalysisState, zone_id: str) -> Dict[str, Any]:
    """
    Get a zone using stable zoneId.
    """
    zone = get_zone(state, zone_id)

    if not isinstance(zone, dict):
        raise ValueError(f"Zone '{zone_id}' could not be found.")

    return zone


def weather_node(state: AnalysisState) -> AnalysisState:
    """
    Run Weather Agent independently for every zone.
    """
    planned_datetime = _get_planned_datetime(state)

    for zone_id in get_zone_ids(state):
        try:
            zone = _safe_zone(state, zone_id)

            result = weather_agent(
                zone=zone,
                planned_datetime=planned_datetime,
            )

            if not isinstance(result, dict):
                raise ValueError(
                    f"Weather agent returned invalid result for zone '{zone_id}'."
                )

            if result.get("zoneId") != zone_id:
                raise ValueError(
                    f"Weather agent zoneId mismatch for zone '{zone_id}'."
                )

            state.setdefault("weather_results", {})[zone_id] = result

            update_zone_result(
                state,
                zone_id,
                "weather",
                result,
            )

        except Exception as exc:
            error = {
                "type": "agent",
                "component": "weather",
                "zoneId": zone_id,
                "message": str(exc),
            }

            add_error(state, error, zone_id)
            mark_partial(state, zone_id)

    validate_state_zone_identity(state)

    return state


def ocean_node(state: AnalysisState) -> AnalysisState:
    """
    Run Ocean Agent independently for every zone.
    """
    planned_datetime = _get_planned_datetime(state)

    for zone_id in get_zone_ids(state):
        try:
            zone = _safe_zone(state, zone_id)

            result = ocean_agent(
                zone=zone,
                planned_datetime=planned_datetime,
            )

            if not isinstance(result, dict):
                raise ValueError(
                    f"Ocean agent returned invalid result for zone '{zone_id}'."
                )

            if result.get("zoneId") != zone_id:
                raise ValueError(
                    f"Ocean agent zoneId mismatch for zone '{zone_id}'."
                )

            state.setdefault("ocean_results", {})[zone_id] = result

            update_zone_result(
                state,
                zone_id,
                "ocean",
                result,
            )

        except Exception as exc:
            error = {
                "type": "agent",
                "component": "ocean",
                "zoneId": zone_id,
                "message": str(exc),
            }

            add_error(state, error, zone_id)
            mark_partial(state, zone_id)

    validate_state_zone_identity(state)

    return state


def ecosystem_node(state: AnalysisState) -> AnalysisState:
    """
    Run Ecosystem Agent independently for every zone.
    """
    planned_datetime = _get_planned_datetime(state)

    for zone_id in get_zone_ids(state):
        try:
            zone = _safe_zone(state, zone_id)

            result = ecosystem_agent(
                zone=zone,
                planned_datetime=planned_datetime,
            )

            if not isinstance(result, dict):
                raise ValueError(
                    f"Ecosystem agent returned invalid result for zone '{zone_id}'."
                )

            if result.get("zoneId") != zone_id:
                raise ValueError(
                    f"Ecosystem agent zoneId mismatch for zone '{zone_id}'."
                )

            state.setdefault("ecosystem_results", {})[zone_id] = result

            update_zone_result(
                state,
                zone_id,
                "ecosystem",
                result,
            )

        except Exception as exc:
            error = {
                "type": "agent",
                "component": "ecosystem",
                "zoneId": zone_id,
                "message": str(exc),
            }

            add_error(state, error, zone_id)
            mark_partial(state, zone_id)

    validate_state_zone_identity(state)

    return state


def risk_node(state: AnalysisState) -> AnalysisState:
    """
    Run Risk Agent after Weather, Ocean and Ecosystem analysis.

    Each zone receives only its own domain results.
    """
    weather_results = state.get("weather_results", {})
    ocean_results = state.get("ocean_results", {})
    ecosystem_results = state.get("ecosystem_results", {})

    for zone_id in get_zone_ids(state):
        try:
            zone = _safe_zone(state, zone_id)

            weather_result = weather_results.get(zone_id)
            ocean_result = ocean_results.get(zone_id)
            ecosystem_result = ecosystem_results.get(zone_id)

            result = risk_agent(
                zone=zone,
                weather_result=weather_result,
                ocean_result=ocean_result,
                ecosystem_result=ecosystem_result,
            )

            if not isinstance(result, dict):
                raise ValueError(
                    f"Risk agent returned invalid result for zone '{zone_id}'."
                )

            if result.get("zoneId") != zone_id:
                raise ValueError(
                    f"Risk agent zoneId mismatch for zone '{zone_id}'."
                )

            state.setdefault("risk_results", {})[zone_id] = result

            update_zone_result(
                state,
                zone_id,
                "risk",
                result,
            )

        except Exception as exc:
            error = {
                "type": "agent",
                "component": "risk",
                "zoneId": zone_id,
                "message": str(exc),
            }

            add_error(state, error, zone_id)
            mark_partial(state, zone_id)

    validate_state_zone_identity(state)

    return state


def decision_node(state: AnalysisState) -> AnalysisState:
    """
    Run Decision Agent for every zone and create a cross-zone comparison.

    The comparison is deterministic and uses zoneId rather than
    array position as the zone identity.
    """
    weather_results = state.get("weather_results", {})
    ocean_results = state.get("ocean_results", {})
    ecosystem_results = state.get("ecosystem_results", {})
    risk_results = state.get("risk_results", {})

    decisions = []

    for zone_id in get_zone_ids(state):
        try:
            zone = _safe_zone(state, zone_id)

            weather_result = weather_results.get(zone_id)
            ocean_result = ocean_results.get(zone_id)
            ecosystem_result = ecosystem_results.get(zone_id)
            risk_result = risk_results.get(zone_id)

            result = decision_agent(
                zone=zone,
                weather_result=weather_result,
                ocean_result=ocean_result,
                ecosystem_result=ecosystem_result,
                risk_result=risk_result,
            )

            if not isinstance(result, dict):
                raise ValueError(
                    f"Decision agent returned invalid result for zone '{zone_id}'."
                )

            if result.get("zoneId") != zone_id:
                raise ValueError(
                    f"Decision agent zoneId mismatch for zone '{zone_id}'."
                )

            state.setdefault("decision_results", {})[zone_id] = result

            update_zone_result(
                state,
                zone_id,
                "decision",
                result,
            )

            decisions.append(result)

        except Exception as exc:
            error = {
                "type": "agent",
                "component": "decision",
                "zoneId": zone_id,
                "message": str(exc),
            }

            add_error(state, error, zone_id)
            mark_partial(state, zone_id)

    # Only compare successfully generated zone decisions.
    if decisions:
        comparison = compare_zone_decisions(decisions)
    else:
        comparison = []

    state["decision"] = {
        "analysisId": state.get("analysis_id"),
        "zone_decisions": decisions,
        "zone_comparison": comparison,
        "zone_count": len(get_zone_ids(state)),
        "successful_zone_decisions": len(decisions),
    }

    validate_state_zone_identity(state)

    return state


def finalize_node(state: AnalysisState) -> AnalysisState:
    """
    Final validation before returning the graph result.
    """
    validate_state_zone_identity(state)

    errors = state.get("errors", [])

    state["partial"] = bool(state.get("partial", False) or errors)
    state["success"] = not state["partial"]

    return state
