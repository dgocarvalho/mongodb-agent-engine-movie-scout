# Movie Scout

> **Comece pelo [guia didático em português na raiz](../../README.md)** para entender
> o funcionamento, configurar as conexões, iniciar o Playground e seguir os testes.
> Este documento mantém a referência técnica do agente.

Movie Scout is an educational conversational AI agent for title/filter/recommendation
and semantic plot discovery through MongoDB Atlas Agent Engine. Traditional queries use
`sample_mflix.movies`; semantic queries use the verified read-only
`sample_mflix.embedded_movies` vector source.

**Current status:** Title search, combined filters, rated recommendations, semantic plot
search, same-session refinement/reset and profile isolation are implemented and locally
validated in the native SDK graph. Image rendering remains intentionally text-only:
native poster support was not demonstrated, so no image renderer, fetcher or proxy is
enabled. Deployment was not performed; cloud secret delivery, deployed egress/security
and non-development execution remain unvalidated. See the [semantic validation record](../../specs/002-semantic-movie-search/quickstart.md)
and the [traditional validation record](../../specs/001-movie-discovery-recommendations/quickstart.md).

## Project Governance

Constitution v4.0.0 authorizes read-only semantic discovery from
`sample_mflix.embedded_movies` in the same cluster, using native tools and official
PyMongo. Existing title/filter/rating behavior remains unchanged. The semantic index
and Voyage 4/2048/cosine mapping were verified locally; any index adjustment remains
manual maintainer work. Optional images require proven native chat support; otherwise
the active contract is text-only.

The [Movie Scout constitution](../../.specify/memory/constitution.md) governs all
specifications, plans, tasks, and implementation. Principle I takes precedence:

