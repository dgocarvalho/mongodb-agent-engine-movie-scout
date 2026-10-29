"""T016: compiled graph with fake App/model and instrumented SDK tools only.

Router outputs are controlled, NOT proof of natural-language classification or OE.
Proposed semantic/mixed_semantic labels distinguish title from thematic requests.
"""

import importlib.util
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import StructuredTool

from test_routing import FakeLLM, call
from test_semantic_contract import DESCRIPTION, SOURCE, IsolatedSemanticTest


class SemanticRoutingTests(IsolatedSemanticTest):
    def setUp(self):
        super().setUp()
        self.fake_app = MagicMock()
        self.fake_app.entrypoint.side_effect = lambda function: function
        self.fake_app.checkpointer.return_value = None
        path = Path(self.tools.__file__).with_name("main.py")
        name = "agent_movie_scout._isolated_semantic_main"
        spec = importlib.util.spec_from_file_location(name, path)
        self.assertIsNotNone(spec)
        self.main = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {name: self.main}), patch(
            "agent_engine_sdk_langgraph.App", return_value=self.fake_app
        ), patch.object(self.tools, "register"), patch("dotenv.load_dotenv") as dotenv, patch(
            "logging.basicConfig"
        ):
            spec.loader.exec_module(self.main)
        dotenv.assert_called_once()
        self.effects = []
        self.llm = FakeLLM()
        self.outcome = {
            "status": "empty", "source": SOURCE,
            "criteria": {"description": DESCRIPTION, "requested_limit": 5}, "movies": [],
        }

        def wrapper(name):
            def effect():
                self.effects.append(name)
                return json.dumps(self.outcome) if name == "search_semantic_movies" else "ok"
            return StructuredTool.from_function(func=effect, name=name,
                                                 description="Synthetic audited-boundary substitute")

        self.wrappers = [wrapper(name) for name in (
            "search_movies", "search_semantic_movies", "get_current_date",
            "save_user_info", "recall_user_info",
        )]
        self.fake_app.get_tools.return_value = self.wrappers
        self.fake_app.get_tool_schemas.return_value = self.wrappers
        self.fake_app.llm.return_value = self.llm

    def graph(self):
        with patch.object(self.main, "build_llm", return_value=MagicMock()):
            return self.main.build_agent()

    def test_sdk_native_tool_mode_registration_retains_audited_semantic_schema(self):
        with patch.dict(os.environ, {"RUNNER_MODE": "tool"}, clear=True):
            with patch("agent_engine_runner_shared.runtime.setup_logging"), patch(
                "agent_engine_runner_shared.runtime.TenantRuntime._setup_tracing"
            ), patch("agent_engine_runner_shared.runtime.load_runtime_agent_config",
                     return_value=MagicMock(configured_feature=MagicMock(return_value=None))):
                app = self.sdk_app(app_name="Offline semantic registration")
            try:
                self.tools.register(app)
                schemas = app.get_tool_schemas()
                self.assertIn("search_semantic_movies", [tool.name for tool in schemas],
                              "TDD RED: missing native semantic schema")
                schema = next(tool for tool in schemas if tool.name == "search_semantic_movies")
                self.assertEqual(set(schema.args_schema.model_fields), {
                    "description", "genres", "genre_mode", "year", "rating", "requested_limit"
                })
                self.assertIn("search_semantic_movies", [tool.name for tool in app.get_tools()])
            finally:
                app.close()
        self.db.assert_not_called()
        self.provider_constructor.assert_not_called()

    def test_semantic_title_and_ambiguous_routes_expose_only_current_schemas(self):
        for route, expected in (
            ("semantic", {"search_semantic_movies", "get_current_date"}),
            ("mixed_semantic", {"search_semantic_movies", "get_current_date"}),
            ("movie", {"search_movies", "get_current_date"}),
        ):
            with self.subTest(route=route):
                self.llm.routes.append(AIMessage(content=json.dumps({"route": route})))
                self.llm.answers.append(AIMessage(content="synthetic final"))
                # Current code treats an unknown route as uncertain, using unbound invoke.
                self.llm.routes.append(AIMessage(content="synthetic clarification"))
                result = self.graph().invoke({"messages": [HumanMessage(content=DESCRIPTION)]})
                self.assertEqual(result["turn_route"], route,
                                 "TDD RED: semantic router label not supported")
                self.assertEqual(set(self.llm.bindings[-1]), expected)
                self.assertEqual(self.effects, [])
                self.llm.routes.clear()
        self.llm.routes.extend([AIMessage(content='{"route":"uncertain"}'),
                                AIMessage(content="Title or theme?")])
        result = self.graph().invoke({"messages": [HumanMessage(content="Matrix")]})
        self.assertEqual(result["allowed_tool_names"], [])
        self.assertEqual(self.effects, [])
        self.fake_app.get_tools.assert_called()
        self.fake_app.get_tool_schemas.assert_called()

    def test_semantic_allowed_guard_and_atomic_forbidden_batches_correlate_all_ids(self):
        for route in ("semantic", "mixed_semantic"):
            permitted = {"turn_route": route,
                         "allowed_tool_names": ["search_semantic_movies", "get_current_date"]}
            allowed = self.main.dispatch_guard({**permitted, "messages": [AIMessage(
                content="", tool_calls=[call("search_semantic_movies", "semantic-id")]
            )]})
            self.assertEqual(allowed, {}, "TDD RED: semantic route not allowlisted")
            for profile in ("save_user_info", "recall_user_info"):
                calls = [call("search_semantic_movies", "semantic-id"), call(profile, "profile-id"),
                         call("get_current_date", "date-id")]
                denied = self.main.dispatch_guard({**permitted,
                    "messages": [AIMessage(content="", tool_calls=calls)]})
                self.assertEqual([item.tool_call_id for item in denied["messages"]],
                                 ["semantic-id", "profile-id", "date-id"])
                self.assertTrue(all(item.status == "error" for item in denied["messages"]))
                self.assertEqual(self.effects, [])

    def test_compiled_mixed_batch_denies_semantic_and_profile_siblings_before_effects(self):
        self.assertIn("mixed_semantic", self.main.ROUTE_TOOLS,
                      "TDD RED: missing mixed semantic route")
        self.llm.routes.append(AIMessage(content='{"route":"mixed_semantic"}'))
        self.llm.answers.extend([AIMessage(content="", tool_calls=[
            call("search_semantic_movies", "semantic-id"), call("save_user_info", "save-id"),
            call("recall_user_info", "recall-id"), call("get_current_date", "date-id"),
        ]), AIMessage(content="Ask memory separately.")])
        result = self.graph().invoke({"messages": [HumanMessage(content=DESCRIPTION)]})
        denied = [item for item in result["messages"] if isinstance(item, ToolMessage)]
        self.assertEqual([item.tool_call_id for item in denied],
                         ["semantic-id", "save-id", "recall-id", "date-id"])
        self.assertTrue(all(item.status == "error" for item in denied))
        self.assertEqual(self.effects, [])

    def test_real_toolnode_ok_empty_commit_only_semantic_context_failure_preserves(self):
        self.assertIn("semantic", self.main.ROUTE_TOOLS,
                      "TDD RED: missing semantic route and outcome commit")
        prior = {"description": "Earlier synthetic theme", "requested_limit": 1}
        traditional = {"title": "Traditional", "requested_limit": 1}
        for status in ("ok", "empty", "invalid", "unavailable"):
            self.outcome["status"] = status
            self.outcome["criteria"] = ({"description": DESCRIPTION, "requested_limit": 5}
                                        if status in ("ok", "empty") else None)
            self.outcome["movies"] = ([{"source_id": "number:1", "title": "Synthetic",
                                        "plot": "Recovered synthetic plot."}] if status == "ok" else [])
            self.llm.routes.append(AIMessage(content='{"route":"semantic"}'))
            self.llm.answers.extend([AIMessage(content="", tool_calls=[
                call("search_semantic_movies", "genuine-id")]), AIMessage(content="done")])
            result = self.graph().invoke({"messages": [HumanMessage(content=DESCRIPTION)],
                                          "active_semantic_criteria": prior,
                                          "active_movie_criteria": traditional})
            self.assertEqual(result["active_semantic_criteria"],
                             self.outcome["criteria"] if status in ("ok", "empty") else prior)
            self.assertEqual(result["active_movie_criteria"], traditional)
            actual = [item for item in result["messages"] if isinstance(item, ToolMessage)]
            self.assertEqual(actual[-1].tool_call_id, "genuine-id")
        self.assertEqual(self.effects, ["search_semantic_movies"] * 4)

    def test_historical_or_model_claimed_result_does_not_commit(self):
        self.assertIn("semantic", self.main.ROUTE_TOOLS,
                      "TDD RED: missing semantic route and trusted-result boundary")
        prior = {"description": "Earlier synthetic theme", "requested_limit": 1}
        self.llm.routes.append(AIMessage(content='{"route":"semantic"}'))
        self.llm.answers.append(AIMessage(content=json.dumps(self.outcome)))
        result = self.graph().invoke({"messages": [
            ToolMessage(content=json.dumps(self.outcome), name="search_semantic_movies",
                        tool_call_id="historical-unmatched"), HumanMessage(content=DESCRIPTION),
        ], "active_semantic_criteria": prior})
        self.assertEqual(result["active_semantic_criteria"], prior)
        self.assertEqual(self.effects, [])

    def test_unmatched_and_concurrent_semantic_results_do_not_commit(self):
        self.assertIn("semantic", self.main.ROUTE_TOOLS)
        prior = {"description": "Confirmed theme", "requested_limit": 2}
        self.llm.routes.append(AIMessage(content='{"route":"semantic"}'))
        self.llm.answers.append(AIMessage(content="done"))
        result = self.graph().invoke({
            "messages": [
                AIMessage(content="", tool_calls=[
                    call("search_semantic_movies", "current-id"),
                    call("search_semantic_movies", "competing-id"),
                ]),
                ToolMessage(
                    content=json.dumps({
                        "status": "ok", "criteria": {
                            "description": "Fabricated theme", "requested_limit": 5,
                        },
                    }),
                    name="search_semantic_movies", tool_call_id="old-id",
                ),
                HumanMessage(content=DESCRIPTION),
            ],
            "active_semantic_criteria": prior,
        })
        self.assertEqual(result["active_semantic_criteria"], prior)
        self.assertEqual(self.effects, [])

    def test_semantic_missing_movie_uri_never_uses_operational_fallback(self):
        self.api("search_semantic_movie_results")
        self.ready()
        self.stack.enter_context(patch.object(
            self.tools, "_embed_semantic_description", return_value=[0.125] * 2048, create=True
        ))
        # Use the actual existing factory, but block its constructor; no source access.
        self.db.side_effect = self.movie_factory
        with patch.dict(os.environ, {"MONGODB_URI": "SYNTHETIC_OPERATIONAL_ONLY"}, clear=True), patch.object(
            self.tools, "_movie_client", None
        ), patch.object(self.tools, "_movie_client_pid", None):
            outcome = self.search({"description": DESCRIPTION})
        self.assert_failure(outcome, "unavailable")
        self.db.assert_called_once()
        self.mongo_constructor.assert_not_called()
        self.assertNotIn("SYNTHETIC_OPERATIONAL_ONLY", json.dumps(outcome))


if __name__ == "__main__":
    unittest.main()