"""Opt-in native semantic trace assertions with sanitized bounded output.

This module never starts services, reads environment variables, probes writes, or runs
during unit-test discovery. Its CLI only observes explicitly supplied session IDs from
the established local Agent Engine endpoint.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from collections.abc import Mapping, Sequence
from typing import Any, Literal


BASE_URL = "http://localhost:3000"
SEMANTIC_SOURCE = "sample_mflix.embedded_movies"
MAX_RESULTS = 10
Origin = Literal["real_catalog", "synthetic_fixture"]


class NativeObservationError(ValueError):
    """Native evidence is malformed, unsafe, or outside the fixed observation scope."""


def _decode(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            raise NativeObservationError() from None
    return value


def _tool_names(value: Any) -> list[str]:
    names: list[str] = []
    for item in value if isinstance(value, list) else []:
        if not isinstance(item, Mapping):
            continue
        function = item.get("function")
        name = (
            function.get("name") if isinstance(function, Mapping)
            else item.get("name") or item.get("title")
        )
        if isinstance(name, str) and name:
            names.append(name)
    return names


def _record_facts(record: Any, origin: Origin) -> dict[str, Any]:
    if not isinstance(record, Mapping):
        raise NativeObservationError() from None
    source_id = record.get("source_id")
    title = record.get("title")
    plot = record.get("plot")
    if not all(isinstance(value, str) and value.strip() for value in (source_id, title, plot)):
        raise NativeObservationError() from None
    if origin == "real_catalog" and not source_id.startswith("objectId:"):
        raise NativeObservationError() from None
    if origin == "synthetic_fixture" and not source_id.startswith("string:synthetic-"):
        raise NativeObservationError() from None
    return {
        "source_id": source_id,
        "title": title,
        "plot": plot,
        "genres": record.get("genres"),
        "year": record.get("year"),
        "imdb_rating": record.get("imdb_rating"),
    }


def compare_records(
    observed: Sequence[Mapping[str, Any]],
    expected: Sequence[Mapping[str, Any]],
    *,
    origin: Origin,
) -> dict[str, Any]:
    """Compare bounded allowlisted facts without performing source or provider I/O."""
    if origin not in ("real_catalog", "synthetic_fixture"):
        raise NativeObservationError() from None
    if not 0 < len(observed) <= MAX_RESULTS or len(observed) != len(expected):
        raise NativeObservationError() from None
    actual_facts = [_record_facts(record, origin) for record in observed]
    expected_facts = [_record_facts(record, origin) for record in expected]
    if actual_facts != expected_facts:
        raise NativeObservationError() from None
    if len({record["source_id"] for record in actual_facts}) != len(actual_facts):
        raise NativeObservationError() from None
    return {"origin": origin, "records": len(actual_facts)}


def _validated_outcome(value: Any, origin: Origin) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    outcome = _decode(value)
    if not isinstance(outcome, dict) or outcome.get("source") != SEMANTIC_SOURCE:
        raise NativeObservationError() from None
    status = outcome.get("status")
    if status not in ("ok", "empty", "invalid", "unavailable"):
        raise NativeObservationError() from None
    movies = outcome.get("movies")
    returned = outcome.get("returned_count")
    effective = outcome.get("effective_limit")
    if not isinstance(movies, list) or type(returned) is not int or returned != len(movies):
        raise NativeObservationError() from None
    if returned < 0 or returned > MAX_RESULTS:
        raise NativeObservationError() from None
    if effective is not None and (
        type(effective) is not int or effective < 1 or effective > MAX_RESULTS or returned > effective
    ):
        raise NativeObservationError() from None
    if (status == "ok") != bool(movies):
        raise NativeObservationError() from None
    records = [_record_facts(record, origin) for record in movies]
    if len({record["source_id"] for record in records}) != len(records):
        raise NativeObservationError() from None
    return outcome, records


def observe_native_session(rows: Sequence[Mapping[str, Any]], *, origin: Origin) -> dict[str, Any]:
    """Assert one semantic call and return only a sanitized evidence summary."""
    if origin not in ("real_catalog", "synthetic_fixture") or not rows:
        raise NativeObservationError() from None
    if not all(isinstance(row, Mapping) for row in rows):
        raise NativeObservationError() from None
    execution_ids = {row.get("execution_id") for row in rows}
    if len(execution_ids) != 1 or not all(isinstance(value, str) and value for value in execution_ids):
        raise NativeObservationError() from None
    execution_id = next(iter(execution_ids))

    started_calls = [
        row.get("tool") for row in rows
        if row.get("status") == "started" and row.get("tool") != "invoke_llm"
    ]
    if started_calls != ["search_semantic_movies"]:
        raise NativeObservationError() from None

    schemas: list[list[str]] = []
    for row in rows:
        if row.get("status") != "started" or row.get("tool") != "invoke_llm":
            continue
        inputs = _decode(row.get("input") if row.get("input") is not None else row.get("inputs"))
        if isinstance(inputs, Mapping):
            schemas.append(_tool_names(inputs.get("tools")))
    if not schemas or not any("search_semantic_movies" in names for names in schemas):
        raise NativeObservationError() from None
    if any({"save_user_info", "recall_user_info"} & set(names) for names in schemas):
        raise NativeObservationError() from None

    outcomes = [
        row.get("output") for row in rows
        if row.get("status") == "success" and row.get("tool") == "search_semantic_movies"
    ]
    if len(outcomes) != 1:
        raise NativeObservationError() from None
    outcome, records = _validated_outcome(outcomes[0], origin)

    model_outputs = []
    for row in rows:
        if row.get("status") == "success" and row.get("tool") == "invoke_llm":
            decoded = _decode(row.get("output"))
            if isinstance(decoded, Mapping) and isinstance(decoded.get("content"), str):
                model_outputs.append(decoded["content"])
    if not model_outputs or not model_outputs[-1].strip():
        raise NativeObservationError() from None
    final_text = model_outputs[-1].casefold()

    return {
        "origin": origin,
        "execution_id": execution_id,
        "tool_calls": started_calls,
        "status": outcome["status"],
        "source": SEMANTIC_SOURCE,
        "returned_count": outcome["returned_count"],
        "effective_limit": outcome.get("effective_limit"),
        "shortfall": outcome.get("shortfall"),
        "source_ids": [record["source_id"] for record in records],
        "titles": [record["title"] for record in records],
        "final_grounding_titles_present": all(
            record["title"].casefold() in final_text for record in records
        ),
        "profile_calls": 0,
    }


def fetch_session(session_id: str) -> list[dict[str, Any]]:
    """Read an explicitly named local session; never invoke or mutate the stack."""
    if not isinstance(session_id, str) or not session_id.strip() or len(session_id) > 200:
        raise NativeObservationError() from None
    query = urllib.parse.urlencode({"session_id": session_id})
    with urllib.request.urlopen(f"{BASE_URL}/api/v1/execution-logs?{query}", timeout=20) as response:
        payload = json.load(response)
    rows = payload.get("logs") if isinstance(payload, Mapping) else None
    if not isinstance(rows, list) or len(rows) > 500:
        raise NativeObservationError() from None
    return rows


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Observe existing native semantic sessions")
    parser.add_argument("--session-id", action="append", required=True)
    parser.add_argument("--origin", choices=("real_catalog", "synthetic_fixture"), required=True)
    arguments = parser.parse_args(argv)
    try:
        summaries = [
            observe_native_session(fetch_session(session_id), origin=arguments.origin)
            for session_id in arguments.session_id
        ]
    except Exception as error:
        print(json.dumps({"native_semantic_observation": "FAILED_SANITIZED",
                          "category": type(error).__name__}))
        return 1
    print(json.dumps({"native_semantic_observation": "PASS", "sessions": summaries},
                     sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())