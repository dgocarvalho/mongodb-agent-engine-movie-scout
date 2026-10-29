"""Offline regressions for permission attribution; never load private configuration."""

import unittest

from native_connection_audit import classify_privileges


class PermissionAttributionTests(unittest.TestCase):
    def grant(self, resource, actions):
        return {"resource": resource, "actions": actions}

    def test_exact_find_only_and_duplicate_entries(self):
        grant = self.grant({"db": "sample_mflix", "collection": "movies"}, ["find"])
        self.assertTrue(classify_privileges([grant, grant])["collection_find_only"])

    def test_unrelated_mutations_are_not_movie_mutations(self):
        result = classify_privileges([
            self.grant({"db": "sample_mflix", "collection": "movies"}, ["find"]),
            self.grant({"db": "operational", "collection": ""}, ["insert", "update"]),
            self.grant({"cluster": True}, ["dropCollection"]),
        ])
        self.assertTrue(result["movie_actions"]["find"])
        self.assertFalse(result["movie_actions"]["insert"])
        self.assertFalse(result["movie_actions"]["dropCollection"])
        self.assertFalse(result["collection_find_only"])

    def test_false_any_resource_does_not_grant_global_access(self):
        result = classify_privileges([
            self.grant({"anyResource": False}, ["insert"]),
        ])
        self.assertFalse(result["movie_actions"]["insert"])
        self.assertFalse(result["all_resource_forms_understood"])

    def test_wildcards_and_any_action_apply_only_to_matching_resources(self):
        for resource in ({"db": "", "collection": ""},
                         {"db": "sample_mflix", "collection": ""},
                         {"db": "", "collection": "movies"}, {"anyResource": True}):
            with self.subTest(resource=resource):
                result = classify_privileges([self.grant(resource, ["anyAction"])])
                self.assertTrue(all(result["movie_actions"].values()))
                self.assertFalse(result["collection_find_only"])
        result = classify_privileges([
            self.grant({"db": "elsewhere", "collection": "movies"}, ["anyAction"])])
        self.assertFalse(any(result["movie_actions"].values()))

    def test_empty_missing_and_malformed_fail_closed(self):
        for grants in (None, [], {}, [None], [self.grant({}, ["find"])],
                       [self.grant({"db": "sample_mflix", "collection": "movies"}, "find")]):
            with self.subTest(grants=grants):
                self.assertFalse(classify_privileges(grants)["collection_find_only"])


if __name__ == "__main__":
    unittest.main()