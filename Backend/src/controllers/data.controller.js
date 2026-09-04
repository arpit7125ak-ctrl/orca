const snapshotService = require("../services/snapshot.service");

const { sendSuccess } = require("../utils/response");
const { badRequest } = require("../utils/errors");


// ======================================
// GET DATA SNAPSHOTS
// ======================================

const getSnapshots = async (req, res, next) => {
  try {
    const { analysisId } = req.params;
    const { zoneId } = req.query;


    // ======================================
    // VALIDATION
    // ======================================

    if (!analysisId || typeof analysisId !== "string") {
      throw badRequest(
        "Valid analysisId is required"
      );
    }


    // ======================================
    // GET SNAPSHOTS
    // ======================================

    const snapshots =
      await snapshotService.getSnapshots(
        analysisId,
        zoneId || null
      );


    // ======================================
    // RESPONSE
    // ======================================

    return sendSuccess(
      res,
      {
        analysisId,
        zoneId: zoneId || null,
        count: snapshots.length,
        snapshots,
      },
      "Data snapshots retrieved"
    );

  } catch (error) {
    next(error);
  }
};


// ======================================
// EXPORT
// ======================================

module.exports = {
  getSnapshots,
};