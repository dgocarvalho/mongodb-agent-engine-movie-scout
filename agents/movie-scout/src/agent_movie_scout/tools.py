"""Tool definitions for Movie Scout."""

from __future__ import annotations

import atexit
import json
import logging
import math
import os
import re
import threading
from collections.abc import Callable, Mapping
from datetime import datetime
from decimal import Decimal
from importlib import import_module
from time import monotonic
from typing import Any, Literal, cast
from typing_extensions import TypedDict
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import pymongo
from bson import Decimal128, ObjectId, json_util
from agent_engine_sdk_langgraph import App
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pydantic import ConfigDict, StrictBool, StrictFloat, StrictInt, StrictStr, validate_call

from agent_movie_scout.state import MovieCriteria

logger = logging.getLogger(__name__)
_movie_client: MongoClient[dict[str, Any]] | None = None
_movie_client_pid: int | None = None
_movie_client_lock = threading.Lock()
MOVIE_PROJECTION = {key: 1 for key in ("_id", "title", "year", "genres", "imdb.rating", "plot")}
GENRES = (
    "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary",
    "Drama", "Family", "Fantasy", "Film-Noir", "History", "Horror", "Music", "Musical",
    "Mystery", "News", "Romance", "Sci-Fi", "Short", "Sport", "Talk-Show", "Thriller",
    "War", "Western",
)
GENRE_ALIASES = {name.casefold(): name for name in GENRES}
GENRE_ALIASES["science fiction"] = "Sci-Fi"
SEMANTIC_SOURCE = "sample_mflix.embedded_movies"
SEMANTIC_FIELDS = {
    "description", "genres", "genre_mode", "year", "rating", "requested_limit",
}
SEMANTIC_PROJECTION = {
    "_id": 1,
    "title": 1,
    "plot": 1,
    "genres": 1,
    "year": 1,
    "imdb.rating": 1,
    "semantic_score": {"$meta": "vectorSearchScore"},
}


class SemanticInterval(TypedDict, total=False):
    min: int | float
    max: int | float
    min_inclusive: bool
    max_inclusive: bool


class SemanticCriteria(TypedDict):
    description: str
    genres: list[str]
    genre_mode: Literal["all", "any"]
    year: SemanticInterval | None
    rating: SemanticInterval | None
    requested_limit: int


class SemanticYearInput(TypedDict, total=False):
    __pydantic_config__ = ConfigDict(extra="forbid")
    min: StrictInt | None = None
    max: StrictInt | None = None
    min_inclusive: StrictBool = True
    max_inclusive: StrictBool = True


class SemanticRatingInput(TypedDict, total=False):
    __pydantic_config__ = ConfigDict(extra="forbid")
    min: StrictInt | StrictFloat | None = None
    max: StrictInt | StrictFloat | None = None
    min_inclusive: StrictBool = True
    max_inclusive: StrictBool = True


class MovieNotConfigured(Exception):
    """Dedicated movie configuration is absent; contains no secret values."""


class InvalidCriteria(ValueError):
    """Invalid structured arguments; never echo supplied input."""


class SemanticUnavailable(Exception):
    """Semantic prerequisites or provider output are not usable."""


class SemanticDiagnosticError(Exception):
    """Internal sanitized stage marker; never serialized to a tool response."""

    def __init__(self, stage: str, code: str):
        super().__init__()
        self.stage = stage
        self.code = code


class IneligibleSemanticMovie(ValueError):
    """A projected row lacks a usable semantic identity, title, or plot."""


def _log_semantic_failure(stage: str, code: str) -> None:
    logger.warning("semantic search unavailable | stage=%s code=%s", stage, code)


def _failure_code(error: Exception, default: str) -> str:
    if isinstance(error, (TimeoutError, pymongo.errors.ExecutionTimeout)):
        return "timeout"
    if isinstance(error, pymongo.errors.ServerSelectionTimeoutError):
        return "server_selection_timeout"
    if isinstance(error, pymongo.errors.NetworkTimeout):
        return "network_timeout"
    if isinstance(error, pymongo.errors.AutoReconnect):
        return "auto_reconnect"
    if isinstance(error, pymongo.errors.InvalidURI):
        return "invalid_uri"
    if isinstance(error, pymongo.errors.ConfigurationError):
        return "configuration"
    error_name = type(error).__name__.casefold()
    if "authentication" in error_name or "unauthorized" in error_name:
        return "authentication"
    if "permission" in error_name or "forbidden" in error_name:
        return "permission"
    if "ratelimit" in error_name:
        return "rate_limited"
    if "connection" in error_name or "network" in error_name:
        return "connection"
    if "badrequest" in error_name or "invalidrequest" in error_name:
        return "invalid_request"
    if isinstance(error, pymongo.errors.OperationFailure):
        return "operation_failure"
    return default


