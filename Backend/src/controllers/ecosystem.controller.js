const ecosystemService = require("../services/ecosystem.service");
const { sendSuccess } = require("../utils/response");
const { badRequest } = require("../utils/errors");

// ==========================================
// GET ECOSYSTEM DATA
// ==========================================

const getEcosystemData = async (req, res, next) => {
  try {
    const { zoneId } = req.params;

    const {
      latitude,
      longitude,
      date,
    } = req.query;

    const lat = Number(latitude);
    const lon = Number(longitude);

    if (!Number.isFinite(lat) || !Number.isFinite(lon)) {
      throw badRequest(
        "latitude and longitude must be valid numbers"
      );
    }

    const ecosystemData =
      await ecosystemService.getEcosystemData({
        latitude: lat,
        longitude: lon,
        date,
      });

    return sendSuccess(
      res,
      {
        zoneId,

        location: {
          latitude: lat,
          longitude: lon,
        },

        ecosystem: ecosystemData,
      },
      "Ecosystem data retrieved"
    );
  } catch (error) {
    next(error);
  }
};

module.exports = {
  getEcosystemData,
};