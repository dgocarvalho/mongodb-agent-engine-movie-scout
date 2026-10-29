# Feature Specification: Movie Discovery and Recommendations

**Feature Branch**: `master` (existing branch; no branch-creation hook is configured)

**Feature Directory**: [specs/001-movie-discovery-recommendations](.)

**Created**: 2026-10-19

**Status**: Implemented and validated locally; native V01–V22 evidence reconciled.
**2026-10-22:49/49 tasks complete**, including T049's fresh native proof of a separate
movie identity with exclusively find on sample_mflix.movies. Constitution v3.0.0 and
accepted behavior unchanged; current movie access no longer needs the temporary broad
credential exception. Deployment not performed; cloud delivery/egress/security and
non-development execution remain unvalidated. See [current credential evidence](quickstart.md#t049-complete-fresh-native-find-only-verification--2026-10-22).
See [validation](quickstart.md#current-local-validation-checkpoint--2026-10-21) and
[requirement reconciliation](plan.md#current-acceptance-reconciliation--t044-2026-10-21).

**Input**: User description: Extend the existing Movie Scout Agent Engine project with
conversational title search, combined movie filters, grounded recommendations, and
natural-language follow-ups using Atlas `sample_mflix.movies`; preserve compatible
existing functionality and configuration without regenerating the project.

## Clarifications

### Session 2026-10-20

- Q: Continue local development with the existing broad shared database identity? → A:
  Exact maintainer reply “POde continuar” to the explicit exception warning recorded in
  constitution v3.0.0. Approved ONLY for temporary local development/native tests with
  strictly read-only tools, separate configuration roles and no fallback. Known grants
  include insert/update/remove/dropCollection; these are NOT read-only credentials.
  Separate verified collection-find-only identity remains mandatory before deployment or
  non-development acceptance (T049). Earlier diagnostic-only restrictions are superseded
  within this scope; no provisioning, network changes, secret upload or deployment approved.

- Q: How should existing native memory behave during movie conversations? → A: Keep existing native memory and automatic extraction unchanged. Native storage may retain movie preferences, but this feature neither explicitly saves them nor uses cross-conversation profiles for recommendations (Option A).
- Q: How should B1, the missing official movie-data integration evidence, be pursued? → A: Keep the constitution unchanged and seek an official Agent Engine reference supporting application-data queries. B1 remains open until that evidence is verified; no undocumented driver or integration is approved (Option A).
- Q: May B1 be resolved through a scoped constitution amendment? → A: Approved “Approve scoped driver amendment”: permit the official MongoDB Python driver inside Agent Engine tools for read-only Atlas movie access, with documented driver compatibility and native runtime validation. This supersedes the earlier evidence-only B1 decision; constitution v2.0.0 governs. No application implementation or deployment occurred through this approval.
- Q: Should unrated movies remain eligible when the user asks for highly rated recommendations? → A: Exclude movies without an available numeric IMDb rating, sort rated matches descending, and explain any shortfall without filling positions with unrated movies. No minimum score is implied; requests without rating constraints or rating-prioritized ordering may include unrated movies (Option A).
- Q: How should a request combining movie discovery with a nonmovie profile-memory operation behave? → A: Complete the movie request where possible, perform no explicit profile save or lookup on that turn, and ask the user to submit the memory operation separately. Standalone compatible nonmovie memory behavior and native automatic extraction remain unchanged (Option A).

## User Scenarios & Testing *(mandatory)*

Validation MUST exercise the existing platform-supported local conversational interface.
Expected outcomes below define acceptance, not a prescribed technical design. Record
conversation inputs, visible responses, the retrieved movie records supporting those
responses, and pass/fail outcomes using native platform capabilities. Successful search
fixtures MUST be selected from available records; an illustrative title is not proof that
matching data exists. Failure scenarios MUST not modify the movie dataset.

### User Story 1 - Search Movies by Title (Priority: P1)

As a user, I want to search using a complete or partial movie title so that I can find
specific movies and understand their basic information.

**Why this priority**: Title lookup is the smallest independently useful movie-discovery
capability and establishes that answers come from the available catalog.

**Independent Test**: Search for an existing full title, a partial title shared by available
records, and a nonexistent title. Compare every returned movie and displayed fact with
the retrieved records; no recommendation workflow is required.

**Acceptance Scenarios**:

1. **Given** a record with a known title, **When** the user requests that complete title,
   **Then** matching catalog movies are returned with title, release year, genres, IMDb
   rating, and a brief plot where those fields are available.
2. **Given** records whose titles contain a known fragment, **When** the user asks
   "Find movies with Batman in the title" using a fragment confirmed in the catalog,
   **Then** returned titles contain that fragment regardless of letter case and results
   do not exceed the applicable result limit.
3. **Given** no title matches the supplied text, **When** the user searches for it,
   **Then** the agent clearly states that no matching movies were found and invents none.
4. **Given** a matching record lacks a year, genres, rating, or plot, **When** it is
   displayed, **Then** the unavailable information is explicitly identified rather than
   filled from model recollection or represented as a zero rating.
5. **Given** distinct matching records share a title, **When** results are displayed,
   **Then** they remain distinct and are differentiated by available metadata such as year;
   the same source record is not repeated.

---

### User Story 2 - Discover Movies Using Filters (Priority: P1)

As a user, I want to combine natural-language movie filters so that I can find movies
matching my interests without learning query syntax.

**Why this priority**: Combined filters make discovery useful beyond a known title and
provide an objective way to check relevance.

**Independent Test**: Request movies by genre, exact year, year range, minimum IMDb rating,
and title, both individually and in combination; check every result against all active criteria.

**Acceptance Scenarios**:

1. **Given** matching records exist, **When** the user requests science fiction movies
   released after 2010 with an IMDb rating above 7, **Then** each result has the requested
   genre, a year strictly greater than 2010, and an available numeric rating strictly above 7.
2. **Given** matching records exist, **When** the user combines a title fragment, genre,
   inclusive year range, and minimum rating, **Then** every returned record satisfies all
   four criteria without silently relaxing any of them.
3. **Given** the user requests "from 2010 through 2015" and "at least 7", **When** matches
   are retrieved, **Then** the year endpoints and rating 7 are eligible; "before", "after",
   "above", and "below" instead apply strict comparisons.
4. **Given** a movie has an unavailable or nonnumeric rating, **When** a numeric rating
   filter is active, **Then** that movie is excluded rather than treated as having rating zero;
   without a rating filter it remains eligible if other criteria match.
5. **Given** no records satisfy all criteria, **When** discovery is requested, **Then** the
   response states that no matches were found for those criteria and may suggest changing
   a filter, but does not silently substitute nonmatching movies.
6. **Given** a reversed year range, a rating outside 0–10, or an invalid result count,
   **When** the request is submitted, **Then** the agent explains the invalid value and
   asks for correction instead of claiming successful matching results.

---

### User Story 3 - Recommend Movies (Priority: P1)

As a user, I want recommendations based on my explicit preferences so that I can choose
movies relevant to my interests and understand why they were suggested.

**Why this priority**: Grounded recommendations are Movie Scout's main user value and must
be available as a useful standalone conversation without requiring a prior title search.

**Independent Test**: Ask for three highly rated comedies from the 2000s using confirmed
matching catalog records; check distinctness, count, criteria, facts, and explanations.

**Acceptance Scenarios**:

1. **Given** at least three matching records with available numeric IMDb ratings exist,
   **When** the user asks "Recommend three
   highly rated comedy movies from the 2000s", **Then** exactly three distinct comedies
   released from 2000 through 2009 are returned, ordered by available IMDb rating for this
   explicit highly-rated request, each with a short preference-based explanation.
2. **Given** more than five matching records exist, **When** a user requests recommendations
   without specifying a count, **Then** no more than five distinct matching movies are returned.
3. **Given** fewer records match than requested, **When** recommendations are requested,
   **Then** only the available matching records are returned and the shortfall is explained;
   no invented or nonmatching movies fill the remaining positions.
4. **Given** a recommended movie has available metadata, **When** it is presented,
   **Then** factual fields reflect its retrieved record, subjective fit is clearly phrased
   as an explanation, and IMDb rating is identified as a catalog rating, not a personalized score.
5. **Given** no movies match, **When** recommendations are requested, **Then** the agent
   explains the absence of matches and may offer a filter adjustment without presenting
   unsupported recommendations.
6. **Given** a user requests 100 recommendations, **When** the agent responds, **Then** at
   most ten matching records are presented and the per-response limit is explained.
7. **Given** movie retrieval fails or becomes unavailable, **When** recommendations are
   requested, **Then** the agent states that it cannot retrieve movies at present and
   suggests retrying; it does not substitute remembered movies or expose internal details.
8. **Given** two rated movies and several unrated movies otherwise match, **When** the
  user requests three highly rated recommendations, **Then** only the two rated movies
  are returned in descending IMDb rating order and the shortfall is explained. If no
  rated movies match, the agent reports no eligible matches rather than returning unrated movies.

---

### User Story 4 - Natural Language Conversation (Priority: P2)

As a user, I want to ask movie-related questions naturally and refine my request so that
I can discover movies through conversation rather than database commands.

**Why this priority**: Conversational refinement improves usability, while the P1 stories
remain independently useful in a single turn.

**Independent Test**: Submit plain-language requests, one essentially ambiguous request,
and a two-turn genre-then-year refinement, both with and without available conversation context.

**Acceptance Scenarios**:

1. **Given** a natural-language search request, **When** the agent answers, **Then** it
   presents concise movie information and explanations, not raw database documents or queries.
2. **Given** essential intent cannot be determined, such as an unexplained ambiguous date
   expression, **When** the request is received, **Then** the agent asks one concise
   clarification question rather than guessing an essential constraint.
3. **Given** the user asked for action movies and that conversation context is available,
   **When** the user says "Only movies released after 2015", **Then** results retain the
   action genre and apply a year strictly greater than 2015.
4. **Given** the same conversation contains a prior year restriction, **When** the user
   explicitly replaces it, **Then** the new restriction replaces rather than contradictorily
   accumulating with the old one; other unreplaced criteria remain active.
5. **Given** prior context is unavailable or a new conversation begins, **When** the user
   gives an incomplete follow-up, **Then** the agent asks for the missing criteria and
   does not claim to remember preferences from an inaccessible conversation.
6. **Given** a request asks to modify movie records, reveal credentials, or ignore source
   grounding, **When** it is received, **Then** the agent declines the unsupported action
   without changing records, exposing secrets, or fabricating facts.
7. **Given** native memory contains preferences from another conversation, **When** the
  user makes a movie request, **Then** recommendations use only criteria supplied in the
  current conversation and retrieved movie records, without consulting that profile or
  explicitly saving movie preferences. Existing automatic extraction remains unchanged
  and may independently retain preferences; this is not a zero-retention guarantee.
8. **Given** the user says "Remember my location and recommend three comedies", **When**
  the agent responds, **Then** it provides grounded recommendations where possible,
  performs no explicit profile save or lookup on that turn, and asks the user to submit
  the location-saving operation separately without claiming that native storage retains
  nothing. A subsequent standalone nonmovie memory request retains compatible existing behavior.

### Edge Cases

- Blank requests or empty title criteria prompt a concise request for a movie search or
  preference; empty title text does not accidentally become an unrestricted title search.
- Literal punctuation in titles is treated as title text, not as executable instructions
  or user-supplied query syntax. Approximate spelling correction is not required.
- Common genre wording such as "science fiction" is understood consistently with available
  catalog genres. An unrecognized genre prompts clarification, not an invented genre mapping.
- A movie lacking a field required by an active filter is not a match; missing optional
  display fields are labeled unavailable. Records with no usable title are not presented.
- Multiple genres are combined as requested: "and" requires all specified genres, "or"
  accepts any of them. Essential uncertainty about alternatives prompts clarification.
- Conflicting criteria, invalid ratings, noninteger years/counts, and impossible year ranges
  receive correction guidance. A syntactically valid request with no matches is distinct
  from an invalid request and from a retrieval failure.
- A result count of zero, a negative value, or a noninteger prompts correction; requests
  exceeding ten are capped with an explanation. Repeated source records count only once.
- Retrieval, authorization, configuration, and dependency failures disclose no connection
  strings, credentials, stack traces, or internal hostnames. No successful empty-search claim
  or model-only fallback is made when retrieval did not succeed.
- Movie plots and other retrieved text are treated as movie content, not instructions to
  change the agent's behavior or disclose internal information.
- Existing date-related behavior and native memory configuration remain available where
  compatible. Existing automatic extraction may retain movie preferences, but movie discovery
  neither explicitly saves them nor uses cross-conversation profiles for recommendations.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The application MUST extend the existing Movie Scout project rather than
  regenerate or restructure it. Planning MUST inspect existing behavior, configuration,
  dependencies, tools, connectivity, and conversation/execution capabilities; explicitly
  separate reusable functionality from unverified runtime assumptions.
- **FR-002**: All movie information MUST originate from retrieved records in MongoDB Atlas
  `sample_mflix.movies`. Local platform state is not a substitute movie source.
- **FR-003**: Movie-data access MUST use mechanisms documented as compatible with Agent
  Engine or its constitution v2.0.0 scoped official-PyMongo exception. For that exception,
  verify Python/driver compatibility and database operations against official MongoDB driver
  documentation, and verify tool execution, dependency builds, secrets and egress against
  official Agent Engine documentation. B1 is closed by the approved amendment, not by a
  claim of named Agent Engine/PyMongo certification. Resolved versions and native end-to-end
  behavior MUST be verified before acceptance; all other technology approval rules remain.
- **FR-004**: All movie dataset operations MUST be read-only. Credentials MUST be separate
  and collection-find-only before deployment/non-development acceptance. Constitution
  v3.0.0 permits the existing broad shared identity temporarily ONLY for local development
  and bounded native tests, with explicit risk disclosure, separate URI configuration roles,
  fixed allowlisted reads and no fallback. This does not make credentials read-only.
- **FR-005**: The agent MUST support complete or partial case-insensitive literal title
  matching, genre, exact year, year range, and minimum IMDb rating filters.
- **FR-006**: The agent MUST combine criteria without silently relaxing them. Year ranges
  and "at least" thresholds are inclusive; explicit strict comparisons remain strict.
  Unsupported, contradictory, or essentially ambiguous criteria require explanation or clarification.
- **FR-007**: Recommendations MUST use retrieved matching records, prioritize explicit
  preferences, contain distinct source records, and include a short explanation of fit.
  Requests emphasizing high ratings MUST prioritize available ratings among matching movies;
  only records with an available numeric IMDb rating are eligible and MUST be ordered by
  descending rating. No minimum threshold is implied by "highly rated" alone. If fewer
  rated records match than requested, return those records and explain the shortfall;
  do not fill positions with unrated movies. Requests without rating constraints or
  rating-prioritized ordering MAY include unrated movies, labeled unavailable.
- **FR-008**: Search and recommendations MUST return up to five movies by default, honor
  explicit positive integer counts up to ten, and cap larger requests at ten with notice.
  Retrieval MUST use bounded result sets, not unnecessary full-catalog transfers. Fewer
  available matches MUST be reported honestly without padding results.
- **FR-009**: Results MUST present title, year, genres, IMDb rating, and a brief plot when
  available, labeling missing fields unavailable. Unknown ratings MUST NOT become zero.
  Missing or invalid fields required by active criteria MUST exclude that record from matching.
- **FR-010**: The agent MUST distinguish successful searches with no matches from retrieval
  failures. Both MUST receive understandable responses without fabricated recommendations;
  failures MUST suggest retrying or correcting the request where appropriate.
- **FR-011**: Existing configuration structure and compatible functionality MUST be
  preserved. The feature MUST continue to run through the existing supported Agent Engine
  development workflow without replacing configurations or requiring a separate application.
- **FR-012**: The feature MUST remain a single agent and MUST NOT introduce external
  orchestration, custom backends/APIs/frontends, alternative deployment platforms, additional
  database technologies, or unnecessary infrastructure.
- **FR-013**: Responses MUST distinguish objective retrieved facts from subjective fit
  explanations. IMDb ratings MUST NOT be described as personalized recommendation scores.
- **FR-014**: Responses and tracked artifacts MUST NOT reveal credentials or connection
  strings; user-visible responses MUST NOT reveal internal errors or infrastructure details.
  Secrets MUST use documented platform configuration and secret-management mechanisms.
- **FR-015**: The agent MUST accept natural-language movie requests and ask a concise
  clarification question when essential criteria cannot be interpreted. Users MUST NOT
  need query syntax, and responses MUST NOT expose raw database documents.
- **FR-016**: Follow-ups MUST reuse and refine active criteria when existing conversation
  context is available. Explicit replacements override prior criteria; unavailable context
  MUST prompt clarification rather than invented memory. Existing native memory and automatic
  extraction MUST remain unchanged and MAY retain movie preferences under their existing
  behavior. This feature MUST NOT explicitly save movie preferences, consult cross-conversation
  profiles for recommendations, or introduce custom memory infrastructure. It does not
  guarantee that native storage contains no movie preferences.
  A turn combining movie discovery with a nonmovie profile-memory request MUST perform
  no explicit profile save or lookup. The agent MUST complete the movie request where
  possible using current-conversation criteria and retrieved records, and ask the user
  to submit the memory operation separately. Standalone compatible nonmovie memory
  requests remain supported; native automatic recording and extraction remain unchanged.
- **FR-017**: The agent MUST reject unsupported mutation requests and treat user-supplied
  title text and retrieved content as data, never authorization to bypass grounding or security.
- **FR-018**: Validation MUST cover all four user stories, successful recommendations,
  empty results, invalid requests, missing metadata, retrieval/tool failures, safe error
  disclosure, read-only access, and compatible starter behavior through supported local
  platform capabilities, recording results and source-record evidence.

### Key Entities *(include if feature involves data)*

- **Movie Record**: An authoritative catalog item identified by its source-record identity;
  carries a title and, when available, release year, genres, IMDb rating, and plot. Identical
  titles alone do not imply identical records.
- **Movie Criteria**: The user's active title text, genres, year restrictions, rating
  restriction, and requested count; includes explicit alternatives and replacements.
- **Movie Result**: A retrieved matching movie presented with available facts and clear
  missing-data indicators, optionally accompanied by a subjective recommendation explanation.
- **Conversation Context**: Prior messages or active criteria available in the current
  conversation; availability is conditional and is not a persistent preference profile.
- **Retrieval Outcome**: A successful bounded set of matching records, a successful empty
  result, or an unavailable/failed retrieval; these outcomes must remain distinguishable.

### Constitutional Constraints *(mandatory)*

- [Constitution v3.0.0](../../.specify/memory/constitution.md) governs this feature;
  Principle I takes precedence. This is an enhancement, not project initialization.
- MongoDB Atlas Agent Engine and its official CLI remain the exclusive development,
  execution, orchestration, and deployment platform. Preserve the generated Python project
  and configuration structure; use the existing platform-provided conversational interface.
- Official [Agent Engine documentation](https://www.mongodb.com/docs/agentengine/get-started/)
  is the primary reference. Runtime, dependencies, tools, database access, and secrets
  choices belong in the plan and require official compatibility evidence; existing
  dependencies are not automatically approved solely because they are present.
- Movie access remains read-only and Atlas remains the sole database technology. Native
  platform operational state/memory permissions do not authorize movie dataset writes.
- Follow approved specification → compliant plan → tasks → incremental implementation;
  prefer native capabilities, use supported local validation and native observability,
  and introduce no unnecessary external testing, tracing, or monitoring service.
- Any scope deviation requires an explicit constitution amendment; this specification
  does not authorize implementation before approval and technical planning.

### Non-Functional Requirements

- **NFR-001 — Simplicity**: Reuse compatible existing components and preserve one agent;
  avoid abstractions and dependencies that are unnecessary for the approved behavior.
- **NFR-002 — Compatibility**: The technical plan MUST document support for each selected
  technology against official documentation and leave no unverified choice silently approved.
- **NFR-003 — Bounded work**: Each movie retrieval and response MUST be bounded to the
  applicable count limits; satisfying a request MUST NOT require transferring the full catalog.
- **NFR-004 — Maintainability**: Movie interpretation, retrieval, and response behavior
  MUST have separately identifiable acceptance checks; implementation organization is deferred.
- **NFR-005 — Reliability and security**: All specified invalid-input, missing-data, and
  unavailable-dependency cases MUST terminate in understandable outcomes without invented
  facts, dataset mutation, or disclosure of internal details.

### Out of Scope

- Recreating/restructuring the Agent Engine project or replacing its configurations.
- Custom web/mobile interfaces, separate backend APIs, external orchestration, extra agents,
  or production-scale deployment architecture.
- Vector Search, embedding generation for movie discovery, fuzzy spelling search,
  external movie services such as TMDB or IMDb, and movie-record modifications.
- Feature-added persistent movie preference profiles, explicit movie-preference saves,
  use of cross-conversation profiles for recommendations, custom conversation-memory
  infrastructure, or changes to existing native memory and automatic extraction settings.
  Incidental preference retention by unchanged native behavior is permitted.
- Additional authentication beyond existing Agent Engine capabilities.
- Exhaustive catalog browsing, pagination, or responses larger than ten movies.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All full-title, partial-title, mixed-case, nonexistent-title, and missing-field
  acceptance searches produce the specified outcome through the existing conversational
  interface; every displayed factual field matches the supporting source record.
- **SC-002**: In 100% of combined-filter acceptance requests, every returned movie satisfies
  all active title, genre, year, and rating conditions; boundary values follow the requested
  inclusive/strict interpretation and unavailable ratings never satisfy numeric constraints.
- **SC-003**: A request for three recommendations returns exactly three distinct matching
  source records whenever at least three exist. Default requests return at most five and
  no response exceeds ten; shortfalls and caps are explained in every applicable test.
  For highly rated requests, only records with available numeric IMDb ratings count as
  eligible matches; mixed-rated and all-unrated acceptance cases follow FR-007 with no
  unrated fallback.
- **SC-004**: 100% of acceptance-test recommendations correspond to retrieved records,
  include a short preference-based explanation, and never label a catalog rating as a
  personalized score. There are zero invented movies or unsupported factual claims.
- **SC-005**: All empty-result, malformed-request, missing-field, unavailable-context, and
  retrieval-failure scenarios produce understandable outcomes, with zero fabricated fallback
  recommendations and zero disclosures of credentials, connection strings, or internal errors.
- **SC-006**: All context-available refinement tests retain unreplaced criteria and apply
  replacements correctly; all context-unavailable tests ask for essential missing criteria.
  Across all movie acceptance scenarios, there are zero feature-initiated explicit movie-preference
  saves or cross-conversation profile lookups for recommendations. Existing native memory
  and automatic extraction settings remain unchanged; incidental native retention is not
  treated as a failed acceptance test.
  All mixed movie/nonmovie-memory acceptance turns perform zero explicit profile saves
  or lookups, explain the separate-request requirement, and follow ordinary movie outcomes.
  A separate standalone nonmovie-memory regression check preserves compatible behavior.
- **SC-007**: All four user stories and compatible starter-behavior checks pass through
  the existing local conversational workflow with recorded evidence, without regenerating
  the project, adding another user interface, or introducing extra infrastructure.
- **SC-008**: The movie dataset is unchanged throughout acceptance validation, tracked
  changes contain zero credential values, and every introduced technology choice has
  documented approval before implementation acceptance.

## Assumptions

- **Existing-project baseline**: Repository inspection on 2026-10-19 is static evidence,
  not proof of live operation. No credentials were inspected, no movie queries were run,
  and no application code or runtime configuration was changed while writing this spec.
- **Observed agent**: [Agent entrypoint](../../agents/movie-scout/src/agent_movie_scout/main.py)
  already registers one agent, a model/tool conversation loop, and native checkpointing.
  [Conversation state](../../agents/movie-scout/src/agent_movie_scout/state.py) carries messages.
  These are reuse candidates subject to documented compatibility and runtime checks, not
  proof that multi-turn criteria retention currently works.
- **Observed behavior and tools**: [Starter instructions](../../agents/movie-scout/src/agent_movie_scout/system_message.py)
  describe the Daily inspiration assistant. [Existing tools](../../agents/movie-scout/src/agent_movie_scout/tools.py)
  implement date lookup and native profile save/recall, not movie search. Date lookup and
  compatible existing platform functionality should be reused without unnecessary changes;
  movie-discovery behavior is new and the starter identity must not override it.
- **Observed configuration/dependencies**: [Agent configuration](../../agents/movie-scout/agent.yaml)
  enables durable workflow and native memory, registers the three starter tools, and
  declares provider network access. [Dependencies](../../agents/movie-scout/pyproject.toml)
  declare Python 3.11+, Agent Engine runner/SDK, and model/tooling libraries.
  [Model configuration](../../agents/movie-scout/src/agent_movie_scout/llm.py) selects an
  existing provider client. These facts do not establish support or availability for any
  proposed movie-data access approach; the plan must verify them without replacing the project.
- **Observed connectivity**: [Local development settings](../../agents/movie-scout/dev.yaml)
  document default local platform services; [environment placeholders](../../agents/movie-scout/env.example)
  do not establish live Atlas access. No current movie tool or demonstrated connection to
  Atlas `sample_mflix.movies` was found. Provisioned secrets, dataset presence, network access,
  permissions, and live provider/tool availability remain unverified dependencies for planning.
- **Native-memory boundary**: Native profile memory is already configured as enabled,
  despite the [starter README](../../agents/movie-scout/README.md) describing it as off by
  default. Preserve existing native memory and automatic extraction unchanged. Native
  storage may retain movie preferences through that behavior; no zero-retention guarantee
  is made. Movie requests MUST NOT initiate explicit movie-preference saves or use
  cross-conversation profiles for recommendations. Compatible existing nonmovie memory
  behavior remains in scope for preservation. This approved scope resolves the B2 policy
  ambiguity; the plan and recovery tasks must be reconciled with it during replanning.
  Existing native-memory operation is not claimed as runtime-verified.
- **Default semantics**: Search and recommendations share a five-result default and
  ten-result maximum. Title matching means a literal case-insensitive substring, not fuzzy
  search. Four-digit years and conventional decade wording are supported; the 2000s mean
  2000–2009. Valid year values are integers from 1–9999, rating thresholds are numeric from
  0–10, and explicit result counts must be positive integers.
- **Preference interpretation**: Ordinary genre wording may map to equivalent catalog
  labels, but uncertain mappings require clarification. "Highly rated" requests exclude
  unavailable or nonnumeric ratings and rank eligible matches by descending rating without
  imposing an invented threshold; explicit numeric cutoffs govern
  eligibility. General recommendation requests may offer grounded discovery without requiring
  a profile or asking for nonessential preferences.
- **Dependencies and approval**: An accessible Atlas sample movie collection, authorized
  read-only movie access, working existing execution/model services, and a documented
  supported connection approach are required before acceptance testing. Their absence
  blocks runtime verification, not specification quality; selection/setup belongs to planning.
  The accepted B1 path preserves the constitution and requires verified official Agent Engine
  application-data integration evidence. A clarification, local prototype, or successful
  platform startup alone does not close B1 or approve an undocumented movie-data integration.
  Spec quality validation does not imply feature implementation or runtime success.