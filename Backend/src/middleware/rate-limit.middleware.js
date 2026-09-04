const config = require("../config/config");
const { sendError } = require("../utils/response");

const requestCounts = new Map();

const rateLimitMiddleware = (req, res, next) => {
  const clientKey =
    req.ip || req.headers["x-forwarded-for"] || "unknown";

  const now = Date.now();

  let clientData = requestCounts.get(clientKey);

  if (!clientData || now - clientData.startTime > config.rateLimit.windowMs) {
    clientData = {
      startTime: now,
      count: 0,
    };
  }

  clientData.count += 1;

  requestCounts.set(clientKey, clientData);

  if (clientData.count > config.rateLimit.maxRequests) {
    return sendError(
      res,
      "Too many requests. Please try again later.",
      429
    );
  }

  next();
};

module.exports = rateLimitMiddleware;