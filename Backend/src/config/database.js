const mongoose = require("mongoose");
const config = require("./config");

const connectDatabase = async () => {
  try {
    await mongoose.connect(config.database.mongodbUri);

    console.log("MongoDB connected successfully");
  } catch (error) {
    console.error("MongoDB connection failed:");
    console.error(error.message);

    process.exit(1);
  }
};

const disconnectDatabase = async () => {
  try {
    await mongoose.disconnect();

    console.log("MongoDB disconnected");
  } catch (error) {
    console.error("MongoDB disconnect failed:");
    console.error(error.message);
  }
};

module.exports = {
  connectDatabase,
  disconnectDatabase,
};