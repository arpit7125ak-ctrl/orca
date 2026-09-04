const express = require("express");
const { getGISData } = require("../controllers/gis.controller");

const router = express.Router();

router.get("/zone/:zoneId", getGISData);

module.exports = router;