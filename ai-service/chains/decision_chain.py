from typing import Any, Dict, List, Optional

from agents.decision_agent import (
    analyze_decision,
    compare_zone_decisions,
)


def decision_chain(
    zone: Dict[str, Any],
    weather_result: Optional[Dict[str, Any]],
    ocean_result: Optional[Dict[str, Any]],
    ecosystem_result: Optional[Dict[str, Any]],
    risk_result: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Execute the Decision reasoning chain for a single zone.

    The final recommendation is based only on the supplied
    domain assessments and risk assessment.
    """

    if not isinstance(zone, dict):
        raise ValueError("Zone must be a dictionary.")

    zone_id = zone.get("zoneId")

    if not zone_id:
        raise ValueError("zoneId is required for decision analysis.")

    try:
        result = analyze_decision(
            zone_id=zone_id,
            weather_result=weather_result,
            ocean_result=ocean_result,
            ecosystem_result=ecosystem_result,
            risk_result=risk_result,
        )

        if not isinstance(result, dict):
            raise ValueError(
                "Decision agent returned an invalid result."
            )

        if result.get("zoneId") != zone_id:
            raise ValueError(
                f"Decision result zoneId mismatch. "
                f"Expected '{zone_id}', "
                f"received '{result.get('zoneId')}'."
            )

        return result

    except Exception as exc:
        return {
            "zoneId": zone_id,
            "risk_level": "unknown",
            "recommendation": (
                "A reliable recommendation cannot be produced "
                "because decision analysis failed."
            ),
            "key_reasons": [],
            "confidence": 0.0,
            "evidence": [],
            "limitations": [
                "Decision analysis could not be completed."
            ],
            "component_summaries": {},
            "data_quality": {
                "status": "error",
            },
            "error": {
                "type": "chain",
                "component": "decision",
                "message": str(exc),
            },
        }


def compare_decision_chain(
    decisions: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Compare decisions across multiple zones.

    Zone identity is preserved using zoneId.
    """

    if not isinstance(decisions, list):
        raise ValueError("Decisions must be provided as a list.")

    valid_decisions = []

    for decision in decisions:
        if not isinstance(decision, dict):
            continue

        zone_id = decision.get("zoneId")

        if not zone_id:
            continue

        valid_decisions.append(decision)

    if not valid_decisions:
        return []

    try:
        comparison = compare_zone_decisions(valid_decisions)

        if not isinstance(comparison, list):
            raise ValueError(
                "Decision comparison returned an invalid result."
            )

        return comparison

    except Exception:
        # Preserve the individual decisions even if the
        # optional comparison step fails.
        return [
            {
                "zoneId": decision.get("zoneId"),
                "risk_level": decision.get("risk_level", "unknown"),
                "confidence": decision.get("confidence", 0.0),
            }
            for decision in valid_decisions
        ]


run_decision_chain = decision_chain
