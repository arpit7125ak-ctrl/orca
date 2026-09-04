const logger = require("../utils/logger");

const errorMiddleware = (err, req, res, next) => {
  const statusCode = err.statusCode || 500;

  logger.error(
    `[${req.requestId || "NO_REQUEST_ID"}]`,
    err.message
  );

  // Never expose internal stack traces in production
  const response = {
    success: false,
    message:
      statusCode === 500
        ? "Internal server error"
        : err.message,
    errors: err.details || null,
    requestId: req.requestId || null,
  };

  // Stack trace is useful during local development
  if (process.env.NODE_ENV === "development") {
    response.stack = err.stack;
  }

  res.status(statusCode).json(response);
};

module.exports = errorMiddleware;