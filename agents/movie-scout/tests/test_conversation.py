"""Offline criteria transitions; no runtime, secrets, network or memory access."""

import json
import unittest

from agent_movie_scout import state


class ConversationStateTests(unittest.TestCase):
    def test_semantic_state_contract_is_separate_serializable_and_safe_for_old_sessions(self):
        self.assertIn("active_semantic_criteria", state.HelloWorldState.__optional_keys__)
        self.assertEqual(set(state.SemanticMovieCriteria.__annotations__), {
            "description", "genres", "genre_mode", "year", "rating", "requested_limit",
        })
        first = state.safe_turn_defaults()
        first["active_semantic_criteria"]["genres"] = ["Action"]
        second = state.safe_turn_defaults()
        self.assertEqual(second["active_semantic_criteria"], {})
        self.assertEqual(json.loads(json.dumps(second))["active_semantic_criteria"], {})
        self.assertNotEqual(first["active_semantic_criteria"], first["active_movie_criteria"])

    def test_semantic_commit_copies_only_successful_complete_criteria(self):
        previous = {"description": "Earlier theme", "genres": ["Action"],
                    "requested_limit": 1}
        proposal = {"description": "New theme", "genres": ["Drama"], "genre_mode": "all",
                    "year": {"min": 2000, "min_inclusive": False}, "rating": None,
                    "requested_limit": 5}
        for status in ("invalid", "unavailable", "denied"):
            retained = state.semantic_criteria_after_outcome(
                previous, {"status": status, "criteria": proposal})
            self.assertEqual(retained, previous)
            self.assertIsNot(retained, previous)
        for status in ("ok", "empty"):
            committed = state.semantic_criteria_after_outcome(
                previous, {"status": status, "criteria": proposal})
            self.assertEqual(committed, proposal)
            committed["genres"].append("Comedy")
            committed["year"]["min"] = 1990
            self.assertEqual(proposal["genres"], ["Drama"])
            self.assertEqual(proposal["year"]["min"], 2000)
            self.assertEqual(previous["genres"], ["Action"])
            json.dumps(committed, allow_nan=False)

    def test_dimension_replacement_and_omission(self):
        old = {"genres": ["Action"], "year_min": 2015, "year_min_inclusive": False,
               "year_max": 2025, "requested_limit": 2}
        merged = state.merge_movie_criteria(old, {"year_min": 2005, "year_max": 2005})
        self.assertEqual(merged, {"genres": ["Action"], "requested_limit": 2,
                                  "year_min": 2005, "year_max": 2005})
        merged["genres"].append("Comedy")
        self.assertEqual(old["genres"], ["Action"])
        json.dumps(merged, allow_nan=False)

    def test_reset_removes_every_old_dimension(self):
        self.assertEqual(state.merge_movie_criteria(
            {"title": "Batman", "genres": ["Action"], "sort": "rating_desc"},
            {"genres": ["Comedy"]}, replace=True), {"genres": ["Comedy"]})

    def test_result_commit_only_successful_search_current_call(self):
        old = {"genres": ["Action"]}
        for status in ("invalid", "unavailable", "denied"):
            self.assertEqual(state.criteria_after_outcome(old, {
                "status": status, "criteria": {"genres": ["Comedy"]}}), old)
        for status in ("ok", "empty"):
            self.assertEqual(state.criteria_after_outcome(old, {
                "status": status, "criteria": {"genres": ["Comedy"]}}),
                {"genres": ["Comedy"]})


if __name__ == "__main__":
    unittest.main()