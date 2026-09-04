const analysisService = require("../services/analysis.service");
const { sendSuccess } = require("../utils/response");

const createAnalysis = async (req, res, next) => {
  try {
    const { activity, date, time, zones } = req.body;

    const analysis = await analysisService.createAnalysis({
      activity,
      date,
      time,
      zones,
    });

    return sendSuccess(
      res,
      {
        analysisId: analysis.analysisId,
        status: analysis.status,
        zones: analysis.zones,
      },
      "Analysis created",
      201
    );
  } catch (error) {
    next(error);
  }
};

const getAnalysis = async (req, res, next) => {
  try {
    const analysis = await analysisService.getAnalysis(
      req.params.analysisId
    );

    return sendSuccess(
      res,
      analysis,
      "Analysis retrieved"
    );
  } catch (error) {
    next(error);
  }
};

const getAnalysisStatus = async (req, res, next) => {
  try {
    const analysis = await analysisService.getAnalysisStatus(
      req.params.analysisId
    );

    return sendSuccess(
      res,
      analysis,
      "Analysis status retrieved"
    );
  } catch (error) {
    next(error);
  }
};

const deleteAnalysis = async (req, res, next) => {
  try {
    const { analysisId } = req.params;

    await analysisService.deleteAnalysis(analysisId);

    return sendSuccess(
      res,
      { analysisId },
      "Analysis deleted"
    );
  } catch (error) {
    next(error);
  }
};

module.exports = {
  createAnalysis,
  getAnalysis,
  getAnalysisStatus,
  deleteAnalysis,
};