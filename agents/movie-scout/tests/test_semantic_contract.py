"""T012: isolated proposed semantic contract; RED until T019/T021.

Shared test-only sandbox, not an application helper or native acceptance harness.
API assumptions are recorded in the feature quickstart. Never load private dotenv.
"""

from __future__ import annotations

import importlib
import json
import os
import sys
import types
import unittest
from contextlib import ExitStack
from unittest.mock import MagicMock, patch

from langchain_core.tools import StructuredTool


SOURCE = "sample_mflix.embedded_movies"
DESCRIPTION = "A traveller discovers a simulated world."


class IsolatedSemanticTest(unittest.TestCase):
    """Fail closed even if a future implementation accidentally attempts live I/O."""

    def setUp(self):
        from agent_engine_sdk_langgraph import App

        self.sdk_app = App
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(patch.dict(os.environ, {}, clear=True))
        self.network = []
        for target in ("socket.create_connection", "socket.getaddrinfo",
                       "socket.socket.connect", "socket.socket.connect_ex"):
            self.network.append(self.stack.enter_context(patch(
                target, side_effect=AssertionError("OFFLINE_NETWORK_FORBIDDEN")
            )))
        self.dotenv = self.stack.enter_context(patch("dotenv.load_dotenv"))
        self.app_constructor = self.stack.enter_context(patch(
            "agent_engine_sdk_langgraph.App",
            side_effect=AssertionError("REAL_APP_FORBIDDEN"),
        ))
        self.mongo_constructor = self.stack.enter_context(patch(
            "pymongo.MongoClient", side_effect=AssertionError("REAL_MONGO_FORBIDDEN")
        ))
        self.voyage = types.ModuleType("voyageai")
        self.voyage.__version__ = "0.5.0"
        self.provider = MagicMock(name="synthetic_voyage_client")
        self.provider_constructor = MagicMock(return_value=self.provider)
        setattr(self.voyage, "Client", self.provider_constructor)
        self.stack.enter_context(patch.dict(sys.modules, {"voyageai": self.voyage}))
        self.tools = importlib.import_module("agent_movie_scout.tools")
        self.stack.enter_context(patch.object(
            self.tools, "MongoClient", self.mongo_constructor
        ))
        self.movie_factory = self.tools._get_movie_client
        self.db = self.stack.enter_context(patch.object(self.tools, "_get_movie_client"))
        self.addCleanup(self.assert_offline)

    def assert_offline(self):
        for boundary in self.network:
            boundary.assert_not_called()
        self.mongo_constructor.assert_not_called()
        self.dotenv.assert_not_called()

    def api(self, name):
        function = getattr(self.tools, name, None)
        self.assertTrue(callable(function), f"TDD RED: missing semantic API {name}")
        return function

    def search(self, arguments):
        raw = self.api("search_semantic_movie_results")(arguments)
        self.assertIsInstance(raw, str)
        return json.loads(raw)

    def registered(self):
        registered = {}
        raw_registered = {}

        class Registration:
            def tool(inner, *args, **kwargs):
                def decorate(function):
                    raw_registered[function.__name__] = function
                    registered[function.__name__] = StructuredTool.from_function(function)
                    return function
                return decorate

        self.tools.register(Registration())
        self.assertIn("search_semantic_movies", registered,
                      "TDD RED: missing semantic SDK registration")
        self.raw_semantic_tool = raw_registered["search_semantic_movies"]
        return registered["search_semantic_movies"]

    def ready(self):
        # Proposed internal seams; no operational readiness PASS is fabricated.
        self.stack.enter_context(patch.object(
            self.tools, "_semantic_ready", return_value=True, create=True
        ))

    def assert_failure(self, outcome, status):
        self.assertEqual(outcome["status"], status)
        self.assertEqual(outcome["source"], SOURCE)
        self.assertEqual(outcome["movies"], [])
        self.assertEqual(outcome["returned_count"], 0)
        self.assertIsNone(outcome["criteria"])
        self.assertEqual(outcome["error_code"],
                         "invalid_input" if status == "invalid" else "semantic_unavailable")


