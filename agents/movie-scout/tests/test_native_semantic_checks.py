"""T026: opt-in native semantic observation helpers stay bounded and inert."""

import importlib
import json
import sys
import unittest
from unittest.mock import patch


def movie(identity="573a1391f29313caabcd93a3", **values):
    return {
        "source_id": f"objectId:{identity}",
        "title": "Observed title",
        "plot": "Observed recovered plot.",
        "genres": ["Drama"],
        "year": 2001,
        "imdb_rating": 7.5,
        "semantic_score": 0.8,
        "missing_fields": [],
        "truncated_fields": [],
        **values,
    }


def trace_rows(outcome, final="Observed title is grounded in the recovered plot."):
    tools = [{"function": {"name": "search_semantic_movies"}}]
    return [
        {
            "execution_id": "execution-1",
            "status": "started",
            "tool": "invoke_llm",
            "input": json.dumps({"tools": tools}),
        },
        {
            "execution_id": "execution-1",
            "status": "started",
            "tool": "search_semantic_movies",
        },
        {
            "execution_id": "execution-1",
            "status": "success",
            "tool": "search_semantic_movies",
            "output": json.dumps(outcome),
        },
        {
            "execution_id": "execution-1",
            "status": "success",
            "tool": "invoke_llm",
            "output": json.dumps({"content": final}),
        },
    ]


class NativeSemanticCheckTests(unittest.TestCase):
    def setUp(self):
        sys.modules.pop("native_semantic_checks", None)

    def test_import_is_inert_and_never_opens_native_endpoint(self):
        with patch("urllib.request.urlopen") as urlopen:
            module = importlib.import_module("native_semantic_checks")
        urlopen.assert_not_called()
        self.assertTrue(callable(module.observe_native_session))

    def test_real_catalog_trace_is_allowlisted_bounded_and_sanitized(self):
        checks = importlib.import_module("native_semantic_checks")
        outcome = {
            "status": "ok",
            "source": "sample_mflix.embedded_movies",
            "criteria": {"description": "A theme", "genres": [], "genre_mode": "all",
                         "year": None, "rating": None, "requested_limit": 5},
            "requested_limit": 5,
            "effective_limit": 5,
            "cap_applied": False,
            "returned_count": 1,
            "shortfall": 4,
            "movies": [movie()],
            "warnings": ["fewer_results"],
            "error_code": None,
            "message": "Retrieved eligible semantic movie matches.",
        }
        observation = checks.observe_native_session(
            trace_rows(outcome), origin="real_catalog",
        )
        self.assertEqual(observation["execution_id"], "execution-1")
        self.assertEqual(observation["tool_calls"], ["search_semantic_movies"])
        self.assertEqual(observation["source_ids"], [movie()["source_id"]])
        self.assertEqual(observation["titles"], ["Observed title"])
        self.assertTrue(observation["final_grounding_titles_present"])
        serialized = json.dumps(observation)
        for forbidden in ("semantic_score", "queryVector", "VOYAGE_API_KEY", "Traceback"):
            self.assertNotIn(forbidden, serialized)

    def test_native_schema_title_is_recognized(self):
        checks = importlib.import_module("native_semantic_checks")
        self.assertEqual(
            checks._tool_names([{"title": "search_semantic_movies"}]),
            ["search_semantic_movies"],
        )

    def test_empty_classifier_schema_does_not_block_semantic_schema(self):
        checks = importlib.import_module("native_semantic_checks")
        rows = trace_rows(
            {
                "status": "ok",
                "source": "sample_mflix.embedded_movies",
                "returned_count": 1,
                "effective_limit": 5,
                "movies": [movie()],
            },
        )
        rows.insert(0, {
            "execution_id": "execution-1",
            "status": "started",
            "tool": "invoke_llm",
            "input": json.dumps({"tools": []}),
        })
        checks.observe_native_session(rows, origin="real_catalog")

    def test_synthetic_fixture_cannot_be_mislabeled_as_real_catalog(self):
        checks = importlib.import_module("native_semantic_checks")
        synthetic = movie(
            identity="ignored",
            source_id="string:synthetic-semantic-fixture",
        )
        with self.assertRaises(checks.NativeObservationError):
            checks.compare_records([synthetic], [synthetic], origin="real_catalog")
        summary = checks.compare_records(
            [synthetic], [synthetic], origin="synthetic_fixture",
        )
        self.assertEqual(summary, {"origin": "synthetic_fixture", "records": 1})

    def test_forbidden_calls_duplicate_searches_and_oversized_batches_fail_closed(self):
        checks = importlib.import_module("native_semantic_checks")
        outcome = {
            "status": "ok",
            "source": "sample_mflix.embedded_movies",
            "criteria": {"description": "A theme", "genres": [], "genre_mode": "all",
                         "year": None, "rating": None, "requested_limit": 10},
            "requested_limit": 10,
            "effective_limit": 10,
            "cap_applied": False,
            "returned_count": 11,
            "shortfall": 0,
            "movies": [movie(str(index).zfill(24)) for index in range(11)],
            "warnings": [],
            "error_code": None,
            "message": "Retrieved eligible semantic movie matches.",
        }
        with self.assertRaises(checks.NativeObservationError):
            checks.observe_native_session(trace_rows(outcome), origin="real_catalog")

        rows = trace_rows({**outcome, "returned_count": 1, "movies": [movie()]})
        rows.insert(2, {
            "execution_id": "execution-1",
            "status": "started",
            "tool": "recall_user_info",
        })
        with self.assertRaises(checks.NativeObservationError):
            checks.observe_native_session(rows, origin="real_catalog")

        duplicate = trace_rows({**outcome, "returned_count": 1, "movies": [movie()]})
        duplicate.insert(2, {
            "execution_id": "execution-1",
            "status": "started",
            "tool": "search_semantic_movies",
        })
        with self.assertRaises(checks.NativeObservationError):
            checks.observe_native_session(duplicate, origin="real_catalog")


if __name__ == "__main__":
    unittest.main()