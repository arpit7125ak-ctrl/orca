const config = require("../config/config");
const { badRequest, AppError } = require("../utils/errors");

const getTideData = async ({
  latitude,
  longitude,
  fromDate,
  toDate,
}) => {
  if (
    typeof latitude !== "number" ||
    typeof longitude !== "number"
  ) {
    throw badRequest(
      "Valid latitude and longitude are required"
    );
  }

  if (!config.externalData.tideApiUrl) {
    return {
      status: "unavailable",
      data: null,
      reason: "Tide API is not configured",
    };
  }

  const controller = new AbortController();

  const timeout = setTimeout(() => {
    controller.abort();
  }, config.request.timeoutMs);

  try {
    const url = new URL(
      config.externalData.tideApiUrl
    );

    url.searchParams.set("lat", String(latitude));
    url.searchParams.set("lon", String(longitude));

    if (fromDate) {
      url.searchParams.set(
        "fromDate",
        String(fromDate)
      );
    }

    if (toDate) {
      url.searchParams.set(
        "toDate",
        String(toDate)
      );
    }

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
        `Tide API returned HTTP ${response.status}`,
        502,
        {
          service: "tide",
          upstreamStatus: response.status,
          details: errorText,
        }
      );
    }

    const data = await response.json();

    return {
      status: "available",
      data,
      source: config.externalData.tideApiUrl,
      retrievedAt: new Date().toISOString(),
    };
  } catch (error) {
    if (error.name === "AbortError") {
      throw new AppError(
        "Tide API request timed out",
        504,
        {
          service: "tide",
        }
      );
    }

    if (error instanceof AppError) {
      throw error;
    }

    throw new AppError(
      "Unable to connect to Tide API",
      502,
      {
        service: "tide",
        reason: error.message,
      }
    );
  } finally {
    clearTimeout(timeout);
  }
};


const getPFZData = async ({
  latitude,
  longitude,
}) => {
  if (
    typeof latitude !== "number" ||
    typeof longitude !== "number"
  ) {
    throw badRequest(
      "Valid latitude and longitude are required"
    );
  }

  if (!config.externalData.pfzApiUrl) {
    return {
      status: "unavailable",
      data: null,
      reason: "PFZ API is not configured",
    };
  }

  const controller = new AbortController();

  const timeout = setTimeout(() => {
    controller.abort();
  }, config.request.timeoutMs);

  try {
    const url = new URL(
      config.externalData.pfzApiUrl
    );

    url.searchParams.set(
      "latitude",
      String(latitude)
    );

    url.searchParams.set(
      "longitude",
      String(longitude)
    );

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
        `PFZ API returned HTTP ${response.status}`,
        502,
        {
          service: "pfz",
          upstreamStatus: response.status,
          details: errorText,
        }
      );
    }

    const data = await response.json();

    return {
      status: "available",
      data,
      source: config.externalData.pfzApiUrl,
      retrievedAt: new Date().toISOString(),
    };
  } catch (error) {
    if (error.name === "AbortError") {
      throw new AppError(
        "PFZ API request timed out",
        504,
        {
          service: "pfz",
        }
      );
    }

    if (error instanceof AppError) {
      throw error;
    }

    throw new AppError(
      "Unable to connect to PFZ API",
      502,
      {
        service: "pfz",
        reason: error.message,
      }
    );
  } finally {
    clearTimeout(timeout);
  }
};


const getOceanData = async ({
  latitude,
  longitude,
  fromDate,
  toDate,
}) => {
  const [tide, pfz] = await Promise.allSettled([
    getTideData({
      latitude,
      longitude,
      fromDate,
      toDate,
    }),

    getPFZData({
      latitude,
      longitude,
    }),
  ]);

  return {
    tide:
      tide.status === "fulfilled"
        ? tide.value
        : {
            status: "error",
            data: null,
            reason: tide.reason?.message || "Tide request failed",
          },

    pfz:
      pfz.status === "fulfilled"
        ? pfz.value
        : {
            status: "error",
            data: null,
            reason: pfz.reason?.message || "PFZ request failed",
          },
  };
};


module.exports = {
  getTideData,
  getPFZData,
  getOceanData,
};