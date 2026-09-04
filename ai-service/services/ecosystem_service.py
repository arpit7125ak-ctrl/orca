from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

from utils.helpers import build_error


class EcosystemService:
    """
    Adapter for ecosystem and environmental data providers.

    Provider-specific implementation remains inside this service.
    The ecosystem agent is responsible only for interpretation.

    Missing ecosystem information is explicitly represented as
    unavailable. No ecological values are fabricated.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
    ):
        self.base_url = (
            base_url
            or os.getenv("ECOSYSTEM_API_URL", "")
        )

        self.timeout = timeout or int(
            os.getenv("ECOSYSTEM_API_TIMEOUT", "15")
        )

    # ========================================================
    # PUBLIC INTERFACE
    # ========================================================

    def get_ecosystem(
        self,
        latitude: float,
        longitude: float,
        planned_datetime: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve ecosystem/environmental information for a zone.

        If no provider is configured, explicitly return unavailable.
        """

        if not self.base_url:
            return {
                "success": False,
                "data": {
                    "source": None,
                    "status": "unavailable",
                    "latitude": latitude,
                    "longitude": longitude,
                    "planned_datetime": planned_datetime,
                    "variables": {},
                },
                "error": build_error(
                    component="ecosystem_service",
                    message=(
                        "No ecosystem data provider configured. "
                        "Set ECOSYSTEM_API_URL in the environment."
                    ),
                    error_type="service",
                ),
            }

        params = self._build_params(
            latitude=latitude,
            longitude=longitude,
            planned_datetime=planned_datetime,
        )

        try:
            response = requests.get(
                self.base_url,
                params=params,
                timeout=self.timeout,
            )

            response.raise_for_status()

            raw_data = response.json()

            normalized = self._normalize_response(
                raw_data=raw_data,
                latitude=latitude,
                longitude=longitude,
                planned_datetime=planned_datetime,
            )

            return {
                "success": True,
                "data": normalized,
                "error": None,
            }

        except requests.Timeout:
            return {
                "success": False,
                "data": None,
                "error": build_error(
                    component="ecosystem_service",
                    message="Ecosystem provider request timed out",
                    error_type="timeout",
                ),
            }

        except requests.RequestException as exc:
            return {
                "success": False,
                "data": None,
                "error": build_error(
                    component="ecosystem_service",
                    message=(
                        f"Ecosystem provider request failed: {exc}"
                    ),
                    error_type="service",
                ),
            }

        except ValueError as exc:
            return {
                "success": False,
                "data": None,
                "error": build_error(
                    component="ecosystem_service",
                    message=(
                        f"Invalid ecosystem provider response: {exc}"
                    ),
                    error_type="data",
                ),
            }

        except Exception as exc:
            return {
                "success": False,
                "data": None,
                "error": build_error(
                    component="ecosystem_service",
                    message=(
                        f"Unexpected ecosystem service error: {exc}"
                    ),
                    error_type="unknown",
                ),
            }

    # ========================================================
    # REQUEST PARAMETERS
    # ========================================================

    def _build_params(
        self,
        latitude: float,
        longitude: float,
        planned_datetime: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Build generic ecosystem-provider parameters.

        The exact provider-specific parameters can be changed
        here without modifying agents or graph logic.
        """

        params: Dict[str, Any] = {
            "latitude": latitude,
            "longitude": longitude,
        }

        if planned_datetime:
            params["datetime"] = planned_datetime

        return params

    # ========================================================
    # RESPONSE NORMALIZATION
    # ========================================================

    def _normalize_response(
        self,
        raw_data: Dict[str, Any],
        latitude: float,
        longitude: float,
        planned_datetime: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Normalize ecosystem-provider output.

        Only supplied provider values are retained.
        """

        variables = self._extract_variables(raw_data)

        return {
            "source": (
                raw_data.get("source")
                or raw_data.get("provider")
                or "configured_ecosystem_provider"
            ),
            "status": "available",
            "latitude": latitude,
            "longitude": longitude,
            "planned_datetime": planned_datetime,
            "timestamp": raw_data.get("timestamp"),
            "variables": variables,
            "raw_metadata": self._extract_metadata(raw_data),
        }

    # ========================================================
    # ECOSYSTEM VARIABLES
    # ========================================================

    def _extract_variables(
        self,
        raw_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Extract known ecosystem/environmental variables.

        No missing variable is replaced with a guessed value.
        """

        possible_variables = [
            "ecosystem_condition",
            "sensitivity",
            "biodiversity",
            "biodiversity_index",
            "chlorophyll",
            "chlorophyll_a",
            "productivity",
            "primary_productivity",
            "habitat",
            "habitat_type",
            "protected_area",
            "protected_area_status",
            "sensitive_area",
            "ecological_constraint",
            "ecological_constraints",
        ]

        variables: Dict[str, Any] = {}

        # ----------------------------------------------------
        # Top-level provider fields
        # ----------------------------------------------------

        for variable in possible_variables:
            if variable in raw_data:
                variables[variable] = raw_data[variable]

        # ----------------------------------------------------
        # Nested provider fields
        # ----------------------------------------------------

        for container_name in (
            "ecosystem",
            "environment",
            "ecology",
            "data",
        ):
            container = raw_data.get(container_name)

            if not isinstance(container, dict):
                continue

            for variable in possible_variables:
                if variable in container:
                    variables[variable] = container[variable]

        return variables

    # ========================================================
    # METADATA
    # ========================================================

    def _extract_metadata(
        self,
        raw_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Preserve provider metadata required for provenance.
        """

        metadata: Dict[str, Any] = {}

        allowed_metadata = [
            "provider",
            "source",
            "dataset",
            "dataset_version",
            "model",
            "model_run",
            "forecast",
            "observation",
            "units",
            "timezone",
            "resolution",
        ]

        for key in allowed_metadata:
            if key in raw_data:
                metadata[key] = raw_data[key]

        return metadata


# ============================================================
# DEFAULT SERVICE INSTANCE
# ============================================================

ecosystem_service = EcosystemService()


# ============================================================
# FUNCTION INTERFACE
# ============================================================

def get_ecosystem(
    latitude: float,
    longitude: float,
    planned_datetime: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Convenience function used by tools/agents.
    """

    return ecosystem_service.get_ecosystem(
        latitude=latitude,
        longitude=longitude,
        planned_datetime=planned_datetime,
    )