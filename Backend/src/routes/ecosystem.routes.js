const express = require("express");

const {
  getEcosystemData,
} = require("../controllers/ecosystem.controller");

const router = express.Router();

// Ecosystem data
router.get("/zone/:zoneId", getEcosystemData);

module.exports = router;