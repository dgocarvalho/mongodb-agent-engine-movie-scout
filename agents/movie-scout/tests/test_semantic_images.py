"""Text-only semantic output safeguards; no image fetch or enrichment."""

import unittest
from unittest.mock import patch

from agent_movie_scout.system_message import SYSTEM_PROMPT
from agent_movie_scout.tools import normalize_semantic_movie


class SemanticImageTests(unittest.TestCase):
    def test_text_only_prompt_disables_images_and_external_fetch(self):
        prompt = SYSTEM_PROMPT.casefold()
        self.assertIn("text only", prompt)
        self.assertIn("do not add images", prompt)
        self.assertIn("fetch", prompt)
        self.assertIn("posters", prompt)
        self.assertIn("enrich records externally", prompt)

    def test_semantic_normalization_excludes_poster_and_extra_fields(self):
        record = {
            "_id": 1,
            "title": "A film",
            "plot": "A plot",
            "genres": ["Drama"],
            "year": 2020,
            "imdb": {"rating": 7.5},
            "poster": "https://image.example/poster.jpg",
            "unexpected": "drop",
        }
        normalized = normalize_semantic_movie(record)
        self.assertNotIn("poster", normalized)
        self.assertNotIn("unexpected", normalized)

    def test_text_only_path_never_opens_or_validates_image_urls(self):
        references = (
            "https://image.example/poster.jpg",
            "http://image.example/poster.jpg",
            "http://localhost/poster.jpg",
            "https://127.0.0.1/poster.jpg",
            "file:///tmp/poster.jpg",
        )
        with patch("urllib.request.urlopen", side_effect=AssertionError("image fetch")) as opener:
            for reference in references:
                normalized = normalize_semantic_movie({
                    "_id": 1,
                    "title": "A film",
                    "plot": "A plot",
                    "poster": reference,
                })
                self.assertNotIn("poster", normalized)
        opener.assert_not_called()


if __name__ == "__main__":
    unittest.main()
