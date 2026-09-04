from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ============================================================
# ENUMS
# ============================================================

class DataStatus(str, Enum):
    OBSERVED = "observed"
    FORECAST = "forecast"
    MISSING = "missing"
    UNAVAILABLE = "unavailable"
    STALE = "stale"
    LOW_QUALITY = "low_quality"
    ERROR = "error"


class QualityStatus(str, Enum):
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    POOR = "poor"
    UNKNOWN = "unknown"


class RiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class ErrorType(str, Enum):
    VALIDATION = "validation"
    SERVICE = "service"
    AGENT = "agent"
    DATA = "data"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"


# ============================================================
# PROVENANCE / EVIDENCE
# ============================================================

class Evidence(BaseModel):
    """
    Represents a supplied environmental observation/forecast.

    The AI must not create environmental evidence that was not
    supplied by the upstream service.
    """

    model_config = ConfigDict(extra="allow")

    variable: str = Field(..., min_length=1)
    value: Any = None
    unit: Optional[str] = None

    source: Optional[str] = None
    timestamp: Optional[datetime] = None

    status: DataStatus = DataStatus.OBSERVED
    quality: QualityStatus = QualityStatus.UNKNOWN

    forecast_lead_hours: Optional[float] = Field(
        default=None,
        ge=0
    )

    notes: Optional[str] = None


# ============================================================
# ZONE
# ============================================================

class Zone(BaseModel):
    """
    Stable identity for an analysis zone.

    zoneId is mandatory. Array position must never be used as
    zone identity.
    """

    model_config = ConfigDict(extra="allow")

    zoneId: str = Field(..., min_length=1)

    name: Optional[str] = None

    latitude: Optional[float] = Field(
        default=None,
        ge=-90,
        le=90
    )

    longitude: Optional[float] = Field(
        default=None,
        ge=-180,
        le=180
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)


# ============================================================
# REQUEST
# ============================================================

class AnalysisRequest(BaseModel):
    """
    Main AI-Service request.

    Every request uses zones[], even when there is only one zone.
    """

    model_config = ConfigDict(extra="allow")

    analysisId: str = Field(..., min_length=1)

    zones: List[Zone] = Field(..., min_length=1)

    planned_datetime: Optional[datetime] = None

    activity: Optional[str] = None

    user_input: Optional[str] = None

    context: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("zones")
    @classmethod
    def validate_unique_zone_ids(cls, zones: List[Zone]) -> List[Zone]:
        zone_ids = [zone.zoneId for zone in zones]

        if len(zone_ids) != len(set(zone_ids)):
            raise ValueError("zoneId values must be unique")

        return zones


# ============================================================
# WEATHER
# ============================================================

class WeatherAssessment(BaseModel):
    zoneId: str

    assessment: str

    evidence: List[Evidence] = Field(default_factory=list)

    factors: List[str] = Field(default_factory=list)

    limitations: List[str] = Field(default_factory=list)

    status: DataStatus = DataStatus.OBSERVED


# ============================================================
# OCEAN
# ============================================================

class OceanAssessment(BaseModel):
    zoneId: str

    assessment: str

    evidence: List[Evidence] = Field(default_factory=list)

    factors: List[str] = Field(default_factory=list)

    limitations: List[str] = Field(default_factory=list)

    status: DataStatus = DataStatus.OBSERVED


# ============================================================
# ECOSYSTEM
# ============================================================

class EcosystemAssessment(BaseModel):
    zoneId: str

    assessment: str

    evidence: List[Evidence] = Field(default_factory=list)

    factors: List[str] = Field(default_factory=list)

    limitations: List[str] = Field(default_factory=list)

    status: DataStatus = DataStatus.OBSERVED


# ============================================================
# RISK FACTOR
# ============================================================

class RiskFactor(BaseModel):
    """
    A traceable factor contributing to risk.

    factor must be linked to supplied evidence rather than
    invented environmental measurements.
    """

    name: str = Field(..., min_length=1)

    description: str

    level: RiskLevel = RiskLevel.UNKNOWN

    evidence_variables: List[str] = Field(default_factory=list)

    zoneId: str


# ============================================================
# RISK
# ============================================================

class RiskAssessment(BaseModel):
    zoneId: str

    level: RiskLevel = RiskLevel.UNKNOWN

    summary: str

    factors: List[RiskFactor] = Field(default_factory=list)

    evidence: List[Evidence] = Field(default_factory=list)

    confidence: Optional[float] = Field(
        default=None,
        ge=0,
        le=1
    )

    limitations: List[str] = Field(default_factory=list)


# ============================================================
# DECISION
# ============================================================

