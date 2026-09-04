const config = require("../config/config");
const { badRequest, AppError } = require("../utils/errors");

// ==========================================
// OPEN-METEO WEATHER SERVICE
// ==========================================

const getWeather = async ({
  latitude,
  longitude,
  date,
  time,
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
  // CHECK WEATHER API CONFIGURATION
  // ==========================================

  if (!config.externalData.weatherApiUrl) {
    return {
      status: "unavailable",
      data: null,
      reason: "Weather API is not configured",
    };
  }

  // ==========================================
  // BUILD OPEN-METEO URL
  // ==========================================

  const url = new URL(
    config.externalData.weatherApiUrl
  );

  // Location
  url.searchParams.set(
    "latitude",
    String(latitude)
  );

  url.searchParams.set(
    "longitude",
    String(longitude)
  );

  // ==========================================
  // HOURLY WEATHER VARIABLES
  // ==========================================

  url.searchParams.set(
    "hourly",
    [
      "temperature_2m",
      "relative_humidity_2m",
      "apparent_temperature",
      "precipitation_probability",
      "precipitation",
      "weather_code",
      "pressure_msl",
      "cloud_cover",
      "visibility",
      "wind_speed_10m",
      "wind_direction_10m",
      "wind_gusts_10m",
    ].join(",")
  );

  // ==========================================
  // UNITS
  // ==========================================

  url.searchParams.set(
    "temperature_unit",
    "celsius"
  );

  // Knots are useful for marine operations.
  url.searchParams.set(
    "wind_speed_unit",
    "kn"
  );

  url.searchParams.set(
    "precipitation_unit",
    "mm"
  );

  // Automatically use the location's timezone.
  url.searchParams.set(
    "timezone",
    "auto"
  );

  // ==========================================
  // DATE FILTER
  // ==========================================

  if (date) {
    url.searchParams.set(
      "start_date",
      String(date)
    );

    url.searchParams.set(
      "end_date",
      String(date)
    );
  } else {
    // If no date is supplied, get the default
    // forecast period from Open-Meteo.
    url.searchParams.set(
      "forecast_days",
      "7"
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
      `[WEATHER] Requesting: ${url.toString()}`
    );

    // ==========================================
    // CALL OPEN-METEO
    // ==========================================

    const response = await fetch(url, {
      method: "GET",

      headers: {
        Accept: "application/json",
      },

      signal: controller.signal,
    });

    console.log(
      `[WEATHER] HTTP status: ${response.status}`
    );

    // ==========================================
    // HANDLE HTTP ERROR
    // ==========================================

    if (!response.ok) {
      const errorText = await response.text();

      throw new AppError(
        `Open-Meteo API returned HTTP ${response.status}`,
        502,
        {
          service: "weather",
          provider: "Open-Meteo",
          upstreamStatus: response.status,
          details: errorText,
        }
      );
    }

    // ==========================================
    // PARSE RESPONSE
    // ==========================================

    const data = await response.json();

    // ==========================================
    // SELECT REQUESTED TIME
    // ==========================================

    let selectedWeather = null;

    if (
      time &&
      data.hourly &&
      Array.isArray(data.hourly.time)
    ) {
      const requestedTime = String(time).slice(0, 5);

      const requestedDate =
        String(date || "").slice(0, 10);

      const targetDateTime =
        `${requestedDate}T${requestedTime}`;

      const index =
        data.hourly.time.findIndex(
          (weatherTime) =>
            weatherTime === targetDateTime
        );

      if (index !== -1) {
        selectedWeather = {
          time: data.hourly.time[index],

          temperature_2m:
            data.hourly.temperature_2m?.[index] ?? null,

          relative_humidity_2m:
            data.hourly.relative_humidity_2m?.[index] ?? null,

          apparent_temperature:
            data.hourly.apparent_temperature?.[index] ?? null,

          precipitation_probability:
            data.hourly.precipitation_probability?.[index] ?? null,

          precipitation:
            data.hourly.precipitation?.[index] ?? null,

          weather_code:
            data.hourly.weather_code?.[index] ?? null,

          pressure_msl:
            data.hourly.pressure_msl?.[index] ?? null,

          cloud_cover:
            data.hourly.cloud_cover?.[index] ?? null,

          visibility:
            data.hourly.visibility?.[index] ?? null,

          wind_speed_10m:
            data.hourly.wind_speed_10m?.[index] ?? null,

          wind_direction_10m:
            data.hourly.wind_direction_10m?.[index] ?? null,

          wind_gusts_10m:
            data.hourly.wind_gusts_10m?.[index] ?? null,
        };
      }
    }

    // ==========================================
    // RETURN WEATHER RESULT
    // ==========================================

    return {
      status: "available",

      provider: "Open-Meteo",

      requested: {
        latitude,
        longitude,
        date: date || null,
        time: time || null,
      },

      selected: selectedWeather,

      data,

      source: url.toString(),

      retrievedAt:
        new Date().toISOString(),
    };
  } catch (error) {
    // ==========================================
    // TIMEOUT
    // ==========================================

    if (error.name === "AbortError") {
      throw new AppError(
        "Open-Meteo weather request timed out",
        504,
        {
          service: "weather",
          provider: "Open-Meteo",
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
      "Unable to connect to Open-Meteo",
      502,
      {
        service: "weather",
        provider: "Open-Meteo",
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
  getWeather,
};