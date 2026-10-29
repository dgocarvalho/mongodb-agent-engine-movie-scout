"""Supplemental constructed-record checks, never native catalog acceptance."""

import json
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch

from bson import Decimal128, ObjectId
from pymongo.synchronous.pool import Connection

from agent_movie_scout import tools


class MovieTests(unittest.TestCase):
    def test_csot_wire_command_never_exceeds_server_budget(self):
        # Installed PyMongo overwrites cursor maxTimeMS with remaining CSOT.
        # Exercise that real serializer, not only the cursor setter mock.
        cursor = MagicMock()
        client = MagicMock()
        client.__getitem__.return_value.__getitem__.return_value.find.return_value = cursor
        sent = {}

        def records():
            command = {'maxTimeMS': 5000}
            connection = SimpleNamespace(connect_rtt=0.001, set_conn_timeout=lambda _: None)
            Connection.apply_timeout(connection, client, command)
            sent.update(command)
            yield {'_id': ObjectId(), 'title': 'Batman Begins'}

        cursor.__iter__.side_effect = records
        with patch.object(tools, '_get_movie_client', return_value=client):
            outcome = json.loads(tools.search_movie_results({'title': 'Batman Begins'}))
        self.assertEqual(outcome['status'], 'ok')
        self.assertGreater(sent['maxTimeMS'], 0)
        self.assertLessEqual(sent['maxTimeMS'], 5000)
        cursor.close.assert_called_once()

    def test_registered_schema_preserves_strict_counts_and_title(self):
        from langchain_core.tools import StructuredTool

        registered = {}

        class Registration:
            def tool(self, *args, **kwargs):
                def decorate(function):
                    registered[function.__name__] = StructuredTool.from_function(function)
                    return function
                return decorate

        tools.register(Registration())
        schema = registered['search_movies'].args_schema
        for args in ({'requested_limit': True}, {'requested_limit': '3'},
                     {'requested_limit': 1.5}, {'title': 123}):
            with self.assertRaises(ValueError):
                schema.model_validate(args)

    def test_normalization_missing_numeric_identity_and_display_bounds(self):
        oid = ObjectId()
        row = tools.normalize_movie({
            '_id': oid, 'title': 'X' * 301, 'year': True,
            'genres': ['Drama', 'Y' * 81], 'imdb': {'rating': Decimal128('7.5')},
            'plot': 'P' * 501,
        })
        self.assertEqual(row['source_id'], 'objectId:' + str(oid))
        self.assertEqual(row['imdb_rating'], 7.5)
        self.assertIsNone(row['year'])
        self.assertEqual(row['missing_fields'], ['year'])
        self.assertEqual(set(row['truncated_fields']), {'title', 'genres', 'plot'})
        self.assertEqual(len(row['title']), 300)
        self.assertEqual(len(row['plot']), 500)
        for rating in (True, '8', [8], float('nan'), float('inf'), Decimal128('NaN'), -1, 11):
            row = tools.normalize_movie({'_id': 1, 'title': 'Valid', 'imdb': {'rating': rating}})
            self.assertIsNone(row['imdb_rating'])
        for identity in (None, {}, [], True, float('nan')):
            with self.assertRaises(ValueError):
                tools.normalize_movie({'_id': identity, 'title': 'Valid'})
        for title in ('', '  ', None, ['name']):
            with self.assertRaises(ValueError):
                tools.normalize_movie({'_id': 1, 'title': title})
        self.assertNotEqual(tools.normalize_movie({'_id': 1, 'title': 'A'})['source_id'],
                            tools.normalize_movie({'_id': '1', 'title': 'A'})['source_id'])

    def test_title_predicate_escapes_literal_and_eligibility_before_limit(self):
        criteria = tools.validate_movie_arguments({'title': 'A.*(B)', 'requested_limit': 100})
        predicate = tools.title_movie_predicate(criteria)
        text = json.dumps(predicate)
        self.assertIn('A\\\\.\\\\*\\\\(B\\\\)', text)
        self.assertIn('$expr', predicate)
        self.assertIn('$type', text)
        self.assertIn('$trim', text)
        self.assertNotIn('$where', text)

    def test_title_tool_rejects_unknown_and_invalid_before_query(self):
        for args in ({'title': ''}, {'requested_limit': True}, {'requested_limit': 0},
                     {'sort': 'unknown'}, {'genres': ['unknown']},
                     {'$where': 'unsafe'}, {'title': {'$ne': None}}):
            with patch.object(tools, '_get_movie_client') as client:
                outcome = json.loads(tools.search_movie_results(args))
                self.assertEqual(outcome['status'], 'invalid')
                client.assert_not_called()

    def test_search_fixed_read_default_cap_empty_and_failure_cleanup(self):
        for count in (None, 1, 10, 100):
            cursor = MagicMock()
            cursor.__iter__.return_value = iter([{'_id': ObjectId(), 'title': 'A'}])
            client = MagicMock()
            collection = client.__getitem__.return_value.__getitem__.return_value
            collection.find.return_value = cursor
            args = {'title': 'A'} if count is None else {'title': 'A', 'requested_limit': count}
            with patch.object(tools, '_get_movie_client', return_value=client):
                outcome = json.loads(tools.search_movie_results(args))
            self.assertEqual(outcome['status'], 'ok')
            self.assertEqual(outcome['effective_limit'], min(count or 5, 10))
            cursor.limit.assert_called_once_with(min(count or 5, 10))
            cursor.sort.assert_called_once_with([('title', 1), ('_id', 1)])
            cursor.max_time_ms.assert_called_once_with(5000)
            cursor.close.assert_called_once()
            self.assertEqual(collection.find.call_args.args[1], tools.MOVIE_PROJECTION)
        with patch.object(tools, '_get_movie_client', side_effect=tools.MovieNotConfigured):
            outcome = json.loads(tools.search_movie_results({'title': 'A'}))
        self.assertEqual(outcome['status'], 'unavailable')
        self.assertEqual(outcome['error_code'], 'NOT_CONFIGURED')

    def test_empty_partial_failure_and_cursor_close_discard_every_record(self):
        for mode in ('empty', 'partial_failure', 'close_failure'):
            cursor = MagicMock()
            client = MagicMock()
            client.__getitem__.return_value.__getitem__.return_value.find.return_value = cursor

            def records():
                if mode != 'empty':
                    yield {'_id': ObjectId(), 'title': 'A'}
                if mode == 'partial_failure':
                    raise RuntimeError('PRIVATE_SENTINEL')

            cursor.__iter__.side_effect = records
            if mode == 'close_failure':
                cursor.close.side_effect = RuntimeError('PRIVATE_SENTINEL')
            with patch.object(tools, '_get_movie_client', return_value=client):
                outcome = tools.search_movie_results({'title': 'A'})
            value = json.loads(outcome)
            self.assertEqual(value['status'], 'empty' if mode == 'empty' else 'unavailable')
            self.assertEqual(value['movies'], [])
            self.assertNotIn('PRIVATE_SENTINEL', outcome)
            cursor.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()