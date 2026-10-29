"""Seed Voyage 4 embeddings for sample_mflix.embedded_movies.

This maintenance script does not create or modify indexes. It is a dry run unless
--apply is supplied explicitly. Run it with the approved Atlas movie URI and Voyage
configuration exported in the shell; do not commit those values.
"""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Iterator
from typing import Any
from urllib.parse import urlsplit

import voyageai
from pymongo import MongoClient, UpdateOne

MODEL = "voyage-4-large"
SOURCE_DATABASE = "sample_mflix"
SOURCE_COLLECTION = "embedded_movies"
PLOT_FIELD = "plot"
VECTOR_FIELD = "plot_embedding_voyage_4_large"
DIMENSION = 2048
DEFAULT_BATCH_SIZE = 64
MAX_BATCH_SIZE = 128


def required_environment(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def validate_base_url(value: str) -> str:
    parsed = urlsplit(value)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
    ):
        raise RuntimeError("VOYAGE_URL must be an HTTPS API base URL without credentials")
    return value.rstrip("/")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write embeddings to MongoDB; without this flag only a dry run is performed.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Process at most this many source documents.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help=f"Voyage batch size, from 1 to {MAX_BATCH_SIZE} (default: {DEFAULT_BATCH_SIZE}).",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Regenerate documents that already have the new vector field.",
    )
    args = parser.parse_args()
    if args.limit is not None and args.limit <= 0:
        parser.error("--limit must be positive")
    if not 1 <= args.batch_size <= MAX_BATCH_SIZE:
        parser.error(f"--batch-size must be between 1 and {MAX_BATCH_SIZE}")
    return args


def source_filter(replace: bool) -> dict[str, Any]:
    criteria: dict[str, Any] = {
        PLOT_FIELD: {"$type": "string", "$regex": r"\S"},
    }
    if not replace:
        criteria[VECTOR_FIELD] = {"$exists": False}
    return criteria


def documents(
    collection: Any, *, replace: bool, limit: int | None,
) -> Iterator[dict[str, Any]]:
    cursor = collection.find(
        source_filter(replace),
        {"_id": 1, PLOT_FIELD: 1},
        batch_size=DEFAULT_BATCH_SIZE,
    )
    if limit is not None:
        cursor = cursor.limit(limit)
    try:
        yield from cursor
    finally:
        cursor.close()


def finite_vectors(vectors: Any, expected: int) -> list[list[float]]:
    if not isinstance(vectors, list) or len(vectors) != expected:
        raise RuntimeError("Voyage returned an unexpected embedding batch")
    normalized: list[list[float]] = []
    for vector in vectors:
        if not isinstance(vector, list) or len(vector) != DIMENSION:
            raise RuntimeError("Voyage returned an unexpected embedding dimension")
        if not all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in vector):
            raise RuntimeError("Voyage returned a non-numeric embedding")
        normalized.append([float(value) for value in vector])
    return normalized


def main() -> int:
    args = parse_args()
    movies_uri = required_environment("MOVIES_MONGODB_URI")
    api_key = required_environment("VOYAGE_API_KEY")
    base_url = validate_base_url(required_environment("VOYAGE_URL"))

    client = MongoClient(movies_uri, connect=False)
    voyage = voyageai.Client(
        api_key=api_key,
        base_url=base_url,
        timeout=30,
        max_retries=0,
    )
    collection = client[SOURCE_DATABASE][SOURCE_COLLECTION]
    processed = 0
    written = 0

    try:
        batch: list[dict[str, Any]] = []
        for document in documents(collection, replace=args.replace, limit=args.limit):
            batch.append(document)
            if len(batch) == args.batch_size:
                written += process_batch(
                    voyage, collection, batch, apply=args.apply, replace=args.replace,
                )
                processed += len(batch)
                batch.clear()
        if batch:
            written += process_batch(
                voyage, collection, batch, apply=args.apply, replace=args.replace,
            )
            processed += len(batch)
    finally:
        close = getattr(voyage, "close", None)
        if callable(close):
            close()
        client.close()

    mode = "applied" if args.apply else "dry-run"
    print(f"{mode}: processed={processed} written={written} field={VECTOR_FIELD} model={MODEL}")
    return 0


def process_batch(
    voyage: Any,
    collection: Any,
    batch: list[dict[str, Any]],
    *,
    apply: bool,
    replace: bool,
) -> int:
    response = voyage.embed(
        [document[PLOT_FIELD] for document in batch],
        model=MODEL,
        input_type="document",
        output_dimension=DIMENSION,
        output_dtype="float",
        truncation=False,
    )
    vectors = finite_vectors(getattr(response, "embeddings", None), len(batch))
    if not apply:
        return len(batch)

    operations = []
    for document, vector in zip(batch, vectors, strict=True):
        selector = {"_id": document["_id"]}
        if not replace:
            selector[VECTOR_FIELD] = {"$exists": False}
        operations.append(UpdateOne(selector, {"$set": {VECTOR_FIELD: vector}}))
    result = collection.bulk_write(operations, ordered=False)
    return result.modified_count


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
    except Exception as error:
        print(f"seed failed: {type(error).__name__}: {error}", file=sys.stderr)
        raise SystemExit(1)
