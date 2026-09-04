const express = require("express");

const {
  getSnapshots,
} = require("../controllers/data.controller");

const router = express.Router();


// ======================================
// GET DATA SNAPSHOTS
// ======================================

router.get(
  "/snapshots/:analysisId",
  getSnapshots
);


module.exports = router;