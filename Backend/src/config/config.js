const dotenv = require("dotenv");

dotenv.config();

const config = {
  server: {
    port: Number(process.env.PORT) || 3000,
    nodeEnv: process.env.NODE_ENV || "development",
  },

  database: {
    mongodbUri:
      process.env.MONGODB_URI ||
      "mongodb://localhost:27017/orca",
  },

  frontend: {
    url:
      process.env.FRONTEND_URL ||
      "http://localhost:5173",
  },

  services: {
    ai: {
      url: process.env.AI_SERVICE_URL || "http://localhost:8000",
      analyzeEndpoint:
        process.env.AI_ANALYZE_ENDPOINT || "/api/v1/analyze",
    },

    gis: {
      url:
        process.env.GIS_SERVICE_URL ||
        "http://localhost:3005",
    },

    ecosystem: {
      url:
        process.env.ECOSYSTEM_SERVICE_URL ||
        "http://localhost:3006",
    },
  },

  externalData: {
    weatherApiUrl: process.env.WEATHER_API_URL || "",
    tideApiUrl: process.env.TIDE_API_URL || "",
    pfzApiUrl: process.env.PFZ_API_URL || "",
  },

  request: {
    timeoutMs:
      Number(process.env.REQUEST_TIMEOUT_MS) || 10000,
  },

  rateLimit: {
    windowMs:
      Number(process.env.RATE_LIMIT_WINDOW_MS) ||
      15 * 60 * 1000,

    maxRequests:
      Number(process.env.RATE_LIMIT_MAX_REQUESTS) || 100,
  },
};

module.exports = config;