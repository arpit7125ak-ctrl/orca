const config = require("../config/config");
const { sendSuccess } = require("../utils/response");

const getHealth = (req, res) => {
  return sendSuccess(
    res,
    {
      service: "orca-backend",
      status: "running",
      environment: config.server.nodeEnv,
      requestId: req.requestId || null,
      timestamp: new Date().toISOString(),
    },
    "ORCA Backend is healthy"
  );
};

module.exports = {
  getHealth,
};