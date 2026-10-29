"""T013: proposed semantic filters on G2 indexed paths, never live queries."""

import unittest

from test_semantic_contract import DESCRIPTION, IsolatedSemanticTest


class SemanticFilterTests(IsolatedSemanticTest):
    def validate(self, **values):
        return self.api("validate_semantic_arguments")({"description": DESCRIPTION, **values})

    def test_aliases_modes_genre_bounds_and_unknown_values(self):
        criteria = self.validate(genres=["science fiction", "ACTION", "Action"])
        self.assertEqual(criteria["genres"], ["Sci-Fi", "Action"])
        self.assertEqual(criteria["genre_mode"], "all")
        self.assertEqual(len(self.validate(genres=list(self.tools.GENRES[:10]))["genres"]), 10)
        self.assertEqual(self.validate(genres=[])["genres"], [])
        for genres in ("Drama", [True], [""], [" \t"], ["x" * 81],
                       ["Drama"] * 11, ["unknown"], ["Drama", "unknown"]):
            with self.subTest(genres=genres), self.assertRaises(ValueError):
                self.validate(genres=genres)
        # A value at the character bound is not permission to invent a genre alias.
        with self.assertRaises(ValueError):
            self.validate(genres=["x" * 80])
        for mode in ("xor", True, [], "any"):
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                self.validate(genre_mode=mode)

    def test_strict_interval_invalid_matrix_before_io(self):
        validate = self.api("validate_semantic_arguments")
        invalid = []
        for dimension, bad in (
            ("year", (True, "2000", 2000.0, 0, 10000, [], float("nan"), float("inf"))),
            ("rating", (True, "8", [], -1, 11, float("nan"), float("inf"), -float("inf"))),
        ):
            for endpoint in ("min", "max"):
                invalid.extend({dimension: {endpoint: value}} for value in bad)
            invalid.extend({dimension: value} for value in (True, [], "range", {}))
            invalid.extend({dimension: {"min": 8, "max": 7}} for _ in range(1))
            for flag in ("min_inclusive", "max_inclusive"):
                invalid.extend({dimension: {"min": 7, flag: value}}
                               for value in (1, 0, "true", None))
                invalid.append({dimension: {"min": 7, "max": 7, flag: False}})
            invalid.append({dimension: {"min": 7, "extra": 1}})
        for values in invalid:
            with self.subTest(values=values), self.assertRaises(ValueError):
                validate({"description": DESCRIPTION, **values})
        self.db.assert_not_called()
        self.provider_constructor.assert_not_called()

    def test_valid_domains_zero_rating_null_clear_and_inclusive_defaults(self):
        criteria = self.validate(year={"min": 1, "max": 9999}, rating={"min": 0, "max": 10})
        for dimension in ("year", "rating"):
            self.assertIs(criteria[dimension]["min_inclusive"], True)
            self.assertIs(criteria[dimension]["max_inclusive"], True)
        self.assertEqual(criteria["rating"]["min"], 0)
        self.assertEqual(self.validate(year=None, rating=None)["year"], None)
        self.assertEqual(self.validate(rating={"min": 7.5, "max": 7.5})["rating"]["min"], 7.5)

    def test_g2_all_any_predicates_exact_paths_no_unsupported_all_or_postfilter(self):
        predicate = self.api("semantic_filter_predicate")
        for mode, genre_clause in (
            ("all", {"$and": [{"genres": {"$eq": "Action"}}, {"genres": {"$eq": "Sci-Fi"}}]}),
            ("any", {"genres": {"$in": ["Action", "Sci-Fi"]}}),
        ):
            criteria = self.validate(genres=["Action", "science fiction"], genre_mode=mode,
                                     year={"min": 2000, "max": 2010, "min_inclusive": False},
                                     rating={"min": 0, "max": 8, "max_inclusive": False})
            self.assertEqual(predicate(criteria), {"$and": [
                genre_clause, {"year": {"$gt": 2000, "$lte": 2010}},
                {"imdb.rating": {"$gte": 0, "$lt": 8}},
            ]})
        for lower, upper in ((True, True), (True, False), (False, True), (False, False)):
            for dimension, path in (("year", "year"), ("rating", "imdb.rating")):
                criteria = self.validate(**{dimension: {
                    "min": 2, "max": 8, "min_inclusive": lower, "max_inclusive": upper,
                }})
                self.assertEqual(predicate(criteria), {path: {
                    "$gte" if lower else "$gt": 2, "$lte" if upper else "$lt": 8,
                }})
        self.assertEqual(predicate(self.validate()), {})


if __name__ == "__main__":
    unittest.main()