def _semantic_readiness_code() -> str | None:
    if not isinstance(os.environ.get("VOYAGE_API_KEY"), str) or not os.environ["VOYAGE_API_KEY"].strip():
        return "missing_api_key"
    try:
        _validated_semantic_url(os.environ.get("VOYAGE_URL"))
    except SemanticUnavailable:
        return "invalid_base_url"
    movie_uri = os.environ.get("MOVIES_MONGODB_URI")
    if not isinstance(movie_uri, str) or not movie_uri.strip():
        return "missing_movie_uri"
    try:
        voyageai = import_module("voyageai")
    except Exception:
        return "voyage_import_failed"
    if getattr(voyageai, "__version__", None) != "0.5.0":
        return "voyage_version_mismatch"
    return None


def _validated_semantic_url(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SemanticUnavailable() from None
    parsed = urlsplit(value.strip())
    if (
        parsed.scheme != "https" or not parsed.hostname or parsed.username is not None
        or parsed.password is not None or parsed.query or parsed.fragment
    ):
        raise SemanticUnavailable() from None
    return value.strip()


def _semantic_binding() -> tuple[str, str]:
    api_key = os.environ.get("VOYAGE_API_KEY")
    if not isinstance(api_key, str) or not api_key.strip():
        raise SemanticUnavailable() from None
    return api_key, _validated_semantic_url(os.environ.get("VOYAGE_URL"))


def _semantic_ready() -> bool:
    """Check local prerequisites without constructing clients or performing I/O."""
    return _semantic_readiness_code() is None


def _new_semantic_client(remaining_seconds: float) -> Any:
    """Construct the explicitly bound hosted client only when work is authorized."""
    api_key, base_url = _semantic_binding()
    voyageai = import_module("voyageai")
    if getattr(voyageai, "__version__", None) != "0.5.0":
        raise SemanticUnavailable() from None
    return voyageai.Client(
        api_key=api_key,
        base_url=base_url,
        timeout=min(float(remaining_seconds), 6.0),
        max_retries=0,
    )


def _validate_semantic_interval(value: Any, dimension: str) -> SemanticInterval | None:
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise InvalidCriteria() from None
    allowed = {"min", "max", "min_inclusive", "max_inclusive"}
    if not value or set(value) - allowed or not ({"min", "max"} & set(value)):
        raise InvalidCriteria() from None

    normalized: SemanticInterval = {}
    for endpoint in ("min", "max"):
        if endpoint not in value:
            continue
        candidate = value[endpoint]
        if dimension == "year":
            valid = type(candidate) is int and 1 <= candidate <= 9999
        else:
            valid = (
                type(candidate) in (int, float) and math.isfinite(candidate)
                and 0 <= candidate <= 10
            )
        if not valid:
            raise InvalidCriteria() from None
        normalized[endpoint] = candidate

    for endpoint in ("min", "max"):
        flag = f"{endpoint}_inclusive"
        if flag in value and endpoint not in value:
            raise InvalidCriteria() from None
        candidate = value.get(flag, True)
        if type(candidate) is not bool:
            raise InvalidCriteria() from None
        normalized[flag] = candidate

    lower, upper = normalized.get("min"), normalized.get("max")
    if lower is not None and upper is not None and (
        lower > upper or (lower == upper and not (
            normalized["min_inclusive"] and normalized["max_inclusive"]
        ))
    ):
        raise InvalidCriteria() from None
    return normalized


def validate_semantic_arguments(arguments: Mapping[str, Any]) -> SemanticCriteria:
    """Normalize the fixed semantic request schema before any readiness or I/O."""
    if not isinstance(arguments, Mapping) or set(arguments) - SEMANTIC_FIELDS:
        raise InvalidCriteria() from None
    description = arguments.get("description")
    if not isinstance(description, str):
        raise InvalidCriteria() from None
    description = description.strip()
    if not description or len(description) > 2000:
        raise InvalidCriteria() from None

    requested_limit = arguments.get("requested_limit", 5)
    if type(requested_limit) is not int or requested_limit <= 0:
        raise InvalidCriteria() from None

    raw_genres = arguments.get("genres", [])
    if not isinstance(raw_genres, list) or len(raw_genres) > 10:
        raise InvalidCriteria() from None
    genres: list[str] = []
    try:
        for raw_genre in raw_genres:
            if not isinstance(raw_genre, str):
                raise InvalidCriteria() from None
            genre = raw_genre.strip()
            if not genre or len(genre) > 80:
                raise InvalidCriteria() from None
            canonical = GENRE_ALIASES[genre.casefold()]
            if canonical not in genres:
                genres.append(canonical)
    except KeyError:
        raise InvalidCriteria() from None

    genre_mode = arguments.get("genre_mode", "all")
    if not isinstance(genre_mode, str) or genre_mode not in ("all", "any"):
        raise InvalidCriteria() from None
    if genre_mode == "any" and not genres:
        raise InvalidCriteria() from None

    return SemanticCriteria(
        description=description,
        genres=genres,
        genre_mode=cast(Literal["all", "any"], genre_mode),
        year=_validate_semantic_interval(arguments.get("year"), "year"),
        rating=_validate_semantic_interval(arguments.get("rating"), "rating"),
        requested_limit=requested_limit,
    )


def semantic_envelope(
    status: Literal["ok", "empty", "invalid", "unavailable"],
    criteria: SemanticCriteria | None = None,
    movies: list[dict[str, Any]] | None = None,
    *,
    excluded_count: int = 0,
) -> str:
    """Serialize the fixed semantic outcome without private failure details."""
    if status not in ("ok", "empty", "invalid", "unavailable"):
        raise ValueError("Invalid semantic status")
    failed = status in ("invalid", "unavailable")
    if failed:
        criteria = None
        rows: list[dict[str, Any]] = []
        requested = effective = None
    else:
        if criteria is None:
            raise ValueError("Successful semantic outcomes require criteria")
        requested = criteria["requested_limit"]
        effective = min(requested, 10)
        rows = movies if status == "ok" and movies else []
        if len(rows) > effective:
            raise ValueError("Semantic result limit exceeded")
        if status == "ok" and not rows:
            status = "empty"
    shortfall = 0 if effective is None else effective - len(rows)
    warnings = []
    if requested is not None and requested > 10:
        warnings.append("limit_applied")
    if shortfall:
        warnings.append("fewer_results")
    if excluded_count or any(row.get("missing_fields") for row in rows):
        warnings.append("missing_metadata")
    if any(row.get("truncated_fields") for row in rows):
        warnings.append("truncated_metadata")
    result = {
        "status": status,
        "source": SEMANTIC_SOURCE,
        "criteria": criteria,
        "requested_limit": requested,
        "effective_limit": effective,
        "cap_applied": requested is not None and requested > 10,
        "returned_count": len(rows),
        "shortfall": shortfall,
        "movies": rows,
        "warnings": warnings,
        "error_code": (
            "invalid_input" if status == "invalid" else
            "semantic_unavailable" if status == "unavailable" else None
        ),
        "message": {
            "ok": "Retrieved eligible semantic movie matches.",
            "empty": "No eligible semantic movie matches were returned.",
            "invalid": "The semantic movie request is invalid.",
            "unavailable": "Semantic movie search is unavailable.",
        }[status],
    }
    return json.dumps(result, allow_nan=False)


def _embed_semantic_description(
    description: str, *, remaining_seconds: float = 6,
) -> list[float]:
    """Generate one transient query vector through the explicitly bound client."""
    if (
        type(remaining_seconds) not in (int, float)
        or not math.isfinite(remaining_seconds) or remaining_seconds <= 0
    ):
        raise SemanticUnavailable() from None
    try:
        client = _new_semantic_client(remaining_seconds)
    except Exception as error:
        raise SemanticDiagnosticError("provider_client", _failure_code(error, "error")) from None
    try:
        try:
            response = client.embed(
                [description], model="voyage-4-large", input_type="query",
                output_dimension=2048, output_dtype="float", truncation=False,
            )
        except Exception as error:
            raise SemanticDiagnosticError("provider_request", _failure_code(error, "error")) from None
    finally:
        close = getattr(client, "close", None)
        if callable(close):
            try:
                close()
            except Exception as error:
                raise SemanticDiagnosticError("provider_cleanup", _failure_code(error, "error")) from None
    embeddings = getattr(response, "embeddings", None)
    if not isinstance(embeddings, list) or len(embeddings) != 1:
        raise SemanticDiagnosticError("provider_response", "invalid_response") from None
    vector = embeddings[0]
    if not isinstance(vector, list) or len(vector) != 2048 or not all(
        type(value) in (int, float) and math.isfinite(value) for value in vector
    ):
        raise SemanticDiagnosticError("provider_response", "invalid_response") from None
    return [float(value) for value in vector]


def semantic_filter_predicate(criteria: SemanticCriteria) -> dict[str, Any]:
    """Build only the G2-verified Vector Search pre-filter subset."""
    clauses: list[dict[str, Any]] = []
    genres = criteria["genres"]
    if genres:
        if criteria["genre_mode"] == "all":
            clauses.append({"$and": [
                {"genres": {"$eq": genre}} for genre in genres
            ]})
        else:
            clauses.append({"genres": {"$in": genres}})

    for dimension, path in (("year", "year"), ("rating", "imdb.rating")):
        interval = criteria[dimension]
        if interval is None:
            continue
        bounds: dict[str, int | float] = {}
        if "min" in interval:
            bounds["$gte" if interval["min_inclusive"] else "$gt"] = interval["min"]
        if "max" in interval:
            bounds["$lte" if interval["max_inclusive"] else "$lt"] = interval["max"]
        clauses.append({path: bounds})

    if not clauses:
        return {}
    if len(clauses) == 1:
        return clauses[0]
    return {"$and": clauses}


def semantic_movie_pipeline(
    criteria: SemanticCriteria, query_vector: list[float],
) -> list[dict[str, Any]]:
    """Build the fixed two-stage semantic pipeline without caller-supplied MQL."""
    effective_limit = min(criteria["requested_limit"], 10)
    vector_search: dict[str, Any] = {
        "index": "plot_vector_index",
        "path": "plot_embedding_voyage_4_large",
        "queryVector": query_vector,
        "limit": effective_limit,
        "numCandidates": 20 * effective_limit,
    }
    predicate = semantic_filter_predicate(criteria)
    if predicate:
        vector_search["filter"] = predicate
    return [
        {"$vectorSearch": vector_search},
        {"$project": dict(SEMANTIC_PROJECTION)},
    ]


def normalize_semantic_movie(document: Mapping[str, Any]) -> dict[str, Any]:
    """Normalize only projected semantic facts and enforce presentation eligibility."""
    identity = document.get("_id")
    if isinstance(identity, ObjectId):
        source_id = "objectId:" + str(identity)
    elif isinstance(identity, str) and identity.strip():
        source_id = "string:" + identity
    elif isinstance(identity, int) and not isinstance(identity, bool):
        source_id = "number:" + str(identity)
    else:
        raise IneligibleSemanticMovie() from None

    title = document.get("title")
    plot = document.get("plot")
    if not isinstance(title, str) or not title.strip():
        raise IneligibleSemanticMovie() from None
    if not isinstance(plot, str) or not plot.strip():
        raise IneligibleSemanticMovie() from None

    year = document.get("year")
    if not isinstance(year, int) or isinstance(year, bool) or not 1 <= year <= 9999:
        year = None

    genres = document.get("genres")
    if not isinstance(genres, list) or not genres or not all(
        isinstance(item, str) and item.strip() for item in genres
    ):
        genres = None

    imdb = document.get("imdb")
    rating = imdb.get("rating") if isinstance(imdb, Mapping) else None
    if isinstance(rating, Decimal128):
        rating = rating.to_decimal()
    if isinstance(rating, (int, float, Decimal)) and not isinstance(rating, bool):
        try:
            rating = float(rating)
            if not math.isfinite(rating) or not 0 <= rating <= 10:
                rating = None
        except (ValueError, OverflowError):
            rating = None
    else:
        rating = None

    score = document.get("semantic_score")
    if isinstance(score, (int, float, Decimal)) and not isinstance(score, bool):
        try:
            score = float(score)
            if not math.isfinite(score):
                score = None
        except (ValueError, OverflowError):
            score = None
    else:
        score = None

    missing = [key for key, value in (
        ("year", year), ("genres", genres), ("imdb_rating", rating),
        ("semantic_score", score),
    ) if value is None]
    truncated = []
    if len(title) > 300:
        truncated.append("title")
    if len(plot) > 500:
        truncated.append("plot")
    if genres is not None and (len(genres) > 10 or any(len(item) > 80 for item in genres)):
        truncated.append("genres")
    return {
        "source_id": source_id,
        "title": title[:300],
        "plot": plot[:500],
        "genres": [item[:80] for item in genres[:10]] if genres is not None else None,
        "year": year,
        "imdb_rating": rating,
        "semantic_score": score,
        "missing_fields": missing,
        "truncated_fields": truncated,
    }


def search_semantic_movie_results(arguments: Mapping[str, Any]) -> str:
    """Run one fixed, bounded semantic aggregation and normalize eligible rows."""
    started_at = monotonic()
    try:
        criteria = validate_semantic_arguments(arguments)
    except (InvalidCriteria, TypeError, ValueError):
        return semantic_envelope("invalid")
    if not _semantic_ready():
        _log_semantic_failure("readiness", _semantic_readiness_code() or "failed")
        return semantic_envelope("unavailable")
    try:
        provider_seconds = min(6.0, 12.0 - (monotonic() - started_at))
        query_vector = _embed_semantic_description(
            criteria["description"], remaining_seconds=provider_seconds,
        )
    except Exception as error:
        _log_semantic_failure(
            getattr(error, "stage", "provider"),
            getattr(error, "code", _failure_code(error, "provider_error")),
        )
        return semantic_envelope("unavailable")
    database_stage = "connect"
    try:
        database_seconds = min(5.0, 12.0 - (monotonic() - started_at))
        if database_seconds <= 0:
            _log_semantic_failure("database", "budget_exhausted")
            return semantic_envelope("unavailable")
        effective_limit = min(criteria["requested_limit"], 10)
        pipeline = semantic_movie_pipeline(criteria, query_vector)
        excluded_count = 0
        movies: list[dict[str, Any]] = []
        consumption_completed = False
        with pymongo.timeout(database_seconds):
            collection = _get_movie_client()["sample_mflix"]["embedded_movies"]
            database_stage = "aggregate"
            cursor = collection.aggregate(
                pipeline, maxTimeMS=max(1, min(5000, int(database_seconds * 1000))),
                batchSize=effective_limit,
            )
            try:
                database_stage = "consume"
                raw_count = 0
                for document in cursor:
                    raw_count += 1
                    if raw_count > effective_limit:
                        raise SemanticUnavailable() from None
                    try:
                        movies.append(normalize_semantic_movie(document))
                    except IneligibleSemanticMovie:
                        excluded_count += 1
                consumption_completed = True
            finally:
                database_stage = "cleanup"
                try:
                    cursor.close()
                except Exception as error:
                    if not consumption_completed:
                        raise
                    logger.warning(
                        "semantic cursor cleanup degraded | code=%s",
                        _failure_code(error, "database_error"),
                    )
    except Exception as error:
        _log_semantic_failure(
            f"database_{database_stage}", _failure_code(error, "database_error"),
        )
        return semantic_envelope("unavailable")
    return semantic_envelope(
        "ok" if movies else "empty", criteria, movies, excluded_count=excluded_count,
    )


def _reset_movie_client_after_fork() -> None:
    # Never acquire an inherited lock or close/use a parent's client in a child.
    global _movie_client, _movie_client_pid, _movie_client_lock
    _movie_client = None
    _movie_client_pid = None
    _movie_client_lock = threading.Lock()


def _get_movie_client() -> MongoClient[dict[str, Any]]:
    global _movie_client, _movie_client_pid
    with _movie_client_lock:
        pid = os.getpid()
        if _movie_client is None or _movie_client_pid != pid:
            uri = os.environ.get("MOVIES_MONGODB_URI")
            if not uri or not uri.strip():
                raise MovieNotConfigured() from None
            # Lazy first-operation connection; pool defaults until measured evidence.
            _movie_client = MongoClient(uri, connect=False)
            _movie_client_pid = pid
        return _movie_client


def _close_movie_client() -> None:
    global _movie_client, _movie_client_pid
    with _movie_client_lock:
        client, pid = _movie_client, _movie_client_pid
        _movie_client = None
        _movie_client_pid = None
    if client is not None and pid == os.getpid():
        try:
            client.close()
        except Exception:
            pass  # Best effort at process shutdown; never log driver exception text.


if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_reset_movie_client_after_fork)
atexit.register(_close_movie_client)


