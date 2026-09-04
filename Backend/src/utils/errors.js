class AppError extends Error {
  constructor(message, statusCode = 500, details = null) {
    super(message);

    this.name = "AppError";
    this.statusCode = statusCode;
    this.details = details;
    this.isOperational = true;

    Error.captureStackTrace(this, this.constructor);
  }
}

const badRequest = (message, details = null) => {
  return new AppError(message, 400, details);
};

const unauthorized = (message = "Unauthorized") => {
  return new AppError(message, 401);
};

const forbidden = (message = "Forbidden") => {
  return new AppError(message, 403);
};

const notFound = (message = "Resource not found") => {
  return new AppError(message, 404);
};

const conflict = (message, details = null) => {
  return new AppError(message, 409, details);
};

const internalServer = (message = "Internal server error") => {
  return new AppError(message, 500);
};

module.exports = {
  AppError,
  badRequest,
  unauthorized,
  forbidden,
  notFound,
  conflict,
  internalServer,
};