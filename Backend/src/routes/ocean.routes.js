const express = require("express");

const {
  getTideData,
  getPFZData,
} = require("../controllers/ocean.controller");

const router = express.Router();

// Tide
router.get("/zone/:zoneId/tide", getTideData);

// PFZ
router.get("/zone/:zoneId/pfz", getPFZData);

module.exports = router;