- Use the official `agentengine` CLI, generated configuration structure, Python runtime,
  and supported agent/tool interfaces. Verify technologies and dependencies against the
  [official getting-started guide](https://www.mongodb.com/docs/agentengine/get-started/)
  and relevant official documentation before approving them.
- Keep one conversational agent; do not introduce custom APIs, servers, frontends,
  external orchestration services, alternative databases/deployment platforms, or extra
  infrastructure. The native local development UI is permitted.
- Retrieve movie facts only from Atlas `sample_mflix.movies` with read-only,
  least-privilege access in the implemented traditional flow; v4.0.0 permits only the
  additional semantic source described above. Do not fabricate metadata or substitute a local platform database
  for the Atlas movie dataset. Keep movie-tool permissions distinct from platform operations.
- Use documented secret mechanisms and keep credentials out of source control.
- Constitution v3.0.0's temporary broad-identity exception applies ONLY to local development
  and bounded native tests; such credentials must never be called read-only. The current
  separate movie identity now passes feature 001 T049's complete effective collection-find-only check
  and does not need that exception. Keep separate URI roles, no movie-client fallback
  and allowlisted reads only; preserve least privilege before any non-development use. Existing
  deployment examples below are NOT authorization or evidence of release readiness.
- Follow GitHub Spec Kit: approved specification, compliant documented plan, tasks,
  incremental implementation, and platform-supported validation.

Constitution v2.0.0 introduced the official MongoDB Python driver exception inside native
Agent Engine tools for read-only movie access, extended only as scoped in v4.0.0.
The approved original amendment closes the earlier
B1 documentation blocker; it is not named platform certification or a completed runtime
test. See the [feature plan](../../specs/001-movie-discovery-recommendations/plan.md).

Validation MUST cover successful grounded recommendations, empty results, invalid
requests, missing metadata, and tool failures. Record outcomes using native platform
testing/debugging capabilities; no external testing or monitoring service is required.

**Features:** Native memory and automatic extraction are enabled in the current configuration.
They remain unchanged; incidental retention is permitted, while movie recommendations must
not explicitly save preferences or consult cross-conversation profiles.

## Implemented behavior

- Literal case-insensitive title containment, including punctuation as data.
- Combined title/genre/year/IMDb filters, explicit AND/OR, strict and inclusive bounds;
  science fiction maps to Sci-Fi. Unknown genres/essential ambiguity ask for clarification.
- Highly rated recommendations use numeric catalog IMDb descending, without a hidden
  minimum. Missing ratings never fill a rated shortfall; missing facts remain unavailable.
- Default five, maximum ten results. Original counts above ten produce a cap notice;
  fewer eligible records produce a separate shortfall, never invented substitutes.
- Same-session successful criteria survive refinements. Replacing a year/rating dimension
  clears its previous endpoints/strictness; invalid/unavailable changes do not overwrite
  successful criteria. “Start over” starts fresh. Incomplete new-session follow-ups clarify.
- Movie/mixed turns expose movie/date tools only and independently block profile dispatch.
  Ask for any nonmovie memory operation in a separate turn. Native automatic recording
  and extraction remain enabled; this is not a zero-retention promise.
- Native date and compatible standalone nonmovie memory behavior remain available.
- Semantic plot discovery accepts Portuguese or English descriptions, default five and
  maximum ten results, genre/year/IMDb filters, strict/inclusive bounds, and honest
  `empty`/`unavailable`/shortfall outcomes from `sample_mflix.embedded_movies`.
- Semantic and traditional criteria are separate. A same-session semantic refinement
  can replace semantic dimensions, while a new session asks for clarification instead
  of importing movie criteria from history or profile memory.
- Image output is not part of the active contract. Poster-like fields are discarded and
  no URL is fetched, validated, proxied, or used for external enrichment.

Examples: “Find Batman Begins”; “Find two Action or Adventure movies from 2005, IMDb at
least 8”; “Describe a tense story about navy divers in a rescue mission”; “Recommend
three highly rated comedies from the 2000s”; then “Only after 2005” or “Instead in 2009”;
“Start over: find two science-fiction movies”. Facts always come from the bounded
read-only Atlas tool, never model/profile recollection.

Projects generated by `agentengine create` contain the selected LLM client. Azure presets supply authentication and protocol headers automatically;
every client reads `LLM_API_KEY` from `.env` or project secrets.
Manual setup generates a builder stub to implement before running the agent.

Memory extraction runs in a separate service. In this repository, `project-config.yaml`
explicitly selects `LLM_API_KEY` for extraction as well as the agent client. Do not assume
a separate `OPENAI_API_KEY` is required by the current configuration. Embeddings also
require `VOYAGE_API_KEY`; the installed memory runtime recognizes `VOYAGE_URL` for an
optional compatible base-URL override, not `ENDPOINT_URL_VOYAGE`.

## Quick Start

### Which connection is used where?

| Variable | Consumer | Purpose |
|----------|----------|---------|
| `MOVIES_MONGODB_URI` | Registered `search_movies` → movie-client factory | Atlas catalog, fixed `sample_mflix.movies`, bounded reads only; no operational fallback |
| `MONGODB_URI` (reserved native name) | Native platform/checkpointer and operational services, including memory storage | Execution state, history and memory; never the movie-tool selector |

Local development defaults to `services.mongodb.local=true`. The CLI injects a local
operational URI, which can differ from the value in private configuration. A remote
operational URI requires the documented `services.mongodb.local=false` setting; do not
change that setting merely to test the catalog. Keep both canonical variable names:
renaming the reserved platform variable or adding movie aliases obscures this boundary.

The generated supervisor preserves injected `MONGODB_URI` and passes movie secrets to
the tool worker. Application `load_dotenv()` does not override existing environment.
The movie client is cached per worker process; editing private configuration does not
prove that a running client changed. Verify the actual worker against the private source
before considering a supported reload. Do not print private values or raw diagnostics.

The opt-in [connection audit](tests/native_connection_audit.py) independently reads the
private movie configuration on the host, compares the unique native TOOL worker,
checks fresh-client authentication/permissions and observes the real SDK-registered
movie tool's factory/namespace. It prints only categories/booleans and user counts.
It performs bounded reads, never write probes, memory calls or infrastructure changes.
Direct registered-tool validation is not an OE/model conversation test. See the
[current audit evidence](../../specs/001-movie-discovery-recommendations/quickstart.md#independent-connection-selection-audit--2026-10-22).

Before starting, privately configure the existing provider/memory prerequisites and the
dedicated `MOVIES_MONGODB_URI` secret. It has no fallback to platform `MONGODB_URI`.
The local platform database is not the movie source. Never commit credentials or paste
them into chat. Keep the generated provider, extraction and service configuration.

- Set `LLM_API_KEY` for the configured client
- Preserve existing private configuration. In default local development, the CLI injects
  the operational `MONGODB_URI`; do not replace it with the movie catalog URI.
- Preserve the existing verified LLM builder/provider; no switch is required.
- Native memory is already enabled with `features.memory: true` in `agent.yaml`;
  configure its compatible embedding credential through `VOYAGE_API_KEY`.

Movie operations use only fixed collection/projection, bounded allowlisted find queries,
ten-second outer CSOT and nested five-second server/consumption budget. Failures are
sanitized unavailable outcomes, not empty results or permission to fabricate movies.

## Validation matrix

Run the offline suite first from this directory:

```bash
PYTHONPATH=src:tests uv run pytest -q
PYTHONPATH=src:tests uv run python -m unittest tests/test_semantic_images.py
uv run ruff check src tests
uv run pyright  # atualmente reporta 34 diagnósticos de tipagem conhecidos
agentengine agent validate
```

For native validation, start the configured local stack with `agentengine dev up`, then
use the root [complete validation matrix](../../README.md#6-roteiro-completo-de-validação).
Traditional title/filter cases must invoke `search_movies` against
`sample_mflix.movies`; plot descriptions must invoke `search_semantic_movies` against
`sample_mflix.embedded_movies`. Verify route, source, criteria, status, count and
shortfall in the native trace, not only the final prose.

Ruff e a suíte funcional são os checks verdes de referência. Pyright permanece como
check informativo: atualmente reporta 34 diagnósticos de tipagem conhecidos em
`main.py`, `state.py` e `tools.py`, sem invalidar os testes funcionais; não o registre
como PASS até esses diagnósticos serem corrigidos.

The read-only boundary helper can observe an existing semantic session:

```bash
PYTHONPATH=src:tests uv run python tests/native_semantic_checks.py \
  --origin real_catalog --session-id <SESSION_ID>
```

The conversation helper is opt-in and performs real calls (including a read-only
nonmovie-memory case); it must not be run indiscriminately because provider quota and
native history can be consumed. Never provoke an Atlas/provider failure to test
`unavailable`; use only the authorized disposable synthetic fixture for that branch.

Then start the local stack:

```bash
agentengine dev up
```

Once the local stack is running:

- Open the Playground UI at `http://localhost:3000` to chat with the agent
- The playground port is configured in `dev.yaml` under
  `services.playground.port`

Stop the local stack with:

```bash
agentengine dev stop
```

## Release gate

No build, deployment, resource provisioning or cloud-secret upload is authorized by local
validation. Feature 001 T049 was completed on 2026-10-22: the separate movie identity's complete
effective grants were verified as only find on the movie collection, without write probes.
Preserve and revalidate that scope in the target environment. Platform-managed storage
retains its separate operational role. Cloud secret delivery, deployed egress/security and
execution remain unvalidated. See the feature plan and validation record for exact tested
versions, native evidence and outstanding limitations.