def validate_movie_arguments(arguments: Mapping[str, Any]) -> MovieCriteria:
    """Strict JSON types and explicit genre vocabulary before any client access."""
    fields = set(MovieCriteria.__annotations__)
    if not isinstance(arguments, Mapping) or set(arguments) - fields:
        raise InvalidCriteria()
    values = dict(arguments)
    values.setdefault("genres", [])
    values.setdefault("genre_mode", "all")
    values.setdefault("sort", "title")
    values.setdefault("requested_limit", 5)
    for field, value in values.items():
        if field == "title":
            valid = isinstance(value, str) and bool(value.strip()) and len(value) <= 300
        elif field == "genres":
            valid = isinstance(value, list) and len(value) <= 10 and all(
                isinstance(item, str) and bool(item.strip()) and len(item) <= 80
                for item in value
            )
        elif field in ("genre_mode", "sort"):
            valid = isinstance(value, str) and value in (
                ("all", "any") if field == "genre_mode" else ("title", "rating_desc")
            )
        elif field.endswith("_inclusive"):
            valid = type(value) is bool
        elif field.startswith("rating_"):
            valid = type(value) in (int, float) and 0 <= value <= 10 and math.isfinite(value)
        else:
            valid = type(value) is int and value > 0
            if field.startswith("year_"):
                valid = valid and value <= 9999
        if not valid:
            raise InvalidCriteria()
    try:
        values["genres"] = list(dict.fromkeys(
            GENRE_ALIASES[item.strip().casefold()] for item in values["genres"]
        ))
    except KeyError:
        raise InvalidCriteria() from None
    for dimension in ("year", "rating"):
        for endpoint in ("min", "max"):
            values.setdefault(f"{dimension}_{endpoint}_inclusive", True)
        lower, upper = values.get(f"{dimension}_min"), values.get(f"{dimension}_max")
        if lower is not None and upper is not None and (
            lower > upper or (lower == upper and not (
                values[f"{dimension}_min_inclusive"] and values[f"{dimension}_max_inclusive"]
            ))
        ):
            raise InvalidCriteria()
    return cast(MovieCriteria, values)


