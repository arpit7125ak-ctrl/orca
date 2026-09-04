from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

from utils.helpers import build_error


class OceanService:
    """
    Adapter for ocean / marine data providers.

    Provider-specific API calls stay inside this service.
    Agents should only receive normalized marine evidence.

    No marine values are fabricated when a provider does not
    return a variable.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
    ):
        self.base_url = (
            base_url
            or os.getenv("OCEAN_API_URL", "")
        )

        self.timeout = timeout or int(
            os.getenv("OCEAN_API_TIMEOUT", "15")
        )

    # ========================================================
    # PUBLIC INTERFACE
    # ========================================================

    def get_ocean(
        self,
        latitude: float,
        longitude: float,
        planned_datetime: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve marine information for a coordinate.

        If no ocean provider has been configured, the service
        explicitly reports the data as unavailable.

        It never invents wave, current, tide, SST, or sea-state
        values.
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
                    component="ocean_service",
                    message=(
                        "No ocean data provider configured. "
                        "Set OCEAN_API_URL in the environment."
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
                    component="ocean_service",
                    message="Ocean provider request timed out",
                    error_type="timeout",
                ),
            }

        except requests.RequestException as exc:
            return {
                "success": False,
                "data": None,
                "error": build_error(
                    component="ocean_service",
                    message=f"Ocean provider request failed: {exc}",
                    error_type="service",
                ),
            }

        except ValueError as exc:
            return {
                "success": False,
                "data": None,
                "error": build_error(
                    component="ocean_service",
                    message=(
                        f"Invalid ocean provider response: {exc}"
                    ),
                    error_type="data",
                ),
            }

        except Exception as exc:
            return {
                "success": False,
                "data": None,
                "error": build_error(
                    component="ocean_service",
                    message=(
                        f"Unexpected ocean service error: {exc}"
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
        Build generic marine-provider request parameters.

        The exact parameters can be adapted to the agreed
        ocean provider without changing the agent layer.
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
        Normalize the provider response.

        The method preserves only values actually present in
        the provider response.
        """

        variables = self._extract_variables(raw_data)

        return {
            "source": (
                raw_data.get("source")
                or raw_data.get("provider")
                or "configured_ocean_provider"
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
    # MARINE VARIABLES
    # ========================================================

    def _extract_variables(
        self,
        raw_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Extract known marine variables if they exist.

        Missing variables are not replaced with estimated values.
        """

        possible_variables = [
            "wave_height",
            "wave_period",
            "wave_direction",
            "current_speed",
            "current_direction",
            "tide_height",
            "tide",
            "sea_surface_temperature",
            "sst",
            "sea_state",
            "depth",
        ]

        variables: Dict[str, Any] = {}

        # Check top-level response.
        for variable in possible_variables:
            if variable in raw_data:
                variables[variable] = raw_data[variable]

        # Also support providers that place variables inside
        # a "marine", "ocean", or "data" object.
        for container_name in (
            "marine",
            "ocean",
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
        Preserve useful provider metadata without interpreting it.
        """

        metadata: Dict[str, Any] = {}

        allowed_metadata = [
            "provider",
            "source",
            "model",
            "model_run",
            "forecast",
            "observation",
            "units",
            "timezone",
        ]

        for key in allowed_metadata:
            if key in raw_data:
                metadata[key] = raw_data[key]

        return metadata


# ============================================================
# DEFAULT SERVICE INSTANCE
# ============================================================

ocean_service = OceanService()


# ============================================================
# FUNCTION INTERFACE
# ============================================================

def get_ocean(
    latitude: float,
    longitude: float,
    planned_datetime: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Convenience function used by tools/agents.
    """

    return ocean_service.get_ocean(
        latitude=latitude,
        longitude=longitude,
        planned_datetime=planned_datetime,
    )