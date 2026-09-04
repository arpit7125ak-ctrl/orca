"""
AI-Service/agents/decision_agent.py

Decision Agent

Responsibilities:
- Produce the final recommendation for a zone.
- Use Weather, Ocean, Ecosystem, and Risk outputs.
- Preserve stable zoneId.
- Explain recommendations using traceable evidence.
- Communicate missing data and limitations.
- Support comparison across multiple zones.

This agent must not:
- Invent environmental values.
- Invent sources, timestamps, or confidence.
- Hide missing data.
- Expose hidden chain-of-thought.
- Override unavailable or failed data with assumptions.
"""

from typing import Any, Dict, List, Optional

from models.schemas import RiskLevel


RISK_ORDER = {
    RiskLevel.LOW.value: 0,
    RiskLevel.MODERATE.value: 1,
    RiskLevel.HIGH.value: 2,
    RiskLevel.CRITICAL.value: 3,
    RiskLevel.UNKNOWN.value: -1,
}


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


def _risk_level(
    risk_result: Optional[Dict[str, Any]],
) -> str:
    """
    Extract risk level safely.
    """

    if not isinstance(risk_result, dict):
        return RiskLevel.UNKNOWN.value

    level = risk_result.get("risk_level")

    if level is None:
        return RiskLevel.UNKNOWN.value

    return str(level).lower()


