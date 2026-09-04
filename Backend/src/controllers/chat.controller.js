const conversationService = require("../services/conversation.service");

const { sendSuccess } = require("../utils/response");
const { badRequest } = require("../utils/errors");


// ======================================
// SEND MESSAGE
// ======================================

const sendMessage = async (req, res, next) => {
  try {
    const {
      conversationId,
      analysisId,
      zoneId,
      message,
    } = req.body;


    // ======================================
    // VALIDATION
    // ======================================

    if (!message || typeof message !== "string") {
      throw badRequest(
        "message is required"
      );
    }


    if (!analysisId) {
      throw badRequest(
        "analysisId is required"
      );
    }


    // ======================================
    // SAVE + PROCESS MESSAGE
    // ======================================

    const result =
      await conversationService.sendMessage({
        conversationId,
        analysisId,
        zoneId: zoneId || null,
        message: message.trim(),
      });


    // ======================================
    // RESPONSE
    // ======================================

    return sendSuccess(
      res,
      result,
      "Message processed",
      201
    );

  } catch (error) {

    next(error);

  }
};


// ======================================
// GET CONVERSATION
// ======================================

const getConversation = async (
  req,
  res,
  next
) => {
  try {

    const {
      conversationId,
    } = req.params;


    const conversation =
      await conversationService.getConversation(
        conversationId
      );


    return sendSuccess(
      res,
      conversation,
      "Conversation retrieved"
    );

  } catch (error) {

    next(error);

  }
};


// ======================================
// GET MESSAGES
// ======================================

const getMessages = async (
  req,
  res,
  next
) => {
  try {

    const {
      conversationId,
    } = req.params;


    const messages =
      await conversationService.getMessages(
        conversationId
      );


    return sendSuccess(
      res,
      messages,
      "Messages retrieved"
    );

  } catch (error) {

    next(error);

  }
};


// ======================================
// EXPORT
// ======================================

module.exports = {
  sendMessage,
  getConversation,
  getMessages,
};