const crypto = require("crypto");

const requestIdMiddleware = (req, res, next) => {
  const incomingRequestId = req.headers["x-request-id"];

  const requestId =
    incomingRequestId || crypto.randomUUID();

  req.requestId = requestId;

  res.setHeader("X-Request-ID", requestId);

  next();
};

module.exports = requestIdMiddleware;