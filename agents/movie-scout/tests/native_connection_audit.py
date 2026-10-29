"""Opt-in local connection audit. Fixed reads only; stdout is categories/booleans.

Run with the project's interpreter from the repository root. Private values are
read internally, never returned. No main import, dotenv mutation, writes or restart.
The host control takes its URI from the exact agent dotenv, NOT the tool process.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
import subprocess
import sys
from typing import Any


def classify_privileges(privileges: Any) -> dict[str, Any]:
    """Attribute actions only to matching resources; never infer grants from reads."""
    actions = {name: False for name in ("find", "insert", "update", "remove", "dropCollection")}
    valid = isinstance(privileges, list) and bool(privileges)
    exact_only = valid
    extra = False
    for grant in privileges if isinstance(privileges, list) else []:
        if not isinstance(grant, dict):
            valid = False
            continue
        resource, granted = grant.get("resource"), grant.get("actions")
        if not isinstance(resource, dict) or not isinstance(granted, list) or not granted or not all(
            isinstance(action, str) and action for action in granted
        ):
            valid = False
            continue
        exact = resource == {"db": "sample_mflix", "collection": "movies"}
        namespace = set(resource) == {"db", "collection"} and all(
            isinstance(resource[key], str) for key in ("db", "collection"))
        universal = resource == {"anyResource": True}
        cluster = resource == {"cluster": True}
        if not (namespace or universal or cluster):
            valid = False
        matches = universal or (namespace and resource["db"] in ("", "sample_mflix")
                                and resource["collection"] in ("", "movies"))
        for action in actions:
            actions[action] |= bool(matches and (action in granted or "anyAction" in granted))
        extra |= not exact
        exact_only &= exact and set(granted) == {"find"}
    return {"all_resource_forms_understood": valid, "collection_find_only": bool(valid and exact_only),
            "extra_resources": extra, "movie_actions": actions}


def principal(uri: str) -> tuple[Any, Any]:
    """Use the driver's resolved authSource, including SRV TXT/default handling."""
    from pymongo import MongoClient, timeout

    with timeout(10):
        client = MongoClient(uri, connect=False)
        try:
            credentials = client.options.pool_options._credentials
            if credentials is None:
                return None, None  # Native local operational MongoDB can be unauthenticated.
            return credentials.username, credentials.source
        finally:
            client.close()


def inspect_connection(uri: str, expected: tuple[Any, Any]) -> dict[str, Any]:
    from pymongo import MongoClient, monitoring, timeout

    result: dict[str, Any] = {}
    events: list[tuple[str, dict[str, Any], str]] = []

    class Listener(monitoring.CommandListener):
        def started(self, event):
            events.append((event.command_name, dict(event.command), event.database_name))

        def succeeded(self, event):
            pass

        def failed(self, event):
            pass

    client = None
    try:
        with timeout(10):
            client = MongoClient(uri, connect=False, event_listeners=[Listener()])
            try:
                with timeout(5):
                    cursor = client["sample_mflix"]["movies"].find({}, {"_id": 1}).limit(1)
                    try:
                        cursor.batch_size(1).max_time_ms(5000)
                        result["document_present"] = bool(list(cursor))
                        result["read"] = "READ_OK"
                    finally:
                        cursor.close()
            except Exception as error:
                result["read"] = type(error).__name__
            try:
                with timeout(5):
                    info = client.admin.command({"connectionStatus": 1, "showPrivileges": True})
                auth = info.get("authInfo", {})
                users = auth.get("authenticatedUsers", [])
                privileges = auth.get("authenticatedUserPrivileges")
                result["resource_shapes"] = sorted({
                    ",".join(sorted(key for key in grant.get("resource", {})
                                    if key in {"db", "collection", "cluster", "anyResource"}))
                    for grant in privileges if isinstance(grant, dict)
                }) if isinstance(privileges, list) else []
                result["authenticated_user_count"] = len(users)
                result["single_expected_principal"] = users == [
                    {"user": expected[0], "db": expected[1]}]
                result.update(classify_privileges(privileges))
                result["metadata"] = "METADATA_OK"
            except Exception as error:
                result["metadata"] = type(error).__name__
    except Exception as error:
        result["connection"] = type(error).__name__
    finally:
        if client is not None:
            client.close()
        result["client_closed"] = client is not None
    finds = [(command, db) for name, command, db in events if name == "find"]
    result["one_bounded_catalog_find"] = len(finds) == 1 and all(
        db == "sample_mflix" and command.get("find") == "movies"
        and command.get("filter") == {} and command.get("projection") == {"_id": 1}
        and command.get("limit") == 1 and 0 < command.get("maxTimeMS", 0) <= 5000
        and 0 < command.get("batchSize", 0) <= 2 for command, db in finds)
    result["one_metadata_command"] = sum(name == "connectionStatus" for name, _, _ in events) == 1
    internal = {"hello", "isMaster", "ismaster", "saslStart", "saslContinue", "authenticate",
                "getnonce", "endSessions", "killCursors"}
    result["unexpected_application_command"] = any(
        name not in internal | {"find", "connectionStatus"} for name, _, _ in events)
    return result


