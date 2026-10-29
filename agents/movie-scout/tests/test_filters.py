"""US2 test-first expectations; constructed predicates are not native acceptance."""

import json
import unittest
from unittest.mock import MagicMock, patch

from agent_movie_scout import tools


class FilterTests(unittest.TestCase):
    def test_aliases_and_unknown_genres(self):
        criteria = tools.validate_movie_arguments({'genres': ['science fiction', 'ACTION']})
        self.assertEqual(criteria['genres'], ['Sci-Fi', 'Action'])
        for genres in (['invented-genre'], ['Drama', 'unknown'], [''], [True]):
            with self.subTest(genres=genres), self.assertRaises(tools.InvalidCriteria):
                tools.validate_movie_arguments({'genres': genres})

    def test_combined_filter_runs_with_prelimit_scalar_eligibility(self):
        cursor = MagicMock()
        cursor.__iter__.return_value = iter([])
        client = MagicMock()
        collection = client.__getitem__.return_value.__getitem__.return_value
        collection.find.return_value = cursor
        with patch.object(tools, '_get_movie_client', return_value=client):
            result = json.loads(tools.search_movie_results({
                'title': 'Batman', 'genres': ['Action', 'Adventure'], 'genre_mode': 'all',
                'year_min': 2005, 'year_max': 2005, 'rating_min': 8.3,
            }))
        self.assertEqual(result['status'], 'empty')
        predicate = collection.find.call_args.args[0]
        self.assertEqual(predicate['genres'], {'$all': ['Action', 'Adventure']})
        text = json.dumps(predicate)
        for term in ('$expr', '$type', '$isArray', '$allElementsTrue', 'int', 'long',
                     'double', 'decimal', '$gte', '$lte', 'imdb.rating', '$year'):
            self.assertIn(term, text)
        self.assertNotIn('$where', text)
        cursor.limit.assert_called_once_with(5)
        cursor.close.assert_called_once()

    def test_any_genres_strict_boundaries_and_invalid_sort(self):
        criteria = tools.validate_movie_arguments({
            'genres': ['Action', 'Comedy'], 'genre_mode': 'any',
            'year_min': 2000, 'year_min_inclusive': False,
            'year_max': 2010, 'year_max_inclusive': False,
            'rating_min': 7, 'rating_min_inclusive': False,
            'rating_max': 9, 'rating_max_inclusive': False,
        })
        predicate = tools.filtered_movie_predicate(criteria)
        self.assertEqual(predicate['genres'], {'$in': ['Action', 'Comedy']})
        expression = json.dumps(predicate['$expr'])
        for field, endpoint in (('$year', 2000), ('$year', 2010),
                                ('$imdb.rating', 7), ('$imdb.rating', 9)):
            self.assertIn(json.dumps([field, endpoint]), expression)
        self.assertIn('"$gt"', expression)
        self.assertIn('"$lt"', expression)
        with patch.object(tools, '_get_movie_client') as client:
            self.assertEqual(json.loads(tools.search_movie_results({'sort': 'unknown'}))['status'],
                             'invalid')
            client.assert_not_called()

    def test_invalid_numerics_and_contradictions_never_acquire_client(self):
        bad = [
            {'year_min': x} for x in (True, '2000', [2000], 2000.0, 0, 10000)
        ] + [
            {'rating_min': x} for x in (True, '8', [8], float('nan'), float('inf'), -1, 11)
        ] + [
            {'year_min': 2005, 'year_max': 2005, 'year_min_inclusive': False},
            {'rating_min': 9, 'rating_max': 8}, {'genres': ['unknown']},
            {'genre_mode': 'xor'}, {'rating_max_inclusive': 'true'}, {'unknown': 1},
        ]
        for args in bad:
            with self.subTest(args=args), patch.object(tools, '_get_movie_client') as client:
                self.assertEqual(json.loads(tools.search_movie_results(args))['status'], 'invalid')
                client.assert_not_called()

    def test_registered_filter_schema_preserves_strict_types(self):
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
        fields = schema.model_fields
        for field in ('genres', 'genre_mode', 'year_min', 'year_max', 'rating_min',
                      'rating_max', 'year_min_inclusive', 'rating_max_inclusive'):
            self.assertIn(field, fields)
        for args in ({'year_min': True}, {'year_min': '2005'}, {'rating_min': '8'},
                     {'rating_min': True}, {'year_max_inclusive': 1}, {'genres': 'Drama'}):
            with self.subTest(args=args), self.assertRaises(ValueError):
                schema.model_validate(args)


if __name__ == '__main__':
    unittest.main()