def movie_envelope(
    status: Literal["ok", "empty", "invalid", "unavailable"],
    criteria: MovieCriteria | None = None,
    movies: list[dict[str, Any]] | None = None,
    error_code: str | None = None,
) -> str:
    """Serialize strict JSON and fixed safe guidance, never exception messages."""
    rows = movies if status == "ok" and movies else []
    if status == "ok" and not rows:
        status = "empty"
    requested = criteria.get("requested_limit", 5) if criteria is not None else None
    limit = min(requested, 10) if requested is not None else None
    if limit is not None and len(rows) > limit:
        raise ValueError("Result limit exceeded")
    result = {
        "status": status, "movies": rows, "criteria": criteria,
        "requested_limit": requested, "effective_limit": limit,
        "returned_count": len(rows), "capped": requested is not None and requested > 10,
        "shortfall": status in ("ok", "empty") and limit is not None and len(rows) < limit,
        "message": {
            "ok": "Retrieved matching movies. Explain any cap or shortfall.",
            "empty": "No eligible movies matched. You can adjust the criteria.",
            "invalid": "Please correct the movie criteria or positive integer result count.",
            "unavailable": "Movie retrieval is unavailable. Retry or review configuration privately.",
        }[status],
    }
    if error_code is not None:
        if error_code not in {
            "INVALID_CRITERIA", "NOT_CONFIGURED", "RETRIEVAL_TIMEOUT", "RETRIEVAL_UNAVAILABLE"
        }:
            raise ValueError("Invalid error category")
        result["error_code"] = error_code
    return json.dumps(result, allow_nan=False)


