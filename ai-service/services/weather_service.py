from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

from utils.helpers import (
    build_error,
    remove_none_values,
)


class WeatherService:
    """
    Adapter for weather-data providers.

    Provider-specific implementation stays inside this service.
    Agents should not directly call external weather APIs.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
    ):
        self.base_url = (
            base_url
            or os.getenv(
                "WEATHER_API_URL",
                "https://api.open-meteo.com/v1/forecast",
            )
        )

        self.timeout = timeout or int(
            os.getenv("WEATHER_API_TIMEOUT", "15")
        )

    # ========================================================
    # PUBLIC INTERFACE
    # ========================================================

    def get_weather(
        self,
        latitude: float,
        longitude: float,
        planned_datetime: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve weather information for a coordinate.

        The service returns only values supplied by the provider.
        No environmental values are generated here.
        """

        params = self._build_params(
            latitude=latitude,
            longitude=longitude,
        )

        try:
            response = requests.get(
                self.base_url,
                params=params,
                timeout=self.timeout,
            )

            response.raise_for_status()

            raw_data = response.json()

            return self._normalize_response(
                raw_data=raw_data,
                latitude=latitude,
                longitude=longitude,
                planned_datetime=planned_datetime,
            )

        except requests.Timeout:
            return {
                "success": False,
                "data": None,
                "error": build_error(
                    component="weather_service",
                    message="Weather provider request timed out",
                    error_type="timeout",
                ),
            }

        except requests.RequestException as exc:
            return {
                "success": False,
                "data": None,
                "error": build_error(
                    component="weather_service",
                    message=f"Weather provider request failed: {exc}",
                    error_type="service",
                ),
            }

        except ValueError as exc:
            return {
                "success": False,
                "data": None,
                "error": build_error(
                    component="weather_service",
                    message=f"Invalid weather provider response: {exc}",
                    error_type="data",
                ),
            }

        except Exception as exc:
            return {
                "success": False,
                "data": None,
                "error": build_error(
                    component="weather_service",
                    message=f"Unexpected weather service error: {exc}",
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
    ) -> Dict[str, Any]:
        """
        Build Open-Meteo request parameters.

        Only variables explicitly requested here are returned.
        """

        return {
            "latitude": latitude,
            "longitude": longitude,
            "current": ",".join(
                [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "apparent_temperature",
                    "precipitation",
                    "rain",
                    "weather_code",
                    "pressure_msl",
                    "surface_pressure",
                    "wind_speed_10m",
                    "wind_direction_10m",
                    "wind_gusts_10m",
                ]
            ),
            "hourly": ",".join(
                [
                    "temperature_2m",
                    "precipitation",
                    "rain",
                    "visibility",
                    "pressure_msl",
                    "wind_speed_10m",
                    "wind_direction_10m",
                    "wind_gusts_10m",
                ]
            ),
            "forecast_days": 10,
            "timezone": "UTC",
        }

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
        Normalize provider response while preserving the original
        environmental values.

        No missing values are replaced with guesses.
        """

        current = raw_data.get("current") or {}
        hourly = raw_data.get("hourly") or {}

        current_units = raw_data.get("current_units") or {}
        hourly_units = raw_data.get("hourly_units") or {}

        result = {
            "success": True,
            "source": "Open-Meteo",
            "provider": "open-meteo",
            "latitude": latitude,
            "longitude": longitude,
            "timezone": raw_data.get("timezone"),
            "elevation": raw_data.get("elevation"),
            "planned_datetime": planned_datetime,
            "current": self._extract_current(
                current=current,
                units=current_units,
            ),
            "hourly": self._extract_hourly(
                hourly=hourly,
                units=hourly_units,
            ),
        }

        return result

    # ========================================================
    # CURRENT DATA
    # ========================================================

    def _extract_current(
        self,
        current: Dict[str, Any],
        units: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Extract current weather variables exactly as supplied
        by the provider.
        """

        variables = [
            "time",
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "rain",
            "weather_code",
            "pressure_msl",
            "surface_pressure",
            "wind_speed_10m",
            "wind_direction_10m",
            "wind_gusts_10m",
        ]

        output: Dict[str, Any] = {}

        for variable in variables:
            if variable in current:
                output[variable] = {
                    "value": current[variable],
                    "unit": units.get(variable),
                }

        return output

    # ========================================================
    # HOURLY DATA
    # ========================================================

    def _extract_hourly(
        self,
        hourly: Dict[str, Any],
        units: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Extract hourly weather variables without modifying
        provider values.
        """

        variables = [
            "time",
            "temperature_2m",
            "precipitation",
            "rain",
            "visibility",
            "pressure_msl",
            "wind_speed_10m",
            "wind_direction_10m",
            "wind_gusts_10m",
        ]

        output: Dict[str, Any] = {}

        for variable in variables:
            if variable in hourly:
                output[variable] = {
                    "values": hourly[variable],
                    "unit": units.get(variable),
                }

        return output


# ============================================================
# DEFAULT SERVICE INSTANCE
# ============================================================

weather_service = WeatherService()


# ============================================================
# FUNCTION INTERFACE
# ============================================================

def get_weather(
    latitude: float,
    longitude: float,
    planned_datetime: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Convenience function used by tools/agents.
    """

    return weather_service.get_weather(
        latitude=latitude,
        longitude=longitude,
        planned_datetime=planned_datetime,
    )