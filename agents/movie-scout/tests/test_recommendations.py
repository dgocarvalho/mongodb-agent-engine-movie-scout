"""US3 test-first rating ordering and no-unrated-fallback contract."""

import json
import unittest
from unittest.mock import MagicMock, patch

from agent_movie_scout import tools


class RecommendationTests(unittest.TestCase):
    def test_high_rating_requires_numeric_eligibility_without_hidden_minimum(self):
        cursor = MagicMock()
        cursor.__iter__.return_value = iter([
            {'_id': 1, 'title': 'A', 'imdb': {'rating': 8}},
            {'_id': 2, 'title': 'B', 'imdb': {'rating': 0}},
        ])
        client = MagicMock()
        collection = client.__getitem__.return_value.__getitem__.return_value
        collection.find.return_value = cursor
        with patch.object(tools, '_get_movie_client', return_value=client):
            result = json.loads(tools.search_movie_results({'sort': 'rating_desc', 'requested_limit': 3}))
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['returned_count'], 2)
        self.assertTrue(result['shortfall'])
        self.assertFalse(result['capped'])
        self.assertEqual(result['movies'][1]['imdb_rating'], 0)
        cursor.sort.assert_called_once_with([('imdb.rating', -1), ('title', 1), ('_id', 1)])
        predicate = json.dumps(collection.find.call_args.args[0])
        self.assertIn('$imdb.rating', predicate)
        self.assertIn('decimal', predicate)
        self.assertIn('"$gte": ["$imdb.rating", 0]', predicate)
        cursor.close.assert_called_once()

    def test_ordinary_unrated_and_empty_high_rating_have_no_fallback(self):
        criteria = tools.validate_movie_arguments({})
        self.assertNotIn('$imdb.rating', json.dumps(tools.filtered_movie_predicate(criteria)))
        cursor = MagicMock()
        cursor.__iter__.return_value = iter([])
        client = MagicMock()
        collection = client.__getitem__.return_value.__getitem__.return_value
        collection.find.return_value = cursor
        with patch.object(tools, '_get_movie_client', return_value=client):
            result = json.loads(tools.search_movie_results({'sort': 'rating_desc', 'requested_limit': 100}))
        self.assertEqual(result['status'], 'empty')
        self.assertEqual(result['movies'], [])
        self.assertTrue(result['shortfall'])
        self.assertTrue(result['capped'])
        self.assertEqual(result['effective_limit'], 10)
        collection.find.assert_called_once()


if __name__ == '__main__':
    unittest.main()