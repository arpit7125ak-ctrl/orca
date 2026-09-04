const gisService = require("../services/gis.service");
const { sendSuccess } = require("../utils/response");

const getGISData = async (req, res, next) => {
  try {
    const { zoneId } = req.params;
    const { latitude, longitude } = req.query;

    const lat = Number(latitude);
    const lon = Number(longitude);

    const gisData = await gisService.getGISData({
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
        gis: gisData,
      },
      "GIS data retrieved"
    );
  } catch (error) {
    next(error);
  }
};

module.exports = {
  getGISData,
};