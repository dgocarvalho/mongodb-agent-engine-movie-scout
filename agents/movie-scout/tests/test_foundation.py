"""Host-only isolated foundation checks. No native acceptance or catalog fixtures."""

from __future__ import annotations

import importlib
import json
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from unittest.mock import MagicMock, patch

from pymongo.errors import (
    AutoReconnect, ConfigurationError, ExecutionTimeout, InvalidURI,
    NetworkTimeout, OperationFailure, ServerSelectionTimeoutError,
)

from agent_movie_scout import state, tools


class StateTests(unittest.TestCase):
    def test_defaults_are_serializable_independent_and_fail_closed(self):
        first = state.safe_turn_defaults()
        first["allowed_tool_names"].append("save_user_info")
        second = state.safe_turn_defaults()
        self.assertEqual(second["allowed_tool_names"], [])
        self.assertEqual(json.loads(json.dumps(second))["turn_route"], "uncertain")
        self.assertIn("active_movie_criteria", state.HelloWorldState.__optional_keys__)


class ClientTests(unittest.TestCase):
    def setUp(self):
        tools._reset_movie_client_after_fork()

    def tearDown(self):
        tools._reset_movie_client_after_fork()

    def test_import_and_registration_never_construct_client(self):
        with patch("pymongo.MongoClient") as factory:
            importlib.reload(tools)
            tools.register(MagicMock())
            factory.assert_not_called()

    def test_failure_codes_distinguish_sanitized_mongo_connection_stages(self):
        cases = (
            (ServerSelectionTimeoutError("private host"), "server_selection_timeout"),
            (NetworkTimeout("private host"), "network_timeout"),
            (AutoReconnect("private host"), "auto_reconnect"),
            (ConfigurationError("private URI"), "configuration"),
            (InvalidURI("private URI"), "invalid_uri"),
        )
        for error, expected in cases:
            with self.subTest(expected=expected):
                self.assertEqual(tools._failure_code(error, "fallback"), expected)

    def test_concurrent_reuse_and_dedicated_variable_only(self):
        with patch.object(tools, "MongoClient") as factory, patch.dict(
            tools.os.environ, {"MOVIES_MONGODB_URI": "offline-placeholder"}, clear=True
        ):
            with ThreadPoolExecutor(max_workers=8) as pool:
                clients = list(pool.map(lambda _: tools._get_movie_client(), range(32)))
            self.assertTrue(all(client is clients[0] for client in clients))
            factory.assert_called_once_with("offline-placeholder", connect=False)
            tools._close_movie_client()
            clients[0].close.assert_called_once()

    def test_no_platform_fallback(self):
        with patch.dict(tools.os.environ, {"MONGODB_URI": "not-movie-config"}, clear=True), patch.object(
            tools, "MongoClient"
        ) as factory:
            with self.assertRaises(tools.MovieNotConfigured):
                tools._get_movie_client()
            factory.assert_not_called()

    def test_child_resets_locked_lock_and_does_not_close_parent(self):
        parent = MagicMock()
        tools._movie_client = parent
        tools._movie_client_pid = 1
        inherited = threading.Lock()
        inherited.acquire()
        tools._movie_client_lock = inherited
        tools._reset_movie_client_after_fork()
        self.assertIsNone(tools._movie_client)
        self.assertIsNot(inherited, tools._movie_client_lock)
        self.assertFalse(tools._movie_client_lock.locked())
        parent.close.assert_not_called()
        inherited.release()

    def test_pid_change_recreates_and_shutdown_failure_is_safe(self):
        with patch.object(tools, "MongoClient") as factory, patch.dict(
            tools.os.environ, {"MOVIES_MONGODB_URI": "offline-placeholder"}, clear=True
        ), patch.object(tools.os, "getpid", side_effect=[1, 2, 2]):
            first = tools._get_movie_client()
            second = tools._get_movie_client()
            self.assertEqual(factory.call_count, 2)
            first.close.assert_not_called()
            second.close.side_effect = RuntimeError("PRIVATE_SENTINEL")
            tools._close_movie_client()
            self.assertIsNone(tools._movie_client)


class ArgumentTests(unittest.TestCase):
    def test_strict_invalid_matrix_before_client_access(self):
        invalid = [
            {"$where": "code"}, {"database": "elsewhere"}, {"title": {"$ne": ""}},
            {"title": " "}, {"title": None}, {"title": "x" * 301},
            {"genres": "Comedy"}, {"genres": [False]}, {"genres": ["x"] * 11},
            {"genre_mode": "xor"}, {"sort": "random"}, {"sort": []},
            {"year_min": True}, {"year_min": 0}, {"year_max": 10000},
            {"year_min": "2000"}, {"year_min": 2000.0}, {"year_max": [2000]},
            {"year_min": 2001, "year_max": 2000},
            {"year_min": 2000, "year_max": 2000, "year_min_inclusive": False},
            {"rating_min": float("nan")}, {"rating_max": float("inf")},
            {"rating_min": True}, {"rating_min": "7"}, {"rating_max": [7]},
            {"rating_min": -1}, {"rating_max": 11}, {"rating_min": None},
            {"rating_min": 8, "rating_max": 7}, {"rating_min_inclusive": 1},
        ] + [{"requested_limit": value} for value in (0, -1, True, 1.5, "5", [], None)]
        with patch.object(tools, "_get_movie_client") as client:
            for arguments in invalid:
                with self.subTest(arguments=arguments):
                    result = json.loads(tools._read_movie_results(arguments, {}, [], dict))
                    self.assertEqual(result["status"], "invalid")
                    self.assertEqual(result["error_code"], "INVALID_CRITERIA")
                    self.assertEqual(result["movies"], [])
            client.assert_not_called()

    def test_defaults_caps_and_json_envelopes(self):
        for requested, effective in ((5, 5), (1, 1), (10, 10), (100, 10)):
            criteria = tools.validate_movie_arguments({"requested_limit": requested})
            envelope = json.loads(tools.movie_envelope("empty", criteria))
            self.assertEqual(envelope["effective_limit"], effective)
            self.assertEqual(envelope["capped"], requested > 10)
            self.assertTrue(envelope["shortfall"])
        self.assertEqual(tools.validate_movie_arguments({})["requested_limit"], 5)
        with self.assertRaises(ValueError):
            tools.movie_envelope("ok", movies=[{"bad": float("nan")}])
        with self.assertRaises(ValueError):
            tools.movie_envelope("unavailable", error_code="PRIVATE_SENTINEL")