class ZoneDecision(BaseModel):
    zoneId: str

    recommendation: str

    key_reasons: List[str] = Field(default_factory=list)

    risk_level: RiskLevel = RiskLevel.UNKNOWN

    confidence: Optional[float] = Field(
        default=None,
        ge=0,
        le=1
    )

    evidence: List[Evidence] = Field(default_factory=list)

    limitations: List[str] = Field(default_factory=list)


class ZoneComparison(BaseModel):
    """
    Comparison between zones.

    Used only when multiple zones are supplied.
    """

    zoneId: str

    compared_with: List[str] = Field(default_factory=list)

    summary: str

    advantages: List[str] = Field(default_factory=list)

    concerns: List[str] = Field(default_factory=list)


class DecisionAssessment(BaseModel):
    recommendation: str

    key_reasons: List[str] = Field(default_factory=list)

    confidence: Optional[float] = Field(
        default=None,
        ge=0,
        le=1
    )

    zone_decisions: List[ZoneDecision] = Field(
        default_factory=list
    )

    comparisons: List[ZoneComparison] = Field(
        default_factory=list
    )

    evidence: List[Evidence] = Field(
        default_factory=list
    )

    limitations: List[str] = Field(
        default_factory=list
    )


# ============================================================
# ERRORS / PARTIAL FAILURE
# ============================================================

class ServiceError(BaseModel):
    """
    Explicit representation of a failed/unavailable component.

    A service failure must never result in fabricated data.
    """

    zoneId: Optional[str] = None

    component: str

    error_type: ErrorType

    message: str

    recoverable: bool = True

    timestamp: Optional[datetime] = None


# ============================================================
# ZONE RESULT
# ============================================================

class ZoneResult(BaseModel):
    """
    Complete result for one zone.

    Each result retains its zoneId throughout the workflow.
    """

    analysisId: str

    zoneId: str

    weather: Optional[WeatherAssessment] = None

    ocean: Optional[OceanAssessment] = None

    ecosystem: Optional[EcosystemAssessment] = None

    risk: Optional[RiskAssessment] = None

    decision: Optional[ZoneDecision] = None

    errors: List[ServiceError] = Field(
        default_factory=list
    )

    partial: bool = False


# ============================================================
# COMPLETE ANALYSIS RESPONSE
# ============================================================

class AnalysisResponse(BaseModel):
    """
    Final structured response returned by AI-Service.
    """

    analysisId: str

    success: bool

    zones: List[ZoneResult] = Field(
        default_factory=list
    )

    decision: Optional[DecisionAssessment] = None

    errors: List[ServiceError] = Field(
        default_factory=list
    )

    data_quality: List[str] = Field(
        default_factory=list
    )


# ============================================================
# CHAT
# ============================================================

class ChatRequest(BaseModel):
    conversation_id: str = Field(..., min_length=1)

    analysisId: str = Field(..., min_length=1)

    current_zone: Optional[str] = None

    user_question: str = Field(..., min_length=1)

    history: List[Dict[str, Any]] = Field(
        default_factory=list
    )


class ChatResponse(BaseModel):
    conversation_id: str

    analysisId: str

    current_zone: Optional[str] = None

    answer: str

    evidence: List[Evidence] = Field(
        default_factory=list
    )

    limitations: List[str] = Field(
        default_factory=list
    )

    errors: List[ServiceError] = Field(
        default_factory=list
    )


# ============================================================
# VALIDATION HELPERS
# ============================================================

def validate_zone_identity(
    analysis_id: str,
    zone_id: str,
    result: ZoneResult
) -> ZoneResult:
    """
    Ensures a ZoneResult cannot silently belong to another zone.
    """

    if result.analysisId != analysis_id:
        raise ValueError(
            "ZoneResult analysisId does not match request analysisId"
        )

    if result.zoneId != zone_id:
        raise ValueError(
            "ZoneResult zoneId does not match expected zoneId"
        )

    return result


def validate_zone_results(
    analysis_id: str,
    zones: List[Zone],
    results: List[ZoneResult]
) -> None:
    """
    Validate that every requested zone has exactly one result
    and that no unknown zone is introduced.
    """

    expected_ids = {zone.zoneId for zone in zones}
    result_ids = [result.zoneId for result in results]

    if len(result_ids) != len(set(result_ids)):
        raise ValueError(
            "Duplicate zoneId found in zone results"
        )

    actual_ids = set(result_ids)

    missing = expected_ids - actual_ids
    unexpected = actual_ids - expected_ids

    if missing:
        raise ValueError(
            f"Missing zone results: {sorted(missing)}"
        )

    if unexpected:
        raise ValueError(
            f"Unexpected zone results: {sorted(unexpected)}"
        )

    for result in results:
        if result.analysisId != analysis_id:
            raise ValueError(
                f"Invalid analysisId for zone {result.zoneId}"
            )

        