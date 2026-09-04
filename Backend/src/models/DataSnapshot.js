const mongoose = require("mongoose");

const dataSnapshotSchema = new mongoose.Schema(
  {
    analysisId: {
      type: String,
      required: true,
      index: true,
    },

    zoneId: {
      type: String,
      required: true,
      index: true,
    },

    source: {
      type: String,
      required: true,
    },

    variable: {
      type: String,
      required: true,
    },

    value: {
      type: mongoose.Schema.Types.Mixed,
      default: null,
    },

    unit: {
      type: String,
      default: null,
    },

    validAt: {
      type: Date,
      default: null,
    },

    retrievedAt: {
      type: Date,
      default: Date.now,
    },

    dataType: {
      type: String,
      default: null,
    },

    quality: {
      type: String,
      default: null,
    },

    status: {
      type: String,
      enum: ["available", "unavailable", "error"],
      default: "available",
    },
  },
  {
    timestamps: true,
  }
);

dataSnapshotSchema.index({
  analysisId: 1,
  zoneId: 1,
});

const DataSnapshot = mongoose.model(
  "DataSnapshot",
  dataSnapshotSchema
);

module.exports = DataSnapshot;