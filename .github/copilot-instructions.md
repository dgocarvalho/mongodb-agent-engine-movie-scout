<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan
at specs/002-semantic-movie-search/plan.md
<!-- SPECKIT END -->

Read `.specify/memory/constitution.md` before specifications, plans, tasks, or implementation.
It is authoritative; Principle I (MongoDB Atlas Agent Engine exclusivity) takes precedence.
Verify technology choices against https://www.mongodb.com/docs/agentengine/get-started/
and relevant official documentation. Unverified technologies remain unapproved except for
the explicitly scoped official-PyMongo path in constitution v2.0.0: native read-only movie
tools, official driver compatibility/API evidence, and mandatory native runtime validation.
Do not reopen the retired B1 named-integration-documentation requirement.
Constitution v3.0.0 also records the maintainer's exact “POde continuar” approval for
temporary LOCAL DEVELOPMENT ONLY use of the existing broad shared identity. Do not repeat
the approval loop or call those credentials read-only: known movie grants include insert,
update, remove and dropCollection. Preserve separate MOVIES_MONGODB_URI/MONGODB_URI roles,
no fallback, bounded allowlisted read-only tools, no writes/write probes or infrastructure
changes. T005 is DEV readiness; T049 completed on 2026-10-22 verifies find-only access
to sample_mflix.movies, not cloud readiness or permissions on any other collection.

Constitution v4.0.0 formalizes the maintainer's “A” approval: additionally allow semantic
read-only search of sample_mflix.embedded_movies in the same cluster through native tools
with official PyMongo. Preserve traditional functionality; no source fallback or arbitrary
pipelines. The historical broad-identity exception does NOT extend to semantic access.
Verify exact collection-find-only grants, schema/index/filter paths and compatible query
embeddings before native semantic use; T049 is not evidence for the new collection.
Any required existing-index adjustment is manual maintainer work, not agent permission
to mutate indexes/catalog/roles/network. Native images are optional and require official
support plus runtime evidence; otherwise text only. No custom UI/proxy/enrichment services.
Active semantic requirements are in specs/002-semantic-movie-search/spec.md. The semantic
plan at specs/002-semantic-movie-search/plan.md records the maintainer's exact “sim, aprovo”
on 2026-10-23 approving the scoped LOCAL TEST DEVELOPMENT documentary simplification.
No constitution amendment is needed or applied: official documented compatibility before
implementation and native validation before acceptance remain mandatory. G3 selects the
documented official voyageai==0.5.0 client with voyage-3-large/query/2048/float/truncation=False,
semantic Python runtime >=3.11,<3.15. G4-A is documentary API/runtime/build/secret/egress
feasibility for this revised path, NOT operational PASS. Replace the unsupported hard
global30s guarantee with measured healthy>=19/20<=20s and failure30s TARGET, not guarantee
or server cancellation. Keep explicit supported provider<=6s/DB<=5s/tool12s proposed budgets,
bounded work and zero application retries; no assumed global OE/model deadline propagation.
G4-B is the single mandatory LOCAL acceptance checklist, currently NOT RUN: resolve/import
dependencies and verify actual secret delivery/segregation, endpoint binding/egress/connectivity
and native search/filters/sanitized failures/state/security/traditional regression/relevance/timing
DURING implementation and BEFORE acceptance, not circular pre-code results. Do not fabricate
PASS or hide overruns. The recorded approval must not be requested again; a separate
implementation workflow may proceed after reconciling T001–T011, not in this docs-only invocation.
Semantic presentation requires usable recovered ID/title AND plot; exclude missing,
null, nonstring, empty or whitespace-only plot, preserving eligible relative order and
reporting shortfall/empty without invented plot/affinity, fallback or refill queries.
This rule does not change traditional missing-metadata behavior.
Feature-001 planning remains historical traditional-flow context. Feature002 already
has 55 unchecked tasks; preserve IDs, checkbox states, stories and all13[P] mappings.
The same2026-10-23 approval permits in-place amendment only of clauses conflicting with
this simplification (including T001/T008–T011/T018 and deadline wording); never regenerate tasks.
Current evidence checkpoint 2026-10-23: G1 PASS for exact local native movie configuration
(find only on both collections); G2 PASS with bounded first100 sample plus maintainer
attestation of manual filter additions/Ready/Queryable and MongoDB9.0.4. Not cloud,
exhaustive schema or actual vector-query acceptance. Provenance corroborated by official
sample_mflix docs and maintainer Load Sample Dataset: plot/voyage-3-large/2048.
Preserve existing VOYAGE_API_KEY/VOYAGE_URL; do not request endpoint/key again or assume
memory delivery/egress is tool delivery. Select explicit api_key/base_url binding of the
EXISTING VOYAGE_API_KEY/VOYAGE_URL in the necessary TOOL sandbox through official mechanisms,
no autodetected destination/fallback or secret reads/requests now. Actual resolution,
binding/egress/model access remains unproven until G4-B; documented selection is not installation.
Execution-duration policy does not interrupt in-flight calls; client timeout is not server
cancellation. Earlier G3 partial/G4-A BLOCKED statements are historical, superseded only
by the approved local plan revision, not invented native evidence. See current research.
Do not implement, regenerate tasks, or mutate/restart the running stack in this
planning-only revision; preserve existing artifacts rather than replacing with templates.
Operational start/stop/restart/build/deploy still requires separate authorization; no
catalog/index/role/network mutations, new infrastructure or cloud-readiness claims.