def native_audit(payload: dict[str, Any]) -> dict[str, Any]:
    """Fresh process; inspect same factory used by the registered SDK tool."""
    logging.disable(logging.CRITICAL)
    from unittest.mock import patch

    from agent_engine_sdk_langgraph import App
    from pymongo import MongoClient, monitoring
    from agent_movie_scout import tools

    movie_uri = os.environ["MOVIES_MONGODB_URI"]
    expected = tuple(payload["expected_principal"])
    result = {"native_movie_matches_private_file": movie_uri == payload["private_movie_uri"],
              "native_operational_matches_private_file":
                  os.environ.get("MONGODB_URI") == payload["private_operational_uri"],
              "native_principal_matches_private_file": principal(movie_uri) == expected}
    operational = os.environ.get("MONGODB_URI")
    if operational:
        from urllib.parse import urlsplit

        other = principal(operational)
        result["native_operational_targets_local_stack_service"] = (
            urlsplit(operational).hostname == "mongodb")
        result["native_operational_authentication_configured"] = other[0] is not None
        result["native_movie_operational_principals_distinct"] = principal(movie_uri) != other
        result["native_movie_operational_usernames_distinct"] = expected[0] != other[0]
    result["native_fresh_movie_connection"] = inspect_connection(movie_uri, expected)
    # Do not import main: it loads dotenv and constructs platform state. This is a
    # real SDK registered-tool invocation in TOOL mode, not an OE/model execution.
    events = []
    factory_matches = []

    class Listener(monitoring.CommandListener):
        def started(self, event):
            if event.command_name == "find":
                command = event.command
                events.append(event.database_name == "sample_mflix"
                              and command.get("find") == "movies"
                              and command.get("projection") == tools.MOVIE_PROJECTION
                              and command.get("limit") == 1
                              and 0 < command.get("maxTimeMS", 0) <= 5000)

        def succeeded(self, event):
            pass

        def failed(self, event):
            pass

    def factory(uri, **kwargs):
        factory_matches.append(uri == payload["private_movie_uri"])
        return MongoClient(uri, event_listeners=[Listener()], **kwargs)

    app = App(app_name="Movie Scout connection audit")
    try:
        tools.register(app)
        search = next(tool for tool in app.get_tools() if tool.name == "search_movies")
        with patch.object(tools, "MongoClient", side_effect=factory):
            outcome = json.loads(search.invoke({"title": "Batman Begins", "requested_limit": 1}))
        result["registered_tool_status"] = outcome["status"]
        result["registered_tool_factory_uses_private_movie_uri"] = factory_matches == [True]
        result["registered_tool_one_bounded_catalog_find"] = events == [True]
        result["registered_tool_cache_reuses_own_client"] = tools._get_movie_client() is tools._movie_client
    finally:
        tools._close_movie_client()
        app.close()
    return result


