from typing import Any, Dict, List, Optional, TypedDict


class ChatState(TypedDict, total=False):
    """
    Shared state for the ORCA conversational assistant.

    Chat state is kept separate from the main analysis graph state.
    """

    conversation_id: str
    analysis_id: Optional[str]

    current_zone: Optional[str]

    user_question: str

    history: List[Dict[str, Any]]

    context: Dict[str, Any]

    route: Optional[str]

    answer: Optional[str]

    errors: List[Dict[str, Any]]

    success: bool


def create_chat_state(
    conversation_id: str,
    user_question: str,
    analysis_id: Optional[str] = None,
    current_zone: Optional[str] = None,
    history: Optional[List[Dict[str, Any]]] = None,
    context: Optional[Dict[str, Any]] = None,
) -> ChatState:
    """
    Create the initial state for a chat request.
    """

    return ChatState(
        conversation_id=conversation_id,
        analysis_id=analysis_id,
        current_zone=current_zone,
        user_question=user_question,
        history=history or [],
        context=context or {},
        route=None,
        answer=None,
        errors=[],
        success=False,
    )


def add_chat_message(
    state: ChatState,
    role: str,
    content: str,
) -> ChatState:
    """
    Append a message to conversation history.
    """

    if "history" not in state:
        state["history"] = []

    state["history"].append(
        {
            "role": role,
            "content": content,
        }
    )

    return state


def add_chat_error(
    state: ChatState,
    error: Dict[str, Any],
) -> ChatState:
    """
    Add a structured chat error.
    """

    if "errors" not in state:
        state["errors"] = []

    state["errors"].append(error)
    state["success"] = False

    return state


def set_chat_context(
    state: ChatState,
    context: Dict[str, Any],
) -> ChatState:
    """
    Replace the contextual information available to the chatbot.
    """

    if not isinstance(context, dict):
        raise ValueError("Chat context must be a dictionary.")

    state["context"] = context

    return state


def set_current_zone(
    state: ChatState,
    zone_id: Optional[str],
) -> ChatState:
    """
    Set the active zone for the current conversation.

    Zone identity is always represented by zoneId.
    """

    state["current_zone"] = zone_id

    return state


def set_route(
    state: ChatState,
    route: str,
) -> ChatState:
    """
    Store the route selected by the chat router.
    """

    if not isinstance(route, str) or not route.strip():
        raise ValueError("Chat route must be a non-empty string.")

    state["route"] = route.strip()

    return state


def set_answer(
    state: ChatState,
    answer: str,
) -> ChatState:
    """
    Store the final assistant response.
    """

    if not isinstance(answer, str):
        raise ValueError("Chat answer must be a string.")

    state["answer"] = answer
    state["success"] = True

    return state


def get_chat_zone_id(
    state: ChatState,
) -> Optional[str]:
    """
    Return the currently active zoneId.
    """

    zone_id = state.get("current_zone")

    if zone_id is None:
        return None

    if not isinstance(zone_id, str) or not zone_id.strip():
        return None

    return zone_id.strip()


def get_chat_history(
    state: ChatState,
) -> List[Dict[str, Any]]:
    """
    Return conversation history safely.
    """

    history = state.get("history", [])

    if not isinstance(history, list):
        return []

    return history


def get_chat_context(
    state: ChatState,
) -> Dict[str, Any]:
    """
    Return the current contextual analysis data.
    """

    context = state.get("context", {})

    if not isinstance(context, dict):
        return {}

    return context