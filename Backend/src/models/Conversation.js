const mongoose = require("mongoose");


// ======================================
// CONVERSATION SCHEMA
// ======================================

const conversationSchema = new mongoose.Schema(
  {
    conversationId: {
      type: String,
      required: true,
      unique: true,
      index: true,
      trim: true,
    },

    analysisId: {
      type: String,
      required: true,
      index: true,
      trim: true,
    },

    zoneId: {
      type: String,
      default: null,
      index: true,
      trim: true,
    },
  },

  {
    timestamps: true,
  }
);


// ======================================
// MODEL
// ======================================

const Conversation =
  mongoose.model(
    "Conversation",
    conversationSchema
  );


// ======================================
// EXPORT
// ======================================

module.exports = Conversation;