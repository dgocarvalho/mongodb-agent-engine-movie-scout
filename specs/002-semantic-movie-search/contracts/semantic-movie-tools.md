# Native semantic movie tool contract (proposed)

## Active embedding migration — 2026-10-27

The active contract uses `voyage-4-large` and `plot_embedding_voyage_4_large`,
both at 2048 dimensions. The G2 index definition below describes the historical
Voyage 3 field and is retained as provenance; it is not the active index. Manual
maintainer work is required to seed and validate the new field/index before T027
acceptance.

**Status**: revised LOCAL design approved by exact “sim, aprovo”,2026-10-23. G1/G2 retain scoped evidence; documented embedding path selected, actual native acceptance G4-B NOT RUN. See [plan](../plan.md), [research](../research.md), [data model](../data-model.md). Documentation only in this invocation; no HTTP endpoint/service/implementation introduced.

## G2 — Index definition and maintainer receipt, 2026-10-23

Fixed namespace sample_mflix.embedded_movies; existing index plot_vector_index/type vectorSearch. Initial JSON supplied by maintainer: vector path plot_embedding_voyage_3_large, numDimensions2048, similarity cosine; no filters. After authorized bounded inventory, maintainer manually applied precisely this definition and subsequently confirmed Ready/Queryable, MongoDB9.0.4:

```json
{
	"fields": [
		{"type": "vector", "path": "plot_embedding_voyage_3_large", "numDimensions": 2048, "similarity": "cosine"},
		{"type": "filter", "path": "genres"},
		{"type": "filter", "path": "year"},
		{"type": "filter", "path": "imdb.rating"}
	]
}
```

Sanitized maintainer attestation, not independently listed metadata or successful vector/filter query. No index changes or administrative-grant expansion performed by assistant. Observed vectors:98 FLOAT32 binData subtype9/2048; dimension matches. No explicit quantization setting supplied; do not invent one. Display fields are projected from records, not additional filters. fullplot is not a fallback; poster inactive.

### T006 — verified mapping and documentary operator cross-check

Phase 2 review,2026-10-23, after T005: cross-checked the existing bounded inventory against the maintainer's initial definition and subsequent manual-preparation attestation; no new metadata query or index mutation. The only verified initial-to-final difference is the addition of the three filter entries above. No further adjustment is identified or authorized. No quantization setting is inferred from contemporary documentation defaults.

| Role | Fixed path / type in existing evidence | Selected use |
|---|---|---|
| vector | plot_embedding_voyage_3_large; observed binData subtype9 FLOAT32/2048 | Classic vector index, queryVector numeric finite2048 array, cosine; not AutoEmbed/query/model generation in the database |
| filter | genres; observed array of strings | all: `$and` of one `{genres: {$eq: genre}}` per genre; any: `{genres: {$in: genres}}`; bounded canonical values only |
| filter | year; decoded integer, exact BSON integer subtype unestablished | `$gt`/`$gte` lower and `$lt`/`$lte` upper according to validated inclusion flags |
| filter | imdb.rating; observed nested numeric double | Same strict/inclusive range mapping on this exact dotted path; combine requested dimensions with `$and` |
| display | _id, title, plot, genres, year, imdb.rating | Positive projection; semantic ID/title/nonblank plot eligibility applied without changing relative order; vector excluded |
| inactive | fullplot, poster | No plot fallback, enrichment or active image projection |

