const mongoose = require("mongoose");

const zoneSchema = new mongoose.Schema(
  {
    zoneId: {
      type: String,
      required: true,
      trim: true,
    },

    location: {
      latitude: {
        type: Number,
        required: true,
        min: -90,
        max: 90,
      },

      longitude: {
        type: Number,
        required: true,
        min: -180,
        max: 180,
      },
    },

    gis: {
      type: mongoose.Schema.Types.Mixed,
      default: null,
    },

    weather: {
      type: mongoose.Schema.Types.Mixed,
      default: null,
    },

    ocean: {
      type: mongoose.Schema.Types.Mixed,
      default: null,
    },

    ecosystem: {
      type: mongoose.Schema.Types.Mixed,
      default: null,
    },

    risk: {
      type: mongoose.Schema.Types.Mixed,
      default: null,
    },

    recommendation: {
      type: mongoose.Schema.Types.Mixed,
      default: null,
    },
  },
  { _id: false }
);

const analysisSchema = new mongoose.Schema(
  {
    analysisId: {
      type: String,
      required: true,
      unique: true,
      index: true,
    },

    status: {
      type: String,
      enum: [
        "pending",
        "processing",
        "completed",
        "partial",
        "failed",
      ],
      default: "pending",
    },

    request: {
      activity: {
        type: String,
        required: true,
        trim: true,
      },

      date: {
        type: String,
        required: true,
      },

      time: {
        type: String,
        required: true,
      },
    },

    zones: {
      type: [zoneSchema],
      required: true,
      validate: {
        validator: (zones) => zones.length > 0,
        message: "At least one zone is required",
      },
    },

    overallDecision: {
      type: mongoose.Schema.Types.Mixed,
      default: null,
    },

    dataQuality: {
      type: mongoose.Schema.Types.Mixed,
      default: null,
    },

    agentTrace: {
      type: mongoose.Schema.Types.Mixed,
      default: null,
    },
  },
  {
    timestamps: true,
  }
);

const Analysis = mongoose.model("Analysis", analysisSchema);

module.exports = Analysis;