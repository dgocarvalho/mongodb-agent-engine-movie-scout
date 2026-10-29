"""T030: semantic criteria transitions remain isolated and serializable."""

import json
import unittest

from agent_movie_scout import state


class SemanticStateTests(unittest.TestCase):
    def setUp(self):
        self.previous = {
            "description": "A rescue at sea",
            "genres": ["Action"],
            "genre_mode": "all",
            "year": {"min": 1990, "max": 2020, "min_inclusive": True,
                      "max_inclusive": True},
            "rating": {"min": 7, "min_inclusive": True},
            "requested_limit": 5,
        }

    def test_omitted_dimensions_are_preserved(self):
        merged = state.merge_semantic_criteria(
            self.previous, {"description": "A submarine rescue"},
        )
        self.assertEqual(merged["description"], "A submarine rescue")
        self.assertEqual(merged["genres"], ["Action"])
        self.assertEqual(merged["year"], self.previous["year"])
        self.assertEqual(merged["rating"], self.previous["rating"])
        json.dumps(merged, allow_nan=False)

    def test_replacing_interval_replaces_all_endpoints_and_inclusivity(self):
        merged = state.merge_semantic_criteria(
            self.previous,
            {"year": {"min": 2000, "min_inclusive": False}},
        )
        self.assertEqual(merged["year"], {"min": 2000, "min_inclusive": False})
        self.assertEqual(merged["requested_limit"], 5)

    def test_new_defaults_do_not_recover_semantic_theme(self):
        defaults = state.safe_turn_defaults()
        self.assertEqual(defaults["active_semantic_criteria"], {})
        self.assertNotIn("description", defaults["active_semantic_criteria"])

    def test_null_intervals_and_empty_genres_clear_dimensions(self):
        merged = state.merge_semantic_criteria(
            self.previous, {"genres": [], "year": None, "rating": None},
        )
        self.assertNotIn("genres", merged)
        self.assertNotIn("genre_mode", merged)
        self.assertNotIn("year", merged)
        self.assertNotIn("rating", merged)

    def test_genre_mode_alone_does_not_change_confirmed_genres(self):
        merged = state.merge_semantic_criteria(
            self.previous, {"genre_mode": "any"},
        )
        self.assertEqual(merged["genres"], ["Action"])
        self.assertEqual(merged["genre_mode"], "all")

    def test_new_search_and_reset_replace_all_semantic_dimensions(self):
        replacement = state.merge_semantic_criteria(
            self.previous, {"description": "A courtroom mystery"}, replace=True,
        )
        self.assertEqual(replacement, {"description": "A courtroom mystery"})
        reset = state.merge_semantic_criteria(self.previous, {}, replace=True)
        self.assertEqual(reset, {})
        self.assertEqual(state.reset_semantic_criteria(), {})

    def test_failed_outcomes_retain_and_empty_confirms_copy(self):
        proposal = {"description": "A courtroom mystery", "requested_limit": 3}
        for status in ("invalid", "unavailable"):
            retained = state.semantic_criteria_after_outcome(
                self.previous, {"status": status, "criteria": proposal},
            )
            self.assertEqual(retained, self.previous)
            self.assertIsNot(retained, self.previous)
        committed = state.semantic_criteria_after_outcome(
            self.previous, {"status": "empty", "criteria": proposal},
        )
        self.assertEqual(committed, proposal)
        committed["description"] = "mutated"
        self.assertEqual(proposal["description"], "A courtroom mystery")


if __name__ == "__main__":
    unittest.main()
