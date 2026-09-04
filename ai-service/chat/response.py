from typing import Any, Dict, List, Optional

from chat.memory import get_recent_messages


def _safe_text(value: Any) -> str:
    """
    Convert a value to safe display text.
    """

    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    return str(value).strip()


def _format_evidence(evidence: Any) -> List[str]:
    """
    Convert structured evidence into concise readable statements.
    """

    if not isinstance(evidence, list):
        return []

    formatted = []

    for item in evidence:
        if not isinstance(item, dict):
            continue

        variable = _safe_text(item.get("variable"))
        value = item.get("value")
        unit = _safe_text(item.get("unit"))
        source = _safe_text(item.get("source"))

        if not variable or value is None:
            continue

        statement = f"{variable}: {value}"

        if unit:
            statement += f" {unit}"

        if source:
            statement += f" (source: {source})"

        formatted.append(statement)

    return formatted


def _get_zone_context(
    context: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Extract the currently selected zone context.
    """

    if not isinstance(context, dict):
        return {}

    zone = context.get("zone", {})

    return zone if isinstance(zone, dict) else {}


def _get_component(
    zone_context: Dict[str, Any],
    component: str,
) -> Dict[str, Any]:
    """
    Safely retrieve one analysis component.
    """

    value = zone_context.get(component, {})

    return value if isinstance(value, dict) else {}


def _build_weather_response(
    zone_context: Dict[str, Any],
) -> str:
    weather = _get_component(zone_context, "weather")

    if not weather:
        return "Weather analysis is not available for the selected zone."

    summary = _safe_text(weather.get("summary"))

    if summary:
        return summary

    status = _safe_text(weather.get("status"))

    if status in {"missing", "unavailable", "error"}:
        return "Weather data is currently unavailable for the selected zone."

    return "Weather analysis is available, but no summary was provided."


def _build_ocean_response(
    zone_context: Dict[str, Any],
) -> str:
    ocean = _get_component(zone_context, "ocean")

    if not ocean:
        return "Ocean analysis is not available for the selected zone."

    summary = _safe_text(ocean.get("summary"))

    if summary:
        return summary

    status = _safe_text(ocean.get("status"))

    if status in {"missing", "unavailable", "error"}:
        return "Ocean data is currently unavailable for the selected zone."

    return "Ocean analysis is available, but no summary was provided."


def _build_ecosystem_response(
    zone_context: Dict[str, Any],
) -> str:
    ecosystem = _get_component(zone_context, "ecosystem")

    if not ecosystem:
        return "Ecosystem analysis is not available for the selected zone."

    summary = _safe_text(ecosystem.get("summary"))

    if summary:
        return summary

    status = _safe_text(ecosystem.get("status"))

    if status in {"missing", "unavailable", "error"}:
        return (
            "Ecosystem data is currently unavailable "
            "for the selected zone."
        )

    return (
        "Ecosystem analysis is available, "
        "but no summary was provided."
    )


def _build_risk_response(
    zone_context: Dict[str, Any],
) -> str:
    risk = _get_component(zone_context, "risk")

    if not risk:
        return "Risk analysis is not available for the selected zone."

    risk_level = _safe_text(
        risk.get("risk_level", "unknown")
    )

    summary = _safe_text(risk.get("summary"))

    if summary:
        return (
            f"Risk level: {risk_level}. "
            f"{summary}"
        )

    return f"Risk level: {risk_level}."


def _build_decision_response(
    zone_context: Dict[str, Any],
) -> str:
    decision = _get_component(zone_context, "decision")

    if not decision:
        return (
            "A decision recommendation is not available "
            "for the selected zone."
        )

    recommendation = _safe_text(
        decision.get("recommendation")
    )

    risk_level = _safe_text(
        decision.get("risk_level", "unknown")
    )

    if recommendation:
        return (
            f"Risk level: {risk_level}. "
            f"{recommendation}"
        )

    return f"Risk level: {risk_level}. No recommendation was provided."


def _build_general_response(
    zone_context: Dict[str, Any],
) -> str:
    """
    Provide a concise overview without inventing information.
    """

    if not zone_context:
        return (
            "No analysis context is currently available. "
            "Please provide or select an analysis first."
        )

    zone_id = _safe_text(zone_context.get("zoneId"))

    weather = _get_component(zone_context, "weather")
    ocean = _get_component(zone_context, "ocean")
    ecosystem = _get_component(zone_context, "ecosystem")
    risk = _get_component(zone_context, "risk")
    decision = _get_component(zone_context, "decision")

    parts = []

    if zone_id:
        parts.append(f"Zone {zone_id}")

    if weather:
        parts.append(
            f"Weather: {_safe_text(weather.get('summary')) or 'available'}"
        )

    if ocean:
        parts.append(
            f"Ocean: {_safe_text(ocean.get('summary')) or 'available'}"
        )

    if ecosystem:
        parts.append(
            "Ecosystem: "
            f"{_safe_text(ecosystem.get('summary')) or 'available'}"
        )

    if risk:
        parts.append(
            f"Risk: {_safe_text(risk.get('risk_level', 'unknown'))}"
        )

    if decision:
        recommendation = _safe_text(
            decision.get("recommendation")
        )

        if recommendation:
            parts.append(
                f"Recommendation: {recommendation}"
            )

    return "\n".join(parts) if parts else (
        "Analysis context is available, "
        "but no usable assessment was found."
    )


def _build_comparison_response(
    context: Dict[str, Any],
) -> str:
    """
    Build a comparison response using only existing
    cross-zone decision data.
    """

    comparison = context.get("comparison", {})

    if not isinstance(comparison, dict):
        return "Zone comparison data is not available."

    decision = comparison.get("decision", {})

    if not isinstance(decision, dict):
        return "Zone comparison data is not available."

    zone_comparison = decision.get(
        "zone_comparison",
        [],
    )

    if not isinstance(zone_comparison, list) or not zone_comparison:
        return "No cross-zone comparison is available."

    lines = ["Zone comparison:"]

    for item in zone_comparison:
        if not isinstance(item, dict):
            continue

        zone_id = _safe_text(item.get("zoneId"))

        if not zone_id:
            continue

        risk_level = _safe_text(
            item.get("risk_level", "unknown")
        )

        confidence = item.get("confidence")

        line = f"- {zone_id}: risk={risk_level}"

        if confidence is not None:
            line += f", confidence={confidence}"

        lines.append(line)

    if len(lines) == 1:
        return "No usable zone comparison data is available."

    return "\n".join(lines)


def build_response(
    route: str,
    context: Dict[str, Any],
    state: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Build a deterministic response from trusted analysis context.

    The user's question is never treated as an instruction for
    accessing external services or changing analysis results.
    """

    route = _safe_text(route).lower()

    if route == "weather":
        zone_context = _get_zone_context(context)
        return _build_weather_response(zone_context)

    if route == "ocean":
        zone_context = _get_zone_context(context)
        return _build_ocean_response(zone_context)

    if route == "ecosystem":
        zone_context = _get_zone_context(context)
        return _build_ecosystem_response(zone_context)

    if route == "risk":
        zone_context = _get_zone_context(context)
        return _build_risk_response(zone_context)

    if route == "decision":
        zone_context = _get_zone_context(context)
        return _build_decision_response(zone_context)

    if route == "comparison":
        return _build_comparison_response(context)

    if route == "general":
        zone_context = _get_zone_context(context)
        return _build_general_response(zone_context)

    return (
        "I could not determine the appropriate analysis context "
        "for this question."
    )


def build_chat_response(
    state: Dict[str, Any],
    route: str,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Produce the final structured chat response.
    """

    context = context or state.get("context", {})

    if not isinstance(context, dict):
        context = {}

    answer = build_response(
        route=route,
        context=context,
        state=state,
    )

    return {
        "conversation_id": state.get("conversation_id"),
        "analysis_id": state.get("analysis_id"),
        "zoneId": state.get("current_zone"),
        "route": route,
        "answer": answer,
        "history": get_recent_messages(state),
        "success": True,
    }


def response_with_evidence(
    answer: str,
    evidence: Any,
) -> Dict[str, Any]:
    """
    Optional structured response helper that exposes
    provenance without fabricating evidence.
    """

    return {
        "answer": _safe_text(answer),
        "evidence": _format_evidence(evidence),
    }