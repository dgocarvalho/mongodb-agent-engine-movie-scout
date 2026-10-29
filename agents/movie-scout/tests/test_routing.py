"""Compiled host graph checks with fake App/LLM and instrumented tool boundaries.

Import is isolated BEFORE main loads: dotenv, native App construction and model builder
are replaced. No private configuration, native stack, provider or movie access is used.
"""

from __future__ import annotations

import importlib
import json
import sys
import unittest
from unittest.mock import MagicMock, patch

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import StructuredTool


class FakeLLM:
    def __init__(self):
        self.routes = []
        self.answers = []
        self.router_inputs = []
        self.agent_inputs = []
        self.bindings = []

    def invoke(self, messages):
        self.router_inputs.append(messages)
        value = self.routes.pop(0)
        if isinstance(value, Exception):
            raise value
        return value

    def bind_tools(self, schemas):
        self.bindings.append([schema.name for schema in schemas])
        parent = self

        class Bound:
            def invoke(self, messages):
                parent.agent_inputs.append(messages)
                return parent.answers.pop(0)

        return Bound()


def call(name, identity):
    return {"name": name, "args": {}, "id": identity, "type": "tool_call"}


class RoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fake_app = MagicMock()
        cls.fake_app.entrypoint.side_effect = lambda function: function
        cls.fake_app.checkpointer.return_value = None
        # Never import main with the real dotenv or App (which may inspect config).
        sys.modules.pop("agent_movie_scout.main", None)
        with patch("dotenv.load_dotenv") as dotenv, patch(
            "agent_engine_sdk_langgraph.App", return_value=cls.fake_app
        ), patch("agent_movie_scout.tools.register"):
            cls.main = importlib.import_module("agent_movie_scout.main")
        dotenv.assert_called_once()

    def setUp(self):
        self.effects = []
        self.llm = FakeLLM()
        self.wrappers = []
        for name in (
            "search_movies", "search_semantic_movies", "get_current_date",
            "save_user_info", "recall_user_info",
        ):
            def effect(tool_name=name):
                self.effects.append(tool_name)
                return "PROFILE_SENTINEL" if tool_name == "recall_user_info" else "ok"
            self.wrappers.append(StructuredTool.from_function(
                func=effect, name=name, description="Offline instrumented wrapper"
            ))
        self.fake_app.get_tools.return_value = self.wrappers
        self.fake_app.get_tool_schemas.return_value = self.wrappers
        self.fake_app.llm.return_value = self.llm
        with patch.object(self.main, "build_llm", return_value=MagicMock()):
            self.graph = self.main.build_agent()

    def test_exact_router_invalid_matrix(self):
        invalid = [
            "", "movie", '"movie"', '[{"route":"movie"}]',
            '{"route":"movie","extra":true}', '{"route":"unknown"}',
            '{"route":null}', '{"route":["movie"]}', '{"route":"movie","route":"other"}',
            '```json\n{"route":"movie"}\n```',
        ]
        for text in invalid:
            self.assertEqual(self.main.parse_turn_route(AIMessage(content=text)), "uncertain")
        self.assertEqual(self.main.parse_turn_route(AIMessage(
            content='{"route":"movie"}', tool_calls=[call("recall_user_info", "r")]
        )), "uncertain")
        self.assertEqual(self.main.parse_turn_route(AIMessage(
            content=[{"type": "text", "text": '{"route":"movie"}'}]
        )), "uncertain")
        for route in self.main.ROUTE_TOOLS:
            self.assertEqual(self.main.parse_turn_route(AIMessage(
                content=json.dumps({"route": route})
            )), route)

    def test_explicit_thematic_search_bypasses_model_route_variability(self):
        for text in (
            "Find films about people travelling to another planet.",
            "Find two science fiction movies after 2010 with IMDb above 7.",
            "Busque filmes sobre mergulhadores da marinha.",
            "Recommend movies about a family stranded on an island.",
            "Descreva uma história sobre mergulhadores da marinha em uma missão de resgate.",
            "Describe a story about divers on a rescue mission.",
        ):
            self.assertEqual(self.main.explicit_semantic_route(text), "semantic")
        self.assertIsNone(self.main.explicit_semantic_route(
            "Find films about Batman and remember my favorite color."
        ))
        self.assertIsNone(self.main.explicit_semantic_route("Find Batman Begins."))
        self.assertIsNone(self.main.explicit_semantic_route(
            "Find two Action movies after 2010 with IMDb above 7."
        ))

    def test_context_lifecycle_distinguishes_refinement_new_search_and_reset(self):
        self.assertFalse(self.main.context_replacement(
            "only after 2015", "semantic", True,
        ))
        self.assertTrue(self.main.context_replacement(
            "Find films about submarines", "semantic", True,
        ))
        self.assertTrue(self.main.context_replacement(
            "Find Batman Begins", "movie", True,
        ))
        self.assertFalse(self.main.context_replacement(
            "Recommend movies", "movie", True,
        ))

    def test_schema_filter_exposes_only_route_allowlist(self):
        schemas = [type("Schema", (), {"name": name})() for name in (
            "search_movies", "search_semantic_movies", "save_user_info", "get_current_date",
        )]
        selected = self.main.select_allowed_schemas(schemas, {
            "turn_route": "mixed_semantic",
            "allowed_tool_names": ["search_semantic_movies", "get_current_date", "save_user_info"],
        })
        self.assertEqual([schema.name for schema in selected],
                         ["search_semantic_movies", "get_current_date"])
        self.assertTrue(self.main.semantic_reset_requested("reset the search"))

    def test_reset_clears_semantic_context_without_tool_dispatch(self):
        self.llm.answers.append(AIMessage(content="Semantic context cleared."))
        result = self.graph.invoke({
            "messages": [HumanMessage(content="reset the semantic search")],
            "active_semantic_criteria": {"description": "old theme"},
        })
        self.assertEqual(result["active_semantic_criteria"], {})
        self.assertEqual(result["turn_route"], "other")
        self.assertEqual(self.effects, [])

    def test_model_response_is_json_roundtrippable_for_durable_state(self):
        response = AIMessage(content="", tool_calls=[call("search_semantic_movies", "id")])
        normalized = self.main.json_safe_ai_message(response)
        self.assertEqual(normalized.tool_calls[0]["name"], "search_semantic_movies")
        self.assertEqual(normalized.tool_calls[0]["id"], "id")

    def test_route_schema_matrix_and_actual_allowed_dispatch(self):
        for route, expected in self.main.ROUTE_TOOLS.items():
            if route == "uncertain":
                continue
            with self.subTest(route=route):
                self.llm.routes.append(AIMessage(content=json.dumps({"route": route})))
                chosen = "recall_user_info" if route == "nonmovie_memory" else "get_current_date"
                self.llm.answers.extend([
                    AIMessage(content="", tool_calls=[call(chosen, "allowed")]),
                    AIMessage(content="done"),
                ])
                result = self.graph.invoke({"messages": [HumanMessage(content="offline request")]})
                self.assertEqual(set(self.llm.bindings[-1]), set(expected))
                self.assertEqual(result["turn_route"], route)
                self.assertEqual(self.effects[-1], chosen)
                self.assertIsInstance(result["messages"][-2], ToolMessage)
        self.fake_app.get_tools.assert_called()
        self.fake_app.get_tool_schemas.assert_called()
        self.fake_app.checkpointer.assert_called()
        self.fake_app.llm.assert_called()

    def test_mixed_batch_denied_ids_before_all_wrapper_side_effects(self):
        for route in ("movie", "mixed", "other"):
            with self.subTest(route=route):
                self.llm.routes.append(AIMessage(content=json.dumps({"route": route})))
                self.llm.answers.extend([
                    AIMessage(content="", tool_calls=[
                        call("save_user_info", "save-id"), call("recall_user_info", "recall-id"),
                        call("get_current_date", "date-id"), call("unknown_tool", "unknown-id"),
                    ]), AIMessage(content="Please request memory separately."),
                ])
                result = self.graph.invoke({"messages": [HumanMessage(content="mixed request")]})
                denied = [m for m in result["messages"] if isinstance(m, ToolMessage)]
                self.assertEqual([m.tool_call_id for m in denied],
                                 ["save-id", "recall-id", "date-id", "unknown-id"])
                self.assertTrue(all(m.status == "error" for m in denied))
                self.assertEqual(self.effects, [])

    def test_uncertain_failed_route_no_binding_or_dispatch(self):
        for routing in (AIMessage(content="malformed"), RuntimeError("PRIVATE_SENTINEL")):
            # Unbound invocation serves both router and the no-tools clarification step.
            self.llm.routes.extend([routing, AIMessage(content="Please clarify.")])
            result = self.graph.invoke({
                "messages": [HumanMessage(content="ambiguous")],
                "turn_route": "nonmovie_memory",
                "allowed_tool_names": ["save_user_info", "recall_user_info"],
            })
            self.assertEqual(result["turn_route"], "uncertain")
            self.assertEqual(result["allowed_tool_names"], [])
            self.assertEqual(self.llm.bindings, [])
            self.assertEqual(self.effects, [])
            self.assertNotIn("PRIVATE_SENTINEL", result["messages"][-1].content)

    def test_reset_next_turn_excludes_prior_profile_output_and_assistant_summary(self):
        self.llm.routes.append(AIMessage(content='{"route":"nonmovie_memory"}'))
        self.llm.answers.extend([
            AIMessage(content="", tool_calls=[call("recall_user_info", "profile-id")]),
            AIMessage(content="PROFILE_DERIVED_ASSISTANT_SUMMARY"),
        ])
        prior = self.graph.invoke({"messages": [HumanMessage(content="Recall my location")]})
        self.llm.routes.append(AIMessage(content='{"route":"movie"}'))
        self.llm.answers.append(AIMessage(content="Movie retrieval not available yet."))
        result = self.graph.invoke({**prior, "messages": prior["messages"] + [
            HumanMessage(content="Recommend movies")
        ]})
        self.assertEqual(result["turn_route"], "movie")
        self.assertNotIn("recall_user_info", self.llm.bindings[-1])
        for messages in (self.llm.router_inputs[-1], self.llm.agent_inputs[-1]):
            content = " ".join(str(m.content) for m in messages)
            self.assertNotIn("PROFILE_SENTINEL", content)
            self.assertNotIn("PROFILE_DERIVED_ASSISTANT_SUMMARY", content)
        self.assertTrue(all(isinstance(m, (SystemMessage, HumanMessage))
                            for m in self.llm.router_inputs[-1]))
        self.assertEqual(self.effects, ["recall_user_info"])

    def test_guard_distrusts_allowlist_and_denies_movie_on_memory_route(self):
        result = self.main.dispatch_guard({
            "messages": [AIMessage(content="", tool_calls=[call("search_movies", "movie-id")])],
            "turn_route": "nonmovie_memory", "allowed_tool_names": ["search_movies"],
        })
        self.assertEqual(result["messages"][0].tool_call_id, "movie-id")
        result = self.main.dispatch_guard({
            "messages": [AIMessage(content="", tool_calls=[call("save_user_info", "save-id")])],
            "turn_route": "uncertain", "allowed_tool_names": ["save_user_info"],
        })
        self.assertEqual(result["messages"][0].tool_call_id, "save-id")

    def test_uncertain_model_cannot_force_tools_and_mixed_can_retry_movie_only(self):
        self.llm.routes.extend([
            AIMessage(content="malformed"),
            AIMessage(content="", tool_calls=[call("save_user_info", "uncertain-save")]),
            AIMessage(content="Please clarify."),
        ])
        result = self.graph.invoke({"messages": [HumanMessage(content="ambiguous")]})
        self.assertEqual(self.effects, [])
        self.assertEqual(result["messages"][-2].tool_call_id, "uncertain-save")
        self.llm.routes.append(AIMessage(content='{"route":"mixed"}'))
        self.llm.answers.extend([
            AIMessage(content="", tool_calls=[call("save_user_info", "deny"),
                                                call("search_movies", "defer")]),
            AIMessage(content="", tool_calls=[call("search_movies", "retry-movie")]),
            AIMessage(content="Please request memory separately."),
        ])
        self.graph.invoke({"messages": [HumanMessage(content="Remember location and recommend movies")]})
        self.assertEqual(self.effects, ["search_movies"])

    def test_installed_secure_wrapper_binding_preserves_boundary(self):
        from agent_engine_sdk_langgraph.runtime import SecureWrappedLLM

        class Inner:
            model_name = "offline-fake"

            def bind_tools(self, tools, **kwargs):
                return self

        wrapped = SecureWrappedLLM(llm=Inner(), get_wrapper=lambda: None, llm_id="offline")
        date_tool = next(tool for tool in self.wrappers if tool.name == "get_current_date")
        bound = wrapped.bind_tools([date_tool])
        self.assertIsInstance(bound, SecureWrappedLLM)
        self.assertEqual(bound._llm_id, "offline")
        self.assertEqual([tool.name for tool in bound._bound_tools], ["get_current_date"])

    def test_successful_movie_roundtrip_commits_and_invalid_does_not(self):
        for status in ("ok", "empty", "invalid", "unavailable"):
            self.llm.routes.append(AIMessage(content='{"route":"movie"}'))
            self.llm.answers.append(AIMessage(content="done"))
            outcome = json.dumps({"status": status, "criteria": {"genres": ["Comedy"]}})
            # Exercise agent node after an actual ToolNode result via a wrapped fake tool.
            movie = StructuredTool.from_function(
                func=lambda: outcome, name="search_movies", description="offline movie")
            self.fake_app.get_tools.return_value = [movie]
            self.fake_app.get_tool_schemas.return_value = [movie]
            self.llm.answers.insert(0, AIMessage(
                content="", tool_calls=[call("search_movies", "movie-result")]))
            with patch.object(self.main, "build_llm", return_value=MagicMock()):
                graph = self.main.build_agent()
            result = graph.invoke({"messages": [HumanMessage(content="Comedy please")],
                                   "active_movie_criteria": {"genres": ["Action"]}})
            expected = ["Comedy"] if status in ("ok", "empty") else ["Action"]
            self.assertEqual(result["active_movie_criteria"]["genres"], expected)

    def test_movie_inputs_exclude_old_user_memory_instructions(self):
        self.llm.routes.append(AIMessage(content='{"route":"movie"}'))
        self.llm.answers.append(AIMessage(content="done"))
        self.graph.invoke({"messages": [
            HumanMessage(content="Recall PROFILE_REQUEST_SENTINEL silent comedies"),
            AIMessage(content="PROFILE_SUMMARY_SENTINEL"),
            HumanMessage(content="Recommend movies"),
        ], "active_movie_criteria": {"genres": ["Action"]}})
        content = " ".join(str(m.content) for m in self.llm.agent_inputs[-1])
        self.assertNotIn("PROFILE_REQUEST_SENTINEL", content)
        self.assertNotIn("PROFILE_SUMMARY_SENTINEL", content)
        self.assertIn('"genres": ["Action"]', content)


if __name__ == "__main__":
    unittest.main()
