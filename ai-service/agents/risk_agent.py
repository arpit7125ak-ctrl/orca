"""
AI-Service/agents/risk_agent.py

Risk Agent

Responsibilities:
- Combine Weather, Ocean, and Ecosystem evidence.
- Identify risk factors from supplied agent outputs.
- Preserve zoneId.
- Keep every risk factor traceable to supplied evidence.
- Explicitly account for missing/failed components.
- Produce a structured risk assessment.

This agent must not:
- Invent environmental measurements.
- Invent sources or timestamps.
- Hide missing data.
- Make unsupported numerical claims.
- Replace the Decision Agent.
"""

from typing import Any, Dict, List, Optional

from models.schemas import (
    Evidence,
    RiskAssessment,
    RiskFactor,
    RiskLevel,
)


DOMAIN_NAMES = [
    "weather",
    "ocean",
    "ecosystem",
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


def _get_status(
    result: Optional[Dict[str, Any]],
) -> str:
    """
    Safely extract component status.
    """

    if not isinstance(result, dict):
        return "missing"

    return str(
        result.get("status", "unknown")
    ).lower()


def _get_evidence(
    result: Optional[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Safely extract evidence from an agent result.
    """

    if not isinstance(result, dict):
        return []

    evidence = result.get("evidence", [])

    if not isinstance(evidence, list):
        return []

    return [
        item
        for item in evidence
        if isinstance(item, dict)
    ]


def _get_missing_variables(
    result: Optional[Dict[str, Any]],
) -> List[str]:
    """
    Extract missing variables from a domain result.
    """

    if not isinstance(result, dict):
        return []

    missing = result.get(
        "missing_variables",
        [],
    )

    if not isinstance(missing, list):
        return []

    return [
        str(item)
        for item in missing
        if item is not None
    ]


def _build_factor(
    domain: str,
    variable: str,
    value: Any,
    reason: str,
    evidence: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Build a traceable risk factor.

    The factor contains the original variable/value rather
    than creating a new environmental measurement.
    """

    factor: Dict[str, Any] = {
        "domain": domain,
        "variable": variable,
        "value": value,
        "reason": reason,
    }

    if evidence:
        factor["source"] = evidence.get("source")
        factor["timestamp"] = evidence.get("timestamp")
        factor["unit"] = evidence.get("unit")
        factor["status"] = evidence.get("status")
        factor["quality"] = evidence.get("quality")

    return factor


def _find_evidence(
    result: Optional[Dict[str, Any]],
    variable_names: List[str],
) -> Optional[Dict[str, Any]]:
    """
    Find the first matching evidence item.
    """

    evidence = _get_evidence(result)

    for item in evidence:
        variable = item.get("variable")

        if variable in variable_names:
            return item

    return None


def _evaluate_weather(
    weather: Optional[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Identify weather-related risk factors.

    Thresholds are intentionally conservative and only operate
    when numerical values are actually supplied.
    """

    factors: List[Dict[str, Any]] = []

    if not isinstance(weather, dict):
        return factors

    wind_evidence = _find_evidence(
        weather,
        ["wind_speed_10m"],
    )

    if wind_evidence:
        value = _safe_float(
            wind_evidence.get("value")
        )

        if value is not None:
            if value >= 20:
                factors.append(
                    _build_factor(
                        domain="weather",
                        variable="wind_speed_10m",
                        value=value,
                        reason=(
                            "High supplied wind-speed "
                            "value may increase operational risk."
                        ),
                        evidence=wind_evidence,
                    )
                )
            elif value >= 12:
                factors.append(
                    _build_factor(
                        domain="weather",
                        variable="wind_speed_10m",
                        value=value,
                        reason=(
                            "Elevated supplied wind-speed "
                            "value may affect operations."
                        ),
                        evidence=wind_evidence,
                    )
                )

    gust_evidence = _find_evidence(
        weather,
        ["wind_gusts_10m"],
    )

    if gust_evidence:
        value = _safe_float(
            gust_evidence.get("value")
        )

        if value is not None and value >= 20:
            factors.append(
                _build_factor(
                    domain="weather",
                    variable="wind_gusts_10m",
                    value=value,
                    reason=(
                        "Elevated supplied wind gusts "
                        "may increase operational risk."
                    ),
                    evidence=gust_evidence,
                )
            )

    precipitation_evidence = _find_evidence(
        weather,
        ["precipitation"],
    )

    if precipitation_evidence:
        value = _safe_float(
            precipitation_evidence.get("value")
        )

        if value is not None and value > 10:
            factors.append(
                _build_factor(
                    domain="weather",
                    variable="precipitation",
                    value=value,
                    reason=(
                        "Supplied precipitation value "
                        "may reduce operational conditions."
                    ),
                    evidence=precipitation_evidence,
                )
            )

    visibility_evidence = _find_evidence(
        weather,
        ["visibility"],
    )

    if visibility_evidence:
        value = _safe_float(
            visibility_evidence.get("value")
        )

        if value is not None and value < 5000:
            factors.append(
                _build_factor(
                    domain="weather",
                    variable="visibility",
                    value=value,
                    reason=(
                        "Reduced supplied visibility "
                        "may increase operational risk."
                    ),
                    evidence=visibility_evidence,
                )
            )

    return factors


def _evaluate_ocean(
    ocean: Optional[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Identify ocean-related risk factors.

    Only supplied ocean measurements are evaluated.
    """

    factors: List[Dict[str, Any]] = []

    if not isinstance(ocean, dict):
        return factors

    wave_evidence = _find_evidence(
        ocean,
        ["wave_height"],
    )

    if wave_evidence:
        value = _safe_float(
            wave_evidence.get("value")
        )

        if value is not None:
            if value >= 3:
                factors.append(
                    _build_factor(
                        domain="ocean",
                        variable="wave_height",
                        value=value,
                        reason=(
                            "High supplied wave height "
                            "may increase marine operational risk."
                        ),
                        evidence=wave_evidence,
                    )
                )
            elif value >= 2:
                factors.append(
                    _build_factor(
                        domain="ocean",
                        variable="wave_height",
                        value=value,
                        reason=(
                            "Elevated supplied wave height "
                            "may affect marine operations."
                        ),
                        evidence=wave_evidence,
                    )
                )

    wave_period_evidence = _find_evidence(
        ocean,
        ["wave_period"],
    )

    if wave_period_evidence:
        value = _safe_float(
            wave_period_evidence.get("value")
        )

        if value is not None and value >= 12:
            factors.append(
                _build_factor(
                    domain="ocean",
                    variable="wave_period",
                    value=value,
                    reason=(
                        "Long supplied wave period can "
                        "contribute to significant wave energy."
                    ),
                    evidence=wave_period_evidence,
                )
            )

    current_evidence = _find_evidence(
        ocean,
        ["current_speed"],
    )

    if current_evidence:
        value = _safe_float(
            current_evidence.get("value")
        )

        if value is not None and value >= 1.5:
            factors.append(
                _build_factor(
                    domain="ocean",
                    variable="current_speed",
                    value=value,
                    reason=(
                        "Elevated supplied current speed "
                        "may affect marine operations."
                    ),
                    evidence=current_evidence,
                )
            )

    return factors


def _evaluate_ecosystem(
    ecosystem: Optional[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Identify ecological constraints.

    Qualitative ecosystem information is preserved as supplied.
    """

    factors: List[Dict[str, Any]] = []

    if not isinstance(ecosystem, dict):
        return factors

    sensitivity_evidence = _find_evidence(
        ecosystem,
        ["sensitivity"],
    )

    if sensitivity_evidence:
        value = sensitivity_evidence.get("value")

        if value is not None:
            text = str(value).lower()

            if text in {
                "high",
                "very high",
                "critical",
                "sensitive",
            }:
                factors.append(
                    _build_factor(
                        domain="ecosystem",
                        variable="sensitivity",
                        value=value,
                        reason=(
                            "Supplied ecosystem sensitivity "
                            "indicates an ecological constraint."
                        ),
                        evidence=sensitivity_evidence,
                    )
                )

    protected_evidence = _find_evidence(
        ecosystem,
        [
            "protected_area",
            "protected_area_status",
        ],
    )

    if protected_evidence:
        value = protected_evidence.get("value")

        if value is not None:
            text = str(value).lower()

            if text in {
                "true",
                "yes",
                "protected",
                "inside",
                "designated",
            }:
                factors.append(
                    _build_factor(
                        domain="ecosystem",
                        variable=(
                            protected_evidence.get(
                                "variable"
                            )
                            or "protected_area"
                        ),
                        value=value,
                        reason=(
                            "Supplied protected-area "
                            "information indicates an ecological constraint."
                        ),
                        evidence=protected_evidence,
                    )
                )

    sensitive_area_evidence = _find_evidence(
        ecosystem,
        ["sensitive_area"],
    )

    if sensitive_area_evidence:
        value = sensitive_area_evidence.get("value")

        if value is not None:
            text = str(value).lower()

            if text in {
                "true",
                "yes",
                "sensitive",
                "high",
                "critical",
            }:
                factors.append(
                    _build_factor(
                        domain="ecosystem",
                        variable="sensitive_area",
                        value=value,
                        reason=(
                            "Supplied sensitive-area "
                            "information indicates an ecological constraint."
                        ),
                        evidence=sensitive_area_evidence,
                    )
                )

    constraint_evidence = _find_evidence(
        ecosystem,
        [
            "ecological_constraint",
            "ecological_constraints",
        ],
    )

    if constraint_evidence:
        value = constraint_evidence.get("value")

        if value is not None:
            factors.append(
                _build_factor(
                    domain="ecosystem",
                    variable=(
                        constraint_evidence.get(
                            "variable"
                        )
                        or "ecological_constraint"
                    ),
                    value=value,
                    reason=(
                        "Supplied ecological constraint "
                        "information should be considered."
                    ),
                    evidence=constraint_evidence,
                )
            )

    return factors


def _determine_risk_level(
    factors: List[Dict[str, Any]],
    failed_domains: List[str],
) -> RiskLevel:
    """
    Determine a conservative qualitative risk level.

    This is a rule-based assessment, not a statistical model.
    """

    if not factors and failed_domains:
        return RiskLevel.UNKNOWN

    critical_keywords = {
        "critical",
        "very high",
    }

    high_count = 0

    for factor in factors:
        value = factor.get("value")

        if isinstance(value, str):
            if value.lower() in critical_keywords:
                return RiskLevel.CRITICAL

        variable = factor.get("variable")

        if variable in {
            "wave_height",
            "wind_speed_10m",
            "wind_gusts_10m",
        }:
            numeric_value = _safe_float(value)

            if variable == "wave_height" and (
                numeric_value is not None
                and numeric_value >= 3
            ):
                high_count += 1

            if variable in {
                "wind_speed_10m",
                "wind_gusts_10m",
            } and (
                numeric_value is not None
                and numeric_value >= 20
            ):
                high_count += 1

        if factor.get("domain") == "ecosystem":
            high_count += 1

    if high_count >= 3:
        return RiskLevel.CRITICAL

    if high_count >= 2:
        return RiskLevel.HIGH

    if len(factors) >= 2:
        return RiskLevel.MODERATE

    if len(factors) == 1:
        return RiskLevel.MODERATE

    return RiskLevel.LOW


def _calculate_confidence(
    weather: Optional[Dict[str, Any]],
    ocean: Optional[Dict[str, Any]],
    ecosystem: Optional[Dict[str, Any]],
) -> Optional[float]:
    """
    Calculate evidence completeness-based confidence.

    This does NOT represent statistical probability.
    """

    components = [
        weather,
        ocean,
        ecosystem,
    ]

    available = 0

    for component in components:
        if not isinstance(component, dict):
            continue

        completeness = _safe_float(
            component.get("data_completeness")
        )

        if completeness is not None:
            available += max(
                0.0,
                min(1.0, completeness),
            )

    if not components:
        return None

    return round(
        available / len(components),
        2,
    )


def _build_limitations(
    weather: Optional[Dict[str, Any]],
    ocean: Optional[Dict[str, Any]],
    ecosystem: Optional[Dict[str, Any]],
) -> List[str]:
    """
    Build explicit data-quality limitations.
    """

    limitations: List[str] = []

    components = {
        "weather": weather,
        "ocean": ocean,
        "ecosystem": ecosystem,
    }

    for domain, result in components.items():
        if not isinstance(result, dict):
            limitations.append(
                f"{domain} data is unavailable."
            )
            continue

        status = _get_status(result)

        if status in {
            "error",
            "unavailable",
            "missing",
        }:
            limitations.append(
                f"{domain} data is {status}."
            )

        missing = _get_missing_variables(
            result
        )

        if missing:
            limitations.append(
                f"{domain} is missing or unavailable "
                f"variables: {', '.join(missing)}."
            )

    return limitations


def analyze_risk(
    zone_id: Optional[str],
    weather_result: Optional[Dict[str, Any]],
    ocean_result: Optional[Dict[str, Any]],
    ecosystem_result: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Combine domain assessments for one zone.
    """

    weather_factors = _evaluate_weather(
        weather_result
    )

    ocean_factors = _evaluate_ocean(
        ocean_result
    )

    ecosystem_factors = _evaluate_ecosystem(
        ecosystem_result
    )

    factors = (
        weather_factors
        + ocean_factors
        + ecosystem_factors
    )

    failed_domains: List[str] = []

    for domain, result in {
        "weather": weather_result,
        "ocean": ocean_result,
        "ecosystem": ecosystem_result,
    }.items():
        status = _get_status(result)

        if status in {
            "error",
            "unavailable",
            "missing",
        }:
            failed_domains.append(domain)

    risk_level = _determine_risk_level(
        factors=factors,
        failed_domains=failed_domains,
    )

    confidence = _calculate_confidence(
        weather=weather_result,
        ocean=ocean_result,
        ecosystem=ecosystem_result,
    )

    limitations = _build_limitations(
        weather=weather_result,
        ocean=ocean_result,
        ecosystem=ecosystem_result,
    )

    return {
        "zoneId": zone_id,
        "risk_level": risk_level.value,
        "risk_factors": factors,
        "confidence": confidence,
        "failed_domains": failed_domains,
        "limitations": limitations,
        "summary": (
            f"Risk assessment for zone {zone_id or 'unknown'} "
            f"is {risk_level.value} based only on supplied evidence."
        ),
    }


def risk_agent(
    zone: Dict[str, Any],
    weather_result: Optional[Dict[str, Any]],
    ocean_result: Optional[Dict[str, Any]],
    ecosystem_result: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Zone-aware Risk Agent entry point.

    Stable zoneId is preserved and never inferred from
    array position.
    """

    if not isinstance(zone, dict):
        return {
            "zoneId": None,
            "risk_level": RiskLevel.UNKNOWN.value,
            "risk_factors": [],
            "confidence": 0.0,
            "failed_domains": DOMAIN_NAMES,
            "limitations": [
                "Invalid zone supplied to Risk Agent."
            ],
            "summary": "Risk assessment could not be performed.",
        }

    zone_id = zone.get("zoneId")

    return analyze_risk(
        zone_id=zone_id,
        weather_result=weather_result,
        ocean_result=ocean_result,
        ecosystem_result=ecosystem_result,
    )
