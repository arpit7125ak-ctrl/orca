const config = require("../config/config");
const { badRequest, AppError } = require("../utils/errors");

const getGISData = async ({
  latitude,
  longitude,
}) => {
  // ==========================================
  // VALIDATE COORDINATES
  // ==========================================

  if (
    typeof latitude !== "number" ||
    typeof longitude !== "number"
  ) {
    throw badRequest(
      "Valid latitude and longitude are required"
    );
  }

  if (latitude < -90 || latitude > 90) {
    throw badRequest(
      "Latitude must be between -90 and 90"
    );
  }

  if (longitude < -180 || longitude > 180) {
    throw badRequest(
      "Longitude must be between -180 and 180"
    );
  }

  // ==========================================
  // CHECK CONFIGURATION
  // ==========================================

  if (!config.services.gis.url) {
    return {
      status: "unavailable",
      data: null,
      reason: "GIS API is not configured",
    };
  }

  const controller = new AbortController();

  const timeout = setTimeout(() => {
    controller.abort();
  }, config.request.timeoutMs);

  try {
    // ==========================================
    // BUILD GET REQUEST
    // ==========================================

    const url = new URL(
      `${config.services.gis.url}/api/gis`
    );

    url.searchParams.set(
      "latitude",
      String(latitude)
    );

    url.searchParams.set(
      "longitude",
      String(longitude)
    );

    // ==========================================
    // CALL GIS API
    // ==========================================

    const response = await fetch(url, {
      method: "GET",

      headers: {
        Accept: "application/json",
      },

      signal: controller.signal,
    });

    if (!response.ok) {
      const errorText = await response.text();

      throw new AppError(
        `GIS API returned HTTP ${response.status}`,
        502,
        {
          service: "gis",
          upstreamStatus: response.status,
          details: errorText,
        }
      );
    }

    const data = await response.json();

    // ==========================================
    // RETURN GIS RESULT
    // ==========================================

    return {
      status: "available",

      data,

      source: `${config.services.gis.url}/api/gis`,

      retrievedAt: new Date().toISOString(),
    };
  } catch (error) {
    if (error.name === "AbortError") {
      throw new AppError(
        "GIS API request timed out",
        504,
        {
          service: "gis",
        }
      );
    }

    if (error instanceof AppError) {
      throw error;
    }

    throw new AppError(
      "Unable to connect to GIS API",
      502,
      {
        service: "gis",
        reason: error.message,
      }
    );
  } finally {
    clearTimeout(timeout);
  }
};

module.exports = {
  getGISData,
};