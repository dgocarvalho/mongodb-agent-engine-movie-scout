"""Real SDK direct boundaries; no OE/provider or live database calls.

These checks also run in the existing native tool interpreter. They are independent
process evidence, not Playground end-to-end acceptance. No secrets are loaded.
"""

import importlib.util
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch

from agent_engine_sdk_langgraph import App
from langchain_core.messages import AIMessage
from pydantic import ValidationError

from agent_movie_scout import tools


class NativeBoundaryTests(unittest.TestCase):
    def setUp(self):
        with patch.dict(os.environ, {"RUNNER_MODE": "tool"}):
            self.app = App(app_name="Movie Scout direct boundary validation")
        tools.register(self.app)
        self.movie = next(t for t in self.app.get_tools() if t.name == "search_movies")

    def test_sdk_schema_rejects_four_invalid_types_before_client(self):
        for arguments in ({"requested_limit": True}, {"requested_limit": "3"},
                          {"requested_limit": 1.5}, {"title": 123}):
            with self.subTest(arguments=arguments), patch.object(tools, "_get_movie_client") as client:
                with self.assertRaises(ValidationError):
                    self.movie.invoke(arguments)
                client.assert_not_called()

    def test_sdk_tool_rejects_four_invalid_values_before_client(self):
        for arguments in ({"requested_limit": 0}, {"requested_limit": -1},
                          {"title": ""}, {"title": "   "}):
            with self.subTest(arguments=arguments), patch.object(tools, "_get_movie_client") as client:
                result = json.loads(self.movie.invoke(arguments))
                self.assertEqual((result["status"], result["error_code"]),
                                 ("invalid", "INVALID_CRITERIA"))
                self.assertEqual(result["movies"], [])
                client.assert_not_called()

    def test_sdk_missing_secret_restores_environment_and_client_state(self):
        # Isolate the client cache too: never close or alter an existing pooled client.
        prior = os.environ.get("MOVIES_MONGODB_URI")
        with patch.object(tools, "_movie_client", None), patch.object(tools, "_movie_client_pid", None):
            with patch.dict(os.environ):
                os.environ.pop("MOVIES_MONGODB_URI", None)
                with patch.object(tools, "MongoClient") as constructor:
                    result = json.loads(self.movie.invoke({"title": "Batman", "requested_limit": 1}))
                    self.assertEqual((result["status"], result["error_code"]),
                                     ("unavailable", "NOT_CONFIGURED"))
                    self.assertEqual(result["movies"], [])
                    constructor.assert_not_called()
            self.assertEqual(os.environ.get("MOVIES_MONGODB_URI"), prior)

    def test_actual_guard_denies_batches_before_registered_tools(self):
        path = Path(tools.__file__).with_name("main.py")
        spec = importlib.util.spec_from_file_location("movie_native_guard_validation", path)
        module = importlib.util.module_from_spec(spec)
        with patch("dotenv.load_dotenv"), patch.dict(os.environ, {"RUNNER_MODE": "tool"}):
            spec.loader.exec_module(module)
        names = [t.name for t in self.app.get_tool_schemas()]
        self.assertEqual(set(names), {
            "search_movies", "search_semantic_movies", "get_current_date",
            "save_user_info", "recall_user_info",
        })
        for route in ("movie", "mixed", "uncertain"):
            calls = [{"name": name, "args": {}, "id": f"direct-{index}", "type": "tool_call"}
                     for index, name in enumerate(names)]
            with patch.object(tools, "_get_movie_client") as client:
                result = module.dispatch_guard({
                    "messages": [AIMessage(content="", tool_calls=calls)],
                    "turn_route": route, "allowed_tool_names": names,
                })
                self.assertEqual([m.tool_call_id for m in result["messages"]],
                                 [call["id"] for call in calls])
                self.assertTrue(all(m.status == "error" for m in result["messages"]))
                client.assert_not_called()

    def test_recall_preserves_native_formatted_context_list(self):
        from types import SimpleNamespace
        from unittest.mock import MagicMock

        app = MagicMock()
        app.tool.side_effect = lambda **kwargs: lambda function: function
        registered = {}

        def decorator(**kwargs):
            def capture(function):
                registered[function.__name__] = function
                return function
            return capture

        app.tool.side_effect = decorator
        app.memory.build_context.return_value = SimpleNamespace(
            formatted_context=[{"text": "NATIVE_CONTEXT_SENTINEL"}])
        tools.register(app)
        result = json.loads(registered["recall_user_info"]())
        self.assertTrue(result["found"])
        self.assertIn("NATIVE_CONTEXT_SENTINEL", result["profile"])


if __name__ == "__main__":
    unittest.main()