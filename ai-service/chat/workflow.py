from typing import Any, Dict, Optional

from chat.state import ChatState, create_chat_state
from chat.router import route_question
from chat.context import build_chat_context
from chat.response import build_chat_response
from chat.memory import add_message


def chat_route_node(state: ChatState) -> ChatState:
    """
    Determine which analysis context is relevant to the
    user's question.
    """

    question = state.get("user_question", "")
    current_zone = state.get("current_zone")

    routing = route_question(
        user_question=question,
        current_zone=current_zone,
    )

    state["route"] = routing.get("route", "general")

    # Comparison questions operate across zones and therefore
    # do not select a single active zone.
    if state["route"] == "comparison":
        state["current_zone"] = None

    return state


def chat_context_node(
    state: ChatState,
    analysis_context: Optional[Dict[str, Any]] = None,
) -> ChatState:
    """
    Build trusted context for the selected route.

    The context layer ensures that zone-specific questions
    receive only the selected zone's information.
    """

    if analysis_context is not None:
        state["context"] = analysis_context

    context = build_chat_context(state)

    state["context"] = context

    return state


def chat_response_node(state: ChatState) -> ChatState:
    """
    Generate the final response from trusted context.
    """

    route = state.get("route", "general")

    response = build_chat_response(
        state=state,
        route=route,
        context=state.get("context", {}),
    )

    answer = response.get("answer", "")

    state["answer"] = answer

    # Store the exchange in conversation memory.
    add_message(
        state=state,
        role="user",
        content=state.get("user_question", ""),
    )

    add_message(
        state=state,
        role="assistant",
        content=answer,
    )

    state["success"] = True

    return state


def run_chat(
    conversation_id: str,
    user_question: str,
    analysis_context: Dict[str, Any],
    analysis_id: Optional[str] = None,
    current_zone: Optional[str] = None,
    history: Optional[list[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Execute the complete ORCA chat workflow.

    Parameters
    ----------
    conversation_id:
        Stable identifier for the conversation.

    user_question:
        Current user question.

    analysis_context:
        Trusted results from the ORCA analysis workflow.

    analysis_id:
        Optional analysis identifier.

    current_zone:
        Optional active zoneId.

    history:
        Previous conversation messages.

    Returns
    -------
    Dict[str, Any]
        Structured chat response.
    """

    state = create_chat_state(
        conversation_id=conversation_id,
        user_question=user_question,
        analysis_id=analysis_id,
        current_zone=current_zone,
        history=history,
        context=analysis_context,
    )

    try:
        state = chat_route_node(state)

        state = chat_context_node(
            state,
            analysis_context=analysis_context,
        )

        state = chat_response_node(state)

        return {
            "conversation_id": state.get("conversation_id"),
            "analysis_id": state.get("analysis_id"),
            "zoneId": state.get("current_zone"),
            "route": state.get("route"),
            "answer": state.get("answer"),
            "history": state.get("history", []),
            "success": state.get("success", False),
            "errors": state.get("errors", []),
        }

    except Exception as exc:
        state["success"] = False

        state.setdefault("errors", []).append(
            {
                "type": "chat",
                "component": "workflow",
                "message": str(exc),
            }
        )

        return {
            "conversation_id": state.get("conversation_id"),
            "analysis_id": state.get("analysis_id"),
            "zoneId": state.get("current_zone"),
            "route": state.get("route"),
            "answer": (
                "I could not complete the chat request because "
                "the required analysis context could not be processed."
            ),
            "history": state.get("history", []),
            "success": False,
            "errors": state.get("errors", []),
        }


chat_workflow = run_chat