def _read_movie_results(
    criteria: MovieCriteria,
    predicate: Mapping[str, Any],
    sort: list[tuple[str, int]],
    normalize: Callable[[dict[str, Any]], dict[str, Any]],
) -> str:
    """Internal bounded find runner; no raw MQL argument is exposed as a tool."""
    try:
        criteria = validate_movie_arguments(criteria)
    except InvalidCriteria:
        return movie_envelope("invalid", error_code="INVALID_CRITERIA")
    try:
        # Includes lazy setup, find, ALL consumption/normalization and cursor close.
        with pymongo.timeout(10):
            collection = _get_movie_client()["sample_mflix"]["movies"]
            cursor = collection.find(predicate, MOVIE_PROJECTION)
            try:
                cursor.max_time_ms(5000)
                cursor.sort(sort)
                cursor.limit(min(criteria.get("requested_limit", 5), 10))
                # PyMongo CSOT replaces maxTimeMS on the wire. A nested deadline
                # keeps that replacement <=5s, within the outer full-operation 10s.
                with pymongo.timeout(5):
                    movies = [normalize(document) for document in cursor]
            finally:
                cursor.close()
            return movie_envelope("ok" if movies else "empty", criteria, movies)
    except MovieNotConfigured:
        code = "NOT_CONFIGURED"
    except PyMongoError as error:
        code = "RETRIEVAL_TIMEOUT" if error.timeout else "RETRIEVAL_UNAVAILABLE"
    except Exception:
        code = "RETRIEVAL_UNAVAILABLE"
    return movie_envelope("unavailable", criteria, error_code=code)


