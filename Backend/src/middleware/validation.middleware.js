const { badRequest } = require("../utils/errors");

const validateCoordinates = (latitude, longitude) => {
  if (typeof latitude !== "number" || typeof longitude !== "number") {
    return false;
  }

  if (latitude < -90 || latitude > 90) {
    return false;
  }

  if (longitude < -180 || longitude > 180) {
    return false;
  }

  return true;
};

const validateZones = (req, res, next) => {
  try {
    const { zones } = req.body;

    // zones must be an array
    if (!Array.isArray(zones)) {
      throw badRequest("zones must be an array");
    }

    // At least one zone is required
    if (zones.length === 0) {
      throw badRequest("At least one zone is required");
    }

    // Validate every zone
    zones.forEach((zone, index) => {
      if (!zone || typeof zone !== "object") {
        throw badRequest(`Invalid zone at index ${index}`);
      }

      if (!zone.zoneId) {
        throw badRequest(`zoneId is required for zone at index ${index}`);
      }

      if (!validateCoordinates(zone.latitude, zone.longitude)) {
        throw badRequest(
          `Invalid coordinates for zone ${zone.zoneId}`
        );
      }
    });

    next();
  } catch (error) {
    next(error);
  }
};

const validateAnalysisId = (req, res, next) => {
  const { analysisId } = req.params;

  if (!analysisId || typeof analysisId !== "string") {
    return next(badRequest("Invalid analysisId"));
  }

  next();
};

module.exports = {
  validateCoordinates,
  validateZones,
  validateAnalysisId,
};