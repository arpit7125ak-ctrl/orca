from typing import Any, Dict, Optional

from chat.state import ChatState


def _is_valid_zone_id(zone_id: Any) -> bool:
    """
    Validate that a zone identifier is a non-empty string.
    """

    return (
        isinstance(zone_id, str)
        and bool(zone_id.strip())
    )


def _filter_by_zone(
    data: Any,
    zone_id: Optional[str],
) -> Any:
    """
    Return only the requested zone's result.

    This prevents chat responses from accidentally mixing
    results belonging to different zones.
    """

    if zone_id is None:
        return data

    if not isinstance(data, dict):
        return None

    return data.get(zone_id)


def get_zone_context(
    analysis_context: Dict[str, Any],
    zone_id: str,
) -> Dict[str, Any]:
    """
    Extract analysis context for exactly one zone.
    """

    if not isinstance(analysis_context, dict):
        return {}

    if not _is_valid_zone_id(zone_id):
        return {}

    context: Dict[str, Any] = {
        "zoneId": zone_id,
    }

    zone_results = analysis_context.get("zone_results", {})
    weather_results = analysis_context.get("weather_results", {})
    ocean_results = analysis_context.get("ocean_results", {})
    ecosystem_results = analysis_context.get("ecosystem_results", {})
    risk_results = analysis_context.get("risk_results", {})
    decision_results = analysis_context.get("decision_results", {})

    if isinstance(zone_results, dict):
        value = _filter_by_zone(zone_results, zone_id)
        if value is not None:
            context["zone_result"] = value

    if isinstance(weather_results, dict):
        value = _filter_by_zone(weather_results, zone_id)
        if value is not None:
            context["weather"] = value

    if isinstance(ocean_results, dict):
        value = _filter_by_zone(ocean_results, zone_id)
        if value is not None:
            context["ocean"] = value

    if isinstance(ecosystem_results, dict):
        value = _filter_by_zone(ecosystem_results, zone_id)
        if value is not None:
            context["ecosystem"] = value

    if isinstance(risk_results, dict):
        value = _filter_by_zone(risk_results, zone_id)
        if value is not None:
            context["risk"] = value

    if isinstance(decision_results, dict):
        value = _filter_by_zone(decision_results, zone_id)
        if value is not None:
            context["decision"] = value

    return context


def get_comparison_context(
    analysis_context: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Extract cross-zone comparison information.

    Comparison context is intentionally separate from a
    single-zone context.
    """

    if not isinstance(analysis_context, dict):
        return {}

    return {
        "analysisId": analysis_context.get("analysis_id"),
        "decision": analysis_context.get("decision"),
        "zone_results": analysis_context.get("zone_results", {}),
        "decision_results": analysis_context.get(
            "decision_results",
            {},
        ),
    }


def build_chat_context(
    state: ChatState,
    analysis_context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Build the trusted analysis context available to the chatbot.

    The user's question is deliberately not merged into this
    trusted context. It is treated as untrusted input.
    """

    analysis_context = analysis_context or state.get(
        "context",
        {},
    )

    if not isinstance(analysis_context, dict):
        analysis_context = {}

    current_zone = state.get("current_zone")

    context: Dict[str, Any] = {
        "conversation_id": state.get("conversation_id"),
        "analysis_id": state.get("analysis_id"),
    }

    if _is_valid_zone_id(current_zone):
        context["zone"] = get_zone_context(
            analysis_context,
            current_zone,
        )
    else:
        context["comparison"] = get_comparison_context(
            analysis_context,
        )

    return context


def set_analysis_context(
    state: ChatState,
    analysis_context: Dict[str, Any],
) -> ChatState:
    """
    Store analysis results as trusted chatbot context.
    """

    if not isinstance(analysis_context, dict):
        raise ValueError(
            "Analysis context must be a dictionary."
        )

    state["context"] = analysis_context

    analysis_id = analysis_context.get("analysis_id")

    if analysis_id is not None:
        state["analysis_id"] = analysis_id

    return state