def normalize_movie(document: dict[str, Any]) -> dict[str, Any]:
    """Normalize projected facts only; malformed required identity/title fails safely."""
    identity = document.get("_id")
    if isinstance(identity, ObjectId):
        source_id = "objectId:" + str(identity)
    elif isinstance(identity, str) and identity:
        source_id = "string:" + identity
    elif isinstance(identity, int) and not isinstance(identity, bool):
        # BSON Int64 retains its source type through canonical Extended JSON.
        source_id = "number:" + json_util.dumps(identity, json_options=json_util.CANONICAL_JSON_OPTIONS)
    else:
        raise ValueError("Unusable source identity")
    title = document.get("title")
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Unusable movie title")
    year = document.get("year")
    if not isinstance(year, int) or isinstance(year, bool) or not 1 <= year <= 9999:
        year = None
    genres = document.get("genres")
    if not isinstance(genres, list) or not genres or not all(
        isinstance(item, str) and item.strip() for item in genres
    ):
        genres = None
    imdb = document.get("imdb")
    rating = imdb.get("rating") if isinstance(imdb, dict) else None
    if isinstance(rating, Decimal128):
        rating = rating.to_decimal()
    if isinstance(rating, (int, float, Decimal)) and not isinstance(rating, bool):
        try:
            rating = float(rating)
            if not math.isfinite(rating) or not 0 <= rating <= 10:
                rating = None
        except (ValueError, OverflowError):
            rating = None
    else:
        rating = None
    plot = document.get("plot")
    if not isinstance(plot, str) or not plot.strip():
        plot = None
    missing = [key for key, value in (
        ("year", year), ("genres", genres), ("imdb_rating", rating), ("plot", plot)
    ) if value is None]
    truncated = []
    if len(title) > 300:
        truncated.append("title")
    if genres is not None and (len(genres) > 10 or any(len(item) > 80 for item in genres)):
        truncated.append("genres")
    if plot is not None and len(plot) > 500:
        truncated.append("plot")
    return {
        "source_id": source_id, "title": title[:300], "year": year,
        "genres": [item[:80] for item in genres[:10]] if genres is not None else None,
        "imdb_rating": rating, "plot": plot[:500] if plot is not None else None,
        "missing_fields": missing, "truncated_fields": truncated,
    }


