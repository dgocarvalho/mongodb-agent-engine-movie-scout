"""Native Movie Scout graph with independent schema and dispatch boundaries."""

from __future__ import annotations

import json
import logging
import re
from typing import Any, Literal, cast

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, AnyMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode
from agent_engine_sdk_langgraph import App

from agent_movie_scout.llm import build_llm
from agent_movie_scout.state import (
    HelloWorldState, TurnRoute, criteria_after_outcome, safe_turn_defaults,
    semantic_criteria_after_outcome,
)
from agent_movie_scout.system_message import ROUTING_PROMPT, SYSTEM_PROMPT
from agent_movie_scout.tools import register

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s")
logger = logging.getLogger(__name__)
load_dotenv()

app = App(app_name="Movie Scout")

register(app)

ROUTE_TOOLS: dict[TurnRoute, frozenset[str]] = {
    "movie": frozenset({"search_movies", "get_current_date"}),
    "mixed": frozenset({"search_movies", "get_current_date"}),
    "semantic": frozenset({"search_semantic_movies", "get_current_date"}),
    "mixed_semantic": frozenset({"search_semantic_movies", "get_current_date"}),
    "nonmovie_memory": frozenset({"save_user_info", "recall_user_info", "get_current_date"}),
    "other": frozenset({"get_current_date"}),
    "uncertain": frozenset(),
}


def allowed_tools(state: HelloWorldState) -> frozenset[str]:
    """Never trust a persisted/proposed allowed-name list to grant permissions."""
    route = state.get("turn_route", "uncertain")
    return ROUTE_TOOLS.get(route, frozenset()) & frozenset(state.get("allowed_tool_names", []))


def select_allowed_schemas(schemas: list[Any], state: HelloWorldState) -> list[Any]:
    """Expose only the current route's audited tool schemas to the model."""
    permitted = allowed_tools(state)
    return [schema for schema in schemas if getattr(schema, "name", None) in permitted]


def parse_turn_route(response: Any) -> TurnRoute:
    """Exact JSON object only; tool calls, malformed output and unknown labels deny."""
    if not isinstance(response, AIMessage) or response.tool_calls or response.invalid_tool_calls:
        return "uncertain"
    if not isinstance(response.content, str):
        return "uncertain"
    try:
        pairs = json.loads(response.content, object_pairs_hook=list)
    except (ValueError, TypeError):
        return "uncertain"
    if not isinstance(pairs, list) or len(pairs) != 1 or not isinstance(pairs[0], tuple):
        return "uncertain"
    key, route = pairs[0]
    if key != "route" or not isinstance(route, str) or route not in ROUTE_TOOLS:
        return "uncertain"
    return cast(TurnRoute, route)


_EXPLICIT_SEMANTIC_REQUEST = re.compile(
    r"\b(?:find|search|show|recommend|describe|tell|busque|procure|mostre|recomende|"
    r"descreva|conte|narre)"
    r"\s+(?:me\s+)?(?:"
    r"(?:films?|movies?|filmes?)\s+(?:\w+[\s,]+){0,3}(?:about|on|regarding|sobre|a respeito de)|"
    r"(?:(?:a|uma)\s+)?(?:story|história|historia|plot|enredo)\s+(?:about|on|regarding|sobre|a respeito de)|"
    r"(?:\w+[\s,]+){0,3}(?:science\s+fiction|sci[- ]fi)\s+(?:films?|movies?|filmes?)"
    r")\b",
    re.IGNORECASE,
)
_PROFILE_REQUEST = re.compile(
    r"\b(?:remember|recall|save|store|lembr[ae]|recorde|salve|guarde)\b",
    re.IGNORECASE,
)
_RESET_REQUEST = re.compile(
    r"\b(?:reset|start\s+over|clear|restart|recomece|recomeçar|limpe|zerar)\b",
    re.IGNORECASE,
)
_NEW_SEARCH_REQUEST = re.compile(
    r"\b(?:new\s+search|fresh\s+search|start\s+(?:a\s+)?new|"
    r"nova\s+busca|nova\s+pesquisa|comece\s+outra|independent\s+search)\b",
    re.IGNORECASE,
)
_EXPLICIT_TITLE_LOOKUP = re.compile(
    r"^\s*(?:find|search|show|busque|procure|mostre)\s+(?:for\s+)?"
    r"(?!(?:me\s+)?(?:films?|movies?|filmes?)\b).+",
    re.IGNORECASE,
)


