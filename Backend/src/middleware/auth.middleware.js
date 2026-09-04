const authMiddleware = (req, res, next) => {
  // Authentication is not enforced yet.
  // This middleware is prepared for future authentication.

  req.user = null;

  next();
};

module.exports = authMiddleware;