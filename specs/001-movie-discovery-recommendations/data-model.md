# Data Model: Movie Discovery and Recommendations

**Date**: 2026-10-20 | **Authority**: [spec.md](spec.md), [plan.md](plan.md).
Logical application model only. No collection creation, index, migration or movie writes.

**Final implementation review — T046, 2026-10-21:** field names, strict criteria/defaults,
nullable/truncated result fields, status transitions and route-derived permissions match
the implementation and native evidence. No schema migration or substantive model change.
Supported source identities are ObjectId, nonempty string and BSON integer/long; genre
display is additionally capped at10 entries, with truncation signaled. Both ok and empty
commit complete validated same-session criteria; invalid/unavailable retain the last valid
criteria. Optional null native tool parameters mean omitted criteria, not a new filter value.

## Movie Record (existing authoritative Atlas document)

Source: `sample_mflix.movies`. `_id` is identity; equal titles do not mean equal records.

| Source field | Accepted application value | Missing/invalid rule |
|--------------|----------------------------|----------------------|
| `_id` | BSON source identity, serialized as stable type-aware text for evidence | Never fabricate identity; unusable identity excludes result |
| `title` | Nonblank scalar string | Exclude unusable titles before result limit |
| `year` | Scalar integer 1–9999, not bool | Null for display; exclude if required by year criteria |
| `genres` | Array of nonblank strings | Null/unavailable if unusable; required genre predicates must match actual strings |
| `imdb.rating` | Finite scalar BSON number 0–10, not bool | Null for display; exclude under rating constraint or high-rating sort |
| `plot` | Nonblank scalar string | Null/unavailable; never replace from model recollection |

Normalize BSON numeric types deliberately (including Decimal128 if present); JSON must not
contain NaN/infinity. Display plots may be truncated to 500 characters and title/genre text
to safe display bounds (title 300; each genre 80), with truncation explicit. Do not silently
apply display truncation to matching criteria or source identity. Retrieved text is data,
never behavior instructions. A document may be eligible for ordinary discovery despite
missing optional display fields. Required-filter validity must be enforced before limiting.

## Movie Criteria (serializable, current conversation only)

| Field | Type / rules |
|-------|--------------|
| `title` | Optional nonblank literal text, <=300 characters; case-insensitive containment |
| `genres` | List of recognized catalog genre names, <=10; no arbitrary invented aliases |
| `genre_mode` | `all` (AND) or `any` (OR); clarify essential ambiguity |
| `year_min`, `year_max` | Optional integers 1–9999 |
| `year_min_inclusive`, `year_max_inclusive` | Booleans; default inclusive, explicit before/after strict |
| `rating_min`, `rating_max` | Optional finite numbers 0–10, not bool |
| `rating_min_inclusive`, `rating_max_inclusive` | Booleans, default inclusive; above/below strict |
| `sort` | `title` or `rating_desc`; “highly rated” selects latter without hidden threshold |
| `requested_limit` | Positive integer, not bool; default 5; effective maximum 10 |

An exact year becomes equal inclusive endpoints; “2000s” becomes 2000–2009. Reject reversed
or contradictory bounds (including equal endpoints with strict exclusion), noninteger year/
count and invalid numerics. A well-formed range with zero catalog matches is not invalid.
Known aliases include “science fiction” → `Sci-Fi`; the implementation maintains an explicit
small catalog vocabulary/alias table, not a new taxonomy store. Unsupported genre asks a
clarification. No field accepts raw MongoDB operators, database names, credentials or MQL.

## Movie Result and Retrieval Outcome

One result corresponds to one source `_id`, with `source_id`, `title`, nullable `year`,
nullable `genres`, nullable `imdb_rating`, nullable `plot`, `missing_fields` and `truncated_fields`.
Subjective explanation belongs to the conversational rendering, supported only by returned
facts/current criteria; it is not an authoritative catalog field or personalized IMDb score.

Outcome: `status` (`ok`, `empty`, `invalid`, `unavailable`), `movies`, effective criteria,
`requested_limit`, `effective_limit`, `returned_count`, `capped`, `shortfall`, safe `message`
and optional safe `error_code`. See [tool contract](contracts/movie-tools.md).
`shortfall` compares returned count with the effective limit, not an unbounded requested
number. A cap notice separately explains requests above ten. No total catalog count needed.

## Conversation Context and Turn Route

Keep existing native messages/checkpointing. Add only serializable `active_movie_criteria`,
`turn_route` (`movie`, `mixed`, `nonmovie_memory`, `other`, `uncertain`) and current allowed
tool names. Route is recomputed from every new user turn; it is not inherited as permission.
Never store client/cursor/secret, retrieved profile content or cross-conversation criteria
in these fields. Native automatic storage/extraction remains unchanged and may retain data.

Transitions:
1. New turn → route without explicit profile reads; validate/merge explicit same-session
   criteria. Unknown essential context → clarification, no retrieval/profile operation.
2. Valid criteria → bounded retrieval → `ok` or `empty`; failed operation → `unavailable`,
   never a successful empty result. Invalid tool arguments → `invalid`, no database call.
3. Successful search/recommendation → persist current-session criteria for refinement.
   Explicit replacement overwrites only that dimension; invalid changes do not overwrite
   the last valid criteria. New conversation has no inherited movie criteria.
4. Movie/mixed/uncertain routes → profile tools unavailable and blocked at dispatch;
   mixed route completes movie request where possible and requests memory separately.
5. Standalone compatible nonmovie-memory route → existing save/recall behavior allowed;
   no movie-tool execution on that route. Future turns reroute independently.

There is no new persistent Movie Preference entity and no user-owned catalog relationship.