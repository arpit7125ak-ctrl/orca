const crypto = require("crypto");

const Analysis = require("../models/Analysis");

const { getGISData } = require("./gis.service");
const { getOceanData } = require("./ocean.service");
const { getEcosystemData } = require("./ecosystem.service");
const { getWeather } = require("./weather.service");
const { callAI } = require("./ai.service");

const { badRequest, notFound } = require("../utils/errors");


// ======================================
// CREATE ANALYSIS
// ======================================

const createAnalysis = async ({
  activity,
  date,
  time,
  zones,
}) => {

  // ======================================
  // VALIDATION
  // ======================================

  if (!activity || !date || !time) {
    throw badRequest(
      "activity, date and time are required"
    );
  }

  if (!Array.isArray(zones) || zones.length === 0) {
    throw badRequest(
      "At least one zone is required"
    );
  }


  // ======================================
  // CREATE ANALYSIS ID
  // ======================================

  const analysisId =
    `analysis_${crypto.randomUUID()}`;


  // ======================================
  // FORMAT ZONES
  // ======================================

  const formattedZones = zones.map((zone) => ({
    zoneId: zone.zoneId,

    location: {
      latitude: zone.latitude,
      longitude: zone.longitude,
    },

    gis: null,
    weather: null,
    ocean: null,
    ecosystem: null,
    risk: null,
    recommendation: null,
  }));


  // ======================================
  // CREATE DATABASE RECORD
  // ======================================

  const analysis = await Analysis.create({
    analysisId,

    status: "processing",

    request: {
      activity,
      date,
      time,
    },

    zones: formattedZones,

    overallDecision: null,
    dataQuality: null,
    agentTrace: null,
  });


  // ======================================
  // FAILURE TRACKING
  // ======================================

  let hasFailure = false;


  // ======================================
  // PROCESS EVERY ZONE
  // ======================================

  for (const zone of analysis.zones) {

    const {
      latitude,
      longitude,
    } = zone.location;


    console.log(
      `========================================`
    );

    console.log(
      `[ANALYSIS] Processing ${zone.zoneId}`
    );

    console.log(
      `[ANALYSIS] Location: ${latitude}, ${longitude}`
    );


    // ======================================
    // GIS
    // ======================================

    try {

      console.log(
        `[GIS] ${zone.zoneId} started`
      );

      const gisResult = await getGISData({
        latitude,
        longitude,
      });

      zone.gis = gisResult;

      console.log(
        `[GIS] ${zone.zoneId} completed`
      );

    } catch (error) {

      hasFailure = true;

      console.error(
        `[GIS] ${zone.zoneId} failed:`,
        error.message
      );

      zone.gis = {
        status: "error",
        data: null,
        reason: error.message,
      };
    }


    // ======================================
    // OCEAN
    // Tide + PFZ
    // ======================================

    try {

      console.log(
        `[OCEAN] ${zone.zoneId} started`
      );

      const oceanResult =
        await getOceanData({
          latitude,
          longitude,
          fromDate: date,
          toDate: date,
        });

      zone.ocean = oceanResult;


      // Check individual ocean services

      if (
        oceanResult.tide?.status === "error" ||
        oceanResult.pfz?.status === "error"
      ) {
        hasFailure = true;
      }


      console.log(
        `[OCEAN] ${zone.zoneId} completed`
      );

    } catch (error) {

      hasFailure = true;

      console.error(
        `[OCEAN] ${zone.zoneId} failed:`,
        error.message
      );

      zone.ocean = {

        tide: {
          status: "error",
          data: null,
          reason: error.message,
        },

        pfz: {
          status: "error",
          data: null,
          reason: error.message,
        },

      };
    }


    // ======================================
    // ECOSYSTEM
    // ======================================

    try {

      console.log(
        `[ECOSYSTEM] ${zone.zoneId} started`
      );

      const ecosystemResult =
        await getEcosystemData({
          latitude,
          longitude,
          date,
        });

      zone.ecosystem =
        ecosystemResult;


      if (
        ecosystemResult.status === "error"
      ) {
        hasFailure = true;
      }


      console.log(
        `[ECOSYSTEM] ${zone.zoneId} completed`
      );

    } catch (error) {

      hasFailure = true;

      console.error(
        `[ECOSYSTEM] ${zone.zoneId} failed:`,
        error.message
      );

      zone.ecosystem = {

        status: "error",

        data: null,

        reason: error.message,

      };
    }


    // ======================================
    // WEATHER
    // Open-Meteo
    // ======================================

    try {

      console.log(
        `[WEATHER] ${zone.zoneId} started`
      );

      const weatherResult =
        await getWeather({
          latitude,
          longitude,
          date,
          time,
        });


      zone.weather =
        weatherResult;


      if (
        weatherResult.status === "error"
      ) {
        hasFailure = true;
      }


      console.log(
        `[WEATHER] ${zone.zoneId} completed`
      );

    } catch (error) {

      hasFailure = true;

      console.error(
        `[WEATHER] ${zone.zoneId} failed:`,
        error.message
      );

      zone.weather = {

        status: "error",

        data: null,

        reason: error.message,

      };
    }

    // ======================================
// AI ANALYSIS
// ======================================

try {
  console.log(
    `[AI] ${zone.zoneId} started`
  );

  const aiResult = await callAI({
    analysisId,
    request: {
      activity,
      date,
      time,
    },
    zones: [zone],
  });

  if (aiResult.status === "available") {
    const aiData = aiResult.data;

    zone.risk =
      aiData.risk ||
      aiData.data?.risk ||
      null;

    zone.recommendation =
      aiData.recommendation ||
      aiData.data?.recommendation ||
      null;
  } else {
    hasFailure = true;
  }

  console.log(
    `[AI] ${zone.zoneId} completed`
  );

} catch (error) {

  hasFailure = true;

  console.error(
    `[AI] ${zone.zoneId} failed:`,
    error.message
  );

  zone.risk = {
    status: "unavailable",
    data: null,
    reason: error.message,
  };

  zone.recommendation = {
    status: "unavailable",
    data: null,
    reason: error.message,
  };
}

    // ======================================
    // ZONE COMPLETE
    // ======================================

    console.log(
      `[ANALYSIS] ${zone.zoneId} data collection completed`
    );

    console.log(
      `========================================`
    );
  }


  // ======================================
  // UPDATE ANALYSIS STATUS
  // ======================================

  analysis.status = hasFailure
    ? "partial"
    : "processing";


  // ======================================
  // SAVE ALL ZONE DATA
  // ======================================

  await Analysis.updateOne(
    {
      analysisId,
    },

    {
      $set: {

        zones: analysis.zones,

        status: analysis.status,

      },
    }
  );


  // ======================================
  // GET UPDATED ANALYSIS
  // ======================================

  const updatedAnalysis =
    await Analysis.findOne({
      analysisId,
    });


  return updatedAnalysis;
};


// ======================================
// GET ANALYSIS
// ======================================

const getAnalysis = async (
  analysisId
) => {

  const analysis =
    await Analysis.findOne({
      analysisId,
    }).lean();


  if (!analysis) {

    throw notFound(
      "Analysis not found"
    );

  }


  return analysis;
};


// ======================================
// GET ANALYSIS STATUS
// ======================================

const getAnalysisStatus = async (
  analysisId
) => {

  const analysis =
    await Analysis.findOne(
      {
        analysisId,
      },

      {
        _id: 0,

        analysisId: 1,

        status: 1,
      }

    ).lean();


  if (!analysis) {

    throw notFound(
      "Analysis not found"
    );

  }


  return analysis;
};


// ======================================
// DELETE ANALYSIS
// ======================================

const deleteAnalysis = async (
  analysisId
) => {

  const analysis =
    await Analysis.findOneAndDelete({
      analysisId,
    });


  if (!analysis) {

    throw notFound(
      "Analysis not found"
    );

  }


  return analysis;
};


// ======================================
// EXPORT
// ======================================

module.exports = {

  createAnalysis,

  getAnalysis,

  getAnalysisStatus,

  deleteAnalysis,

};