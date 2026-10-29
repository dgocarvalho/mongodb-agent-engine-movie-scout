"""T014: fake official-client boundary; no installed Voyage client is invoked."""

import contextlib
import io
import json
import logging
import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from test_semantic_contract import DESCRIPTION, IsolatedSemanticTest


class SemanticEmbeddingTests(IsolatedSemanticTest):
    def configured(self):
        self.stack.enter_context(patch.dict(os.environ, {
            "VOYAGE_API_KEY": "SYNTHETIC_KEY_NOT_A_CREDENTIAL",
            "VOYAGE_URL": "https://embedding.invalid/v1",
        }))

    def embed(self, remaining=6):
        return self.api("_embed_semantic_description")(
            DESCRIPTION, remaining_seconds=remaining
        )

    def test_exact_official_client_binding_and_single_unmodified_query(self):
        self.configured()
        # Purely constructed numbers: never corpus/query embeddings from a provider.
        synthetic = [0.125] * 2048
        self.provider.embed.return_value = SimpleNamespace(embeddings=[synthetic])
        result = self.embed()
        self.assertEqual(result, synthetic)
        self.provider_constructor.assert_called_once()
        binding = self.provider_constructor.call_args.kwargs
        self.assertEqual(binding["api_key"], "SYNTHETIC_KEY_NOT_A_CREDENTIAL")
        self.assertEqual(binding["base_url"], "https://embedding.invalid/v1")
        self.assertEqual(binding["max_retries"], 0)
        self.assertGreater(binding["timeout"], 0)
        self.assertLessEqual(binding["timeout"], 6)
        self.provider.embed.assert_called_once_with(
            [DESCRIPTION], model="voyage-4-large", input_type="query",
            output_dimension=2048, output_dtype="float", truncation=False,
        )
        self.provider.close.assert_called_once()
        self.db.assert_not_called()

    def test_local_remaining_budget_limits_supported_timeout_without_global_claim(self):
        self.configured()
        self.provider.embed.return_value = SimpleNamespace(embeddings=[[0.125] * 2048])
        self.embed(remaining=0.75)
        timeout = self.provider_constructor.call_args.kwargs["timeout"]
        self.assertGreater(timeout, 0)
        self.assertLessEqual(timeout, 0.75)
        self.provider_constructor.reset_mock()
        self.provider.embed.reset_mock()
        with self.assertRaises(Exception):
            self.embed(remaining=0)
        self.provider_constructor.assert_not_called()
        self.provider.embed.assert_not_called()

    def test_missing_blank_or_invalid_binding_cannot_trigger_sdk_defaults(self):
        embed = self.api("_embed_semantic_description")
        for key, url in ((None, None), ("", "https://embedding.invalid/v1"),
                         (" \t", "https://embedding.invalid/v1"), ("synthetic", None),
                         ("synthetic", ""), ("synthetic", " \t"),
                         ("synthetic", "http://embedding.invalid/v1"),
                         ("synthetic", "not-a-url")):
            values = {}
            if key is not None:
                values["VOYAGE_API_KEY"] = key
            if url is not None:
                values["VOYAGE_URL"] = url
            with self.subTest(binding="synthetic"), patch.dict(os.environ, values, clear=True):
                with self.assertRaises(Exception):
                    embed(DESCRIPTION, remaining_seconds=6)
        self.provider_constructor.assert_not_called()
        self.provider.embed.assert_not_called()
        self.db.assert_not_called()

    def test_invalid_vectors_rejected_without_retry_fallback_or_database(self):
        self.configured()
        embed = self.api("_embed_semantic_description")
        invalid = [[], [[0.125] * 2047], [[0.125] * 2049],
                   [[0.125] * 2048, [0.125] * 2048]]
        invalid.extend([[bad] + [0.125] * 2047] for bad in
                       (True, "0.1", None, float("nan"), float("inf"), -float("inf")))
        for embeddings in invalid:
            self.provider.embed.reset_mock()
            self.provider.embed.return_value = SimpleNamespace(embeddings=embeddings)
            with self.subTest(shape="constructed-invalid"), self.assertRaises(Exception):
                embed(DESCRIPTION, remaining_seconds=6)
            self.provider.embed.assert_called_once()
        self.db.assert_not_called()

    def test_readiness_false_is_unavailable_before_provider_or_database(self):
        self.api("search_semantic_movie_results")
        with patch.object(self.tools, "_semantic_ready", return_value=False, create=True):
            self.assert_failure(self.search({"description": DESCRIPTION}), "unavailable")
        self.provider_constructor.assert_not_called()
        self.provider.embed.assert_not_called()
        self.db.assert_not_called()

    def test_provider_failure_sanitized_no_raw_payload_logs_vectors_or_retries(self):
        self.configured()
        self.ready()
        self.api("search_semantic_movie_results")
        marker = "SYNTHETIC_PRIVATE_PROVIDER_PAYLOAD"
        self.provider.embed.side_effect = RuntimeError(marker)
        output = io.StringIO()
        handler = logging.StreamHandler(output)
        logger = logging.getLogger()
        logger.addHandler(handler)
        self.addCleanup(logger.removeHandler, handler)
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            result = self.search({"description": DESCRIPTION})
        self.assert_failure(result, "unavailable")
        text = json.dumps(result) + output.getvalue()
        self.assertIn("stage=provider_request code=error", output.getvalue())
        for forbidden in (marker, "SYNTHETIC_KEY_NOT_A_CREDENTIAL", "embedding.invalid",
                          "queryVector", "plot_embedding_voyage_4_large"):
            self.assertNotIn(forbidden, text)
        self.provider.embed.assert_called_once()
        self.provider_constructor.assert_called_once()
        self.provider.close.assert_called_once()
        self.db.assert_not_called()


if __name__ == "__main__":
    unittest.main()