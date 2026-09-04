const oceanService = require("../services/ocean.service");
const { sendSuccess } = require("../utils/response");

// ==========================================
// GET TIDE DATA
// ==========================================

const getTideData = async (req, res, next) => {
  try {
    const { zoneId } = req.params;

    const {
      latitude,
      longitude,
      fromDate,
      toDate,
    } = req.query;

    const lat = Number(latitude);
    const lon = Number(longitude);

    const tideData = await oceanService.getTideData({
      latitude: lat,
      longitude: lon,
      fromDate,
      toDate,
    });

    return sendSuccess(
      res,
      {
        zoneId,
        location: {
          latitude: lat,
          longitude: lon,
        },
        tide: tideData,
      },
      "Tide data retrieved"
    );
  } catch (error) {
    next(error);
  }
};

// ==========================================
// GET PFZ DATA
// ==========================================

const getPFZData = async (req, res, next) => {
  try {
    const { zoneId } = req.params;

    const {
      latitude,
      longitude,
    } = req.query;

    const lat = Number(latitude);
    const lon = Number(longitude);

    const pfzData = await oceanService.getPFZData({
      latitude: lat,
      longitude: lon,
    });

    return sendSuccess(
      res,
      {
        zoneId,
        location: {
          latitude: lat,
          longitude: lon,
        },
        pfz: pfzData,
      },
      "PFZ data retrieved"
    );
  } catch (error) {
    next(error);
  }
};

module.exports = {
  getTideData,
  getPFZData,
};