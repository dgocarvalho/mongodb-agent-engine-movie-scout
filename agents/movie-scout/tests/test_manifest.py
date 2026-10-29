"""Nonsecret manifest guardrails; no dotenv, provider or database access."""

from pathlib import Path
import tomllib
import unittest

import yaml


class ManifestTests(unittest.TestCase):
    def test_explicit_sandbox_secrets_preserve_native_features(self):
        root = Path(__file__).resolve().parents[1]
        manifest = yaml.safe_load((root / "agent.yaml").read_text())
        self.assertEqual(manifest["sandboxes"]["agent"]["secrets"], ["LLM_API_KEY"])
        self.assertEqual(manifest["sandboxes"]["tool"]["secrets"],
                         ["LLM_API_KEY", "MOVIES_MONGODB_URI", "VOYAGE_API_KEY", "VOYAGE_URL"])
        self.assertEqual(manifest["sandboxes"]["tool"]["tools"],
                         ["get_current_date", "save_user_info", "recall_user_info", "search_movies",
                          "search_semantic_movies"])
        self.assertEqual(manifest["features"], {"durable_workflow": True, "memory": True})
        self.assertEqual(manifest["network"]["egress"],
                         [{"fqdn": "api.openai.com", "ports": [443]},
                          {"fqdn": "us.ai.mongodb.com", "ports": [443]},
                          {"fqdn": "democluster0.dlm4bb.mongodb.net", "ports": [443]}])
        # No allow-all or deployment linkage.
        self.assertNotIn("atlas_clusters", manifest["network"])
        for sandbox in manifest["sandboxes"].values():
            self.assertNotIn("*", sandbox["secrets"])
            self.assertNotIn("MONGODB_URI", sandbox["secrets"])
        for name in ("VOYAGE_API_KEY", "VOYAGE_URL"):
            self.assertNotIn(name, manifest["sandboxes"]["agent"]["secrets"])

    def test_semantic_dependency_and_empty_existing_placeholders(self):
        root = Path(__file__).resolve().parents[1]
        project = tomllib.loads((root / "pyproject.toml").read_text())["project"]
        self.assertEqual(project["requires-python"], ">=3.11,<3.15")
        voyage = [item for item in project["dependencies"] if item.startswith("voyageai")]
        self.assertEqual(voyage, ["voyageai==0.5.0"])
        assignments = [line.strip() for line in (root / "env.example").read_text().splitlines()
                       if line.strip() and not line.lstrip().startswith("#")]
        self.assertEqual(assignments, ["MONGODB_URI=", "MOVIES_MONGODB_URI=",
                                      "VOYAGE_API_KEY=", "VOYAGE_URL=", "LLM_API_KEY="])


if __name__ == "__main__":
    unittest.main()