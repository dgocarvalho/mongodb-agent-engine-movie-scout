"""Offline safety checks for the explicitly opt-in fixture utility."""

import contextlib
import io
import unittest
from unittest.mock import MagicMock, patch

import native_v17_fixture as fixture


class V17FixtureTests(unittest.TestCase):
    def run_fixture(self, exists=True, recalled=True):
        client = MagicMock()
        stored = {"content": fixture.TEXT, "metadata": {"synthetic": True}}
        client.get_semantic.side_effect = [stored if exists else None, stored]
        client.build_context.return_value.model_dump_json.return_value = (
            fixture.TEXT if recalled else "{}"
        )
        actor = {"org_id": "test-org", "user_id": "test-user",
                 "project_id": "test-project", "session_id": "test-session"}
        with patch.object(fixture, "execution", return_value=actor), \
                patch.object(fixture, "native_memory", return_value=client), \
                patch.object(fixture.logging, "disable"), \
                contextlib.redirect_stdout(io.StringIO()):
            try:
                fixture.run()
            finally:
                client.close.assert_called_once()
        return client, actor

    def test_existing_fixture_never_written_or_deleted(self):
        client, actor = self.run_fixture()
        client.create_semantic.assert_not_called()
        self.assertFalse(any("delete" in call[0] for call in client.mock_calls))
        for call in client.get_semantic.call_args_list:
            self.assertEqual(call.kwargs, {
                "label": fixture.LABEL,
                **{key: actor[key] for key in ("org_id", "user_id", "project_id")},
            })

    def test_new_fixture_single_private_create_no_upsert(self):
        client, actor = self.run_fixture(exists=False)
        client.create_semantic.assert_called_once()
        args = client.create_semantic.call_args.kwargs
        self.assertIs(args["upsert"], False)
        self.assertEqual(args["text"], fixture.TEXT)
        self.assertEqual(args["visibility"], "private")
        self.assertEqual(args["user_id"], actor["user_id"])
        self.assertEqual(args["metadata"], {"synthetic": True, "test": "V17"})

    def test_healthy_empty_recall_does_not_pass(self):
        with self.assertRaisesRegex(AssertionError, "V17_FIXTURE_NOT_RECALLED"):
            self.run_fixture(recalled=False)


if __name__ == "__main__":
    unittest.main()