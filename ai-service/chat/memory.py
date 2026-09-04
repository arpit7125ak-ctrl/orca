from typing import Any, Dict, List, Optional

from chat.state import ChatState


MAX_HISTORY_MESSAGES = 20


def add_message(
    state: ChatState,
    role: str,
    content: str,
) -> ChatState:
    """
    Add a message to the conversation history.

    Only conversational messages are stored. Environmental
    facts must remain in the analysis context.
    """

    if not isinstance(role, str) or not role.strip():
        raise ValueError("Message role is required.")

    if not isinstance(content, str):
        raise ValueError("Message content must be a string.")

    if "history" not in state:
        state["history"] = []

    state["history"].append(
        {
            "role": role.strip(),
            "content": content,
        }
    )

    # Keep memory bounded.
    if len(state["history"]) > MAX_HISTORY_MESSAGES:
        state["history"] = state["history"][-MAX_HISTORY_MESSAGES:]

    return state


def get_history(
    state: ChatState,
    limit: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Retrieve conversation history.

    The returned list is copied so callers cannot accidentally
    modify the stored conversation state.
    """

    history = state.get("history", [])

    if not isinstance(history, list):
        return []

    if limit is not None:
        if limit <= 0:
            return []

        history = history[-limit:]

    return [
        message.copy()
        for message in history
        if isinstance(message, dict)
    ]


def get_recent_messages(
    state: ChatState,
    count: int = 6,
) -> List[Dict[str, Any]]:
    """
    Return the most recent conversation messages.
    """

    return get_history(
        state=state,
        limit=count,
    )


def clear_history(state: ChatState) -> ChatState:
    """
    Clear conversational history.

    Analysis context is intentionally preserved.
    """

    state["history"] = []

    return state


def remember_analysis(
    state: ChatState,
    analysis_id: Optional[str],
) -> ChatState:
    """
    Associate the conversation with an analysis.

    This stores only the analysis identifier; actual analysis
    results remain in the context.
    """

    state["analysis_id"] = analysis_id

    return state


def remember_zone(
    state: ChatState,
    zone_id: Optional[str],
) -> ChatState:
    """
    Set the active zone for the conversation.

    Zone identity always uses the stable zoneId.
    """

    state["current_zone"] = zone_id

    return state


def build_memory_context(
    state: ChatState,
) -> Dict[str, Any]:
    """
    Build the safe conversational memory passed to the response layer.

    User messages are treated as conversation history, not as
    trusted instructions.
    """

    return {
        "conversation_id": state.get("conversation_id"),
        "analysis_id": state.get("analysis_id"),
        "current_zone": state.get("current_zone"),
        "recent_history": get_recent_messages(state),
    }