def _get_risk_factors(
    risk_result: Optional[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Extract risk factors.
    """

    if not isinstance(risk_result, dict):
        return []

    factors = risk_result.get("risk_factors", [])

    if not isinstance(factors, list):
        return []

    return [
        factor
        for factor in factors
        if isinstance(factor, dict)
    ]


def _get_limitations(
    risk_result: Optional[Dict[str, Any]],
) -> List[str]:
    """
    Extract risk limitations.
    """

    if not isinstance(risk_result, dict):
        return ["Risk assessment is unavailable."]

    limitations = risk_result.get(
        "limitations",
        [],
    )

    if not isinstance(limitations, list):
        return []

    return [
        str(item)
        for item in limitations
        if item is not None
    ]


def _get_component_status(
    result: Optional[Dict[str, Any]],
) -> str:
    """
    Extract component status.
    """

    if not isinstance(result, dict):
        return "missing"

    return str(
        result.get("status", "unknown")
    ).lower()


def _get_component_summary(
    result: Optional[Dict[str, Any]],
) -> Optional[str]:
    """
    Extract the factual summary from a domain agent.
    """

    if not isinstance(result, dict):
        return None

    summary = result.get("summary")

    if summary is None:
        return None

    return str(summary)


def _build_key_reasons(
    risk_result: Optional[Dict[str, Any]],
) -> List[str]:
    """
    Build concise reasons directly from risk factors.
    """

    reasons: List[str] = []

    for factor in _get_risk_factors(risk_result):
        domain = factor.get("domain")
        variable = factor.get("variable")
        value = factor.get("value")
        reason = factor.get("reason")

        if reason:
            if variable:
                reasons.append(
                    f"{domain or 'domain'} / "
                    f"{variable}: {reason}"
                )
            else:
                reasons.append(
                    str(reason)
                )
            continue

        if variable and value is not None:
            reasons.append(
                f"{domain or 'domain'} / "
                f"{variable} supplied value: {value}."
            )

    return reasons


def _build_evidence(
    weather_result: Optional[Dict[str, Any]],
    ocean_result: Optional[Dict[str, Any]],
    ecosystem_result: Optional[Dict[str, Any]],
    risk_result: Optional[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Build final traceable evidence references.

    Evidence is copied from the supplied agent outputs.
    """

    evidence: List[Dict[str, Any]] = []

    components = [
        ("weather", weather_result),
        ("ocean", ocean_result),
        ("ecosystem", ecosystem_result),
    ]

    for domain, result in components:
        if not isinstance(result, dict):
            continue

        items = result.get("evidence", [])

        if not isinstance(items, list):
            continue

        for item in items:
            if not isinstance(item, dict):
                continue

            evidence_item = {
                "domain": domain,
                "variable": item.get("variable"),
                "value": item.get("value"),
                "unit": item.get("unit"),
                "source": item.get("source"),
                "timestamp": item.get("timestamp"),
                "status": item.get("status"),
                "quality": item.get("quality"),
            }

            evidence.append(evidence_item)

    # Include risk-factor provenance where available.
    for factor in _get_risk_factors(risk_result):
        factor_evidence = {
            "domain": factor.get("domain"),
            "variable": factor.get("variable"),
            "value": factor.get("value"),
            "unit": factor.get("unit"),
            "source": factor.get("source"),
            "timestamp": factor.get("timestamp"),
            "status": factor.get("status"),
            "quality": factor.get("quality"),
        }

        evidence.append(factor_evidence)

    return evidence


def _build_recommendation(
    risk_level: str,
    failed_domains: List[str],
) -> str:
    """
    Generate a conservative operational recommendation.

    This is a recommendation label, not a claim that an
    activity is objectively safe or unsafe.
    """

    if risk_level == RiskLevel.CRITICAL.value:
        recommendation = (
            "Avoid or defer the planned activity in this zone "
            "until conditions are reassessed."
        )

    elif risk_level == RiskLevel.HIGH.value:
        recommendation = (
            "Exercise strong caution and consider postponing "
            "or selecting a lower-risk zone."
        )

    elif risk_level == RiskLevel.MODERATE.value:
        recommendation = (
            "Proceed only with appropriate operational caution "
            "and reassess conditions before activity."
        )

    elif risk_level == RiskLevel.LOW.value:
        recommendation = (
            "No major risk signal was identified from the "
            "supplied environmental evidence."
        )

    else:
        recommendation = (
            "A reliable recommendation cannot be established "
            "because the available environmental evidence is insufficient."
        )

    if failed_domains:
        recommendation += (
            f" Assessment limitation: "
            f"{', '.join(failed_domains)} data is unavailable "
            f"or incomplete."
        )

    return recommendation


def _calculate_confidence(
    risk_result: Optional[Dict[str, Any]],
) -> Optional[float]:
    """
    Preserve confidence supplied by the Risk Agent.

    No new statistical confidence is fabricated here.
    """

    if not isinstance(risk_result, dict):
        return None

    confidence = _safe_float(
        risk_result.get("confidence")
    )

    if confidence is None:
        return None

    return round(
        max(0.0, min(1.0, confidence)),
        2,
    )


def _build_data_quality_summary(
    weather_result: Optional[Dict[str, Any]],
    ocean_result: Optional[Dict[str, Any]],
    ecosystem_result: Optional[Dict[str, Any]],
    risk_result: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Summarize data quality without inventing values.
    """

    components = {
        "weather": weather_result,
        "ocean": ocean_result,
        "ecosystem": ecosystem_result,
        "risk": risk_result,
    }

    summary: Dict[str, Any] = {}

    for domain, result in components.items():
        if not isinstance(result, dict):
            summary[domain] = {
                "status": "missing",
                "data_completeness": 0.0,
            }
            continue

        item: Dict[str, Any] = {
            "status": _get_component_status(result),
        }

        completeness = _safe_float(
            result.get("data_completeness")
        )

        if completeness is not None:
            item["data_completeness"] = round(
                max(0.0, min(1.0, completeness)),
                2,
            )

        missing = result.get(
            "missing_variables"
        )

        if isinstance(missing, list):
            item["missing_variables"] = [
                str(value)
                for value in missing
                if value is not None
            ]

        summary[domain] = item

    return summary


def analyze_decision(
    zone_id: Optional[str],
    weather_result: Optional[Dict[str, Any]],
    ocean_result: Optional[Dict[str, Any]],
    ecosystem_result: Optional[Dict[str, Any]],
    risk_result: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Produce the final decision for one zone.
    """

    risk_level = _risk_level(risk_result)

    reasons = _build_key_reasons(
        risk_result
    )

    failed_domains: List[str] = []

    if isinstance(risk_result, dict):
        supplied_failed = risk_result.get(
            "failed_domains",
            [],
        )

        if isinstance(supplied_failed, list):
            failed_domains = [
                str(domain)
                for domain in supplied_failed
                if domain is not None
            ]

    recommendation = _build_recommendation(
        risk_level=risk_level,
        failed_domains=failed_domains,
    )

    confidence = _calculate_confidence(
        risk_result
    )

    evidence = _build_evidence(
        weather_result=weather_result,
        ocean_result=ocean_result,
        ecosystem_result=ecosystem_result,
        risk_result=risk_result,
    )

    limitations = _get_limitations(
        risk_result
    )

    # Add domain-level status limitations.
    for domain, result in {
        "weather": weather_result,
        "ocean": ocean_result,
        "ecosystem": ecosystem_result,
    }.items():

        status = _get_component_status(result)

        if status in {
            "missing",
            "unavailable",
            "error",
        }:
            message = (
                f"{domain.capitalize()} data status is {status}."
            )

            if message not in limitations:
                limitations.append(message)

    component_summaries: Dict[str, str] = {}

    for domain, result in {
        "weather": weather_result,
        "ocean": ocean_result,
        "ecosystem": ecosystem_result,
    }.items():

        summary = _get_component_summary(result)

        if summary:
            component_summaries[domain] = summary

    decision: Dict[str, Any] = {
        "zoneId": zone_id,
        "risk_level": risk_level,
        "recommendation": recommendation,
        "key_reasons": reasons,
        "confidence": confidence,
        "evidence": evidence,
        "limitations": limitations,
        "component_summaries": component_summaries,
        "data_quality": _build_data_quality_summary(
            weather_result=weather_result,
            ocean_result=ocean_result,
            ecosystem_result=ecosystem_result,
            risk_result=risk_result,
        ),
    }

    return decision


def compare_zone_decisions(
    decisions: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Create a deterministic comparison of zone decisions.

    Zones are identified only through zoneId.
    """

    comparison: List[Dict[str, Any]] = []

    for decision in decisions:
        if not isinstance(decision, dict):
            continue

        zone_id = decision.get("zoneId")

        if zone_id is None:
            continue

        risk_level = str(
            decision.get(
                "risk_level",
                RiskLevel.UNKNOWN.value,
            )
        ).lower()

        comparison.append(
            {
                "zoneId": zone_id,
                "risk_level": risk_level,
                "risk_rank": RISK_ORDER.get(
                    risk_level,
                    -1,
                ),
                "recommendation": decision.get(
                    "recommendation"
                ),
                "confidence": decision.get(
                    "confidence"
                ),
            }
        )

    comparison.sort(
        key=lambda item: (
            item["risk_rank"] == -1,
            item["risk_rank"],
            -(
                _safe_float(
                    item.get("confidence")
                )
                or 0.0
            ),
        )
    )

    return comparison


def decision_agent(
    zone: Dict[str, Any],
    weather_result: Optional[Dict[str, Any]],
    ocean_result: Optional[Dict[str, Any]],
    ecosystem_result: Optional[Dict[str, Any]],
    risk_result: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Zone-aware Decision Agent entry point.
    """

    if not isinstance(zone, dict):
        return {
            "zoneId": None,
            "risk_level": RiskLevel.UNKNOWN.value,
            "recommendation": (
                "A decision cannot be produced because "
                "the supplied zone is invalid."
            ),
            "key_reasons": [],
            "confidence": 0.0,
            "evidence": [],
            "limitations": [
                "Invalid zone supplied to Decision Agent."
            ],
            "component_summaries": {},
            "data_quality": {},
        }

    zone_id = zone.get("zoneId")

    return analyze_decision(
        zone_id=zone_id,
        weather_result=weather_result,
        ocean_result=ocean_result,
        ecosystem_result=ecosystem_result,
        risk_result=risk_result,
    )
