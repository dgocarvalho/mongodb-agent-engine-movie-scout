"""Offline public configuration checks; never start a stack or load private values."""

from pathlib import Path
import unittest

import yaml


SCAFFOLD = Path(__file__).parent / "scaffolds" / "t043-isolation"


class IsolationScaffoldTests(unittest.TestCase):
    def test_documented_local_settings(self):
        settings = yaml.safe_load((SCAFFOLD / "dev.yaml").read_text())
        self.assertEqual(settings, {"services": {
            "playground": {"port": 3301}, "mongodb": {"local": True},
        }})

    def test_test_only_manifest_has_no_movie_or_memory_credentials(self):
        manifest = yaml.safe_load((SCAFFOLD / "agent.yaml").read_text())
        self.assertEqual(manifest["name"], "movie-scout-t043-review-20261021")
        self.assertEqual(manifest["features"], {"durable_workflow": True, "memory": False})
        self.assertEqual(manifest["entrypoint"], "agent_movie_scout.main:app")
        self.assertEqual(manifest["sandboxes"]["tool"]["tools"],
                         ["get_current_date", "search_movies"])
        for sandbox in manifest["sandboxes"].values():
            self.assertEqual(sandbox["secrets"], ["LLM_API_KEY"])
        self.assertEqual(manifest["network"]["egress"],
                         [{"fqdn": "api.openai.com", "ports": [443]}])

    def test_not_a_runnable_or_credential_bearing_project(self):
        self.assertEqual({p.name for p in SCAFFOLD.iterdir()},
                         {"agent.yaml", "dev.yaml", "README.md"})
        for name in ("agent.yaml", "dev.yaml"):
            text = (SCAFFOLD / name).read_text()
            for forbidden in ("mongodb://", "mongodb+srv://", "MOVIES_MONGODB_URI",
                              "VOYAGE_API_KEY", "${", "sk-"):
                self.assertNotIn(forbidden, text)
        readme = (SCAFFOLD / "README.md").read_text()
        self.assertIn("NOT STARTUP-APPROVED", readme)
        self.assertIn("not executable fixture coverage", readme)


if __name__ == "__main__":
    unittest.main()