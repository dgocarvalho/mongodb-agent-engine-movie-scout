"""Opt-in, single authorized synthetic fixture; never imported by application/tests.

Run explicitly from repository root. Uses the existing native memory HTTP SDK, not
database access. No deletion, other-user discovery, environment-file reads or raw logs.
The fixed prior execution establishes attribution; no user identity is guessed.
"""

import json
import logging
import subprocess
import urllib.request

from agent_engine_sdk_memory._client import MemoryClient

LABEL = "movie_scout_v17_synthetic_20261021"
TEXT = (
    "SYNTHETIC V17 TEST DATA: This test user prefers only silent comedies "
    "released before 1930 and avoids Batman movies."
)
PRIOR = "db397c5a-e51f-42a8-ba93-304b13723ebd"


def execution():
    with urllib.request.urlopen(
        f"http://localhost:3000/api/v1/executions/{PRIOR}", timeout=15
    ) as response:
        value = json.load(response)["execution"]
    assert value["status"] == "completed"
    assert value["session_id"] == "e7c28897-9316-4034-9892-53d65ddf8bed"
    assert all(value.get(key) for key in ("user_id", "org_id", "project_id"))
    return value


def native_memory():
    cid = subprocess.run(
        ["docker", "ps", "-q", "--filter", "label=com.docker.compose.project=movie-scout",
         "--filter", "label=com.docker.compose.service=memory-server"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    assert cid and "\n" not in cid
    info = json.loads(subprocess.run(
        ["docker", "inspect", cid], capture_output=True, text=True, check=True,
    ).stdout)[0]
    assert info["State"]["Health"]["Status"] == "healthy"
    port = info["NetworkSettings"]["Ports"]["8081/tcp"][0]["HostPort"]
    # Exact SDK used by runner's create_memory_client. Direct local service path
    # is explicitly documented by its api_prefix parameter; no auth is invented.
    return MemoryClient(base_url=f"http://127.0.0.1:{port}", api_prefix="/api/v1", timeout=30)


def run():
    logging.disable(logging.CRITICAL)
    actor = execution()
    scope = {key: actor[key] for key in ("org_id", "user_id", "project_id")}
    client = native_memory()
    try:
        existing = client.get_semantic(label=LABEL, **scope)
        if existing is None:
            result = client.create_semantic(
                label=LABEL, text=TEXT, source="authorized_synthetic_v17_test",
                visibility="private", metadata={"synthetic": True, "test": "V17"},
                upsert=False, **scope,
            )
            print("fixture_created", bool(result.id))
        else:
            # Never replace existing memory or create a duplicate on rerun.
            assert TEXT in json.dumps(existing, default=str)
            print("fixture_already_exists", True)
        stored = client.get_semantic(label=LABEL, **scope)
        assert stored is not None and TEXT in json.dumps(stored, default=str)
        print("fixture_stored_exact", True)
        context = client.build_context(
            query="What cinema preferences does this test user have? Silent comedies before 1930 and Batman",
            session_id=actor["session_id"], enabled_sources={"semantic"},
            include_memories=True, top_k=5, max_tokens=2000, **scope,
        )
        recalled = TEXT in context.model_dump_json()
        print("healthy_sdk_context_returned", True)
        print("fixture_recalled", recalled)
        assert recalled, "V17_FIXTURE_NOT_RECALLED"
    finally:
        client.close()


if __name__ == "__main__":
    try:
        run()
    except Exception as error:
        # Fixed allowlisted category only. No error repr, payload, host or identity.
        print("v17_fixture_check", "FAILED", type(error).__name__)
        raise SystemExit(1) from None