class SemanticContractTests(IsolatedSemanticTest):
    def test_sdk_schema_only_allowlisted_properties_and_strict_nested_objects(self):
        tool = self.registered()
        schema = tool.args_schema
        self.assertEqual(set(schema.model_fields), {
            "description", "genres", "genre_mode", "year", "rating", "requested_limit"
        })
        for arguments in ({"description": DESCRIPTION, "requested_limit": True},
                          {"description": DESCRIPTION, "requested_limit": "5"},
                          {"description": DESCRIPTION, "year": {"min": 2000, "$gt": 1}},
                          {"description": DESCRIPTION, "rating": {"max_inclusive": 1}}):
            with self.subTest(keys=sorted(arguments)), self.assertRaises(ValueError):
                schema.model_validate(arguments)
        for arguments in ({"description": DESCRIPTION, "collection": "movies"},
                          {"description": DESCRIPTION, "description_extra": "ignored?"}):
            with self.subTest(keys=sorted(arguments)), self.assertRaises(ValueError):
                self.raw_semantic_tool(**arguments)
        self.db.assert_not_called()
        self.provider_constructor.assert_not_called()

    def test_invalid_input_matrix_has_no_database_provider_or_readiness_io(self):
        search = self.api("search_semantic_movie_results")
        invalid = []
        invalid.extend({"description": value} for value in
                       (None, "", " \t\n", 1, True, [], {}, "x" * 2001))
        invalid.append({})
        invalid.extend({"description": DESCRIPTION, key: "synthetic"} for key in (
            "database", "collection", "index", "path", "queryVector", "model", "endpoint",
            "uri", "pipeline", "sort", "$where", "query", "metadata",
        ))
        invalid.extend({"description": DESCRIPTION, "requested_limit": value}
                       for value in (0, -1, True, 1.5, "5", None, []))
        with patch.object(self.tools, "_semantic_ready", create=True) as readiness:
            for arguments in invalid:
                with self.subTest(keys=sorted(arguments)):
                    self.assert_failure(json.loads(search(arguments)), "invalid")
            readiness.assert_not_called()
        self.db.assert_not_called()
        self.provider_constructor.assert_not_called()
        self.provider.embed.assert_not_called()

    def test_trim_unicode_boundaries_no_silent_description_truncation(self):
        validate = self.api("validate_semantic_arguments")
        for description in (" x ", "é" * 2000, "🙂" * 2000):
            criteria = validate({"description": description})
            self.assertEqual(criteria["description"], description.strip())
            self.assertEqual(criteria["requested_limit"], 5)
        with self.assertRaises(ValueError):
            validate({"description": "é" * 2001})

    def test_envelope_default_cap_statuses_and_safe_fields(self):
        envelope = self.api("semantic_envelope")
        validate = self.api("validate_semantic_arguments")
        for requested in (1, 5, 10, 100):
            criteria = validate({"description": DESCRIPTION, "requested_limit": requested})
            value = json.loads(envelope("empty", criteria))
            self.assertEqual(set(value), {
                "status", "source", "criteria", "requested_limit", "effective_limit",
                "cap_applied", "returned_count", "shortfall", "movies", "warnings",
                "error_code", "message",
            })
            self.assertEqual(value["source"], SOURCE)
            self.assertEqual(value["effective_limit"], min(requested, 10))
            self.assertEqual(value["requested_limit"], requested)
            self.assertIs(type(value["shortfall"]), int)
            self.assertEqual(value["shortfall"], min(requested, 10))
            self.assertEqual(value["cap_applied"], requested > 10)
            self.assertIsNone(value["error_code"])
            self.assertIn("fewer_results", value["warnings"])
            self.assertEqual("limit_applied" in value["warnings"], requested > 10)
        for status in ("invalid", "unavailable"):
            self.assert_failure(json.loads(envelope(status)), status)
        with self.assertRaises(ValueError):
            envelope("PRIVATE_SENTINEL")


if __name__ == "__main__":
    unittest.main()