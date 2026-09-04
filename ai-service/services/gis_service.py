from __future__ import annotations

import math
import os
from typing import Any, Dict, List, Optional, Tuple

import requests

from utils.helpers import build_error


class GISService:
    """
    Adapter for GIS / spatial operations.

    This service handles spatial information such as:
    - distance between coordinates
    - zone relationships
    - optional external GIS provider data

    No environmental or GIS values are fabricated.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
    ):
        self.base_url = (
            base_url
            or os.getenv("GIS_API_URL", "")
        )

        self.timeout = timeout or int(
            os.getenv("GIS_API_TIMEOUT", "15")
        )

    # ========================================================
    # DISTANCE
    # ========================================================

    def calculate_distance(
        self,
        latitude_1: float,
        longitude_1: float,
        latitude_2: float,
        longitude_2: float,
    ) -> Dict[str, Any]:
        """
        Calculate great-circle distance between two coordinates.

        Returns distance in kilometres and nautical miles.
        """

        try:
            distance_km = self._haversine_distance(
                latitude_1,
                longitude_1,
                latitude_2,
                longitude_2,
            )

            distance_nm = distance_km / 1.852

            return {
                "success": True,
                "source": "internal_haversine",
                "distance_km": round(distance_km, 3),
                "distance_nm": round(distance_nm, 3),
                "error": None,
            }

        except Exception as exc:
            return {
                "success": False,
                "distance_km": None,
                "distance_nm": None,
                "error": build_error(
                    component="gis_service",
                    message=f"Distance calculation failed: {exc}",
                    error_type="data",
                ),
            }

    # ========================================================
    # ZONE DISTANCES
    # ========================================================

    def calculate_zone_distances(
        self,
        zones: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Calculate pairwise distances between zones.

        Zone identity is always based on zoneId.
        """

        results: List[Dict[str, Any]] = []

        try:
            for i, zone_a in enumerate(zones):
                zone_a_id = zone_a.get("zoneId")

                if not zone_a_id:
                    raise ValueError(
                        "Every zone must contain zoneId"
                    )

                latitude_a = zone_a.get("latitude")
                longitude_a = zone_a.get("longitude")

                if latitude_a is None or longitude_a is None:
                    continue

                for zone_b in zones[i + 1:]:
                    zone_b_id = zone_b.get("zoneId")

                    if not zone_b_id:
                        raise ValueError(
                            "Every zone must contain zoneId"
                        )

                    latitude_b = zone_b.get("latitude")
                    longitude_b = zone_b.get("longitude")

                    if latitude_b is None or longitude_b is None:
                        continue

                    distance = self.calculate_distance(
                        latitude_1=float(latitude_a),
                        longitude_1=float(longitude_a),
                        latitude_2=float(latitude_b),
                        longitude_2=float(longitude_b),
                    )

                    if not distance["success"]:
                        continue

                    results.append(
                        {
                            "zoneId": zone_a_id,
                            "compared_with": zone_b_id,
                            "distance_km": distance[
                                "distance_km"
                            ],
                            "distance_nm": distance[
                                "distance_nm"
                            ],
                            "source": distance["source"],
                        }
                    )

            return {
                "success": True,
                "pairs": results,
                "error": None,
            }

        except Exception as exc:
            return {
                "success": False,
                "pairs": [],
                "error": build_error(
                    component="gis_service",
                    message=(
                        f"Zone distance calculation failed: {exc}"
                    ),
                    error_type="data",
                ),
            }

    # ========================================================
    # EXTERNAL GIS DATA
    # ========================================================

    def get_spatial_data(
        self,
        latitude: float,
        longitude: float,
        zone_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve optional spatial data from a configured GIS
        provider.

        If no GIS API is configured, explicitly return unavailable.
        """

        if not self.base_url:
            return {
                "success": False,
                "data": {
                    "zoneId": zone_id,
                    "latitude": latitude,
                    "longitude": longitude,
                    "status": "unavailable",
                    "source": None,
                    "variables": {},
                },
                "error": build_error(
                    component="gis_service",
                    message=(
                        "No GIS data provider configured. "
                        "Set GIS_API_URL in the environment."
                    ),
                    error_type="service",
                    zone_id=zone_id,
                ),
            }

        params = {
            "latitude": latitude,
            "longitude": longitude,
        }

        if zone_id:
            params["zoneId"] = zone_id

        try:
            response = requests.get(
                self.base_url,
                params=params,
                timeout=self.timeout,
            )

            response.raise_for_status()

            raw_data = response.json()

            return {
                "success": True,
                "data": self._normalize_spatial_response(
                    raw_data=raw_data,
                    latitude=latitude,
                    longitude=longitude,
                    zone_id=zone_id,
                ),
                "error": None,
            }

        except requests.Timeout:
            return {
                "success": False,
                "data": None,
                "error": build_error(
                    component="gis_service",
                    message="GIS provider request timed out",
                    error_type="timeout",
                    zone_id=zone_id,
                ),
            }

        except requests.RequestException as exc:
            return {
                "success": False,
                "data": None,
                "error": build_error(
                    component="gis_service",
                    message=f"GIS provider request failed: {exc}",
                    error_type="service",
                    zone_id=zone_id,
                ),
            }

        except ValueError as exc:
            return {
                "success": False,
                "data": None,
                "error": build_error(
                    component="gis_service",
                    message=f"Invalid GIS provider response: {exc}",
                    error_type="data",
                    zone_id=zone_id,
                ),
            }

        except Exception as exc:
            return {
                "success": False,
                "data": None,
                "error": build_error(
                    component="gis_service",
                    message=f"Unexpected GIS service error: {exc}",
                    error_type="unknown",
                    zone_id=zone_id,
                ),
            }

    # ========================================================
    # HAVERSINE
    # ========================================================

    @staticmethod
    def _haversine_distance(
        latitude_1: float,
        longitude_1: float,
        latitude_2: float,
        longitude_2: float,
    ) -> float:
        """
        Calculate great-circle distance in kilometres.
        """

        earth_radius_km = 6371.0088

        lat1 = math.radians(latitude_1)
        lat2 = math.radians(latitude_2)

        delta_lat = math.radians(
            latitude_2 - latitude_1
        )

        delta_lon = math.radians(
            longitude_2 - longitude_1
        )

        a = (
            math.sin(delta_lat / 2) ** 2
            + math.cos(lat1)
            * math.cos(lat2)
            * math.sin(delta_lon / 2) ** 2
        )

        a = min(1.0, max(0.0, a))

        c = 2 * math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a),
        )

        return earth_radius_km * c

    # ========================================================
    # RESPONSE NORMALIZATION
    # ========================================================

    def _normalize_spatial_response(
        self,
        raw_data: Dict[str, Any],
        latitude: float,
        longitude: float,
        zone_id: Optional[str],
    ) -> Dict[str, Any]:
        """
        Normalize GIS provider output without inventing
        spatial information.
        """

        variables = {}

        possible_variables = [
            "classification",
            "distance_to_coast",
            "distance_to_port",
            "distance_to_habitat",
            "protected_area",
            "protected_area_status",
            "sensitive_area",
            "marine_zone",
            "bathymetry",
            "depth",
            "geometry",
            "intersections",
        ]

        for variable in possible_variables:
            if variable in raw_data:
                variables[variable] = raw_data[variable]

        for container_name in (
            "gis",
            "spatial",
            "data",
        ):
            container = raw_data.get(container_name)

            if not isinstance(container, dict):
                continue

            for variable in possible_variables:
                if variable in container:
                    variables[variable] = container[variable]

        return {
            "zoneId": zone_id,
            "latitude": latitude,
            "longitude": longitude,
            "status": "available",
            "source": (
                raw_data.get("source")
                or raw_data.get("provider")
                or "configured_gis_provider"
            ),
            "timestamp": raw_data.get("timestamp"),
            "variables": variables,
        }


# ============================================================
# DEFAULT SERVICE INSTANCE
# ============================================================

gis_service = GISService()


# ============================================================
# FUNCTION INTERFACE
# ============================================================

def calculate_distance(
    latitude_1: float,
    longitude_1: float,
    latitude_2: float,
    longitude_2: float,
) -> Dict[str, Any]:
    """
    Convenience function for distance calculation.
    """

    return gis_service.calculate_distance(
        latitude_1=latitude_1,
        longitude_1=longitude_1,
        latitude_2=latitude_2,
        longitude_2=longitude_2,
    )


def calculate_zone_distances(
    zones: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Convenience function for pairwise zone distances.
    """

    return gis_service.calculate_zone_distances(zones)


def get_spatial_data(
    latitude: float,
    longitude: float,
    zone_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Convenience function for external GIS data.
    """

    return gis_service.get_spatial_data(
        latitude=latitude,
        longitude=longitude,
        zone_id=zone_id,
    )