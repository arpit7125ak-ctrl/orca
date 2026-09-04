const config = require("../config/config");
const { badRequest, AppError } = require("../utils/errors");

const getEcosystemData = async ({
  latitude,
  longitude,
  date,
}) => {
  // ==========================================
  // VALIDATE COORDINATES
  // ==========================================

  if (
    typeof latitude !== "number" ||
    typeof longitude !== "number" ||
    !Number.isFinite(latitude) ||
    !Number.isFinite(longitude)
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

  if (!config.services.ecosystem.url) {
    return {
      status: "unavailable",
      data: null,
      reason: "Ecosystem API is not configured",
    };
  }

  // ==========================================
  // BUILD URL
  // ==========================================

  const baseUrl = config.services.ecosystem.url.replace(
    /\/+$/,
    ""
  );

  const url = new URL(
    `${baseUrl}/api/ecosystem`
  );

  url.searchParams.set(
    "latitude",
    String(latitude)
  );

  url.searchParams.set(
    "longitude",
    String(longitude)
  );

  if (date) {
    url.searchParams.set(
      "date",
      String(date)
    );
  }

  // ==========================================
  // CREATE TIMEOUT
  // ==========================================

  const controller = new AbortController();

  const timeout = setTimeout(() => {
    controller.abort();
  }, config.request.timeoutMs);

  try {
    console.log(
      `[ECOSYSTEM] Requesting: ${url.toString()}`
    );

    // ==========================================
    // CALL ECOSYSTEM API
    // ==========================================

    const response = await fetch(url, {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
      signal: controller.signal,
    });

    console.log(
      `[ECOSYSTEM] HTTP status: ${response.status}`
    );

    // ==========================================
    // HANDLE HTTP ERROR
    // ==========================================

    if (!response.ok) {
      const errorText = await response.text();

      throw new AppError(
        `Ecosystem API returned HTTP ${response.status}`,
        502,
        {
          service: "ecosystem",
          upstreamStatus: response.status,
          details: errorText,
        }
      );
    }

    // ==========================================
    // PARSE JSON
    // ==========================================

    const data = await response.json();

    // ==========================================
    // RETURN RESULT
    // ==========================================

    return {
      status: "available",
      data,
      source: url.toString(),
      retrievedAt: new Date().toISOString(),
    };
  } catch (error) {
    // ==========================================
    // TIMEOUT
    // ==========================================

    if (error.name === "AbortError") {
      throw new AppError(
        "Ecosystem API request timed out",
        504,
        {
          service: "ecosystem",
          url: url.toString(),
          timeoutMs: config.request.timeoutMs,
        }
      );
    }

    // ==========================================
    // OUR APPLICATION ERROR
    // ==========================================

    if (error instanceof AppError) {
      throw error;
    }

    // ==========================================
    // NETWORK ERROR
    // ==========================================

    throw new AppError(
      "Unable to connect to Ecosystem API",
      502,
      {
        service: "ecosystem",
        url: url.toString(),
        reason: error.message,
        cause: error.cause
          ? {
              code: error.cause.code || null,
              message: error.cause.message || null,
            }
          : null,
      }
    );
  } finally {
    clearTimeout(timeout);
  }
};

module.exports = {
  getEcosystemData,
};