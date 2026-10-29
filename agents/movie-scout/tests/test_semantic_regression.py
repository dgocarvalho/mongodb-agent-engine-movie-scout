"""T032: semantic failures never change traditional movie behavior."""

import json
import importlib
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

from agent_movie_scout import state, tools


class SemanticRegressionTests(unittest.TestCase):
    def test_semantic_failure_preserves_traditional_criteria(self):
        traditional = {
            "title": "Batman",
            "genres": ["Action"],
            "rating_min": 8,
            "sort": "rating_desc",
            "requested_limit": 5,
        }
        semantic = {"description": "A tense rescue", "requested_limit": 5}
        self.assertEqual(
            state.criteria_after_outcome(traditional, {
                "status": "unavailable", "criteria": semantic,
            }),
            traditional,
        )
        self.assertEqual(
            state.semantic_criteria_after_outcome(semantic, {
                "status": "unavailable", "criteria": {
                    "description": "A different theme",
                },
            }),
            semantic,
        )

    def test_traditional_search_keeps_literal_title_and_rating_sort_contract(self):
        cursor = MagicMock()
        cursor.__iter__.return_value = iter([])
        client = MagicMock()
        collection = client.__getitem__.return_value.__getitem__.return_value
        collection.find.return_value = cursor
        with patch.object(tools, "_get_movie_client", return_value=client):
            outcome = json.loads(tools.search_movie_results({
                "title": "A.*(B)", "rating_min": 8, "sort": "rating_desc",
                "requested_limit": 100,
            }))
        self.assertEqual(outcome["status"], "empty")
        predicate = collection.find.call_args.args[0]
        self.assertIn("$expr", json.dumps(predicate))
        self.assertEqual(outcome["effective_limit"], 10)
        cursor.sort.assert_called_once_with([
            ("imdb.rating", -1), ("title", 1), ("_id", 1),
        ])
        cursor.limit.assert_called_once_with(10)
        cursor.close.assert_called_once()

    def test_semantic_invalid_input_does_not_acquire_traditional_client(self):
        with patch.object(tools, "_get_movie_client") as movie_client:
            outcome = json.loads(tools.search_semantic_movie_results({
                "description": " ", "requested_limit": 5,
            }))
        self.assertEqual(outcome["status"], "invalid")
        movie_client.assert_not_called()

    def test_route_allowlists_keep_movie_and_semantic_sources_disjoint(self):
        fake_app = MagicMock()
        fake_app.entrypoint.side_effect = lambda function: function
        fake_app.checkpointer.return_value = None
        sys.modules.pop("agent_movie_scout.main", None)
        with patch.dict(os.environ, {"RUNNER_MODE": "tool"}), \
                patch("dotenv.load_dotenv"), \
                patch("agent_engine_sdk_langgraph.App", return_value=fake_app), \
                patch("agent_movie_scout.tools.register"):
            main = importlib.import_module("agent_movie_scout.main")
        ROUTE_TOOLS = main.ROUTE_TOOLS

        self.assertIn("search_movies", ROUTE_TOOLS["movie"])
        self.assertNotIn("search_semantic_movies", ROUTE_TOOLS["movie"])
        self.assertIn("search_semantic_movies", ROUTE_TOOLS["semantic"])
        self.assertNotIn("search_movies", ROUTE_TOOLS["semantic"])
        self.assertNotIn("save_user_info", ROUTE_TOOLS["movie"])
        self.assertNotIn("save_user_info", ROUTE_TOOLS["semantic"])


if __name__ == "__main__":
    unittest.main()