LAUNCHER = r'''
import json,os,subprocess,sys
from pathlib import Path
payload=json.load(sys.stdin);matches=[]
for path in Path('/proc').iterdir():
 if not path.name.isdigit():continue
 try:
  cmd=(path/'cmdline').read_bytes().split(b'\0')
  env=dict(item.split(b'=',1) for item in (path/'environ').read_bytes().split(b'\0') if b'=' in item)
  if env.get(b'RUNNER_MODE')==b'tool' and any(Path(x.decode()).name=='entrypoint.py' for x in cmd if x):
   matches.append((path,cmd,env))
 except (OSError,ValueError,UnicodeError):pass
if len(matches)!=1:
 print(json.dumps({'native_selection':'AMBIGUOUS_OR_MISSING'}));sys.exit(1)
path,cmd,env=matches[0]
safe={k.decode():v.decode() for k,v in env.items() if k in
 (b'PATH',b'PYTHONPATH',b'VIRTUAL_ENV',b'RUNNER_MODE',b'MOVIES_MONGODB_URI',b'MONGODB_URI')}
# Code and credentials travel through stdin, not argv, logs, disk or Docker config.
code=payload.pop('audit_source')
bootstrap="import sys,json; d=json.load(sys.stdin); ns={'__name__':'audit_import'}; exec(d.pop('source'),ns); print(json.dumps(ns['native_audit'](d)))"
payload['source']=code
r=subprocess.run([cmd[0].decode(),'-c',bootstrap],input=json.dumps(payload),env=safe,
 cwd=str((path/'cwd').resolve()),capture_output=True,text=True,timeout=50)
if r.returncode:
 import re
 categories=re.findall(r'^(\w+(?:Error|Exception)):',r.stderr,re.M)
 lines=re.findall(r'File "<string>", line (\d+)',r.stderr)
 print(json.dumps({'native_execution':'FAILED_SANITIZED','category':categories[-1] if categories else 'unknown','code_lines':lines}));sys.exit(1)
try:
 value=json.loads(r.stdout)
 print(json.dumps({'unique_tool_process':True,'native':value}))
except Exception:
 print(json.dumps({'native_execution':'INVALID_OUTPUT_SANITIZED'}));sys.exit(1)
'''


def main() -> None:
    from dotenv import dotenv_values

    logging.disable(logging.CRITICAL)
    root = Path(__file__).resolve().parents[3]
    agent = root / "agents/movie-scout"
    values = dotenv_values(agent / ".env", interpolate=False)
    movie_uri = values.get("MOVIES_MONGODB_URI")
    if not movie_uri or "${" in movie_uri:
        raise ValueError("PRIVATE_MOVIE_CONFIGURATION_UNVERIFIED")
    expected = principal(movie_uri)
    if expected[0] is None:
        raise ValueError("MOVIE_AUTH_CONFIGURATION_UNVERIFIED")
    result: dict[str, Any] = {
        "host_environment_movie_absent_or_matches_private_file":
            not os.environ.get("MOVIES_MONGODB_URI") or os.environ["MOVIES_MONGODB_URI"] == movie_uri,
        "host_fresh_private_movie_connection": inspect_connection(movie_uri, expected),
    }
    other_uri = values.get("MONGODB_URI")
    if other_uri:
        other = principal(other_uri)
        result["private_movie_operational_principals_distinct"] = expected != other
        result["private_movie_operational_usernames_distinct"] = expected[0] != other[0]
    container = subprocess.run([
        "docker", "ps", "-q", "--filter", "label=com.docker.compose.project=movie-scout",
        "--filter", "label=com.docker.compose.service=app"],
        capture_output=True, text=True, check=True, timeout=10).stdout.strip()
    if not container or "\n" in container:
        raise ValueError("APP_SELECTION_UNVERIFIED")
    payload = {"private_movie_uri": movie_uri, "private_operational_uri": other_uri,
               "expected_principal": expected, "audit_source": Path(__file__).read_text()}
    native = subprocess.run(["docker", "exec", "-i", container, "python", "-c", LAUNCHER],
                            input=json.dumps(payload), capture_output=True, text=True, timeout=60)
    result["native_execution_ok"] = native.returncode == 0
    result.update(json.loads(native.stdout))
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    try:
        main()
    except Exception as error:
        print(json.dumps({"audit": "FAILED_SANITIZED", "category": type(error).__name__}))
        sys.exit(1)