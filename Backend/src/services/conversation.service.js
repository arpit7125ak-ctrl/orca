const crypto = require("crypto");

const Conversation = require("../models/Conversation");
const Message = require("../models/Message");

const { notFound, badRequest } = require("../utils/errors");


// ======================================
// SEND MESSAGE
// ======================================

const sendMessage = async ({
  conversationId,
  analysisId,
  zoneId,
  message,
}) => {

  // ======================================
  // VALIDATION
  // ======================================

  if (!analysisId) {
    throw badRequest(
      "analysisId is required"
    );
  }

  if (!message || !message.trim()) {
    throw badRequest(
      "Message cannot be empty"
    );
  }


  // ======================================
  // GET OR CREATE CONVERSATION
  // ======================================

  let conversation = null;

  if (conversationId) {

    conversation =
      await Conversation.findOne({
        conversationId,
      });

    if (!conversation) {
      throw notFound(
        "Conversation not found"
      );
    }

  } else {

    const newConversationId =
      `conversation_${crypto.randomUUID()}`;

    conversation =
      await Conversation.create({

        conversationId:
          newConversationId,

        analysisId,

        zoneId: zoneId || null,

      });
  }


  // ======================================
  // SAVE USER MESSAGE
  // ======================================

  const userMessage =
    await Message.create({

      conversationId:
        conversation.conversationId,

      analysisId,

      zoneId: zoneId || null,

      role: "user",

      content: message.trim(),

    });


  // ======================================
  // ASSISTANT RESPONSE
  // ======================================

  /*
    AI chat integration will be connected
    here after the AI-Service chat endpoint
    is available.

    We do NOT fabricate an AI response.
  */

  const assistantMessage =
    await Message.create({

      conversationId:
        conversation.conversationId,

      analysisId,

      zoneId: zoneId || null,

      role: "assistant",

      content:
        "AI response is not available yet.",

      status: "unavailable",

    });


  // ======================================
  // UPDATE CONVERSATION
  // ======================================

  conversation.updatedAt =
    new Date();

  await conversation.save();


  // ======================================
  // RETURN RESULT
  // ======================================

  return {

    conversationId:
      conversation.conversationId,

    analysisId,

    zoneId:
      zoneId || null,

    userMessage,

    assistantMessage,

  };
};


// ======================================
// GET CONVERSATION
// ======================================

const getConversation = async (
  conversationId
) => {

  if (!conversationId) {
    throw badRequest(
      "conversationId is required"
    );
  }


  const conversation =
    await Conversation.findOne({
      conversationId,
    }).lean();


  if (!conversation) {
    throw notFound(
      "Conversation not found"
    );
  }


  return conversation;
};


// ======================================
// GET MESSAGES
// ======================================

const getMessages = async (
  conversationId
) => {

  if (!conversationId) {
    throw badRequest(
      "conversationId is required"
    );
  }


  const conversation =
    await Conversation.findOne({
      conversationId,
    }).lean();


  if (!conversation) {
    throw notFound(
      "Conversation not found"
    );
  }


  const messages =
    await Message.find({
      conversationId,
    })
      .sort({
        createdAt: 1,
      })
      .lean();


  return messages;
};


// ======================================
// EXPORT
// ======================================

module.exports = {

  sendMessage,

  getConversation,

  getMessages,

};