def explicit_semantic_route(message: Any) -> TurnRoute | None:
    """Classify only an unambiguous thematic search without model variability."""
    if not isinstance(message, str) or not _EXPLICIT_SEMANTIC_REQUEST.search(message):
        return None
    if _PROFILE_REQUEST.search(message):
        return None
    return "semantic"


def semantic_reset_requested(message: Any) -> bool:
    """Recognize a direct reset without interpreting old messages or profiles."""
    return isinstance(message, str) and bool(_RESET_REQUEST.search(message))


def context_replacement(message: Any, route: TurnRoute, has_context: bool) -> bool:
    """New standalone catalog requests replace context; narrow follow-ups refine it."""
    if not has_context or route not in ("movie", "mixed", "semantic", "mixed_semantic"):
        return False
    if semantic_reset_requested(message):
        return True
    text = message if isinstance(message, str) else ""
    if explicit_semantic_route(text) == "semantic":
        return True
    if _NEW_SEARCH_REQUEST.search(text):
        return True
    if route in ("movie", "mixed") and _EXPLICIT_TITLE_LOOKUP.search(text):
        return True
    return False


def json_safe_ai_message(message: AIMessage) -> AIMessage:
    """Keep only durable-safe content and tool calls from a model response."""
    tool_calls = []
    for call in message.tool_calls:
        tool_calls.append({
            "name": str(call["name"]),
            "args": json.loads(json.dumps(call.get("args", {}), allow_nan=False)),
            "id": str(call["id"]),
            "type": "tool_call",
        })
    invalid_tool_calls = []
    for call in message.invalid_tool_calls:
        invalid_tool_calls.append({
            "name": str(call.get("name", "")),
            "args": str(call.get("args", "")),
            "id": str(call.get("id", "")),
            "error": str(call.get("error", "")),
            "type": "invalid_tool_call",
        })
    return AIMessage(
        content=json.loads(json.dumps(message.content, allow_nan=False)),
        tool_calls=tool_calls,
        invalid_tool_calls=invalid_tool_calls,
    )


def eligible_messages(state: HelloWorldState) -> list[AnyMessage]:
    """Do not forward historical assistant/profile output into movie reasoning.

    Keep user-supplied same-session intent and the current turn's tool round trips.
    The router sees only user turns; old profile-derived assistant summaries are excluded.
    """
    messages = state.get("messages", [])
    current = max((i for i, message in enumerate(messages) if isinstance(message, HumanMessage)),
                  default=len(messages))
    eligible: list[AnyMessage] = []
    # Movie context comes only from successful validated criteria, never old profile
    # requests, assistant summaries or unsuccessful/invalid historical movie requests.
    if state.get("turn_route") not in (
        "movie", "mixed", "semantic", "mixed_semantic", "uncertain",
    ):
        eligible.extend(message for message in messages[:current] if isinstance(message, HumanMessage))
    eligible.extend(message for message in messages[current:] if not isinstance(message, SystemMessage))
    return eligible


def dispatch_guard(state: HelloWorldState) -> dict:
    """Pre-ToolNode gate: reject a batch atomically if any name is disallowed.

    Every proposed call gets a result with its original ID. Allowed siblings are also
    deferred (not executed), so no message rewriting, raw-function bypass or orphan IDs.
    The model can retry only the allowed subset on the next graph iteration.
    """
    messages = state.get("messages", [])
    last = messages[-1] if messages else None
    if not isinstance(last, AIMessage) or not last.tool_calls:
        return {}
    permitted = allowed_tools(state)
    if all(call["name"] in permitted for call in last.tool_calls):
        return {}
    return {"messages": [
        ToolMessage(
            content=json.dumps({
                "status": "denied", "error_code": "TOOL_NOT_ALLOWED",
                "message": "Batch not executed. Use only permitted tools; submit profile operations separately.",
            }),
            tool_call_id=call["id"],
            status="error",
        ) for call in last.tool_calls
    ]}