Official [vectorSearch stage/filter reference](https://www.mongodb.com/docs/vector-search/query/aggregation-stages/vector-search-stage/) documents numeric/string values including arrays, indexed filter fields, `$eq`, `$in`, `$and`, `$or` and `$gt`/`$gte`/`$lt`/`$lte`. The selected subset above is sufficient; `$all`, regex, expression/user operators and approximate post-filter replacement are not selected. Requested filters cannot be omitted. The reference documents ANN on MongoDB>=6.0.11/7.0.2; maintainer-attested9.0.4 exceeds that documented minimum, not proof of this cluster's actual query behavior. Existing PyMongo>=4.11,<5 and its documented aggregate API provide the driver path; exact resolved runtime versions and real combined filter/boundary behavior remain G4-B NOT RUN. Keep `$vectorSearch` first, numCandidates20*limit<=200, one bounded aggregation and positive projection, without switching search families or tuning the index.

T006 completed documentarily, not native query acceptance. Namespace/index/configuration/schema or version change, altered/missing filter paths, or loss of queryability invalidates readiness. G2 does not establish query embedding/model access, recall or performance; an unsupported required filter means unavailable/STOP for the affected use, not empty, silent omission, runtime grant expansion or fallback.

The revised local plan records approval and official API/build/dependency/secret/egress mechanisms; no global hard-deadline mechanism is required or claimed. G1/G2 remain valid only for the recorded configuration. Dependency resolution/imports, actual secret segregation/delivery, endpoint binding, egress/connectivity and functionality are verified DURING implementation and required BEFORE acceptance in the [single G4-B checklist](../quickstart.md#5-local-acceptance-checklist-g4-b), currently NOT RUN. These results are not circular pre-code gates or documentary PASS claims. A separate implementation workflow is needed; restart/other stack operations still need separate operational authorization.

## Interface

Proposed native tool: `search_semantic_movies`, registered with `App.tool` and obtained via audited native wrapper. Existing `search_movies`, date and nonmovie memory contracts unchanged.

LLM-visible properties: only `description`, `genres`, `genre_mode`, `year`, `rating`, `requested_limit`, with bounds in the data model. Interval objects permit only `min`, `max`, `min_inclusive`, `max_inclusive`. Omitted dimensions preserve confirmed semantic context during refinement; null interval/empty genres clears that dimension. New-search versus refinement is resolved at the agent state boundary, not by trusting persisted tool permissions. Reset is direct state handling, not an aggregation request.

No database/collection/index/path/raw vector/model/endpoint/URI/query/operator/sort/pipeline or arbitrary metadata keys supplied by callers. Reject unknown properties/types before provider/database I/O. Missing description without confirmed semantic theme requires clarification, no retrieval.

## Routing and dispatch

- Explicit traditional intent: existing traditional tool only; no semantic substitution.
- Semantic intent/refinement: semantic tool and existing date if relevant; no explicit save/recall profile.
- Mixed cinematic turn: same profile prohibition, including otherwise nonmovie requests.
- Ambiguous/uncertain: clarify before either catalog tool.
- Existing nonmovie routes unchanged.
- Guard whole batch against current route allowlist before dispatch. Any forbidden call blocks batch and produces correlated responses for every call ID, preserving existing guard behavior.
- Commit context only from genuine tool returns/matching call IDs, never model claims or historical ToolMessages. Concurrent proposals must not overwrite unrelated confirmed criteria.

## Fixed source and execution

Only source sample_mflix.embedded_movies. The active vector field is plot_embedding_voyage_4_large and requires a manually prepared/queryable vector index; the Voyage 3 mapping above is historical provenance. Native execution requires the applicable operational readiness/authorization, not a new approval of the recorded local plan. Movie credentials only MOVIES_MONGODB_URI, never operational MONGODB_URI. No fallback source/index/model/provider. Missing readiness returns unavailable without source access. Semantic failure does not disable traditional functionality.

1. Validate request/proposal within2000 description characters,10 genres and strict interval/limit rules.
2. Obtain one bounded transient query embedding with selected official voyageai==0.5.0: model=voyage-4-large, input_type=query, output_dimension=2048, output_dtype=float, truncation=False. Explicit api_key/base_url bind existing VOYAGE_API_KEY/VOYAGE_URL in the necessary TOOL sandbox via documented mechanisms; no secret reads/requests now, default auto-routing, memory reconfiguration, silent truncation/retry/corpus writes. Require finite2048-vector output; actual model access/binding/egress remains unverified until implementation validation.
3. One controlled read aggregation: `$vectorSearch` first; explicit fixed index/path/queryVector, limit=effective_limit and ANN numCandidates=20*effective_limit (<=200).
4. Requested filters map only to verified paths indexed as filter. Supported equality/set/logical/range predicates; all genres via AND of equality, any via supported OR/set semantics; do not assume `$all`. Strict/inclusive ranges preserved. Missing required index mapping means unavailable, not dropped filters or approximate post-filtering.
5. Positive projection of verified identity/display fields and vectorSearchScore excludes every vector. No joins/writes/user stages/IMDb reranking. Normalize/validate eligibility: exclude candidates with unusable ID/title or unusable recovered plot (missing/null/nonstring/empty/whitespace-only). Never coerce plot or invent plot/affinity; preserve eligible relative order, report shortfall, never widen filters, increase result limit or issue refill queries/fallback to fill page. This semantic-only rule does not change traditional missing-metadata behavior.
6. Close cursor even on cancellation/timeout/normalization failure; bounded batch at most10 documents, no pagination, unbounded materialization or fill queries.

Proposed operational budgets: tool<=12s, provider<=6s, database<=5s, explicit timeouts according to supported behavior and zero application retries (including explicit client max_retries=0). Bound local remaining work where supported, not assumed global routing/model/final-response propagation. Explicit maxTimeMS and driver timeout must be tested together in G4-B: CSOT may affect wire maxTimeMS. Close resources on supported timeout/cancellation paths; do not promise unconditional thread interruption. Measure submission-to-final-response: healthy>=19/20<=20s, failure explanation target<=30s. The latter is NOT a hard global completion/cancellation guarantee. Duration policy checks before calls, not in-flight; client timeout does not cancel server work. No custom watchdog/service, session-cancel side effect or infrastructure change is authorized. Log sanitized overruns honestly and review them before local acceptance; never mark unachieved target PASS or hide missing evidence.

## Result envelope

| Property | Meaning |
|---|---|
| status | ok / empty / invalid / unavailable |
| source | fixed sample_mflix.embedded_movies |
| criteria | sanitized normalized proposal on ok/empty; no secrets/vectors |
| requested_limit / effective_limit | requested count, cap10, default5 |
| cap_applied | request exceeds10 |
| returned_count | length of movies,0–10 |
| shortfall | effective_limit - returned_count, not total catalog matches |
| movies | bounded normalized records, semantic relative order preserved |
| warnings | fixed codes limit_applied, fewer_results, missing_metadata, truncated_metadata |
| error_code | null success; invalid_input or semantic_unavailable failure |
| message | fixed safe explanation, localized without private details |

`ok`: >=1 candidate with usable ID/title AND recovered nonblank string plot. `empty`: successful ready-source retrieval with no eligible candidates, including exclusion of every unusable ID/title/plot; not proof no thematic match exists anywhere. Count/shortfall reflect only eligible records after normalization; exclusions require fewer_results/missing_metadata notices as applicable, without returning rejected candidates. `invalid`: failed contract, no I/O, previous context retained. `unavailable`: provider/auth/index/readiness/dimension/deadline/driver failure, no movies/commit; never relabel empty. Partial failed retrieval is unavailable, not successful partial data. No raw exceptions, hosts, secrets, vectors or provider payloads.

Example semantics, not observed results: request100 yields effective_limit10/limit_applied. “After2000” sets year min2000/min_inclusive=false and clears old upper bound/flags. Failed refinement preserves prior context.

## Presentation and acceptance

At most returned_count genuine eligible films, each with usable recovered plot; other factual missingness explicit, short plot-supported explanation. Missing plot is exclusion, not a displayed film with an invented explanation or a missing-plot disclaimer. Weak thematic relation in a usable plot is described as uncertain/low correspondence; score is not satisfaction probability. Never promise five when fewer returned. Catalog instructions inert. Text-only active; poster-like data cannot trigger external requests/enrichment.

Native traces must establish source/tool, bounded pipeline, filter correctness, no profile calls and correct state. Synthetic failures separate from real-catalog evidence. No write probes, secret dumps or grant expansion. SC-001–SC-008 and existing regression required; image scenarios not applicable while text-only.