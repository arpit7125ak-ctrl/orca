const express = require("express");

const {
  sendMessage,
  getConversation,
  getMessages,
} = require("../controllers/chat.controller");

const router = express.Router();


// ======================================
// SEND CHAT MESSAGE
// ======================================

router.post(
  "/",
  sendMessage
);


// ======================================
// GET CONVERSATION
// ======================================

router.get(
  "/:conversationId",
  getConversation
);


// ======================================
// GET CONVERSATION MESSAGES
// ======================================

router.get(
  "/:conversationId/messages",
  getMessages
);


module.exports = router;