@app.entrypoint
def build_agent() -> CompiledStateGraph:
    """Build the LangGraph agent."""
    logger.info("Building Movie Scout graph")
    runtime_llm = app.llm(build_llm(temperature=0))
    tools = app.get_tools()
    schemas = app.get_tool_schemas()

    def route_node(state: HelloWorldState) -> dict:
        update = safe_turn_defaults()
        update["active_movie_criteria"] = state.get("active_movie_criteria", {})
        update["active_semantic_criteria"] = state.get("active_semantic_criteria", {})
        messages = state.get("messages", [])
        route: TurnRoute = "uncertain"
        if messages and isinstance(messages[-1], HumanMessage):
            message = messages[-1].content
            if semantic_reset_requested(message):
                update["reset_semantic_criteria"] = True
                update["active_semantic_criteria"] = {}
                route = "other"
            else:
                deterministic = explicit_semantic_route(message)
                if deterministic is not None:
                    route = deterministic
                else:
                    try:
                        # Unbound wrapped LLM: no profile/movie tools exposed to classification.
                        response = runtime_llm.invoke([SystemMessage(content=ROUTING_PROMPT)] + [
                            item for item in messages if isinstance(item, HumanMessage)
                        ])
                        route = parse_turn_route(response)
                    except Exception:
                        pass  # Failed routing never inherits previous permissions or raw errors.
                has_context = bool(
                    state.get("active_semantic_criteria") if route in ("semantic", "mixed_semantic")
                    else state.get("active_movie_criteria")
                )
                if context_replacement(message, route, has_context):
                    if route in ("semantic", "mixed_semantic"):
                        update["replace_semantic_criteria"] = True
                        update["active_semantic_criteria"] = {}
                    elif route in ("movie", "mixed"):
                        update["replace_movie_criteria"] = True
                        update["active_movie_criteria"] = {}
        update["turn_route"] = route
        update["allowed_tool_names"] = sorted(ROUTE_TOOLS[route])
        return update

    def agent_node(state: HelloWorldState) -> dict:
        criteria = state.get("active_movie_criteria", {})
        semantic_criteria = state.get("active_semantic_criteria", {})
        if state.get("replace_movie_criteria"):
            criteria = {}
        if state.get("replace_semantic_criteria"):
            semantic_criteria = {}
        # ToolNode has completed through the ordinary audited wrapper. Consider only
        # this turn's actual correlated result, not old checkpoints/profile data.
        messages = state.get("messages", [])
        trailing_start = len(messages)
        while trailing_start and isinstance(messages[trailing_start - 1], ToolMessage):
            trailing_start -= 1
        caller = messages[trailing_start - 1] if trailing_start else None
        call_ids = {
            call["id"] for call in caller.tool_calls
        } if isinstance(caller, AIMessage) else set()
        for message in messages[trailing_start:]:
            if message.tool_call_id not in call_ids or not isinstance(message.content, str):
                continue
            try:
                outcome = json.loads(message.content)
            except (ValueError, TypeError):
                continue
            if message.name == "search_movies":
                try:
                    criteria = criteria_after_outcome(criteria, outcome)
                except (TypeError, AttributeError):
                    pass
            elif message.name == "search_semantic_movies":
                try:
                    semantic_criteria = semantic_criteria_after_outcome(
                        semantic_criteria, outcome,
                    )
                except (TypeError, AttributeError):
                    pass
        selected = select_allowed_schemas(schemas, state)
        # Do not bind an empty tool list (some providers reject tools=[]).
        model = runtime_llm.bind_tools(selected) if selected else runtime_llm
        prompt_messages = [SystemMessage(content=SYSTEM_PROMPT + "\nCurrent route: " +
                         state.get("turn_route", "uncertain") +
                         "\nValidated same-session movie criteria: " +
                         json.dumps(criteria, allow_nan=False) +
                         "\nValidated same-session semantic criteria: " +
                         json.dumps(semantic_criteria, allow_nan=False))]
        response = json_safe_ai_message(model.invoke(prompt_messages + eligible_messages(state)))
        return {
            "messages": [response],
            "active_movie_criteria": criteria,
            "active_semantic_criteria": semantic_criteria,
        }

    def should_continue(state: HelloWorldState) -> Literal["guard", "end"]:
        last = state["messages"][-1]
        return "guard" if isinstance(last, AIMessage) and last.tool_calls else "end"

    def after_guard(state: HelloWorldState) -> Literal["tools", "agent"]:
        return "agent" if isinstance(state["messages"][-1], ToolMessage) else "tools"

    builder = StateGraph(HelloWorldState)
    builder.add_node("route", route_node)
    builder.add_node("agent", agent_node)
    builder.add_node("guard", dispatch_guard)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "route")
    builder.add_edge("route", "agent")
    builder.add_conditional_edges("agent", should_continue, {"guard": "guard", "end": END})
    builder.add_conditional_edges("guard", after_guard, {"tools": "tools", "agent": "agent"})
    builder.add_edge("tools", "agent")
    return builder.compile(checkpointer=app.checkpointer())


def main() -> None:
    """Run the native agent."""
    app.run()


if __name__ == "__main__":
    main()
