const express = require("express");

const {
  createAnalysis,
  getAnalysis,
  getAnalysisStatus,
  deleteAnalysis,
} = require("../controllers/analysis.controller");

const {
  validateZones,
  validateAnalysisId,
} = require("../middleware/validation.middleware");

const router = express.Router();

// Create a new analysis
router.post(
  "/",
  validateZones,
  createAnalysis
);

// Get complete analysis
router.get(
  "/:analysisId",
  validateAnalysisId,
  getAnalysis
);

// Get analysis status
router.get(
  "/:analysisId/status",
  validateAnalysisId,
  getAnalysisStatus
);

// Delete analysis
router.delete(
  "/:analysisId",
  validateAnalysisId,
  deleteAnalysis
);

module.exports = router;