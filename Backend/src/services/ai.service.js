const config = require("../config/config");
const { AppError } = require("../utils/errors");


// ======================================
// CALL AI SERVICE
// ======================================

const callAI = async ({
  analysisId,
  zones,
  request,
}) => {

  // ======================================
  // VALIDATION
  // ======================================

  if (!analysisId) {
    throw new AppError(
      "analysisId is required",
      400
    );
  }

  if (!Array.isArray(zones) || zones.length === 0) {
    throw new AppError(
      "At least one zone is required for AI analysis",
      400
    );
  }


  // ======================================
  // CHECK AI SERVICE
  // ======================================

  if (!config.services.ai.url) {
    return {
      status: "unavailable",
      data: null,
      reason: "AI Service URL is not configured",
    };
  }


  // ======================================
  // CREATE AI REQUEST
  // ======================================

  const payload = {
    analysisId,

    request: {
      activity: request?.activity || null,
      date: request?.date || null,
      time: request?.time || null,
    },

    zones: zones.map((zone) => ({
      zoneId: zone.zoneId,

      location: {
        latitude: zone.location?.latitude ?? null,
        longitude: zone.location?.longitude ?? null,
      },

      gis: zone.gis || null,
      weather: zone.weather || null,
      ocean: zone.ocean || null,
      ecosystem: zone.ecosystem || null,
    })),
  };


  // ======================================
  // REQUEST TIMEOUT
  // ======================================

  const controller = new AbortController();

  const timeout = setTimeout(() => {
    controller.abort();
  }, config.request.timeoutMs);


  // ======================================
  // CALL AI SERVICE
  // ======================================

  try {

    const baseUrl =
      config.services.ai.url.replace(/\/+$/, "");

    /*
      IMPORTANT:
      Change this endpoint if your AI-Service
      uses a different endpoint.
    */

   const endpoint =
  config.services.ai.analyzeEndpoint
    .replace(/^\/+/, "");

const url =
  new URL(`${baseUrl}/${endpoint}`);


    console.log(
      `[AI] Request started for ${analysisId}`
    );

    console.log(
      `[AI] Zones: ${zones.length}`
    );


    const response = await fetch(
      url,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
        },

        body: JSON.stringify(payload),

        signal: controller.signal,
      }
    );


    console.log(
      `[AI] HTTP status: ${response.status}`
    );


    // ======================================
    // HANDLE AI ERROR
    // ======================================

    if (!response.ok) {

      const errorText =
        await response.text();


      throw new AppError(
        `AI Service returned HTTP ${response.status}`,
        502,
        {
          service: "ai",

          upstreamStatus:
            response.status,

          details:
            errorText,
        }
      );
    }


    // ======================================
    // PARSE RESPONSE
    // ======================================

    const data =
      await response.json();


    // ======================================
    // RETURN AI RESULT
    // ======================================

    console.log(
      `[AI] Request completed for ${analysisId}`
    );


    return {
      status: "available",

      data,

      source: url.toString(),

      retrievedAt:
        new Date().toISOString(),
    };


  } catch (error) {

    // ======================================
    // TIMEOUT
    // ======================================

    if (error.name === "AbortError") {

      throw new AppError(
        "AI Service request timed out",
        504,
        {
          service: "ai",

          timeoutMs:
            config.request.timeoutMs,
        }
      );
    }


    // ======================================
    // ALREADY HANDLED ERROR
    // ======================================

    if (error instanceof AppError) {
      throw error;
    }


    // ======================================
    // CONNECTION ERROR
    // ======================================

    throw new AppError(
      "Unable to connect to AI Service",
      502,
      {
        service: "ai",

        reason:
          error.message,

        cause:
          error.cause
            ? {
                code:
                  error.cause.code ||
                  null,

                message:
                  error.cause.message ||
                  null,
              }
            : null,
      }
    );


  } finally {

    clearTimeout(timeout);

  }
};


// ======================================
// EXPORT
// ======================================

module.exports = {
  callAI,
};