class CursorTests(unittest.TestCase):
    def run_read(self, failure=None, stage="iterate", count=1):
        active = []
        cursor = MagicMock()
        collection = MagicMock()
        client = MagicMock()
        client.__getitem__.return_value.__getitem__.return_value = collection
        collection.find.return_value = cursor

        @contextmanager
        def budget(seconds):
            self.assertEqual(seconds, 5 if active else 10)
            active.append(seconds)
            try:
                yield
            finally:
                active.pop()

        def consume():
            self.assertTrue(active)
            yield {"test_value": 1}
            if failure and stage == "iterate":
                raise failure

        def close():
            self.assertTrue(active)
            if failure and stage == "close":
                raise failure

        cursor.__iter__.side_effect = consume if count else lambda: iter([])
        cursor.close.side_effect = close
        if failure and stage in ("find", "max_time_ms", "sort", "limit"):
            target = collection.find if stage == "find" else getattr(cursor, stage)
            target.side_effect = failure
        with patch.object(tools, "_get_movie_client", return_value=client), patch.object(
            tools.pymongo, "timeout", side_effect=budget
        ):
            result = tools._read_movie_results({}, {"fixed": "predicate"}, [("title", 1)], dict)
        self.assertFalse(active)
        client.__getitem__.assert_called_once_with("sample_mflix")
        client.__getitem__.return_value.__getitem__.assert_called_once_with("movies")
        collection.find.assert_called_once_with({"fixed": "predicate"}, tools.MOVIE_PROJECTION)
        if stage != "find" or not failure:
            cursor.close.assert_called_once()
        if not failure:
            cursor.max_time_ms.assert_called_once_with(5000)
            cursor.limit.assert_called_once_with(5)
        return json.loads(result)

    def test_success_empty_and_cleanup(self):
        self.assertEqual(self.run_read()["status"], "ok")
        self.assertEqual(self.run_read(count=0)["status"], "empty")

    def test_failures_discard_partial_rows_and_sanitize(self):
        for stage in ("find", "max_time_ms", "sort", "limit", "iterate", "close"):
            for error in (ExecutionTimeout("PRIVATE_SENTINEL"), OperationFailure("PRIVATE_SENTINEL")):
                with self.subTest(stage=stage, error=type(error).__name__):
                    result = self.run_read(error, stage)
                    self.assertEqual(result["status"], "unavailable")
                    self.assertEqual(result["movies"], [])
                    self.assertFalse(result["shortfall"])
                    self.assertNotIn("PRIVATE_SENTINEL", json.dumps(result))
                    expected = "RETRIEVAL_TIMEOUT" if error.timeout else "RETRIEVAL_UNAVAILABLE"
                    self.assertEqual(result["error_code"], expected)

    def test_missing_config_and_normalization_failure(self):
        with patch.object(tools, "_get_movie_client", side_effect=tools.MovieNotConfigured):
            result = json.loads(tools._read_movie_results({}, {}, [], dict))
        self.assertEqual(result["error_code"], "NOT_CONFIGURED")
        cursor = MagicMock()
        cursor.__iter__.return_value = iter([{}])
        client = MagicMock()
        client.__getitem__.return_value.__getitem__.return_value.find.return_value = cursor
        with patch.object(tools, "_get_movie_client", return_value=client):
            result = json.loads(tools._read_movie_results(
                {}, {}, [], MagicMock(side_effect=RuntimeError("PRIVATE_SENTINEL"))
            ))
        cursor.close.assert_called_once()
        self.assertEqual(result["movies"], [])
        self.assertEqual(result["status"], "unavailable")

    def test_server_cap_and_consumption_inside_real_csot(self):
        from pymongo import _csot

        cursor = MagicMock()
        client = MagicMock()
        client.__getitem__.return_value.__getitem__.return_value.find.return_value = cursor

        def consume():
            self.assertIsNotNone(_csot.get_timeout())
            yield {"test_value": 1}

        cursor.__iter__.side_effect = consume
        with patch.object(tools, "_get_movie_client", return_value=client):
            result = json.loads(tools._read_movie_results(
                {"requested_limit": 100}, {}, [("title", 1), ("_id", 1)], dict
            ))
        cursor.limit.assert_called_once_with(10)
        cursor.sort.assert_called_once_with([("title", 1), ("_id", 1)])
        self.assertEqual(result["effective_limit"], 10)
        self.assertTrue(result["capped"])
        self.assertTrue(result["shortfall"])


if __name__ == "__main__":
    unittest.main()