def title_movie_predicate(criteria: MovieCriteria) -> dict[str, Any]:
    """Scalar usable-title eligibility is evaluated before server sort and limit."""
    predicate: dict[str, Any] = {"$expr": {"$and": [
        {"$eq": [{"$type": "$title"}, "string"]},
        {"$ne": [{"$trim": {"input": {"$cond": [
            {"$eq": [{"$type": "$title"}, "string"]}, "$title", ""
        ]}}}, ""]},
        {"$in": [{"$type": "$_id"}, ["objectId", "string", "int", "long"]]},
        {"$ne": ["$_id", ""]},
    ]}}
    if "title" in criteria:
        predicate["title"] = {"$regex": re.escape(criteria["title"]), "$options": "i"}
    return predicate


def filtered_movie_predicate(criteria: MovieCriteria) -> dict[str, Any]:
    """All required source validity is part of the find, before sorting/limiting."""
    predicate = title_movie_predicate(criteria)
    expressions = predicate["$expr"]["$and"]
    genres = criteria.get("genres", [])
    if genres:
        # $and is not short-circuiting: guard every array/string-only expression.
        safe_array = {"$cond": [{"$isArray": "$genres"}, "$genres", []]}
        expressions.extend([
            {"$isArray": "$genres"},
            {"$allElementsTrue": [{"$map": {
                "input": safe_array, "as": "genre", "in": {"$and": [
                    {"$eq": [{"$type": "$$genre"}, "string"]},
                    {"$ne": [{"$trim": {"input": {"$cond": [
                        {"$eq": [{"$type": "$$genre"}, "string"]}, "$$genre", ""
                    ]}}}, ""]},
                ]},
            }}]},
        ])
        predicate["genres"] = {"$all" if criteria.get("genre_mode") == "all" else "$in": genres}
    for dimension, field, types, lower, upper in (
        ("year", "$year", ["int", "long"], 1, 9999),
        ("rating", "$imdb.rating", ["int", "long", "double", "decimal"], 0, 10),
    ):
        required = any(f"{dimension}_{endpoint}" in criteria for endpoint in ("min", "max"))
        if dimension == "rating" and criteria.get("sort") == "rating_desc":
            required = True
        if not required:
            continue
        # Numeric BSON comparisons plus a finite domain exclude NaN and infinities;
        # expression $type rejects arrays (unlike query $type) and booleans/strings.
        expressions.extend([
            {"$in": [{"$type": field}, types]},
            {"$gte": [field, lower]}, {"$lte": [field, upper]},
        ])
        for endpoint, inclusive_op, strict_op in (("min", "$gte", "$gt"), ("max", "$lte", "$lt")):
            key = f"{dimension}_{endpoint}"
            if key in criteria:
                op = inclusive_op if criteria.get(f"{key}_inclusive", True) else strict_op
                expressions.append({op: [field, criteria[key]]})
    return predicate


def search_movie_results(arguments: Mapping[str, Any]) -> str:
    """Validate all criteria, never relax rated eligibility or pad shortfalls."""
    try:
        criteria = validate_movie_arguments(arguments)
    except InvalidCriteria:
        return movie_envelope("invalid", error_code="INVALID_CRITERIA")
    sort = [("title", 1), ("_id", 1)]
    if criteria.get("sort") == "rating_desc":
        sort.insert(0, ("imdb.rating", -1))
    return _read_movie_results(criteria, filtered_movie_predicate(criteria),
                               sort, normalize_movie)


