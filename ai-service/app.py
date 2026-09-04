from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from pydantic import ValidationError

from graph.workflow import run_analysis
from models.schemas import AnalysisRequest, AnalysisResponse


app = FastAPI(
    title="ORCA AI Service",
    description="Agentic AI service for ORCA Marine Intelligence",
    version="1.0.0",
)


@app.get("/health")
def health_check() -> Dict[str, Any]:
    """
    Health check endpoint.
    """
    return {
        "status": "ok",
        "service": "ORCA AI-Service",
    }


@app.post("/analyze", response_model=AnalysisResponse)
def analyze(request: AnalysisRequest) -> AnalysisResponse:
    """
    Run the complete ORCA marine intelligence workflow.

    Flow:
        Weather
          ↓
        Ocean
          ↓
        Ecosystem
          ↓
        Risk
          ↓
        Decision
    """

    try:
        request_data = request.model_dump(by_alias=True)

        result = run_analysis(request_data)

        if not isinstance(result, dict):
            raise HTTPException(
                status_code=500,
                detail="AI workflow returned an invalid response.",
            )

        response_data = {
            "analysisId": result.get(
                "analysis_id",
                request.analysisId,
            ),
            "success": result.get("success", False),
            "zones": result.get("zone_results", {}),
            "decision": result.get("decision"),
            "errors": result.get("errors", []),
            "data_quality": {
                "partial": result.get("partial", False),
                "zone_count": len(result.get("zones", [])),
                "successful_zone_count": sum(
                    1
                    for zone_result in result.get("zone_results", {}).values()
                    if isinstance(zone_result, dict)
                    and not zone_result.get("partial", False)
                ),
            },
        }

        try:
            return AnalysisResponse.model_validate(response_data)

        except ValidationError as exc:
            raise HTTPException(
                status_code=500,
                detail={
                    "message": "AI workflow produced a response that failed schema validation.",
                    "errors": exc.errors(),
                },
            ) from exc

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "AI analysis failed.",
                "error": str(exc),
            },
        ) from exc


@app.get("/")
def root() -> Dict[str, str]:
    """
    Basic service information.
    """
    return {
        "service": "ORCA AI-Service",
        "status": "running",
        "docs": "/docs",
    }