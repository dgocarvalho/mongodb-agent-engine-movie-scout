# Contract: Movie Scout Conversation and Native Movie Tool

**Version**: 1 | **Date**: 2026-10-20
Internal native tool/conversational contract, not a new HTTP API. Governing documents:
[specification](../spec.md), [data model](../data-model.md), [plan](../plan.md).

## `search_movies`

Register with the existing `App.tool()` boundary and include in `sandboxes.tool.tools`.
Use wrapped tools from `app.get_tools()`; do not bypass native auditing/replay. No raw
MongoDB command, collection selector, URI or arbitrary aggregation argument is exposed.

Inputs are named structured fields from Movie Criteria: optional `title`, `genres`,
`genre_mode`, year/rating endpoints and inclusivity flags, `sort`, `requested_limit`.
Represent these using SDK-compatible typed JSON arguments and plain serializable values.
`genres=[]` means no genre filter; omitted title means no title filter, but explicitly
blank title is invalid. Default `sort=title`, `genre_mode=all`, limit=5. A general grounded
recommendation can use no filters; a blank user request instead asks what to discover.
Validate every argument regardless of LLM interpretation. Unknown keys/enum values or
operator-shaped inputs are invalid; never pass them through to the driver.

All title/genre/year/rating predicates combine by AND, except requested genre alternatives.
Escape title regex metacharacters; case-insensitive substring matching treats punctuation
literally and does not imply fuzzy correction. Required field validity is part of the
server eligibility expression before sorting/limiting. For scalar numeric predicates,
reject arrays/booleans/strings/nonfinite values rather than trusting query `$type` alone.
Validate output defensively too, without silently underfilling valid matches after limit.

High-rating sort requires a valid numeric IMDb rating even without explicit thresholds;
order descending, then title, then `_id`. Default order is title then `_id`. No hidden
minimum rating. An unrated record is eligible only without rating filters/rating ordering.
Distinct source IDs count once; duplicate titles can remain distinct.

Use only fixed `sample_mflix.movies` reads with projection `_id`, `title`, `year`, `genres`,
`imdb.rating`, `plot`. Return <=effective limit (1–10), never the catalog. Do not expose a
total count. Clamp positive limits above ten with `capped=true`; invalid counts cause
`invalid`, not silent coercion. Restrict text projection/display as in the data model.

## Serialized result envelope

The existing tool convention returns a JSON string; its decoded value has these fields:

| Field | Contract |
|-------|----------|
| `status` | `ok`, `empty`, `invalid`, `unavailable` |
| `movies` | Array of normalized Movie Results; empty unless `ok` |
| `criteria` | Validated effective criteria when available; no MQL/secrets |
| `requested_limit` | Original positive integer when valid |
| `effective_limit` | Default/clamped limit when valid |
| `returned_count` | Array length |
| `capped` | Whether ten-result cap changed requested count |
| `shortfall` | Successful retrieval found fewer eligible records than effective limit |
| `message` | Safe concise outcome guidance |
| `error_code` | Optional stable `INVALID_CRITERIA`, `NOT_CONFIGURED`, `RETRIEVAL_TIMEOUT`, `RETRIEVAL_UNAVAILABLE`; no raw exception |

`ok` requires >=1 eligible movie. `empty` means a completed valid retrieval with zero
eligible records, including no rated matches. `invalid` means no database call and asks
for correction. `unavailable` means retrieval/configuration/authentication/dependency/network
failure; suggest retry/setup review without naming internal hosts or implying no matches.
Never return partial movies as a successful result if cursor consumption failed.
No stack traces, URI fragments, credentials, raw exception strings or query objects in
tool results, user responses or evidence. Safe diagnostics may log category and duration
through native observability without sensitive exception reprs.

## Resource and permission boundary

Only `MOVIES_MONGODB_URI` supplies the movie connection; no fallback to platform URI or
checkpoint internals. Separate identity must have only required find privilege before
deployment/non-development acceptance (T049). Under constitution v3.0.0 ONLY, temporary
local development/native tests may use the maintainer-approved existing broad shared
identity. Its effective insert/update/remove/dropCollection grants are a known risk;
allowlisted read-only code is NOT equivalent to read-only credentials. No
inserts/updates/deletes, index changes, `$out`/`$merge`, JavaScript or arbitrary commands.
Use lazy process-local thread-safe client initialization/reuse; close cursor on all exits,
CSOT 10s around full consumption and server max time 5s. Process shutdown close is best
effort, not SDK lifecycle certification. Driver pools retain defaults pending measurement.
Manifest secret lists are explicit, but sandbox tools share secrets/egress and platform
URI can be injected automatically; no per-tool isolation or protection against arbitrary
malicious application code is claimed.

