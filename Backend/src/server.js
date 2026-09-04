const express = require("express");
const cors = require("cors");

const config = require("./config/config");
const { connectDatabase } = require("./config/database");

const logger = require("./utils/logger");

const requestIdMiddleware = require("./middleware/request-id.middleware");
const rateLimitMiddleware = require("./middleware/rate-limit.middleware");
const errorMiddleware = require("./middleware/error.middleware");


// Routes
const healthRoutes = require("./routes/health.routes");
const analysisRoutes = require("./routes/analysis.routes");
const gisRoutes = require("./routes/gis.routes");
const oceanRoutes = require("./routes/ocean.routes");
const ecosystemRoutes = require("./routes/ecosystem.routes");
const chatRoutes = require("./routes/chat.routes");
const dataRoutes = require("./routes/data.routes");


const app = express();

// ==========================================
// BASIC CONFIGURATION
// ==========================================

app.use(
  cors({
    origin: config.frontend.url,
  })
);

app.use(express.json());

// ==========================================
// MIDDLEWARE
// ==========================================

app.use(requestIdMiddleware);
app.use(rateLimitMiddleware);

// ==========================================
// ROUTES
// ==========================================

app.use("/api/v1/health", healthRoutes);
app.use("/api/v1/analysis", analysisRoutes);
app.use("/api/v1/gis", gisRoutes);
app.use("/api/v1/ocean", oceanRoutes);
app.use("/api/v1/ecosystem", ecosystemRoutes);
app.use("/api/v1/chat", chatRoutes);
app.use("/api/v1/data", dataRoutes);
// ==========================================
// ERROR HANDLER
// ==========================================

app.use(errorMiddleware);

// ==========================================
// START SERVER
// ==========================================

const startServer = async () => {
  try {
    await connectDatabase();

    app.listen(config.server.port, () => {
      logger.info(
        `ORCA Backend running on http://localhost:${config.server.port}`
      );
    });
  } catch (error) {
    logger.error(
      "Failed to start ORCA Backend:",
      error.message
    );

    process.exit(1);
  }
};

startServer();

module.exports = app;