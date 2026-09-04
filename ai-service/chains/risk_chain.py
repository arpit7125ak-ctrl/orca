from typing import Any, Dict, Optional

from agents.risk_agent import analyze_risk


def risk_chain(
    zone: Dict[str, Any],
    weather_result: Optional[Dict[str, Any]],
    ocean_result: Optional[Dict[str, Any]],
    ecosystem_result: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Execute the Risk reasoning chain for a single zone.

    Risk is derived only from the supplied Weather, Ocean,
    and Ecosystem evidence. No raw environmental values are
    fabricated when a component is unavailable.
    """

    if not isinstance(zone, dict):
        raise ValueError("Zone must be a dictionary.")

    zone_id = zone.get("zoneId")

    if not zone_id:
        raise ValueError("zoneId is required for risk analysis.")

    try:
        result = analyze_risk(
            zone_id=zone_id,
            weather_result=weather_result,
            ocean_result=ocean_result,
            ecosystem_result=ecosystem_result,
        )

        if not isinstance(result, dict):
            raise ValueError("Risk agent returned an invalid result.")

        if result.get("zoneId") != zone_id:
            raise ValueError(
                f"Risk result zoneId mismatch. "
                f"Expected '{zone_id}', "
                f"received '{result.get('zoneId')}'."
            )

        return result

    except Exception as exc:
        return {
            "zoneId": zone_id,
            "risk_level": "unknown",
            "risk_factors": [],
            "confidence": 0.0,
            "failed_domains": [],
            "limitations": [
                "Risk analysis could not be completed."
            ],
            "summary": "Risk analysis failed.",
            "error": {
                "type": "chain",
                "component": "risk",
                "message": str(exc),
            },
        }


run_risk_chain = risk_chain