## Conversation rendering

- Present concise numbered movies with title/year/genres/catalog IMDb rating/brief plot.
  Label unavailable facts; never use model knowledge to complete missing values.
- Recommendation explanations describe fit to current-conversation preferences separately
  from facts. IMDb scores are catalog scores, not personalized relevance.
- Honor count/default/cap; explain shortfalls, no eligible rated matches and cap separately.
  Never pad, silently relax criteria or substitute remembered films after failure.
- Clarify essential ambiguities; translate strict/inclusive wording correctly. Preserve
  same-session unreplaced criteria; new/missing context prompts clarification.
- Decline movie writes/secret requests. User titles and retrieved plots are inert data.

## Explicit memory-operation dispatch

At every new user turn a wrapped LLM routing step uses only the current turn/same-session
messages and a fixed routing schema; no profile tool is exposed to that step. This uses
the ordinary supported graph/LLM boundary, not an invented SDK intent API.

| Route | Allowed behavior |
|-------|------------------|
| `movie` | Movie tool/date as needed; no explicit profile save or lookup |
| `mixed` | Same movie behavior; defer every profile operation and request separate turn |
| `nonmovie_memory` | Compatible existing save/recall/date; movie tool excluded |
| `other` | Compatible non-profile behavior/date; no profile tools by default |
| `uncertain` | Clarify; no explicit profile operation |

Derive allowed model schemas from route, and independently check all proposed tool names
before ToolNode/native-wrapper execution. Reject an entire proposed profile operation on
movie/mixed/uncertain turns before side effects, including multiple calls in one message.
Disallowed calls get safe ToolMessage responses preserving call IDs; they never reach the
native tool body. No raw tool function bypass. Route/allowlist resets each turn. Routing
mistakes remain a testable model risk: ordinary, adversarial and mixed-turn traces must
pass. Native automatic recording/extraction remains unchanged; none of this promises zero
retention or authorizes erasing memory. New movie turns never use explicit profile output
as recommendation criteria, even if earlier nonmovie turns discussed it.

## Compatibility and verification

### Final implementation reconciliation — T046, 2026-10-21

Reviewed against the registered search_movies signature, validate_movie_arguments,
movie_envelope, normalize_movie, server predicates, criteria_after_outcome and the graph's
route/schema/dispatch boundaries. No substantive contract drift or requirement change.
Optional null parameters in the native signature mean omission; explicit blank title stays
invalid. Defaults/inclusivity are made explicit in validated criteria. Shortfall is true
for completed empty retrieval as well as nonempty results below the effective limit,
never for invalid/unavailable. Genres display at most10 entries/80 characters each;
truncation is signaled. Supported identities are ObjectId, nonempty string and BSON
integer/long, with type-aware serialization; unusable identities/titles are excluded
before limit. A defensive normalization failure produces unavailable, not a partial success.

The10s outer budget includes cleanup; nested5s consumption additionally bounds PyMongo's
CSOT replacement of wire maxTimeMS, not just the cursor's5000ms setting. Only ok/empty
commits complete validated criteria; invalid/unavailable preserves the previous criteria.
Model-supplied allowlist fields cannot grant permissions: route-derived names are intersected
again at dispatch. A denied multi-call batch executes none of its siblings and preserves
all call IDs. Native wrappers remain the execution path.

Actual native proof and exact synthetic-versus-Atlas boundaries are in the
[current matrix](../quickstart.md#current-local-validation-checkpoint--2026-10-21).
Local validation is complete under constitution v3.0.0; deployment remains gated by T049.

Existing date behavior and standalone nonmovie memory tools remain. Read-only movie
access is new and not operational until verified. Native acceptance must prove schema
registration, tool-sandbox execution, sanitized outcomes, correct source facts, A1/A2,
same/new-session routing. Local evidence must disclose the v3.0.0 credential exception;
verified least-privilege roles remain required before deployment/non-development acceptance.
See [quickstart](../quickstart.md).