def register(app: App) -> None:
    @app.tool(is_local=False, timeout=12)
    @validate_call(config=ConfigDict(extra="forbid"))
    def search_semantic_movies(
        description: StrictStr,
        genres: list[StrictStr] | None = None,
        genre_mode: Literal["all", "any"] = "all",
        year: SemanticYearInput | None = None,
        rating: SemanticRatingInput | None = None,
        requested_limit: StrictInt = 5,
    ) -> str:
        """Find movies by semantic plot similarity with optional indexed filters.

        Results use only the fixed semantic movie source and preserve similarity order.
        The default is five results and the maximum is ten. Genre all means AND and
        any means OR. Year and IMDb rating support strict or inclusive bounds.
        """
        arguments: dict[str, Any] = {
            "description": description,
            "genre_mode": genre_mode,
            "requested_limit": requested_limit,
        }
        if genres is not None:
            arguments["genres"] = genres
        if year is not None:
            interval = {key: value for key, value in dict(year).items()
                        if value is not None}
            arguments["year"] = {key: value for key, value in interval.items()
                                  if key in ("min", "max") or key.removesuffix("_inclusive") in interval}
        if rating is not None:
            interval = {key: value for key, value in dict(rating).items()
                        if value is not None}
            arguments["rating"] = {key: value for key, value in interval.items()
                                    if key in ("min", "max") or key.removesuffix("_inclusive") in interval}
        return search_semantic_movie_results(arguments)

    @app.tool()
    def search_movies(
        title: StrictStr | None = None, requested_limit: StrictInt = 5,
        genres: list[StrictStr] | None = None, genre_mode: Literal["all", "any"] = "all",
        year_min: StrictInt | None = None, year_max: StrictInt | None = None,
        year_min_inclusive: StrictBool = True, year_max_inclusive: StrictBool = True,
        rating_min: StrictInt | StrictFloat | None = None,
        rating_max: StrictInt | StrictFloat | None = None,
        rating_min_inclusive: StrictBool = True, rating_max_inclusive: StrictBool = True,
        sort: Literal["title", "rating_desc"] = "title",
    ) -> str:
        """Find movies by literal title AND genre/year/rating filters, default five, cap ten.

        Genres all means AND, any means OR; science fiction maps to Sci-Fi.
        Exact year uses equal bounds. Before/after/above/below require inclusive=False.
        Unknown genres and contradictory bounds are invalid, never silently relaxed.
        Highly rated means rating_desc: numeric rated movies only, no hidden minimum
        and no unrated fallback. Shortfalls and cap are separate notices.
        Missing fields remain unavailable. Never use this tool for profile operations.
        Omit title for general discovery; an explicitly blank title is invalid.
        """
        arguments: dict[str, Any] = {
            "requested_limit": requested_limit, "genre_mode": genre_mode, "sort": sort,
            "year_min_inclusive": year_min_inclusive, "year_max_inclusive": year_max_inclusive,
            "rating_min_inclusive": rating_min_inclusive, "rating_max_inclusive": rating_max_inclusive,
        }
        if title is not None:
            arguments["title"] = title
        for key, value in (("genres", genres), ("year_min", year_min), ("year_max", year_max),
                           ("rating_min", rating_min), ("rating_max", rating_max)):
            if value is not None:
                arguments[key] = value
        return search_movie_results(arguments)

    @app.tool()
    def get_current_date(timezone_name: str = "UTC") -> str:
        """Return today's date in ISO 8601 format for an IANA timezone."""
        try:
            timezone = ZoneInfo(timezone_name)
        except ZoneInfoNotFoundError:
            return json.dumps(
                {
                    "error": f"Unknown timezone: {timezone_name}",
                    "hint": "Use an IANA timezone like America/Los_Angeles.",
                }
            )
        return datetime.now(timezone).date().isoformat()

    @app.tool()
    def save_user_info(info_key: str, info_value: str) -> str:
        """Save a piece of information about the user to long-term memory.

        Args:
            info_key: What the information represents, such as name, location, or interests.
            info_value: The value to store.
        """
        user_id = app.get_current_user_id()
        result = app.memory.save_semantic(
            text=f"User {info_key}: {info_value}",
            label=f"{user_id}_{info_key}",
            source="agent_movie_scout",
            metadata={"type": "user_info", "info_key": info_key},
            user_id=user_id,
        )
        if getattr(result, "acknowledged", result):
            return json.dumps({"status": "saved", "info_key": info_key})
        return json.dumps({"status": "error", "error": "Memory is not enabled"})

    @app.tool()
    def recall_user_info() -> str:
        """Recall stored information about the current user from long-term memory."""
        user_id = app.get_current_user_id()
        context = app.memory.build_context(
            query=f"user profile and information for user {user_id}",
            user_id=user_id,
        )
        formatted = getattr(context, "formatted_context", context)
        # SDK0.11.9 native responses may contain a list of context sections.
        # Preserve that native content for standalone recall instead of reporting
        # a healthy nonempty response as missing. Movie routes never expose it.
        memory_context = formatted if isinstance(formatted, str) else (
            json.dumps(formatted, allow_nan=False) if isinstance(formatted, list) and formatted else ""
        )
        if not memory_context:
            return json.dumps({"found": False, "message": "No stored information found"})
        return json.dumps({"found": True, "profile": memory_context})
