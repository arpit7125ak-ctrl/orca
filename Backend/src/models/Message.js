const mongoose = require("mongoose");


// ======================================
// MESSAGE SCHEMA
// ======================================

const messageSchema = new mongoose.Schema(
  {
    conversationId: {
      type: String,
      required: true,
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

    role: {
      type: String,
      enum: [
        "user",
        "assistant",
        "system",
      ],
      required: true,
    },

    content: {
      type: String,
      required: true,
      trim: true,
    },

    status: {
      type: String,
      enum: [
        "available",
        "unavailable",
        "error",
      ],
      default: "available",
    },

    metadata: {
      type: mongoose.Schema.Types.Mixed,
      default: null,
    },
  },

  {
    timestamps: true,
  }
);


// ======================================
// INDEX
// ======================================

messageSchema.index({
  conversationId: 1,
  createdAt: 1,
});


// ======================================
// MODEL
// ======================================

const Message =
  mongoose.model(
    "Message",
    messageSchema
  );


// ======================================
// EXPORT
// ======================================

module.exports = Message;