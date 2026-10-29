"""T015: synthetic aggregate/cursor and real PyMongo wire serializer, no network."""

import json
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from pymongo import _csot
from pymongo.errors import ExecutionTimeout, OperationFailure
from pymongo.synchronous.pool import Connection

from test_semantic_contract import DESCRIPTION, SOURCE, IsolatedSemanticTest


def record(identity=1, **values):
    return {"_id": identity, "title": "Synthetic film", "plot": "A synthetic recovered plot.",
            "semantic_score": 0.75, **values}


class SemanticMovieTests(IsolatedSemanticTest):
    def fixture(self, rows):
        self.ready()
        self.embedding = self.stack.enter_context(patch.object(
            self.tools, "_embed_semantic_description", return_value=[0.125] * 2048, create=True
        ))
        self.client = MagicMock()
        self.collection = self.client.__getitem__.return_value.__getitem__.return_value
        self.cursor = MagicMock()
        self.cursor.__iter__.side_effect = lambda: iter(rows)
        self.collection.aggregate.return_value = self.cursor
        self.db.return_value = self.client

    def assert_bounded_read(self, effective):
        self.db.assert_called_once()
        self.client.__getitem__.assert_called_once_with("sample_mflix")
        self.client.__getitem__.return_value.__getitem__.assert_called_once_with("embedded_movies")
        self.collection.aggregate.assert_called_once()
        self.collection.find.assert_not_called()
        self.cursor.close.assert_called_once()
        self.embedding.assert_called_once()
        kwargs = self.collection.aggregate.call_args.kwargs
        self.assertGreater(kwargs["maxTimeMS"], 0)
        self.assertLessEqual(kwargs["maxTimeMS"], 5000)
        self.assertGreater(kwargs["batchSize"], 0)
        self.assertLessEqual(kwargs["batchSize"], effective)
        for forbidden in ("insert_one", "update_one", "delete_many", "drop", "create_index"):
            getattr(self.collection, forbidden).assert_not_called()

    def test_fixed_vector_first_pipeline_projection_prefilters_and_limits(self):
        self.api("search_semantic_movie_results")
        self.fixture([])
        for requested in (1, 5, 10, 100):
            self.db.reset_mock()
            self.client.reset_mock()
            self.cursor.reset_mock()
            self.embedding.reset_mock()
            outcome = self.search({
                "description": DESCRIPTION, "requested_limit": requested,
                "genres": ["Action", "Sci-Fi"], "genre_mode": "any",
                "year": {"min": 2000, "min_inclusive": False}, "rating": {"min": 0},
            })
            effective = min(requested, 10)
            self.assert_bounded_read(effective)
            pipeline = self.collection.aggregate.call_args.args[0]
            self.assertEqual([set(stage).pop() for stage in pipeline], ["$vectorSearch", "$project"])
            vector = pipeline[0]["$vectorSearch"]
            self.assertEqual(set(vector), {"index", "path", "queryVector", "limit", "numCandidates", "filter"})
            self.assertEqual(vector["index"], "plot_vector_index")
            self.assertEqual(vector["path"], "plot_embedding_voyage_4_large")
            self.assertEqual(vector["limit"], effective)
            self.assertEqual(vector["numCandidates"], 20 * effective)
            self.assertLessEqual(vector["numCandidates"], 200)
            self.assertEqual(vector["queryVector"], self.embedding.return_value)
            self.assertEqual(vector["filter"], {"$and": [
                {"genres": {"$in": ["Action", "Sci-Fi"]}},
                {"year": {"$gt": 2000}}, {"imdb.rating": {"$gte": 0}},
            ]})
            self.assertEqual(pipeline[1]["$project"], {
                "_id": 1, "title": 1, "plot": 1, "genres": 1, "year": 1,
                "imdb.rating": 1, "semantic_score": {"$meta": "vectorSearchScore"},
            })
            self.assertEqual(outcome["status"], "empty")
            self.assertNotIn("queryVector", json.dumps(outcome))

    def test_mixed_batch_eligibility_order_count_and_no_refill(self):
        self.api("search_semantic_movie_results")
        missing = record(2)
        del missing["plot"]
        self.fixture([record(1), missing, record(3, plot=None), record(4, plot=42),
                      record(5, plot=""), record(6, plot=" \t\n"),
                      record(7, title=" "), record(None), record(9, _id=" "),
                      record(10, semantic_score=0.1, imdb={"rating": 9.9})])
        outcome = self.search({"description": DESCRIPTION, "requested_limit": 10})
        self.assertEqual(outcome["status"], "ok")
        self.assertEqual([row["source_id"] for row in outcome["movies"]], ["number:1", "number:10"])
        self.assertEqual([row["semantic_score"] for row in outcome["movies"]], [0.75, 0.1])
        self.assertEqual(outcome["returned_count"], 2)
        self.assertEqual(outcome["shortfall"], 8)
        self.assertEqual(outcome["source"], SOURCE)
        self.assertIn("fewer_results", outcome["warnings"])
        self.assertIn("missing_metadata", outcome["warnings"])
        self.assert_bounded_read(10)

    def test_all_ineligible_empty_without_fullplot_fallback(self):
        self.api("search_semantic_movie_results")
        self.fixture([record(1, plot=None, fullplot="Do not use this fallback."),
                      {"_id": 2, "title": "No plot"}, record(3, plot=[]),
                      record(4, plot=" "), record(5, title=None)])
        result = self.search({"description": DESCRIPTION})
        self.assertEqual(result["status"], "empty")
        self.assertEqual(result["returned_count"], 0)
        self.assertEqual(result["shortfall"], 5)
        self.assertEqual(result["movies"], [])
        self.assertEqual(result["criteria"]["description"], DESCRIPTION)
        self.assertIn("missing_metadata", result["warnings"])
        self.assert_bounded_read(5)

    def test_normalization_bounds_missing_optional_metadata_and_no_vector_output(self):
        self.api("search_semantic_movie_results")
        self.fixture([record(1, title="T" * 301, plot="P" * 501, year=True,
                             genres=["G" * 81] * 11, imdb={"rating": float("nan")},
                             plot_embedding_voyage_4_large="SYNTHETIC_VECTOR_SENTINEL",
                             poster="https://image.invalid/poster", unexpected="DROP_ME")])
        result = self.search({"description": DESCRIPTION})
        row = result["movies"][0]
        self.assertEqual(set(row), {"source_id", "title", "plot", "genres", "year",
                                    "imdb_rating", "semantic_score", "missing_fields", "truncated_fields"})
        self.assertEqual(len(row["title"]), 300)
        self.assertEqual(len(row["plot"]), 500)
        self.assertEqual(len(row["genres"]), 10)
        self.assertTrue(all(len(item) <= 80 for item in row["genres"]))
        self.assertIsNone(row["year"])
        self.assertIsNone(row["imdb_rating"])
        self.assertEqual(set(row["missing_fields"]), {"year", "imdb_rating"})
        self.assertEqual(set(row["truncated_fields"]), {"title", "plot", "genres"})
        self.assertIn("truncated_metadata", result["warnings"])
        self.assertNotIn("SYNTHETIC_VECTOR_SENTINEL", json.dumps(result))
        self.assertNotIn("DROP_ME", json.dumps(result))
        self.assert_bounded_read(5)

    def test_failures_discard_partial_rows_and_close_cursor(self):
        self.api("search_semantic_movie_results")
        self.fixture([])
        for stage in ("aggregate", "consume", "close", "normalize"):
            for error in (ExecutionTimeout("SYNTHETIC_PRIVATE"), OperationFailure("SYNTHETIC_PRIVATE")):
                self.collection.aggregate.reset_mock(side_effect=True)
                self.cursor.reset_mock(side_effect=True)
                self.collection.aggregate.return_value = self.cursor

                def rows():
                    yield record(1)
                    if stage == "consume":
                        raise error

                self.cursor.__iter__.side_effect = rows
                if stage == "aggregate":
                    self.collection.aggregate.side_effect = error
                if stage == "close":
                    self.cursor.close.side_effect = error
                with self.subTest(stage=stage), patch.object(
                    self.tools, "normalize_semantic_movie", create=True,
                    side_effect=error if stage == "normalize" else None,
                    wraps=None if stage == "normalize" else self.api("normalize_semantic_movie"),
                ):
                    result = self.search({"description": DESCRIPTION})
                if stage == "close":
                    self.assertEqual(result["status"], "ok")
                else:
                    self.assert_failure(result, "unavailable")
                self.assertNotIn("SYNTHETIC_PRIVATE", json.dumps(result))
                self.collection.aggregate.assert_called_once()
                if stage != "aggregate":
                    self.cursor.close.assert_called_once()

    def test_supported_cancellation_closes_cursor_and_never_returns_partial_success(self):
        self.api("search_semantic_movie_results")
        self.fixture([])

        def cancelled():
            yield record(1)
            raise KeyboardInterrupt("SYNTHETIC_CANCELLATION")

        self.cursor.__iter__.side_effect = cancelled
        try:
            outcome = self.search({"description": DESCRIPTION})
        except KeyboardInterrupt:
            pass  # Supported synchronous cancellation may propagate after cleanup.
        else:
            self.assert_failure(outcome, "unavailable")
        self.cursor.close.assert_called_once()
        self.collection.aggregate.assert_called_once()

    def test_real_csot_serializer_at_aggregate_and_consumption_stays_within_5s(self):
        self.api("search_semantic_movie_results")
        self.fixture([])
        sent = []

        def wire():
            self.assertIsNotNone(_csot.get_timeout())
            self.assertGreater(_csot.get_timeout(), 0)
            self.assertLessEqual(_csot.get_timeout(), 5)
            command = {"maxTimeMS": 5000}
            connection = SimpleNamespace(connect_rtt=0.001, set_conn_timeout=lambda _: None)
            Connection.apply_timeout(connection, self.client, command)
            sent.append(command["maxTimeMS"])

        def aggregate(*args, **kwargs):
            wire()
            return self.cursor

        def rows():
            wire()
            yield record(1)

        self.collection.aggregate.side_effect = aggregate
        self.cursor.__iter__.side_effect = rows
        self.assertEqual(self.search({"description": DESCRIPTION})["status"], "ok")
        self.assertEqual(len(sent), 2)
        self.assertTrue(all(0 < value <= 5000 for value in sent))
        self.cursor.close.assert_called_once()

    def test_traditional_missing_plot_remains_present_not_semantic_exclusion(self):
        self.fixture([])
        self.collection.find.return_value = self.cursor
        self.cursor.__iter__.side_effect = lambda: iter([{"_id": 1, "title": "Traditional"}])
        result = json.loads(self.tools.search_movie_results({"title": "Traditional"}))
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["returned_count"], 1)
        self.assertIsNone(result["movies"][0]["plot"])
        self.assertIn("plot", result["movies"][0]["missing_fields"])
        self.collection.aggregate.assert_not_called()
        self.embedding.assert_not_called()


if __name__ == "__main__":
    unittest.main()