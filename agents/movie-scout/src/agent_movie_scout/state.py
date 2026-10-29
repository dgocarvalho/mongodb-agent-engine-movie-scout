"""Agent state definition for Movie Scout."""

from copy import deepcopy
from typing import Annotated, Literal, NotRequired, TypedDict, cast

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


TurnRoute = Literal[
    "movie", "mixed", "semantic", "mixed_semantic",
    "nonmovie_memory", "other", "uncertain",
]


class MovieCriteria(TypedDict, total=False):
    title: str
    genres: list[str]
    genre_mode: Literal["all", "any"]
    year_min: int
    year_max: int
    year_min_inclusive: bool
    year_max_inclusive: bool
    rating_min: float
    rating_max: float
    rating_min_inclusive: bool
    rating_max_inclusive: bool
    sort: Literal["title", "rating_desc"]
    requested_limit: int


class SemanticInterval(TypedDict, total=False):
    min: int | float
    max: int | float
    min_inclusive: bool
    max_inclusive: bool


class SemanticMovieCriteria(TypedDict, total=False):
    description: str
    genres: list[str]
    genre_mode: Literal["all", "any"]
    year: SemanticInterval | None
    rating: SemanticInterval | None
    requested_limit: int


class HelloWorldState(TypedDict):
    """Keep the starter name and message reducer for existing checkpoints."""

    messages: Annotated[list[AnyMessage], add_messages]
    active_movie_criteria: NotRequired[MovieCriteria]
    active_semantic_criteria: NotRequired[SemanticMovieCriteria]
    turn_route: NotRequired[TurnRoute]
    allowed_tool_names: NotRequired[list[str]]
    replace_movie_criteria: NotRequired[bool]
    replace_semantic_criteria: NotRequired[bool]
    reset_semantic_criteria: NotRequired[bool]


def safe_turn_defaults() -> dict:
    """Fresh serializable defaults; never inherit permissions from a checkpoint."""
    return {
        "active_movie_criteria": {},
        "active_semantic_criteria": {},
        "turn_route": "uncertain",
        "allowed_tool_names": [],
        "replace_movie_criteria": False,
        "replace_semantic_criteria": False,
        "reset_semantic_criteria": False,
    }


def merge_movie_criteria(
    previous: MovieCriteria, changes: MovieCriteria, *, replace: bool = False,
) -> MovieCriteria:
    """Replace supplied dimensions atomically; omitted dimensions retain their values.

    Inputs are validated by the tool boundary, not a second query-language parser.
    A new bound must not accidentally retain an old opposite bound/strictness flag.
    """
    merged = {} if replace else dict(deepcopy(previous))
    dimensions = (
        ("title",), ("genres", "genre_mode"),
        ("year_min", "year_max", "year_min_inclusive", "year_max_inclusive"),
        ("rating_min", "rating_max", "rating_min_inclusive", "rating_max_inclusive"),
        ("sort",), ("requested_limit",),
    )
    for dimension in dimensions:
        if any(key in changes for key in dimension):
            for key in dimension:
                merged.pop(key, None)
    merged.update(deepcopy(changes))
    return cast(MovieCriteria, merged)


def merge_semantic_criteria(
    previous: SemanticMovieCriteria,
    changes: SemanticMovieCriteria,
    *,
    replace: bool = False,
) -> SemanticMovieCriteria:
    """Merge validated semantic dimensions without inheriting unrelated state."""
    if replace:
        return cast(SemanticMovieCriteria, deepcopy(changes))
    merged = {} if replace else dict(deepcopy(previous))

    if "description" in changes:
        merged["description"] = changes["description"]

    if "genres" in changes:
        merged.pop("genres", None)
        merged.pop("genre_mode", None)
        genres = changes["genres"]
        if genres:
            merged["genres"] = deepcopy(genres)
            merged["genre_mode"] = changes.get("genre_mode", "all")
    for dimension in ("year", "rating"):
        if dimension not in changes:
            continue
        merged.pop(dimension, None)
        if changes[dimension] is not None:
            merged[dimension] = deepcopy(changes[dimension])

    if "requested_limit" in changes:
        merged["requested_limit"] = changes["requested_limit"]

    return cast(SemanticMovieCriteria, merged)


def reset_semantic_criteria() -> SemanticMovieCriteria:
    """Return a fresh empty semantic context without performing I/O."""
    return {}


def criteria_after_outcome(previous: MovieCriteria, outcome: dict) -> MovieCriteria:
    """Only a completed tool retrieval may commit its complete validated criteria."""
    criteria = outcome.get("criteria")
    if outcome.get("status") in ("ok", "empty") and isinstance(criteria, dict):
        return merge_movie_criteria(previous, cast(MovieCriteria, criteria), replace=True)
    return deepcopy(previous)


def semantic_criteria_after_outcome(
    previous: SemanticMovieCriteria, outcome: dict,
) -> SemanticMovieCriteria:
    """Commit a complete validated semantic proposal only after successful retrieval."""
    criteria = outcome.get("criteria")
    if outcome.get("status") in ("ok", "empty") and isinstance(criteria, dict):
        return merge_semantic_criteria({}, cast(SemanticMovieCriteria, criteria), replace=True)
    return deepcopy(previous)
