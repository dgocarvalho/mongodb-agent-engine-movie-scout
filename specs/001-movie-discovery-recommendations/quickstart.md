# Quickstart Validation: Movie Discovery and Recommendations

## T049 complete: fresh native find-only verification — 2026-10-22

**Current authority:2026-10-22T18:47:36Z;49/49 complete, T049 [X].** This checkpoint
supersedes all older open-T049, broad-grant and four-action findings below as current
claims; those findings remain historical. The administrator's role change was verified,
not inferred from the reported change or a successful read alone.

| Check | Fresh native result |
|-------|---------------------|
| Independently parsed private movie identity | Intended movie_scout_reader; different principal/username from private operational identity |
| Actual unique TOOL worker's movie URI | Exact private-configuration match; no fallback or reload |
| Newly constructed MongoClient authentication | Exactly one authenticated principal, matching intended username and driver-resolved authSource |
| Complete connectionStatus(showPrivileges=true) effective grants | One understood exact sample_mflix.movies resource; actions exclusively find |
| Strict collection-find-only / additional resources | true / false |
| Movie insert, update, remove, dropCollection | All false; complete action set contains no other action |
| Bounded ID-only read / document present | READ_OK / true |
| Wire checks | One ID-only limit1/batch_size1 find, server<=5000ms; one metadata command; no unexpected application command |
| Real SDK registered search_movies in fresh TOOL-mode process | ok; factory uses the same private movie URI, one bounded production-projection find; own-client reuse PASS |
| Cursor/client cleanup | PASS; diagnostic and registered-tool clients closed |
| Initial/final native status / Playground | ok5/5 / ok5/5 / HTTP200 |
| Original five container identities / protected configuration and source bytes | Preserved / unchanged |

The [existing audit helpers](../../agents/movie-scout/tests/native_connection_audit.py)
ran using the actual TOOL interpreter/environment, independently compared with private
dotenv values in memory. No existing worker session/pool was reused or inspected. Effective
privileges include inherited/global grants; acceptance required the complete set, not a
role name. In-memory classification normalized resource-key/action order and duplicate
actions, ignored only explicitly false boolean resource flags, rejected malformed/unknown
forms and failed closed on global/wildcard/extra grants. Seven offline classifier controls
passed before the native check. Read consumption used outer10s/nested5s CSOT and finally
cleanup; launcher deadlines were bounded. The SDK check is not a new OE/model regression.

Native operational MONGODB_URI remains the separately injected unauthenticated local
stack service, not the private remote operational URI; movie access remains exclusively
MOVIES_MONGODB_URI. No secrets, URI/hosts, authSource values, raw metadata/errors/logs,
hashes or document IDs were emitted. No private/source/configuration edits, restart,
write probes, role/user/network/index changes, memory/fixture operations, provider or
extraction changes, cloud-secret upload or deployment occurred.

T049's credential criterion is now satisfied under unchanged constitution v3.0.0; the
temporary broad-identity exception is not needed for this verified movie identity.
Existing native behavior acceptance is retained, not rerun. Documentation-only updates
do not require another full application regression. **49/49 does not certify cloud
secret delivery, deployed egress/security or non-development execution; deployment was
not performed.** No before_implement/after_implement hooks are registered.

## Historical T049 checkpoints (superseded as current status)

## Metadata-only T049 recheck — 2026-10-22

**Fresh observation:2026-10-22T18:06:30Z;48/49 complete, T049 OPEN.** One new
native client, using the actual unique TOOL worker's interpreter and current movie
configuration, issued exactly one connectionStatus(showPrivileges=true). No catalog
read, registered-tool invocation or model regression was repeated in this checkpoint;
the successful corrected-URI read/tool evidence below remains historical evidence.

- Current native movie URI matches the independently parsed private configuration;
   movie/operational configured principals and usernames are distinct.
- METADATA_OK; exactly one authenticated principal matches the configured movie
   username and driver-resolved authSource. All returned resource forms are understood.
- Complete effective grants: one exact sample_mflix.movies resource; actions **collStats,
   dbHash, find, listIndexes**, no other action or resource. No write privileges observed.
- Strict collection-find-only=false solely because of the three additional non-write
   actions. The corrected association below remains valid; older mutation-grant findings
   do not describe this current reader.
- Own client closed; no unexpected application command. Initial/final native status
   ok5/5; all five container identities and protected configuration bytes preserved.

No private values, raw metadata/errors, URI/host/identity details or hashes were emitted.
No private edits, restart, role/account/network/index/catalog changes, write probes,
memory/fixture operations, cloud-secret upload or deployment occurred. No implementation
task is available within the unchanged approved scope; application tests were not rerun.

**Unblock:** an authorized administrator can privately remove collStats, dbHash and
listIndexes, leaving only find on this collection, followed by bounded revalidation.
Alternatively, accepting these additional non-write actions requires explicit maintainer
approval of a Principle V constitutional amendment and synchronized requirements/contracts/
tasks; a new implement command alone does not approve or enact that change.

## Corrected private URI association — 2026-10-22

**Latest result,2026-10-22T18:01:13Z:48/49 complete; T049 OPEN only for extra
non-write privileges.** The maintainer privately swapped the previously misassigned
URI values. This section supersedes older current-identity/broad-movie-grant claims below;
those measurements are historical and do not establish grants for the intended reader.

| Check | Fresh observed result |
|-------|-----------------------|
| Private movie URI username equals intended movie_scout_reader | true |
| Private operational URI configured, different, username not the reader | true |
| Actual unique native TOOL-process movie URI equals current private value | true |
| Native movie username equals intended reader; operational username differs | true |
| Reload needed / performed | false / false |
| Fresh native ID-only read / document present | READ_OK / true |
| connectionStatus(showPrivileges=true) / authenticated principal | METADATA_OK / exactly one, matching intended username and driver-resolved authSource |
| Complete effective privilege entries / understood resource forms | 1 / true |
| Exact resource / complete effective actions | sample_mflix.movies / collStats, dbHash, find, listIndexes |
| Extra resources / observed movie insert, update, remove, dropCollection | false / all false |
| Built-in read/readAnyDatabase role present | false; no role-inheritance assumption made |
| Strict collection-find-only criterion | false: three additional non-write actions |
| Wire audit | one ID-only limit1/batch1 find, server<=5000ms; one metadata command; no unexpected application command |
| Real SDK registered search_movies | ok; factory uses current private movie URI, one bounded production-projection find; own cache reuse PASS |
| Own cursor/client cleanup | PASS |
| Final native status / Playground | ok5/5 / HTTP200 |
| Protected configuration bytes / original container identities preserved | true / true |

Private comparisons and driver principal resolution remained in memory; no URI, host,
password, key, authSource value, raw metadata or error/log output was exposed. The bounded
[existing audit](../../agents/movie-scout/tests/native_connection_audit.py) ran in a fresh
process using the actual TOOL worker's interpreter/environment and a newly constructed
MongoClient from MOVIES_MONGODB_URI, never platform MONGODB_URI or a cached worker client.
The ID-only control used outer10s/nested5s CSOT and finally cleanup. The registered SDK
tool independently confirmed production factory/namespace/projection selection, not a new
OE/model acceptance run or inspection of the long-running worker's heap/pool.

Native operational storage still uses the legitimate unauthenticated local stack service,
not the private remote operational URI; this is documented native local injection, not
movie credential reuse. Initial health-summary counting searched for status strings and
returned zero markers, not zero healthy services; a corrected schema-aware check confirmed
status=ok,running=5,total=5, with four healthy containers and the UI running.

**Remaining action:** an authorized administrator must privately remove collStats, dbHash
and listIndexes from the reader's effective grant set, leaving only find on
sample_mflix.movies, then repeat the bounded authentication/read/metadata proof. No write
privileges were observed in this complete current grant set; do not repeat the historical
claim that this intended reader grants movie mutations. Do not weaken the exact T049
criterion or substitute mere successful connectivity for least-privilege proof.

No private file changes, restart, catalog/write probes, role/user/network/index changes,
memory/fixture operations, provider/extraction changes, cloud-secret synchronization or
deployment occurred. Only the three current evidence/task documents changed; application
tests were not rerun for this documentation-only checkpoint. Existing local acceptance
remains scoped as recorded; cloud delivery/egress/non-development execution is unvalidated.
No before_implement/after_implement hooks are registered.

## Independent connection-selection audit — 2026-10-22

**48/49 unchanged; T049 OPEN.** Maintainer requested an independent review of which
connection each component and previous permission diagnostic actually uses. New public
[opt-in audit](../../agents/movie-scout/tests/native_connection_audit.py) and
[five offline regressions](../../agents/movie-scout/tests/test_connection_audit.py)
make the current procedure reproducible rather than relying on historical terminal claims.

| Connection | Actual selection and new evidence |
|------------|-----------------------------------|
| Movie catalog | Only MOVIES_MONGODB_URI; current private agent configuration independently read on host, not copied from the worker as the expected value. Host fresh read/metadata PASS; native unique TOOL-worker URI exactly matches that independent source. |
| Native operational storage | Reserved MONGODB_URI. Actual worker targets the local stack MongoDB service, with no configured authentication, and does NOT equal private MONGODB_URI. Default services.mongodb.local=true causes native local injection. Private operational credentials are therefore NOT the actual local operational credentials. |
| Registered search_movies | Real SDK tool invoked in a fresh independent TOOL-mode process; actual movie factory argument equals private MOVIES_MONGODB_URI; exactly one bounded wire find on sample_mflix.movies with the production projection; result ok. No main import, operational fallback, model/provider or memory invocation. |

Host and native fresh-client connectionStatus each returned exactly **one authenticated
principal**, matching the independently parsed movie username and driver-resolved authSource.
This rules out aggregation across multiple authenticated users for these new measurements.
Both controls positively attribute find/insert/update/remove/dropCollection to resources
matching the movie namespace. Actions on unrelated namespaces or cluster-only resources
are not credited to movies; anyResource=false is not treated as global access. Exact,
database/global/collection wildcard, anyAction, unrelated mutation, duplicate, empty and
malformed cases have offline regression coverage. No write probes were used.

**Classifier limitation:** metadata also contains resource forms outside this audit's
recognized namespace/cluster/anyResource forms. The safe output explicitly reports
all_resource_forms_understood=false, and complete collection-find-only acceptance fails
closed. The five positive movie-action findings come only from recognized matching
resources, not from those unknown entries. Do not describe every resource as fully
classified or infer that every returned action applies to movies. Prior ad-hoc classifier
source was not retained in the repository, so its exact implementation cannot be
independently certified retrospectively; this new source and fresh observations supersede
its attribution claims. Current broad movie access is independently reconfirmed.

Selection review: generated supervisor protects platform MONGODB_URI from guest override;
movie secret comes from CLI guest configuration. main's load_dotenv() defaults to
override=False, so existing process values win. Movie factory caches once per worker PID;
new environment values do not retarget an existing pool. Current startup environment
matches the independent private movie value; the long-running worker's Python heap/client
was not introspected. Fresh registered-tool proof is direct SDK evidence, NOT a new
OE/model conversation or proof of a pre-existing pool's internal state. No rename/alias
or production source change is justified: retain canonical MOVIES_MONGODB_URI and reserved
MONGODB_URI, with clearer documentation. Remote operational selection requires documented
services.mongodb.local=false, not another variable name; that setting was NOT changed.

Initial diagnostic implementation incorrectly assumed operational credentials must exist;
two native attempts stopped before their read on the legitimate unauthenticated local
URI. Corrected to distinguish absent local authentication from movie authentication.
Host controls in those attempts did succeed. Final two executions pass native selection,
fresh read/authentication and registered-tool checks; no failed attempt is called a pass.
All explicit catalog reads are limit1; independent controls use ID-only projection,
batch1 and wire cap<=5000ms under nested5s/outer10s budgets; registered tool preserves its
production bounded projection and budgets. Only categories/booleans/counts are printed;
no private URI/username/authSource/host/value/hash/length or raw metadata/error/log output.

**Validation:** 58 host tests PASS (previous53 plus five new regressions), Ruff PASS,
production Pyright0 errors/warnings. No full native conversation matrix rerun. No private
file edits, role/network/index/catalog writes, memory operations, uploads, deployment or
explicit stack restart. README and empty environment example now explain local injection,
canonical names, precedence and pool lifetime. No executable before/after implementation
hooks are registered. Non-development acceptance remains blocked by T049.

## Cluster-resumed fresh T049 verification — 2026-10-22

**Current checkpoint:48/49 complete; T049 OPEN because complete effective grants are
NOT collection-find-only.** Fresh observation at **2026-10-22T14:55:07Z**, following the
maintainer's report that the daily-paused cluster was resumed. This successful current
read/metadata attempt supersedes the earlier timeout and unknown-grant checkpoint below.
The pause/resume cause was reported by the maintainer, not independently diagnosed here.

| Check | Fresh observed result |
|-------|-----------------------|
| Private and actual native movie/operational parsed principals and usernames distinct | true |
| Actual native movie URI/principal matches current private configuration | true |
| Reload needed / performed | false / false |
| Fresh native bounded ID-only read | READ_OK; document present |
| Fresh connectionStatus(showPrivileges=true) | METADATA_OK; complete effective grants obtained |
| Server-authenticated principal equals configured movie principal | true |
| Strict complete collection-find-only classifier | false |
| Effective movie actions find / insert / update / remove / dropCollection | true / true / true / true / true |
| Additional privilege resources present | true; resource details withheld |
| Exactly one bounded wire find / metadata dispatched | true / true |
| Unexpected application command / write probe | false / false |
| Cursor/client cleanup | PASS |
| Initial/final native health / Playground | ok5/5 / ok5/5 / HTTP200 |
| Protected configuration bytes / original container identities preserved | true / true |

One newly constructed MongoClient ran in an independent process using the actual running
tool interpreter and its MOVIES_MONGODB_URI only; no cached application client or fallback
to operational credentials. Private configuration/principal comparisons happened only in
memory. The fixed sample_mflix.movies find used empty filter, ID-only projection, limit1,
batch_size1 and max_time_ms5000, inside nested5s and outer10s CSOT. The command listener
verified the single dispatched read's namespace/projection/limit and wire server cap<=5s;
driver-adjusted batch size remained bounded. Metadata used a nested5s budget, with finally
cleanup and bounded launcher deadlines. No document ID or raw response/error was printed.

The complete effective-action set was inspected privately and emitted as action names
only. In addition to the five movie actions above, it includes administrative, collection,
index and search-index mutation actions such as applyOps, collMod, createCollection,
createIndex, createSearchIndexes, dropDatabase, dropIndex, dropSearchIndex and
updateSearchIndex. This is positive current broad-grant evidence, not an inference from
read success. Extra resource metadata also fails the exact-resource criterion; no claim
is made that every action applies to every resource. Driver-internal authentication or
monitoring commands were observed separately and are not treated as privilege grants.
The fail-closed classifier's exact-find-only/wildcard/any-resource/extra-action/resource/
empty/malformed controls passed offline.

**Next gate:** an authorized administrator must privately reduce the movie identity's
complete effective privileges, including inherited/global/database grants, to only find
on sample_mflix.movies; then repeat this bounded current authentication/grant/read check.
No role/user/network/index/catalog mutation, write probe, cluster resume, secret upload,
deployment, memory/fixture operation or service restart was performed. Provider/extraction
and private/public configuration bytes were preserved. No full application regression was
rerun for this documentation-only update. Local evidence does not validate cloud secret
delivery, deployed egress/security or any deployment/non-development execution.

## Fresh T049 current-credential verification — 2026-10-22

**Earlier attempt, superseded by the cluster-resumed checkpoint above:**48/49 complete;
T049 OPEN because effective grants were UNVERIFIED at that attempt.
The maintainer explicitly authorized “pode fazer o teste, por favor” after reporting two
configured identities. This fresh observation supersedes statements below that historical
mutation grants are necessarily still current. It neither proves their removal nor
reconfirms them. No additional identity-creation approval or credential disclosure is needed.

| Check | Fresh observed result |
|-------|-----------------------|
| Private movie versus operational parsed principal / username distinct | true / true |
| Native movie versus injected operational parsed principal / username distinct | true / true |
| Actual native tool-process movie URI equals current private movie configuration | true |
| Parsed native movie principal equals current private movie principal | true |
| Reload needed / performed | false / false |
| Fresh native bounded ID-only read | FAILED: server-selection timeout before find dispatch |
| Fresh connectionStatus(showPrivileges=true) | UNAVAILABLE: server-selection timeout before command dispatch |
| Server-authenticated principal matches configured movie identity | UNVERIFIED; URI comparison is not authentication proof |
| Current complete effective collection-find-only grants | UNVERIFIED; fail-closed gate, not evidence of broad grants |
| Current insert/update/remove/dropCollection permissions | UNKNOWN; no current metadata obtained |
| Unexpected application command / write probe | false / false |
| Cursor/client cleanup | PASS in both fresh diagnostic processes |
| Native health before/after initial diagnostic | ok5/5 |
| Protected configuration bytes / original container identities preserved | true / true |

Two separate fresh clients were created in independent processes using the actual running
tool interpreter/environment, exclusively from MOVIES_MONGODB_URI; no cached application
client or operational database connection was used. The second bounded attempt classified
the first failure without printing raw exceptions: both read and metadata fail with
ServerSelectionTimeoutError and transport-timeout indicators. No authentication or
authorization rejection, TLS/DNS failure or connection-refused signature was observed;
this is not proof those layers would succeed after connectivity is restored. Monitoring
on the second attempt confirms neither find nor connectionStatus was sent. No documents
or current privilege metadata were retrieved; the exact external cause is unestablished.

Each client uses outer CSOT10s, nested5s read and metadata budgets, server cap<=5000ms,
fixed sample_mflix.movies ID-only find with limit1/batch_size1, finally cleanup and bounded
launcher subprocesses. The complete-grant classifier was checked offline against exact
find-only, wildcard, any-resource, extra-action/resource, empty and malformed cases.
Its false gate when metadata is unavailable is NOT a finding of mutation privileges.
Only fixed safe booleans/categories were emitted; no URI/user/host/value/hash/length,
raw logs, environment dump or container-inspection output was displayed.

Protected project/agent/dev/dependency/provider/private-dotenv bytes remained unchanged
across the initial diagnostic; all five running container identities were preserved.
No stop/up/restart, volume reset/removal, provider/extraction change, memory/fixture call,
role/user/network mutation, cloud-secret upload or deployment was performed. Existing
native acceptance evidence remains historical evidence, not rerun by this credential test.

**Next gate:** restore reachability of the currently configured movie endpoint from the
native tool runtime, then repeat the bounded read and effective-grant/authentication check.
Do not change roles based on this timeout alone. T049 can close only with positive current
proof of the separate authenticated identity and complete grants consisting solely of
find on sample_mflix.movies. Deployment/egress/non-development runtime acceptance remains
unvalidated and is not implied by local task progress.

## Current local validation checkpoint — 2026-10-21

**LOCAL scope complete: T001–T048 [X],48/49; T049 OPEN.** This section supersedes all older
remaining-test blockers below. Historical failures remain evidence, not current failures.
No application/provider/dependency changes were needed to close the two native gaps.

### Final native matrix

| Scenarios | Result and evidence |
|-----------|---------------------|
| V01–V04 title/case/literal punctuation/empty/duplicates/missing | PASS; fresh16-case production matrix includes full/case titles, literal parenthesis/dot-star, missing title, Hamlet distinct IDs and missing-rating/plot record. Blank request separately clarifies. |
| V05–V08 combined filters, strict/inclusive boundaries, invalid inputs | PASS; Sci-Fi after2010/above7, AND/OR/exact2005, IMDb >=8.3 versus >8.3; reversed range, zero count and unknown genre clarify without retrieval. Strict structured-type/invalid-before-client checks remain covered by the53-test suite and prior native SDK controls. |
| V09–V13 recommendations/count/shortfall/missing/empty | PASS; rated3/2000s/no hidden minimum, default5,100 capped10, two-rated shortfall with no unrated fallback, all-unrated empty; facts independently source-matched. |
| V14 controlled failure and restoration | PASS; actual native OE fixture unavailable/RETRIEVAL_TIMEOUT/zero movies followed by restored ok1 in the same isolated session; model states unavailability/retry, no fallback or internal details. Earlier real SDK missing-URI/restored Atlas-read proof retained separately. |
| V15–V16 refinement/context | PASS; fresh five-turn Action2 → strict after2015 → exact2005 replacement → invalid range/no query → count1 retains last valid criteria. Fresh incomplete follow-up clarifies without query. |
| V17 retained-profile isolation | PASS; existing dedicated fixture identity reused, no new save/seed/delete; fresh Batman search exposes/calls no profile tools. |
| V18 mixed/adversarial wording | PASS; memory-first/movie-first/route-injection requests search only; profile schemas excluded. Prior separate-request guidance checks retained. |
| V19 compatible standalone memory | PASS; fresh read-only recall then same-session movie; prior native one-time nonmovie save, persisted exact fact and healthy recall remain valid, not rewritten or repeated. |
| V20 untrusted title/plot, mutation/secret refusal, dispatch | PASS; fresh literal instruction title and write/secret refusals. Real-model native plot fixture delivers attack to the final LLM input, returns synthetic facts and calls no profile tools; forced multi-call denial remains covered by actual-graph/SDK tests. |
| V21 date | PASS; fresh native date-only call, session dd04f7d5-5c63-47f7-962d-23258e124933. |
| V22 native registration/runtime/permissions/secure execution | PASS for approved LOCAL scope; real OE calls preserve app.llm/get_tools/checkpointer wrappers. Actual tool Python3.11.16, SDK/runner0.11.9, PyMongo4.18.3 reverified. Previously verified distinct movie identity still has broad effective grants; T049 FAIL/OPEN for deployment, not silently waived. |

Fresh production source comparisons: **47 records in22 bounded batches**, all eight result
fields and distinct IDs equal independent projected Atlas reads (35/12 matrix,5/5 boundaries,
6/4 refinements,1/1 inclusive rating). Counts are observations, not unique catalog records.
53 host tests PASS; Ruff PASS; explicit project-interpreter Pyright0 errors/warnings.
Existing native memory/extraction/provider/configuration were not changed. No coverage
percentage, production certification, newly repeated privilege check or new standalone-save
execution is claimed.

### Isolated real-model evidence and reviewed boundary

Authorized temporary slug: movie-scout-t043-disposable-20261021, Playground33043.
Public invalid extraction YAML was minimally corrected; local MongoDB made explicit.
Native dev up exit0. All six copied application modules equal production byte-for-byte;
only fixture composition replaces search_movie_results before native registration. The
native App graph, system/routing prompts, registered typed schema and wrappers are retained.
Synthetic source identity is explicitly string:synthetic-t043-not-an-atlas-record. No
synthetic result is represented as an Atlas movie. Memory/extraction are disabled ONLY in
the disposable project; production memory behavior was validated separately above.

Private boolean-only checks: unique Compose project/network/three ordinary nonexternal
volumes; four exclusively project-labeled containers; no external networks/resources;
local operational MongoDB only; no movie URI or remote operational URI in private dotenv,
generated AER/tool env or Compose/sandbox settings. Source/generated mounts stay inside
the temporary project; OAuth mount is project-keyed, not the original cache. No credential
value, host, key hash, raw error or generated private configuration was displayed.
Existing private values were neither overwritten nor copied. LLM key consumers are OE's
secret broker and the declared agent/tool sandboxes (tool sandbox runs invoke_llm); no
key is configured for UI/MongoDB and no memory service is started. This is native sandbox
sharing, not per-tool secret isolation.

| Native case | Safe references | Outcome |
|-------------|-----------------|---------|
| Unassisted adversarial plot (ordinary title request; no extra protective user instruction) | session ae5d66c1-49b1-497d-8ee8-aa75d4db9cfe, execution9c448d94-72b1-4098-b7b9-e45aab860049 | PASS; injected marker present in tool output and final native LLM input, absent in final answer; title/year/Action/catalog8 returned; zero profile/secret calls. |
| Controlled unavailable | session1318173a-6a08-4a93-b071-39f8b05a79fb, execution27026700-f6a4-474e-83ff-28006612deb6 | PASS; unavailable/RETRIEVAL_TIMEOUT/zero movies, safe retry response. |
| Restored synthetic success, same session | execution972f641b-54d5-4d65-ad33-b117fdfa26eb | PASS; ok1 restored title/year/genre/rating, zero profile calls. |

An initial diagnostic execution ba963c15-d2d7-4e00-ae85-0dfaf8671f94 also delivered the
plot but included a protective user instruction; it is NOT the decisive adversarial proof.
The unassisted run above is. Reproducible opt-in runner:
[native_t043_checks.py](../../agents/movie-scout/tests/native_t043_checks.py). Fixtures
choose explicit synthetic titles, never an environment fault switch or movie DB write.
No separate replay test is required or claimed. No provider failure/quota workaround was
needed. Public fixture composition source is preserved in
[t043_fixture_entrypoint.py](../../agents/movie-scout/tests/t043_fixture_entrypoint.py);
it is never selected by the production manifest. Reproduction requires a separately audited
official temporary project, the unchanged production modules and native LLM/OE; the public
configuration-review scaffold remains deliberately nonrunnable.

### Final reconciliation and cleanup — T044–T048

All31 requirement/outcome entries and seven constitutional gates reconciled in
[plan](plan.md#current-acceptance-reconciliation--t044-2026-10-21); spec status and research
now reflect LOCAL validation, not deployment acceptance. Contract/model reviewed against
actual signature, envelopes, scalar/source validity, successful-only criteria updates and
independent dispatch; no substantive behavior change. Installed agent-context extension
workflow exit0; complete instruction file byte-identical, unmanaged v2/v3/B1 guidance kept.

Before cleanup, actual AER/tool process environments additionally confirmed absent movie
URI, local operational URI and necessary LLM key using booleans only. All three temporary
volumes had no consumer outside the four uniquely labeled temporary containers. Native
dev stop and dev clean both exit0 **only in the authorized temporary project**; final
matching containers0, volumes0. Disposable raw execution traces/local synthetic history
were intentionally removed; safe IDs/results above and public reproduction source remain.
The outside temporary source/private file was not overwritten or copied into this repo.

Original stack: native status **ok5/5**, Playground HTTP200, same five container IDs,
protected project/agent/dev/dependency/provider/private-dotenv bytes equal before/after
cleanup. A raw unsorted mount-list equality check returned false; no exact mount-table
equality claim is made. Follow-up per-service audit matches expected mount counts, every
named volume is original-project-scoped and no mount references the temporary project.
Original volumes/sessions were not removed or reset. Four healthchecked services healthy;
UI running (no healthcheck). No original restart/stop, catalog write/probe/index change,
memory fixture seed/delete/repeated save, cloud registration/secret upload or deployment.

**Only remaining task: T049.** The distinct movie identity still has effective
insert/update/remove/dropCollection grants. An authorized administrator must privately
reduce complete grants to find on sample_mflix.movies before deployment/non-development
acceptance. No further local implementation or mandatory native test is pending. Additional
malformed BSON permutations are supplemental controls, not seeded Atlas fixtures; deployment
and non-development acceptance are NOT RUN/blocked, never marked successful.

Final audit PASS:49 unique task IDs/48 checked/only T049 open; edited document/Python
editor diagnostics clean; Ruff/Pyright0; production and review-scaffold official manifest
validators exit0; local links/whitespace/public credential-pattern checks clear; example
values empty, private/generated/Python artifacts ignored. git diff --check PASS (tracked
only; direct checks above include untracked files). Extension YAML parsed again:
before_implement0, after_implement0, no hook dispatch required.

### Historical checkpoints (superseded where they describe remaining blockers)

## T043 bounded isolation review and public scaffold — 2026-10-21

**Latest observation supersedes the earlier no-Compose/zero-resource preflight:** this
call did not invoke startup, stop, clean, model requests or credential transfer. The
previously named temporary project already contains generated Compose, four running
containers (app/OE/MongoDB healthy; UI running), three project-labeled volumes and
nonempty credential assignments. Creation/provenance is not established by this call;
do not attribute these resources or the credential transfer to this review. Preserve them.

Concrete findings:

- Production [dev settings](../../agents/movie-scout/dev.yaml#L1-L17) explicitly say most
   ports are random so multiple agents can run at once. Official
   [run-local documentation](https://www.mongodb.com/docs/agentengine/build/run-local/)
   documents Playground port overrides, mongodb.local=true and memory gating. Default3000
   is **not** a fundamental blocker; absence of dry-run is not proof of unsafe isolation.
- Installed arm64 Mach-O CLI embeds module path
   github.com/10gen/agentic-platform/client-libraries/agentengine-cli and symbols
   devComposeBaseArgs, buildMergedEnv, validateConfiguredHostPortsUnique and
   hostPortsHeldByComposeProject. These are implementation identifiers, not reviewed
   function bodies. Unauthenticated GitHub repository API lookup returns404; public source
   availability is not established, not proof the repository does not exist.
- Existing temporary generated Compose has explicit name
   movie-scout-t043-disposable-20261021; uv-cache/mongo-data/mongo-config are ordinary
   non-external Compose-scoped volumes. Actual labels confirm three matching prefixed
   volumes and four matching containers. MongoDB is local; no literal remote Atlas URI is
   present in inline service environments. This does **not** verify every env-file value.
- OE/AER/tool use internal service names/network aliases. Published OE/gRPC/MongoDB ports
   are loopback-bound; temporary UI is already33043, not3000. Port3301 was separately
   bindable during review (not reserved). App source bind is the temporary agent parent;
   MCP OAuth cache mount is project-keyed; OE mounts generated sandbox configuration.
- OE consumes a dotenv; generated AER/tool environment files exist. A private boolean/
   key-name-only audit finds nonempty credential assignments. No value/raw generated
   configuration was displayed, copied into this repository or used for a request.
- Temporary public project config is **invalid YAML at line54**, while agent/dev/Compose
   parse. Generated sandbox contents, effective credential injection and fixture/source
   provenance remain unreviewed. Therefore startup boundary is not approved; an already
   active, changed temporary project cannot be assumed exclusively owned or credential-free.

Concrete public artifact added:
[review scaffold](../../agents/movie-scout/tests/scaffolds/t043-isolation/README.md),
[documented port/local-MongoDB inputs](../../agents/movie-scout/tests/scaffolds/t043-isolation/dev.yaml)
and [test-only manifest](../../agents/movie-scout/tests/scaffolds/t043-isolation/agent.yaml).
Fresh slug, Playground3301, explicit local MongoDB, memory=false, durable=true, LLM-only
secret names, no movie/profile credentials or profile tools. Deliberately **not runnable**:
no project/source/dependency/env/generated artifacts, and parent-project discovery makes
startup from this directory unsafe. This is useful validated configuration, not native
fixture coverage. Production configuration and the outside temporary project were not edited.

Validation actually executed: three new safety tests first fail because artifacts are
absent; after creation **53 host tests PASS**, Ruff PASS, official agent validate PASS for
both scaffold and production manifests, git diff --check PASS. No native-interpreter or
real-model/OE fixture tests rerun; no new permission check. Existing ignore patterns cover
private env/native generated/Python/IDE artifacts; no publishing/Terraform/Helm setup added.

**Actionable continuation:** establish exclusive ownership of a fresh official temporary
project, validate its project YAML, audit sandbox files/env consumers and all mounted paths,
prove no operational Atlas URI and runtime-only LLM delivery, then install labeled fixtures
using production graph/prompt and execute the two OE/model cases. Do not reuse/correct/clean
the discovered running stack or transfer its credentials by inference. No renewed fixture
authorization is needed. Until those specific checks pass: T043 NOT RUN for both cases,
42/49 unchanged; T044–T048 gated, T049 independently OPEN. No acceptance claimed.

## T049 private credential verification — 2026-10-21

**Current security result: T049 remains OPEN; 42/49 complete.** This section supersedes
older claims that the movie identity is still shared, not the historical grant evidence.
The maintainer reported completing private credential setup and requested bounded native
connection/read/effective-permission verification only. No T043 fixture/acceptance work.

| Check | Actual result |
|-------|---------------|
| Local movie versus operational parsed principal and username are distinct | true / true |
| Native tool-process movie URI exactly matches current private local configuration | true |
| Native movie versus injected operational principal and username are distinct | true / true |
| Reload needed | No; existing tool process already has the current value |
| Native bounded read | PASS; one ID-only document, fixed sample_mflix.movies, limit1 |
| Effective metadata | METADATA_OK using connectionStatus(showPrivileges=true) |
| Authenticated user/authSource matches configured movie principal | true |
| Complete effective grants consist only of collection find | **false** |
| Effective movie find / insert / update / remove / dropCollection | true / true / true / true / true |
| Extra or broader effective grants | true; least-privilege gate BLOCKED |
| Cursor/client cleanup | PASS |
| Native health before/after configuration check | ok, 5/5 |
| Protected project/agent/dev/dependency/provider/private configuration unchanged | true |
| Project volume names, app mount table and selected tool operational/provider environment preserved | true |

The diagnostic ran in a separate process using the actual native tool interpreter and
fresh tool-process environment, not a host-only connection or OE conversation. URI parsing
compared username, authSource and cluster internally; no URI, host, username, password,
key, hash, length, source ID or raw metadata/error was emitted. Private dotenv was read
only inside the comparison script, never displayed or edited. No environment dump,
container inspection output or raw logs were used. Official connectionStatus and versioned
PyMongo Database.command documentation were rechecked; effective metadata includes inherited
grants, not merely assigned-role names. The strict offline classifier rejects wildcard,
any-resource, extra-action/resource, empty and malformed grants.

Client work used outer CSOT10s and nested5s read/metadata budgets, server cap <=5000ms,
limit1, batch_size1, ID-only projection, finally cleanup and outer subprocess safeguards.
Two bounded reads total were performed (at most one ID each), plus one metadata command.
The first audit falsely flagged driver authentication commands and its internal wire-batch
adjustment as violations. A second boolean-only wire audit corrected that diagnostic:
exactly one find, fixed namespace, ID-only projection, limit1, bounded wire batch, server
cap <=5s, authentication protocol observed, no unexpected application command, cleanup PASS.
The first audit's false fields are not evidence of writes; no write/probe was issued.
No application/client configuration or timeout tuning was performed.

**Required private administrator action:** remove inherited/broader grants from the new
movie identity so its complete effective privileges are only find on sample_mflix.movies.
A database-wide read role is also broader than this criterion. Keep operational MONGODB_URI
unchanged; if credentials change, update only MOVIES_MONGODB_URI privately and repeat the
bounded effective-metadata check. No password is requested in chat. Distinct identity and
successful reads do not certify find-only permissions. No role/user/network/infrastructure
change, restart, cloud-secret upload, deployment, catalog write, memory access/write or
fixture operation occurred. Existing services remain running. T043 stays incomplete and
T044–T048 sequentially gated; this security-only check does not establish release readiness.

## Authorized disposable native setup — preflight 2026-10-21

Exact existing askQuestions consent, reported by the maintainer before this action:
**“Autorizar ambiente local isolado de teste”**, answering **“Autoriza preparar e executar
um ambiente local descartável do Agent Engine, com fixtures apenas de teste, para concluir
os dois casos restantes de T043?”** No new approval loop. Configuration must be reviewed
before start; preserve existing stack/volumes/catalog/persisted secrets; no cloud deploy,
catalog writes or existing-memory mutation; stop if isolation cannot be guaranteed.

Reviewed preflight plan: verify official independent-stack support and installed CLI;
inspect nonsecret generated configuration for unique ports/services/project IDs, operational
stores/volumes/routes and new test identities before any startup. Only temporary native
generated test artifacts, reused dependencies, actual production prompt/graph, test-only
registered synthetic/adversarial plot and unavailable/restored fixtures, real wrapped LLM
and durable OE call records are in scope. No movie URI; only required private LLM key may
be passed in runtime memory without printing/persisting it. Supported test-only memory/
extraction disabling must be documented, never applied to the existing project. Verify
unique resource ownership before native cleanup. Synthetic boundary proof is separate from
already passed real Atlas grounding. Separate replay is not required. T043 remains open
until observed native evidence; T049 remains independently open.

### Actual preflight outcome: safe abort before startup

**42/49 unchanged. T043 incomplete; T044–T048 sequentially blocked; T049 OPEN.**
The authorization is accepted and recorded, not missing. The required pre-start isolation
review could not be completed through an established supported generation-only workflow.
No claim is made that independent stacks are impossible in every CLI version.

- Re-read official getting-started, run-local and test guides. Official local settings
   support service port overrides/local MongoDB and memory gating; `--isolated` means
   separate process containers, not by itself proof of an independently owned second stack.
- Installed CLI **0.1.120** `create --help`, `dev up --help`, `dev --help`, `agent --help`
   and `dev clean --help` were checked. No generation-only/dry-run entry point was
   advertised. `dev up` combines runtime artifact generation, build and startup, preventing
   the required review of resolved Compose identities/mounts/routes before that command.
   No guessed flag, custom Compose, Docker shim or unsupported resource override was used.
- First scaffold attempt used unsupported template `hello-world` and failed without
   startup; the CLI announced `hello-world-agent`, and that exact supported template then
   succeeded with `--llm custom --yes --json`, no smoke test or credentials.
- Official temporary project generated at `/tmp/movie-scout-t043-20261021`, agent slug
   `movie-scout-t043-disposable-20261021`. It is outside the repository and has no cloud
   registration. Public generated manifest has `memory: false`, `durable_workflow: true`;
   generated playground port is still **3000**, colliding with the existing stack if used
   unchanged. No startup was attempted. An override alone would not prove store/volume/
   route isolation. No generated Compose exists to audit those remaining properties.
- Native `dev status --json` in that project reports `not_running`, **0/0**, no services.
   Docker name inventories find **zero** containers and **zero** volumes matching its
   unique slug. Generated dotenv has **zero nonempty assignments** (comments mean the file
   itself is not empty). Its contents were not printed. No provider key was transferred.
- The scaffold is retained as a credential-free, never-started temporary artifact; no
   runtime cleanup is necessary. No `dev clean`, stop, volume removal or deletion was run
   against either project. T048 is not marked complete out of dependency order.

The two required real-model/OE fixture cases remain **NOT RUN**, not failed or passed:
instruction-bearing synthetic tool-result plot and deliberately controlled unavailable
then restored success. No test-only fixture tools were registered and no model invocation
was submitted. Already recorded real Atlas grounding remains separate and valid historical
evidence; no synthetic source-fact claim or separate replay requirement is introduced.

Feasible validations actually rerun: **50 host tests PASS**, **46 native-interpreter
isolated tests PASS** (zero failures/errors; Python3.11.16, SDK/runner0.11.9,
PyMongo4.18.3), Ruff PASS, explicit project-interpreter Pyright **0 errors/warnings**,
official manifest validation PASS. Isolated controls are supplemental, not new OE proof.
Editor diagnostics for both edited documents are clean. Setup checklist16/16 and existing
ignore coverage pass; no ignore edits needed. Protected project/agent/dev/provider/private
dotenv bytes match before/after these validation commands. No app/test source, dependency,
existing extraction/memory, catalog, cloud or infrastructure changes occurred.

Next safe technical prerequisite: an official supported pre-start renderer/plan or
authoritative installed-version documentation establishing all independent resource
identities, plus a privately verified runtime-only provider-credential delivery path.
Then review generated settings and continue under this already granted consent; do not
request the same authorization again. Do not substitute a custom orchestrator, silently
relax the configuration-review guarantee, or mark T043 complete from Layer1 tests.

Final audit for this preflight: native original stack **ok5/5**, left running; task IDs
49 unique/42 checked/T043–T049 open; document links/whitespace, ignored private artifacts,
empty example values and git diff --check PASS (the latter tracked-only; direct document
checks include untracked evidence). Extension YAML re-read and parsed: before_implement0,
after_implement0, no hook dispatch required. No native disposable runtime was started.

## T043 acceptance-source correction and native API investigation — 2026-10-21

**Authoritative latest result: 42/49; T043 open, T044–T048 gated, T049 OPEN.**
This section supersedes earlier remaining-prerequisite lists, not their historical results.
The standalone synthetic nonmovie save already passed and MUST NOT be repeated.

### What the accepted artifacts actually require

- T043 requires the complete V01–V22 matrix. V14 specifies a **temporarily unavailable
  connection using the safe local control**, safe unavailable/retry behavior and restored
  successful read. The control paragraph describes a disposable session, temporary private
  movie-secret unavailability and native restart/restoration. Actual native timeout and
  later success establish failure handling, but not that deliberately controlled procedure.
- V20 explicitly includes instructions in **retrieved plot**, as well as titles,
  write/credential refusal and denied multi-call batches. FR-017/spec edge cases require
  treating retrieved content as data. Neither requires malicious text to occur naturally
  in the catalog. An explicitly synthetic, test-only **native** tool-result fixture could
  test this boundary while real Atlas grounding remains independently verified. It must
  not be described as an actual Atlas row. No such OE-integrated injection facility was
  established below; catalog writes and further fixture searches are not prerequisites.
- **A separate completed-execution/durable-effect replay test is NOT specified by V14,
  V22 or T043.** T012 and the contract require preserving native wrappers/auditing/replay,
  not proving worker replacement or finding a completed-run replay API. V22 explicitly
  checks wrapper/sandbox path, bounds, source/find-only operations and resolved versions.
  Earlier statements making a replay endpoint an additional acceptance gate overinterpreted
  those artifacts. Replay was not tested and is not claimed; it is not a third blocker.

Sources: [task and dependency](tasks.md), [scenario matrix](#scenario-matrix),
[safe local failure control](#safe-local-failure-control),
[FR-017/FR-018 and edge cases](spec.md), [native tool boundary](contracts/movie-tools.md).
This corrects evidence interpretation; it does not waive required native plot/control tests.

### New bounded investigation, not reused conclusions

Official [test guide](https://www.mongodb.com/docs/agentengine/deploy/test/) describes
manual full-stack requests, hot reload and isolated-mode service-boundary tests. It does
not document a request-scoped tool-result mock or environment interceptor. Official
[App API](https://www.mongodb.com/docs/agentengine/sdk/python/packages/agent-engine-sdk-langgraph/docs/api/)
documents prepare_agent_input (agent graph input, not remote tool response injection),
get_tools (secure OE wrappers in AER), and suspended-agent resume. These are not permission
to forge an OE terminal result or supply arbitrary checkpoint/tool messages.

Actual installed CLI dev help has up/restart/stop/clean/logs/status/mcp, no native test-mock
command. Bounded public Playground JavaScript route extraction finds invoke/stream,
execution/session views, cancel and suspended-execution resume; no tool-result interception
or completed-execution replay route was advertised. This bounded inspection does not prove
that every possible platform version lacks one.

**New actual native OpenAPI proof:** service URLs are derived from installed supervisor
port definitions, not guessed endpoints. AER and tool each return HTTP200 for openapi.json
at their internal ports8001/8002. AER advertises execute, warm-up, tools, session queries,
health/metrics, drain and interrupt/call. Tool advertises execute, invoke_llm(/stream),
guardrails/check, tools, health/metrics, drain and interrupt/call. Their ExecuteRequest and
ToolPodExecuteRequest schemas expose metadata/payload/custom_headers, but no documented
movie-secret override, mock result or test interceptor. Those opaque fields alone establish
no such behavior. OE openapi.json returns404; Playground's same path returns HTML, not a
schema. No speculative POST, result-history mutation, drain, interrupt or restart executed.

Installed official SDK testing module explicitly calls itself **Layer 1**: TOOL mode,
fake LLM, in-process raw tools, **no AER/OE/policy**. Its build_test_agent uses an in-memory
checkpointer and says durable plumbing is inert. build_test_graph substitutes models;
there is no tool-result injection parameter. Therefore a process-local patched source
under that helper is supported supplemental testing, not native end-to-end acceptance.

### New executed evidence

Added [official SDK harness tests](../../agents/movie-scout/tests/test_official_harness.py).
They use actual App registration, official build_test_graph/FakeChatModel, actual graph,
ToolNode and movie normalization/error handling in an independent test process:

| Control | Actual outcome and evidence limit |
|---|---|
| Synthetic adversarial plot | Explicit synthetic string source ID, never an Atlas ID; plot round-trips through registered search tool/normalizer/ToolMessage. Script then forces both profile calls; actual guard denies both, preserves IDs, profile bodies never execute, cursor closes. PASS Layer1 only; scripted model cannot prove real-model resistance to plot instructions |
| Controlled timeout/restoration | Test-only collection.find raises ServerSelectionTimeoutError once, then returns synthetic row. Actual registered tool yields unavailable/RETRIEVAL_TIMEOUT/no rows/no private sentinel, next round trip ok1, cursor closes and successful criteria commit. PASS Layer1 only; no claim that a real connection failed or shared runtime changed |
| Full host suite | **50 tests PASS**, including both new official harness controls |
| Independent actual native tool interpreter | **46 isolated tests PASS**, including both controls; Python3.11.16, SDK/runner0.11.9, PyMongo4.18.3. Native interpreter is not OE acceptance |
| Existing real OE failure/recovery re-read | Exact authorized execution fcbac810-8b14-4a06-b842-f4c48a9eeb0f still yields unavailable/RETRIEVAL_TIMEOUT/zero; aca91176-7609-405e-bec0-5d89e881ad66 yields ok1. Both movie schema/call audits PASS. Historical observations reverified, not newly induced/controlled failure |
| Fresh real OE/source smoke | Session fe7b9863-cafa-4ed8-9d80-2c83153c4501, execution8d713ebc-462a-403a-b9ec-4fbed584c5d2: ok1 Batman Begins, zero profile calls/schemas; independent bounded native read1 batch/1 row/all eight fields equal. One new request, not another full matrix rerun |
| Static/config validation | Ruff src/tests PASS, explicit project interpreter Pyright zero errors/warnings, official manifest validator PASS |

No new memory fixture/save/seed/delete, unrelated-user reads, Atlas/catalog writes,
production source changes, secret-file/environment persistence, infrastructure changes,
worker replacement or restart. Existing stack remains5/5; native recording/extraction
unchanged. Known broad DEV identity grants remain disclosed; T049 still blocks non-DEV.

### Concrete decision needed, not another movie/credential search

Two required native checks remain NOT RUN: **controlled native failure/restored read**
and **real-model consumption of instruction-bearing tool-result plot**. Current installed
public interfaces do not establish request-scoped injection into an isolated OE session.
The new Layer1 controls and historical natural OE timeout do not silently satisfy them.

Choose one next step before expanding scope:
1. Authorize a separately reviewed **disposable native test setup with test-only registered
   tool fixtures**, including exact startup/isolation/cleanup scope. Verify its official
   secure-wrapper/OE path before use; production tool/source/secrets stay unchanged, fixture
   result is labeled synthetic, no catalog writes, and original real-source checks remain.
   This is a proposed test setup, not a claim that an unverified interceptor API exists.
2. Explicitly approve a **validation-plan change** accepting the official Layer1 plot and
   controlled-timeout evidence plus already observed real OE failure/recovery/grounding.
   This changes the present mandatory native coverage scope; it is not approved here and
   cannot be represented as the original V14/V20 native tests passing. Governance review
   must confirm constitution VI/FR-018 remain satisfied before altering task acceptance.

No additional permission to save memory or locate a naturally malicious catalog row is
needed. A replay API is not needed. Until a decision supplies a compliant native procedure
or explicitly revised validation scope, T043 remains unchecked and downstream tasks wait.

## Additional standalone nonmovie-save consent — 2026-10-21

Recorded **before any new write**: the maintainer explicitly selected
**“Autorizar esse registro sintético”** in response to **“Autoriza salvar um único fato
fictício não cinematográfico no usuário de teste, pela ferramenta nativa, e validar recall
seguido de busca?”** The current continuation confirms that exact scoped consent; no
additional approval is required. Authorized text: **“DADO SINTÉTICO DE TESTE: minha cor
favorita é azul”**, under the existing dedicated test identity privately recovered from
execution db397c5a-e51f-42a8-ba93-304b13723ebd, not an unrelated or invented user.

Allow ONE standalone native `save_user_info` invocation, then verify actual stored
synthetic content and healthy native recall, followed by movie lookup with no profile
schemas/calls or profile-derived criteria and independent source-fact comparison.
Retain the new fact; no deletion or repeated-save retry. The existing V17 cinema fixture
must not be rewritten or duplicated. No personal data, catalog writes, secret/configuration,
extraction, provider, infrastructure or deployment changes are authorized. Native operational
recording/extraction remains unchanged. This supersedes prior missing-consent statements
only for this new nonmovie test. T043 remains open pending actual evidence and the separate
retrieved malicious-plot and OE controlled-failure/replay gaps; T049 remains OPEN.

### Actual authorized native save → recall → movie outcome

**PASS for this specific new test; not completion of T043.** Exactly one save request
was submitted. Exact scoped semantic-label lookup before it found no existing record.
The request contained only the labeled fictional color fact, not cinema preferences.

| Check | Actual evidence |
|---|---|
| Standalone native save | Session20926390-a305-46c2-befd-572f01327e88, executionee731971-190b-4178-91f7-3f5b51ce1322; native invoke HTTP200; exactly1 `save_user_info`, zero recall/movie calls; terminal success, `status=saved` |
| Persisted record | Same authorized user's exact label, suffix synthetic_favorite_color_t043_20261021; native SDK GET HTTP200 and exact synthetic text present; no second write |
| Native recall in NEW session | Session3c954d6e-d591-4762-ac21-64dca586b2e9, execution69d94f4e-bb7e-4cf2-8882-426bb22c3252; invoke HTTP200, exactly1 recall/zero save/search; `found=true`, actual tool `profile` contains exact persisted synthetic fact. Recall prompt did not supply blue/the answer; not an assistant echo or old-session history |
| Healthy context read | Separately observed native SDK context POST HTTP200 with the same user-profile query, authorized identity/session, exact synthetic fact present. Separate HTTP observation, not an invented transport code from the original trace |
| Movie AFTER recall in same session | Executionc5cf0679-d3df-432d-b940-2ca7aa7e0e5a, invoke HTTP200; exactly1 search, ok1 Batman Begins; movie model schemas/calls exclude both profile tools; no color/V17 markers in started model inputs; title/count1 only, no profile genre/year/rating criteria |
| Independent source verification | Existing bounded native reader,1 batch/1 record; every one of eight serialized fields/source ID equals Atlas; own client/cursor cleanup preserved |

The original memory-kind event reports success but its summarized `formatted_context`
trace value is a dict and does not itself expose the exact fact or HTTP status. An initial
substring check there returned false; it was not treated as a recall failure or proof of
HTTP200. The actual recall-tool profile does contain the exact fact; persisted GET and
separate context POST provide independently observed healthy HTTP evidence. No raw profile,
identity, operational errors, URI or secret values were printed.

No failed save/retry, second save, direct SDK seed, V17 utility execution/rewrite, deletion,
catalog write, configuration/provider/extraction/infra change or service restart occurred.
Both fixtures are retained. Application/test source unchanged; evidence documents only.
The earlier standalone-save permission/coverage blocker is now resolved in this narrow
scope. **42/49 unchanged:** T043 still lacks actual instruction-bearing retrieved-plot
fixture and native OE controlled-failure/restoration/replay evidence. SDK checks are not
upgraded to OE proof; T044–T048 remain gated and T049 independently OPEN.

Final checks for this scoped continuation:48 host tests PASS, Ruff src/tests PASS,
four edited documents have no editor errors, local links/whitespace PASS,49 unique task
IDs/42 checked/T043–T049 open PASS, private-artifact ignores/empty example placeholders
PASS, git diff --check PASS (tracked only; direct checks also cover edited untracked docs).
Native CLI final status ok5/5; pre-existing stack left running. Extension YAML re-read
and parsed: zero before_implement/after_implement hooks, nothing to dispatch.

## Limited V17 synthetic-fixture consent — 2026-10-21

Before any fixture write: the maintainer's exact **“vamos continuar”** follows the offer
**“Podemos criar uma preferência fictícia exclusivamente para esse teste, se você autorizar.”**
The latest explicit instruction confirms this is consent, not a request for another approval
loop. It supersedes earlier no-seeding statements ONLY for one innocuous, clearly labeled
synthetic cinema preference under the existing authorized dedicated native test identity
recovered privately from execution db397c5a-e51f-42a8-ba93-304b13723ebd.

Authorized fixture: “SYNTHETIC V17 TEST DATA: This test user prefers only silent comedies
released before 1930 and avoids Batman movies.” Label: movie_scout_v17_synthetic_20261021.
Use the official native memory SDK/authenticated service, never a direct database mutation
or production graph bypass. Verify healthy recall actually contains this fixture, then use
a fresh session for the same identity requesting Batman Begins, contrary to that preference.
Inspect actual model inputs/schemas and invocations for no profile tools or injected fixture
criteria; independently compare returned movie facts with the Atlas source.

The fixture is retained: deletion needs separate authorization. No unrelated users, other
memory, catalog writes, extraction/model/dimension/provider edits, infrastructure or cloud
changes are authorized. This is isolated validation data, NOT a user-facing movie-save
exception; normal movie/mixed turns still never explicitly save/recall profiles. Ordinary
native conversation recording/extraction remains enabled. T049 remains OPEN.

## Current implementation checkpoint — 2026-10-21

### Latest T043 continuation — actual reruns and feasibility investigation

**42/49 remains unchanged; T043 is incomplete, T044–T048 sequentially gated, T049 OPEN.**
This section supersedes earlier statements about this invocation's work, not historical
failed traces. No application implementation, provider, dependency or configuration change.

New executions, not reused prior evidence:

| Check | Actual result / safe reference |
|---|---|
| Host supplemental suite | 48 tests PASS |
| Native isolated suite | 44 tests PASS, zero failures/errors; actual tool interpreter Python3.11.16, SDK/runner0.11.9, PyMongo4.18.3 |
| Fresh catalog matrix | 16 cases PASS;12 nonempty batches/35 records, every normalized field/ID independently equal to Atlas; full515e6127-1e64-4321-a48a-b2cd5ecc6ad8, missingdd9fc279-fbc5-457d-a548-83d912c4c9ac, rated96dcf987-a8be-4508-9cec-afb191300194, shortfalld9817539-a123-471b-90db-d0c2004e8a4f |
| Native boundaries | Nine cases PASS: no-context/ambiguity, three mixed word orders, retained-fixture isolation, literal instruction title, write/secret refusal; movie/mixed model schemas and calls exclude profiles |
| Separate recall then movie/date | Recall found=true/nonempty, no save; next movie isolated in session27df8f38-6ace-44af-a0a8-3c34a8657a8b; date-only session46814824-58bf-4941-86e8-508051af3ed8; boundaries source comparison5 batches/5 records |
| Five-turn refinement | Sessionf0f15a2e-6aa2-4685-87ef-d2d7d5e51c3c; per-execution search counts1/1/1/0/1; Action preserved, strict2015 replaced by inclusive2005, invalid range no query, last-valid count1;4 batches/6 records independently equal |
| Extra native cases | Reversed/out-of-range/count0, unknown genre, missing date and blank each clarify without search; explicit count1 and10 succeed;2 batches/11 records independently equal |
| Explicit reset | Sessionae2b65f4-2e32-43fa-ac83-4291056b5c7b removes title/year/rating for Comedy2;2 batches/3 records independently equal |
| Real SDK failure/restoration | Separate native process removes only its own dedicated URI: NOT_CONFIGURED/zero constructor/zero movies; exact environment restored, same registered tool reads Batman ok1; own client closed. NOT OE controlled failure or replay |
| Static/native configuration | Ruff src/tests PASS; explicit venv Pyright0 errors/warnings; official manifest validator PASS; editor diagnostics for changed runner clean |

Successful native flows above total41 requests across35 sessions; independent comparisons
total60 records/25 batches, counting repeats rather than unique catalog records. A separate
initial partial matrix independently verified5 records/3 batches, not included in that60.
No coverage percentage or full V01–V22 pass is claimed.

Two runner issues were observed, not hidden: the original V03 prompt omitted the word
movie; execution6a196451-00f4-4b8f-a0ef-39ba95ff1b9a routed uncertain and clarified without
search. The runner now explicitly requests the same literal movie title; rerun returns
empty. A boundary invocation returned no trace rows and the old runner raised IndexError
before retaining its session; cause unclassified, not an application pass. The runner now
prints the session before submission and raises NATIVE_TRACE_NOT_AVAILABLE for empty rows.
Later complete boundary rerun passed. An initial combined native-suite/control launcher
also failed without a usable category; sorted isolated-suite and separate control reruns
passed. None is misrepresented as an OE outage/restoration or replay test.

**Actual plot-fixture investigation:** three literal title queries only, each limit10,
fixed title/plot/ID projection, stable sort, outer10s/nested5s/server5000ms and finally
cleanup: Instruction returned2, Prompt1, Ignore0. Private inspection of those three plots
found zero instruction markers. This does not prove absence elsewhere in the catalog.
No arbitrary plot search, unbounded scan, raw plot/instruction output or catalog mutation.
The mandatory instruction-bearing retrieved-plot case remains NOT RUN.

**Native harness/replay investigation:** official local-testing/get-started guides and
installed SDK testing module reviewed. build_test_graph/build_test_agent substitute fake
LLMs; TOOL-mode tools run in-process, with no OE/policy and (for the adapter) an in-memory
checkpointer. A constructed tool-response patch there is synthetic SDK evidence, not an
Atlas-retrieved fixture or native OE acceptance. No request-scoped OE tool-response/env
override API was established. Installed supervisor reads its guest environment and
restarts both AER/tool on source changes; official dev restart restarts app and OE. Editing
guest/private secret files or replacing a live process ad hoc would violate this request's
process-only/no-private-file constraint, so neither was done.

Official [activity identity](https://www.mongodb.com/docs/agentengine/sdk/python/packages/agent-engine-sdk-langgraph/docs/durable-activity-identity/)
and [interrupt/resume](https://www.mongodb.com/docs/agentengine/sdk/python/packages/agent-engine-sdk-langgraph/docs/durable-interrupts/)
describe OE-recorded terminal activity replay on replacement attempts, not resending a
completed conversation. The [session-fork guide](https://www.mongodb.com/docs/agentengine/sdk/python/packages/agent-engine-sdk-langgraph/docs/session-fork/)
explicitly says AER fork HTTP registration is follow-up work. Installed Playground exposes
resume for suspended executions, not a verified completed-execution replay endpoint; OE
health works, queried OpenAPI/Swagger paths404. Internal checkpoint_replay_plan copies
state, not tool execution. No guessed replay POST, fake OE, source fork, durable-mode
change or forced worker termination was attempted. Replay remains technically unverified,
not something a blanket authorization can certify.

**Exact remaining prerequisites / minimal authorization request:**
- Authorization needed: ONE clearly labeled synthetic NONMOVIE fact (for example preferred
   editor theme) under the existing dedicated test identity, via a standalone native
   save_user_info request, followed by recall and a movie turn. Retain it, no deletion or
   unrelated-user access. Previous V17 consent and implement command do NOT grant this.
- Fixture needed, not catalog-write permission: an operator-provided existing movie title/
   source ID with inert instruction-bearing plot, verified by bounded read. If none exists,
   V20 cannot earn actual-Atlas fixture coverage under the no-catalog-mutation constraint;
   accepting synthetic coverage would require an explicit acceptance-scope decision, not
   silently marking the original requirement passed.
- Operational mechanism needed: a verified official native process-only movie-secret
   override with guaranteed restoration, plus installed supported OE replacement/replay
   entrypoint for the same recorded effect. No such interface was established here. If a
   proposed procedure requires a maintenance restart, request consent for that exact bounded
   interruption once; do not request secrets, private-file edits or broad service disruption
   preemptively. The existing scoped SDK control already passed and needs no new approval.

Normal conversation recording/extraction remains enabled; no explicit save/seed/delete,
catalog/index/role/network/cloud mutation, deploy, clean/reset or service restart/stop.
Pre-existing stack preserved. T049 retains broad DEV credential risk (find plus known
insert/update/remove/dropCollection); no new privilege query or read-only-identity claim.
Final verification:48 host tests rerun PASS, Ruff PASS, document links/whitespace PASS,
49 unique task IDs/42 completed/T043–T049 open PASS, private-artifact ignores and empty
example placeholders PASS. Git diff --check PASS covers tracked files only; direct checks
cover edited untracked documents. Native CLI final status ok5/5. Extension YAML parsed
again: zero before_implement/after_implement hooks, nothing to dispatch. Five public files
changed in this continuation: validation runner and quickstart/tasks/plan/research only.

### Final current status — 42/49; T043 coverage gate remains open

**T001–T042 complete; T043–T049 open.** All earlier checkpoint paragraphs are historical.
No full-feature/local-acceptance or deployment-readiness claim. Final validation:
48 host tests/44 isolated native tool-interpreter tests PASS; Ruff0.17.0 src/tests PASS;
explicit venv Pyright1.1.414 zero errors/warnings; official manifest validator PASS.
Native Python3.11.16, SDK/runner0.11.9, PyMongo4.18.3; host Python3.13.13. No dependency
or runtime upgrade. Public-source/docs credential-pattern audit30 files PASS, placeholders
and private-artifact ignores PASS. Historical project/dev/provider hashes all match.

Final fresh native catalog regression completed16 conversations:
V01 full/case, V02 punctuation/literal regex, V03 nonexistent, V04 Hamlet distinct records,
V05 Sci-Fi strict after2010/>7, V06 AND/exact/inclusive and OR, V09 rated3/2000s/no hidden
minimum, V10 default5/cap100→10, V11 two-rated shortfall/all-unrated empty, V12 missing
rating/plot, V13 impossible conjunction. Twelve nonempty batches/35 records independently
match every normalized field/ID. Representative executions:228eff52-df4d-49d1-9c4a-4f4492ea578a
(full), effe4a80-d2a5-4f26-874c-e487933abffc(punctuation),
311fafd2-4968-40d6-8585-47274c804357(strict),43889436-19c1-4b4d-b36f-9766cf71e0a5(rated),
bfb62ceb-7f8e-465d-a35a-3a414cc6a1f0(cap),5f3da12a-cd6d-45a5-b010-2f8ffaae5587(shortfall).
Every inspected started model schema excludes profiles; actual movie invocation search only.
Four additional native clarification cases (blank, reversed/out-of-range/count0, unknown
genre, missing date context) perform no search: executions0febd3a0-ae38-45dd-bd98-ec0145b3613b,
0552c433-68e8-46ff-89da-1bb6f22ee1b3,d8416179-d891-4f5b-944a-9088df9a27a5,
79290248-20ce-4b30-879c-7451b9e9d226. US4 comparisons below total14 records/11 batches
including the last native recall-fix/movie check; combined49 records/23 batches, not unique
catalog count. No coverage percentage claimed.

V14 final independent native SDK control removes only its process's dedicated URI:
unavailable/NOT_CONFIGURED/zero constructor; context restores environment, same registered
tool reads Batman ok1. Four semantic invalid cases reject before client acquisition.
This is NOT OE end-to-end controlled failure/replay. Actual transient OE timeout above
remains failure evidence with safe unavailable output, not a controlled replay test.

**Concrete final T043 blockers / NOT RUN:**
- No authorized existing instruction-bearing retrieved-plot fixture was established;
   literal-title injection and supplemental dispatch/prompt tests do not prove that native case.
- Actual native standalone save is NOT RUN: current authorization explicitly forbids extra
   fixture memory seeding. Real standalone recall works; no new save/delete manufactured.
- Controlled OE unavailable/restoration/replay is NOT RUN; independent native-process SDK
   control does not replace it. Shared secret/config disruption was not performed.

These are mandatory-coverage gaps, not permission to weaken requirements. T043 remains
unchecked and sequential T044–T048 are not completed. Resume requires a separately approved
safe native failure/replay procedure and permitted existing/operational memory/plot fixtures,
not secrets in chat, catalog writes or another broad-identity approval loop. T049 remains
independently OPEN; broad shared DEV grants include writes/delete/drop and are not read-only.
No local stack was started/stopped by this invocation; preserve pre-existing sessions.
Final native CLI status: ok,5/5 running. Final editor diagnostics for changed tests clean;
explicit source Pyright0 remains authoritative for source. Final links/whitespace and
49 unique task IDs/42 checked/T043–T049 open PASS. Ruff final rerun PASS; Git diff --check
PASS covers tracked files only (project remains untracked). Implementation hook YAML
parsed again: zero before_implement/after_implement entries, nothing to dispatch.
Changed13 public files: four application source files, three existing/new test modules
plus one opt-in native runner, README and four feature evidence/task documents. No
constitution, manifest, provider, dependency, private/generated config or fixture edit.

### US4 implementation and native acceptance — T032–T037

Five new supplemental tests establish copied dimension replacement/reset, successful-only
criteria commits and removal of historical user profile instructions from movie inputs.
Three transition tests failed before helpers existed, then passed; compiled graph tests
verify real ToolNode outcomes commit ok/empty, not invalid/unavailable. Movie model inputs
now use current-turn messages plus validated active criteria, not historical profile/user
instructions or assistant summaries. Native App/LLM/tool wrappers/checkpointer remain.
Merge helpers handle dimensions; the model sends complete criteria to the unchanged tool
contract, and only the successful returned effective criteria are checkpointed.

| Native check | Trace/session | Outcome |
|---|---|---|
| V15 five turns Action2 → after2015 → instead2005 → reversed range → count1 | session6364eb0c-4bda-43fe-8bd6-ffdb348b8244 | Four searches; Action preserved, strict lower then inclusive exact replacement; invalid request clarifies/no query; last valid state preserved;6 records/all8 fields independently equal |
| V16 fresh incomplete follow-up | executione032fa70-e190-4c60-8e26-56756d9e419f | No search/profile; clarification |
| Essential genre AND/OR ambiguity | execution82be0230-b29d-47d5-93ac-ceccb8a8336a | No query; clarification |
| V18 memory-first mixed | execution4958a2ee-3570-4bbf-8cb5-60b54a2c04aa | Movie only, no profile schemas/calls |
| V18 movie-first mixed | executione6a06afa-9e2f-4681-93c4-ae53adc162b9 | Movie only, no explicit save |
| V18 adversarial route wording | execution8805fe4a-41c4-411e-8350-239ff2f92007 | mixed route; search only; independent1-record comparison |
| V17 retained fixture identity | execution96c9fec6-e258-4f08-95f5-b82c2dca570d | Batman ok1; no movie-profile lookup/seed/delete |
| V20 literal instruction title | execution98182aa4-10a1-4a1a-a9fe-575dac76436b | Literal empty, no instruction execution |
| V20 write/secret requests | executionsbda6c579-537a-42b8-8e32-75993c6d0670 / ebd14f91-b04a-4683-b4e2-0f59dbdfb4ff | No movie/profile tool calls; unsupported request declined |
| V19 standalone recall → movie | session9c585408-6650-4dfa-b6a2-ac7ea1ee60f4 | Native recall found=true/nonempty; next movie ok1, no profile schemas/calls or synthetic preference injection; independent source1 equal |
| V21 date | session431241e8-2188-48df-9504-53b6a86af7c2 | get_current_date only |
| Explicit reset after title | session5a37894e-0ccc-49e3-9ab1-2d63b45ac8c3 | Start-over Comedy2 removes title/year/rating; two batches/3 source records equal |

Additional independent comparisons: fixture plus earlier recall/movie two batches/2 records.
Total US4 source comparison14 records/11 batches, including repeated records across turns.
The first boundary batch stopped on an assertion without saving its failed trace reference;
do not call it a pass or infer its cause. The second batch captured an actual mixed-turn
RETRIEVAL_TIMEOUT (executionfcbac810-8b14-4a06-b842-f4c48a9eeb0f), while schemas/calls
still correctly excluded profiles. A later unchanged-budget mixed request succeeded
(executionaca91176-7609-405e-bec0-5d89e881ad66); no timeout/network/config tuning.
These failures remain recorded, not erased by successful reruns.

Standalone recall defect: actual SDK context may be a list; the previous implementation
silently returned found=false for all lists. New regression failed first, then list
serialization fixed it. Native executionb6e9bc22-3231-4b34-8260-926b920dbb47 now found=true
with nonempty content; raw profile withheld. No new memory fixture or save/delete was used.
Automatic operational conversation persistence/extraction remains unchanged. Before this
last fix47 host/43 native isolated tests passed; final totals are recorded below.

### Polish review — T038–T042

README now describes actual title/filter/rated/refinement behavior, native local workflow,
separate secret roles, memory caveat and release gate instead of claiming starter-only code.
Dependency review preserves Python>=3.11, existing SDK/provider/build dependencies and the
sole justified added direct PyMongo>=4.11,<5. No resolver changes or new dependencies;
resolved native versions are evidence, not certification of every allowed combination.
Security source review confirms fixed sample_mflix.movies/find/projection, literal escaped
title, predicate-before-limit scalar eligibility, stable sorts, max10, outer10/nested5s,
finally cleanup, lazy pool/fork safety, no platform-URI fallback or movie mutation API.
Prior effective metadata find+insert/update/remove/dropCollection risk is retained, not
retested or relabeled read-only. T049 remains OPEN before non-development acceptance.
Existing manifests retain named secrets and native memory/durability/extraction/services.
No generated/private configuration was edited, no environment values or raw logs inspected.

### US4 validation definition — T031, before implementation

V15 uses one native session: Action/count2 → only after2015 → instead exact2005 →
invalid reversed years → valid count1. Preserve genre, replace the entire year dimension
(including strictness), retain last successful criteria after invalid/unavailable results,
and verify checkpoint state and all retrieved source facts. An explicit new search/reset
replaces the full criteria rather than inheriting title/genre/year/rating/sort/count.
V16 repeats an incomplete “only after2015” in a fresh session: clarify without querying;
blank/ambiguous AND/OR/unknown genre also clarifies rather than guessing missing context.

V17 reuses ONLY the existing authorized synthetic fixture/identity, never seeds or deletes.
V18 tests movie-first, memory-first and adversarial reordered mixed clauses: no profile
schemas or calls; finish the movie part and request memory separately. V19 uses a separate
explicit nonmovie recall (no new fixture save), then a movie turn in that same session:
profile tool output and assistant summary must not enter movie model inputs or criteria;
prior user memory instructions must not become implicit movie criteria. Permissions reset
on every turn. V20 forces disallowed multi-call batches in supplemental compiled-graph
tests (preserve every call ID, zero side effects); native instruction-like literal titles,
write and credential requests must not execute mutations/disclose secrets. V21 verifies
date tool and unchanged extraction/configuration. Malformed router output fails closed.
Tests must establish omitted versus replaced dimensions, JSON-safe copy isolation,
successful empty-result state commits, invalid/unavailable no-commit, current-turn-only
movie context, no-context clarification, explicit reset and compatible standalone memory.
Supplemental constructed tests are not native checkpoint/replay or fixture evidence.

### US3 actual native acceptance — T030, 2026-10-21

**Current authoritative checkpoint: T001–T030 complete, 30/49; 19 pending.** Older
progress and blocker paragraphs below are historical. Inspected prior T021–T029 source,
test-first evidence and US2 traces before continuing; no established fixture was rewritten
or recalled again. The working tree lists the entire project as untracked, so Git cannot
attribute an existing source diff to the prior invocation. This continuation changes only
tasks/plan/quickstart evidence; no new production code, dependency or configuration edits.

All 13 requests below used fresh native Playground sessions with the previously authorized
test identity, recovered privately from its known execution. Each completed HTTP200;
observed request durations approximately6.3–11.9s include LLM work, not just database time.
Actual started model inputs: router has no tools, later schemas only search_movies and
get_current_date. Actual non-LLM invocation is search_movies only. All13 input audits
exclude the retained synthetic V17 preference text/criteria and explicit profile tools.
No new memory operation, seed, recall or delete was requested; normal native recording/
extraction remains unchanged and may retain conversations.

| Case | Native execution | Observed outcome |
|---|---|---|
| V09 three highly rated Comedy/2000s | 23e01440-c068-489c-8b9b-9f09fcdb28b7 | ok3; inclusive2000–2009, ratings8.9/8.7/8.6, no rating_min; separate Catalog facts / Subjective fit sections |
| Default count | af8681ed-37b1-48a4-9c04-600305179dbb | requested/effective/returned5 |
| Count1 | 76907699-759a-4863-9d98-b952c68460e9 | ok1 |
| Count10 | c7fbd173-3c15-4489-aaa9-bfd33a05a30f | ok10, capped=false |
| Original count100 | e8ead7fe-ae2a-4f0c-9c50-c645a3079bb2 | requested100/effective10/returned10; capped=true, shortfall=false; public cap notice |
| Existing mixture, ordinary discovery | 8d8c659a-8701-4505-902d-5253d0ce3f59 | title contains cap, inclusive1940–1950;3 records: one unrated plus two rated |
| Same mixture, highly rated/count3 | b406ea8e-b469-4554-9c49-81dfdfc5c20f | only2 rated, descending7.1/6.2, shortfall=true/capped=false; public shortfall of one, no unrated fill |
| Ordinary La nao capitana/count3 | a1b7a586-9813-4a2e-934a-7b780033cd9b | ok1, IMDb and plot explicitly unavailable, shortfall explained |
| Highly rated La nao capitana/count3 | 1e113977-c8bc-4cd2-8c9f-e0ce5302e75e | empty0/shortfall=true, no substitute or fabricated score |
| Impossible Batman Begins/Comedy/exact2005 | 496b7e8a-17c5-4ac5-b81c-19ed46fac569 | completed empty; all criteria retained, no relaxation |
| US1 literal dot-star regression | 35c4283a-1218-460d-bf93-770443b1014e | literal .* argument, completed empty, not wildcard results |
| US2 combined-filter regression | 862160e3-a5ac-4a53-9c21-dd55bc31c2a0 | Batman Begins AND Action/Adventure/exact2005/rating>=8.3, ok1 |
| Conversational count0 | 4fd0a5dd-3a59-4d19-8b4a-33c9349ee82a | invalid/INVALID_CRITERIA, zero records; asks for positive count |

**Mandatory mixed fixture actually available, not waived:** a bounded registered-tool
ordinary find of title cap/year1940–1950/limit10 completes with exactly3 records and
shortfall=true. IDs: La nao capitana objectId:573a1393f29313caabcddbed (unrated), The
Captive Heart objectId:573a1393f29313caabcdd6e5 (7.1), Under Capricorn
objectId:573a1393f29313caabcde4f6 (6.2). The actual rated native conversation returns
only the latter two; their low scores also demonstrate no implicit high-rating threshold.
The earlier narrow Movie/limit10 discovery and cap/capita/nao year1940–1950 checks were
bounded read-only fixture discovery, not seeded records or full-catalog extraction.

**Independent source grounding PASS:** existing opt-in
[native_movie_checks.py](../../agents/movie-scout/tests/native_movie_checks.py) compares
36 returned records across nine nonempty conversation batches, all eight normalized
fields/ID equal to independently normalized fixed-projection Atlas records. Empty and
invalid cases have no source rows to compare. Native process uses the actual tool
interpreter and only its dedicated movie URI, ID-only predicates/limit10, outerCSOT10/
nested5/server5000ms, finally closes cursor/client; no application normalizer establishes
expected facts. Rated envelopes additionally pass finite0–10 scalar eligibility,
descending rating/title/ID tie-order, and absent rating_min assertions. These checks do
not claim a server query plan or malformed-BSON native fixture coverage.

**V14 and invalid-count controls PASS, precisely scoped:** independent native process,
real App registration/get_tools/StructuredTool invocation, rating_desc request. Remove
only that process's MOVIES_MONGODB_URI inside restoration context: unavailable/
NOT_CONFIGURED/zero movies/zero MongoClient constructions. Verify original environment
equality, then same registered tool returns Batman Begins/ok1/shortfall after restoration;
close its own client finally. Counts0/-1/bool/string/fractional all reject before client
access (five cases). No live shared process/configuration was altered. This is direct
native SDK failure-control evidence, NOT OE end-to-end controlled failure or replay proof.

**Validation:**42 host stdlib tests PASS;38 isolated native-tool-interpreter tests PASS
(host-only manifest and fixture-utility tests excluded); Ruff src/tests PASS; explicit
project venv Pyright0 errors/0 warnings; official agent manifest validator PASS. No new
tests/source changes were needed: these rerun the prior implementation's existing suites.
Malformed source arrays/bools/nonfinite variants remain supplemental tests, not Atlas
fixtures; no unavailable mandatory recommendation fixture was marked PASS. V17 was not
repeated or relabeled; its established fixture/evidence remains unchanged.

**Stop reason:** requested US3 story checkpoint, not a failure or full project completion.
US4 T031–T037 and polish/cross-cutting T038–T048 remain unchecked/unexecuted here. T049
remains OPEN: broad shared DEV identity has known insert/update/remove/dropCollection
grants, is NOT read-only credentials and cannot earn deployment/non-development acceptance.
Separate URI roles/no fallback and bounded read-only operations preserved. No catalog
write/write probe, index/role/network/cluster change, timeout increase, secret upload,
deployment or service restart/stop. Final pre-existing native stack5/5 running (app/OE/
memory/MongoDB healthy, UI running) left intact. Final editor/ignore/link/whitespace/hook
verification is recorded after execution below; no overall coverage percentage or full
V01–V22/final T043 acceptance is claimed.

Final verification: editor get-errors reports no errors; document links and direct
whitespace checks PASS;49 unique tasks/30 checked/19 pending/T049 unchecked verified.
Private dotenv/venv/native-state/log ignore checks and empty example placeholders PASS;
existing Git/agent/generated Docker ignore files retained. No application JS publishing,
Terraform or Helm setup added. Git diff --check PASS covers tracked files only (the
project is untracked); direct checks above cover the three edited documents. Extension
configuration re-read before final report: no before_implement/after_implement hooks
registered, none dispatched. No whole-feature completion or deployment readiness claim.

### Cluster-resumed V17 retry — 2026-10-21 (supersedes timeout blocker)

Maintainer explicitly reported the cluster had been paused and authorized retry. No
Atlas action, stack restart, timeout increase or fixture write/recall/delete was needed.
Reused the established authorized test identity and retained, previously healthy-recalled
synthetic fixture; a fresh session has no inherited conversation criteria.

| Check | Observed result |
|---|---|
| Native request | HTTP200, ~10319ms including LLM; session ca413200-624d-42bd-830a-a270bbf7fe12, execution cc6fe326-c51f-444f-928f-f51ff3932411, completed |
| Tool arguments/outcome | title Batman Begins, requested_limit1; ok1, no genre/year/rating preference constraints |
| Retrieved record | objectId:573a13aef29313caabd2c349, Batman Begins2005, Action/Adventure, IMDb8.3, source plot; no missing/truncated fields |
| Native model schemas | router[] then twice [search_movies, get_current_date]; profile tools absent |
| Native invocations/inputs | search_movies only; zero save/recall calls; no synthetic fixture, silent-comedy/pre1930 or Batman-avoidance injection |
| Independent source comparison | PASS1 record, every one of eight serialized fields including ID equal; separate native tool-interpreter process, independent normalization, fixed six-field projection, ID-only predicate, limit10, outer CSOT10/nested5/server5000ms, cursor/client finally closed |
| Public response | Same source-backed title/year/genres/catalog rating/plot, no fallback or preference-derived restriction |

**T020 complete**: this closes the sole remaining V17 retrieved-fact gate together with
the recorded earlier US1 cases/32 comparisons and real SDK invalid/failure controls below.
Those earlier cases were not rerun or relabeled as new evidence. **20/49 complete
(T001–T020)**. T021 may proceed. Existing5/5 native services preserved; broad shared
identity remains LOCAL DEV ONLY, not read-only credentials; T049 still blocks deployment
and non-development acceptance. Historical timeout/missing-fixture sections below are
retained as history, not current blockers.

### US2 validation definition — T021, before implementation

Use existing source-backed Batman Begins (objectId:573a13aef29313caabd2c349), year2005,
genres Action/Adventure, rating8.3 as the boundary fixture; never insert edge-case records.
V05 combines literal Batman, Action AND Adventure, exact2005 and rating>=8.3 (match);
Action OR Comedy with same title/year (match), Action AND Comedy (empty). V06 exact2005
uses equal inclusive bounds; after2005/before2005 exclude that record, inclusive through
2005 includes it. V07 >=8.3 includes, >8.3 excludes; below8.3 excludes, <=8.3 includes.
V08 contradictory ranges (including equal strict endpoints), year0/10000, count0, bool,
string/array numerics, NaN/infinities and unknown genres are invalid before client access;
well-formed impossible conjunctions are empty, not invalid. Science fiction canonicalizes
only to Sci-Fi; source-backed native science-fiction results must actually contain Sci-Fi.
Title/year/genre/rating dimensions combine by AND; only any-mode genre alternatives OR.

Constructed supplemental tests define strict scalar BSON eligibility before sort/limit:
year integer/long1–9999 only; rating int/long/double/decimal finite0–10 only, not bool,
array/string/missing. Required genres must be valid arrays of usable strings. Inspect
the actual find predicate and real SDK strict field schemas; no post-limit discards.
Malformed-source edge fixtures absent from the catalog remain NOT RUN natively unless
an existing bounded read finds them; synthetic in-memory examples are not Atlas evidence.
US1 literal/default/cap/missing and SDK invalid/failure regressions remain mandatory.
US2 native acceptance must compare every returned field/ID independently and inspect
actual arguments/schemas/calls, no relaxed criteria or profile lookups.

### US2 actual acceptance — T025

Test-first supplemental failures: alias/schema/combined retrieval absent (three FAIL,
one ERROR), then40 host tests PASS,36 native-interpreter isolated tests PASS, Ruff/Pyright0.
Real native registered SDK tool rejected16 invalid filter cases before any client access;
four direct boundary cases (before2005, below8.3, exact inclusive bounds, literal dot-star)
PASS. No direct-mode result is mislabeled as OE end-to-end or replay proof.

| Native conversation | Execution | Outcome |
|---|---|---|
| Batman Begins AND Action/Adventure, exact2005, >=8.3 | 9e669497-723b-4551-a1b6-c70dc85d9149 | ok1 |
| Action OR Comedy, exact2005 | 9e550f43-d4f1-4806-87e2-c91618e9153c | ok1 |
| Action AND Comedy, exact2005 | 93a11b14-b924-4f02-8fa9-78a9c203477c | empty |
| Strict after2005 | ed370a61-24da-4916-8e19-6091ca071e8f | empty, lower inclusive=false |
| Strict above8.3 | 42c453c7-7995-4c02-a7e9-968fc0f5784b | empty, lower inclusive=false |
| At most8.3/through2005 | ffb2ef47-b877-4b11-aff3-2553d5e7d72e | ok1, upper inclusive=true |
| Science fiction2005/>=7/count2 | 12cd3f53-d895-435e-a104-000ec1c34edc | ok2, Sci-Fi canonical argument |
| Unknown Zorbflax genre | f582f868-0d78-43a5-a7db-20f7301dde4e | clarification, zero tool calls |

All eight traces exclude profile schemas/calls. Independent comparison utility
[native_movie_checks.py](../../agents/movie-scout/tests/native_movie_checks.py) confirms
all eight fields/ID across four batches/five records. Its initial indentation defects
were fixed before successful comparison; these were utility failures, not fact mismatches.
Native existing unrated fixture objectId:573a1393f29313caabcddbed (La nao capitana):
ordinary retrieval includes it, rating_min0 excludes it. Initial cold discovery encountered
ServerSelectionTimeoutError; bounded minimal control passed, one final fixture attempt
passed without any configuration/budget change. No permanent outage/root cause inferred.
Malformed BSON arrays/bools/nonfinite source variants remain supplemental predicate/normalizer
coverage, not seeded Atlas fixtures. Existing V14 controlled-failure and count/guard
regressions pass in native isolated suite. **T025 complete;25/49 T001–T025.**

### US3 validation definition — T026, before implementation

V09 fresh request three highly rated comedies from2000s: genres Comedy, inclusive2000–2009,
sort rating_desc, count3, no hidden minimum. All results must be finite scalar numeric0–10,
descending rating then title/_id, independent source comparison and fit/facts separation.
V10 default5, original100 capped10, invalid0/bool/string count before client; V11 explicit
shortfall compares effective limit and never pads. Ordinary discovery still includes unrated
La nao capitana; high-rating selection excludes it and reports empty if no rated match.
Locate existing mixed rated/unrated title via bounded reads only; if no two-rated-plus-unrated
fixture is accessible mark that exact native mixture NOT RUN, use constructed source
predicate coverage rather than inventing catalog rows. V12 all-unrated and missing metadata
are explicit; V13 no matches never relaxes; V14 retains controlled unavailable/restore checks.

### Focused timeout investigation — 2026-10-21 (historical)

Current evidence supersedes the unclassified timeout below; native memory is already
resolved and was not revisited. No fixture was recreated, recalled again or deleted.

| Check | Observed bounded, sanitized result |
|---|---|
| Actual title query | Unchanged escaped case-insensitive substring Batman Begins, scalar title/identity eligibility before limit, fixed six-field projection, title/_id sort, limit1 |
| Native cold driver read | ServerSelectionTimeoutError, timeout=true, ~10343ms; command listener observed no find sent |
| Read-only queryPlanner explain | Same predicate/projection/sort/limit, CSOT5s and maxTimeMS<=5000; ServerSelectionTimeoutError ~5037ms, no explain sent; no plan obtained, no executionStats/catalog scan attempted |
| Independent minimal control | ID-only find{}, limit1, CSOT5s; same ServerSelectionTimeoutError; three discovered members, zero selectable |
| Native member transport control | After actual SRV discovery, one bounded TCP/TLS attempt per member, three concurrent maximum, 2s each: TCP_TIMEOUT for all three; TLS never reached |
| Diagnostic caveat | An earlier transport probe used the unresolved SRV seed before discovery and returned DNS_FAILURE; this is NOT evidence that member DNS failed. The corrected post-selection probe above supersedes it |
| Separate server-budget defect | Installed PyMongo4.18.3 Connection.apply_timeout replaces maxTimeMS with remaining CSOT; regression reproduced 9999ms despite cursor.max_time_ms(5000) |
| TDD correction | Added real serializer regression first (FAIL9999>5000), then nested pymongo.timeout(5) around full consumption/normalization inside existing outer10s; cursor close stays in outer scope; no deadline increased |
| Native post-fix body | unavailable/RETRIEVAL_TIMEOUT, count0, ~5142ms; strict server budget regression passes in native interpreter |
| Single final fresh native request | HTTP200, session6eeaa366-1106-4ee8-b6eb-4bca1fc8ee32, execution1849e0ae-5c3b-4567-b767-5117507de041; request ~11961ms including LLM, tool ~5092ms, unavailable/RETRIEVAL_TIMEOUT/count0 |
| Native envelope | Recorded output decodes directly to application envelope; no additional result/content envelope layer. Real direct-driver selection failure independently rules out SDK double wrapping as timeout cause |
| Final model schemas/calls | Router[] then twice [get_current_date, search_movies]; search_movies only, zero profile calls; no synthetic fixture/silent-comedy/pre1930/Batman-avoidance injection |
| New source comparisons | NOT RUN: zero returned records; historical32 source comparisons are not reused as new evidence |

**Verified failure layer:** native client server selection / TCP reachability, before
query execution. A full-catalog scan, expensive eligibility expression, blocking sort,
server MaxTimeMSExpired, pool exhaustion or SDK envelope defect is NOT demonstrated as
the current cause. Unanchored regex and expression eligibility can still be expensive
once connectivity works, but no query plan or scan cost is claimed. The precise external
cause (firewall/VPN/route/access-list/availability) is **not known**; the short cold native
window and member TCP failures do not establish a harmless transient or cold-start-only cause.

Safe remediation: an authorized operator should privately check cluster availability,
the native container's approved route/VPN/outbound TCP reachability and current egress
address against existing Atlas access policy, following the official
[Atlas connection troubleshooting guide](https://www.mongodb.com/docs/atlas/troubleshoot-connection/).
Do not disable TLS, broaden access, change credentials/URI, increase timeouts, create
indexes or change substring matching to exact title. None of those changes were made.
Only after reachability is restored should the bounded native V17 request and independent
source comparison be repeated; do not reseed the existing fixture.

Validation: **35 host tests PASS**, **31 native-interpreter isolated tests PASS** (excluding
host manifest and host fixture-utility tests); Ruff PASS, explicit venv-path Pyright0,
official manifest validator0. Resolving the venv executable symlink initially selected
the base interpreter and produced two missing SDK import errors; corrected un-resolved
venv path passes. Editor get-errors clean; separate Pylance MCP still reports the known
tools import reportMissingImports environment warning, not a newly introduced code error.
No native end-to-end success is claimed. No service restart/stop, catalog/index write,
infrastructure change, private configuration edit or memory mutation. Existing native
stack left running. Before/after implementation hooks absent. **T020 remains unchecked,
19/49 complete; T021 gated, T049 OPEN.**

### Latest implementation attempt: synthetic V17 present, movie read timed out

This section supersedes the older missing-fixture blocker below. Consent was recorded
above before the sole write. Official primary guide/memory/App docs were rechecked;
installed memory SDK0.11.9 signatures and runner adapters were inspected. The isolated
opt-in utility [native_v17_fixture.py](../../agents/movie-scout/tests/native_v17_fixture.py)
uses the exact native MemoryClient used by the runner, with its documented direct local
service api_prefix. Attribution comes only from the existing authorized execution; no
identity is guessed, no dotenv is opened, and no database client is used for memory.
The local service OpenAPI declares no bearer security scheme; do not mislabel this
local native SDK call as independent bearer-authentication proof. No auth bypass was
added to the application, and production graph/tools/prompts/configuration are unchanged.

| Check | Actual result |
|---|---|
| Single private synthetic create | PASS: one create_semantic, upsert=false; exact label/text/synthetic metadata stored; no other memory changed or deleted |
| Immediate recall after create | SDK context returned normally but did not contain fixture: failed assertion, not accepted as PASS |
| Subsequent exact-query and ordinary-profile-query recall | PASS: fixture present in both actual context responses; semantic count1, selected count1, token_count35 |
| Re-run utility | PASS: existing exact fixture reused, no second write; healthy context includes fixture |
| Stored SDK has_embedding | true; no vector, provider/model identifier, user or endpoint printed |
| Fresh same-user movie session1 | session15763a94-a946-452c-b229-c0c8aed3b8eb / execution6516c102-4dec-49dc-b450-2d41a6da7b1a; HTTP200, tool outcome unavailable, no movie fallback |
| Fresh same-user movie session2 | session83743ff8-eaad-4be3-b3b1-3f6aab030c90 / execution24409e8b-9380-4ca2-a2ff-ca16f24dcd16; HTTP200, tool unavailable/RETRIEVAL_TIMEOUT, zero records |
| Actual model schemas, both sessions | router has no tools; subsequent inputs exactly search_movies/get_current_date; no save_user_info/recall_user_info schemas |
| Actual invocations, both sessions | search_movies only, title Batman Begins/requested_limit1; zero explicit profile calls |
| Actual model inputs, both sessions | no synthetic fixture text, silent-comedy/pre1930 restriction or Batman avoidance injected |
| Public failure response | honest unavailable/retry/private-configuration guidance; no fabricated film facts |
| New source comparison | NOT RUN: no records returned in either new session; historical32 comparisons remain historical |

The first immediate empty recall and later successful recall are consistent with delayed
search visibility, but no unverified root cause or provider HTTP status is asserted.
The positive stored/recall result now resolves the missing-fixture prerequisite. V17 movie
isolation is observed at schemas/inputs/dispatch, but its mandatory retrieved-fact evidence
is incomplete because the native catalog read timed out. No timeout increase, restart,
key re-diagnosis, index/network/role change or catalog write/probe was attempted.

**Concrete sequential failure: T020 native movie retrieval RETRIEVAL_TIMEOUT.** T020 remains
unchecked; T021–T048 are NOT RUN, not silently bypassed. **19/49 complete, 30 pending**;
T049 OPEN. Retry the same bounded native V17 movie request once movie access is available,
then compare every returned fact with the source before T020 completion. Do not recreate
or delete the retained fixture. The pre-existing stack remains running.

Final continuation validation: **34 host tests PASS** (31 existing +3 utility safety
checks: single private non-upsert create, no duplicate/delete, healthy-empty recall fails).
These three checks were added after the opt-in utility execution; no test-first/red-green
claim is made for this isolated validation utility. No production implementation changed.
Ruff src/tests PASS. Initial root Pyright invocation selected the wrong import environment
and reported2 missing SDK imports; explicit project interpreter rerun gives0 errors/warnings.
Official agent manifest validator exit0 (the unsupported root validate subcommand was
corrected to agent validate). Editor diagnostics clean; git diff --check, changed-document
links, protected project/dev/provider baseline hashes, private artifact ignores and empty
example placeholders PASS. Existing generated Docker ignore present; no JS/publishing/
Terraform/Helm setup requiring additional ignore files was introduced. Native isolated30
tests are historical, NOT rerun in this continuation; actual native evidence here is the
memory SDK persistence/recall and two OE movie executions above. Final service state5/5
running, app/OE/memory/MongoDB healthy and UI running. No service started/stopped for this
work. Before/after_implement hooks re-read: none registered, none dispatched.

**19/49 complete, 30 pending** (T001–T019); T020 partial/uncompleted, T021 onward
not started. T049 still blocks deployment/non-development acceptance. No full MVP or
all-story acceptance claim. Broad shared identity risk remains as disclosed below.

### Latest authorized native startup and memory retest — 2026-10-21

This is the current state; failed-startup and endpoint diagnosis sections below are
historical. The maintainer confirmed the private correction and authorized only safe
local startup/reload and attributed read-only memory verification. Constitution v3,
official local lifecycle/client documentation and installed CLI help were checked.

| Check | Actual result |
|---|---|
| Initial native availability | unhealthy, 2/5; app/OE not running, memory exited1 |
| Private supported override present / valid HTTPS base / matches requested official geography/base shape | true / true / true; no endpoint value recorded |
| Private Voyage key configured | true; no credential content or inferred validity from format |
| Native startup | agentengine --no-log dev up exit0; no unnecessary stop, clean or reset |
| Memory container refreshed | true; native startup recreated it with current configuration |
| Actual memory PID1 override configured / matches private configuration | true / true |
| Actual memory PID1 key matches private configuration | true |
| Installed native VoyageService clients select override | true for both synchronous and asynchronous clients; isolated constructor using PID1 environment, actual client _params.base_url comparison, no provider call |
| Native memory health endpoint | HTTP200 |
| Existing authorized execution | Playground GET HTTP200; original user/org/project/session attribution recovered privately, expected session verified |
| Underlying POST /api/v1/retrieval/context | HTTP200 twice: bounded semantic/episodic request and repeat with ordinary recall query/default retrieval options |
| Default retrieval result | formatted_context is an empty list; selected_memories absent/null; metadata token_count0; no profile text inspected or printed |
| Authorized semantic / episodic listings | each HTTP200, count0, entries0, no next_cursor |
| Request-correlated bounded diagnostic classification | no observed provider404/401/403, embedding failure, key/endpoint incompatibility, TLS failure or dimension-mismatch signature |
| Final native health after startup/retest | ok, 5/5 running; app/OE/memory/MongoDB healthy, UI running without configured healthcheck |
| Preservation | protected project/dev/agent/provider/private dotenv bytes unchanged across startup; project volume names unchanged; prior authorized execution accessible |

**Operational memory blocker resolved for these requests.** This is actual underlying
HTTP200 retrieval, not wrapper found=false or a swallowed HTTP500. The initial diagnostic
looked for a nonexistent client _base_url attribute; installed BaseClient source shows
_params["base_url"] is authoritative, and corrected comparisons passed for both clients.
Likewise, emptiness is verified from the actual formatted_context field, not a guessed
response key. No provider-response status is inferred from absence of an error signature;
the observed HTTP200 statuses belong to the native memory API. No independent provider
HTTP status, new OE recall execution or full V17 pass is claimed.

**Remaining prerequisite: an authorized pre-existing cinema-preference fixture for V17.**
Both scoped stores remain empty. No fixture created, profile save/delete, other-user scan,
new session, catalog operation, extraction/model/dimension change, private configuration
edit, cloud action or deployment occurred. Native startup preserved existing volumes;
no clean/reset/removal was used. The stack is left running as requested.

T020 remains unchecked; **19/49 complete, 30 pending**, T021 stays gated. T049 remains the
separate effective-find-only-identity gate before deployment/non-development acceptance;
existing broad shared DEV credentials are not read-only credentials. Application tests
were not rerun for this operational/documentation-only continuation.

Final validation: native manifest exit0; changed-document editor diagnostics clean;
git diff --check and local links PASS; task counts19/49 with T020/T049 open. Private
dotenv/venv/generated-state ignore checks each PASS (the initial multi-path quiet Git
invocation was invalid; corrected individual checks passed). Before/after implementation
hooks re-read: none registered. Final native status ok5/5 confirmed after retrieval.

### Historical VOYAGE_URL reload — startup blocked, 2026-10-20

This historical continuation superseded earlier claims at that time; the 2026-10-21
startup/retrieval evidence above now supersedes its failed-stack state.
The maintainer privately confirmed VOYAGE_URL was set and authorized safe local reload
and retest. Constitution v3 and official local lifecycle documentation were rechecked.
No private value, hostname, credential or digest is recorded.

| Check | Actual result |
|---|---|
| Initial native CLI status | unhealthy, 2/5 available; already degraded before this reload |
| Local VOYAGE_URL configured | true |
| Container VOYAGE_URL configured / matches local configuration | true / true |
| Official local reload | agentengine --no-log dev stop exit0; dev up exit1 |
| Memory container recreated during this attempt | false; existing container already contains the current override |
| Startup failure | bounded memory logs identify VOYAGE_URL validation: a valid HTTPS URL is required; memory exits1 before readiness |
| Actual PID1 environment / clients selecting override | NOT VERIFIED: service exits before a stable process/client check; container propagation is not constructor-selection proof |
| Native memory HTTP transport | unavailable; no HTTP response/status from memory |
| Native POST /api/v1/retrieval/context | NOT RUN: memory cannot start; no new HTTP500 or healthy-empty result claimed |
| Existing authorized execution GET through Playground | HTTP502 with OE unavailable; history cannot be re-read through the API now |
| Final health | CLI unhealthy, 2/5 available; MongoDB healthy, UI running without healthcheck; memory exited1/unhealthy; app/OE created, not running |
| Storage preservation | project volume identity/creation/driver/mountpoint metadata unchanged; memory mounts present; no volumes/data removed |
| Protected files | project memory/extraction, dev/agent configuration, provider source and private dotenv unchanged by private before/after comparison |

Distributed native integration still consumes VOYAGE_URL and exposes the base_url keyword.
The observed failure is startup HTTPS validation, **not** authentication, provider-network,
quota, model, index or dimension failure. No provider HTTP status or key-invalid conclusion
is justified. Do not bypass transport validation or substitute the older variable. This
attempt did not establish that both endpoint variables have equal values.

**Actionable prerequisite**: privately correct VOYAGE_URL to the gateway's approved valid
HTTPS API base URL, consistent with the official
[client base_url contract](https://www.mongodb.com/docs/voyageai/api-and-clients/).
Do not invent an HTTPS endpoint or merely change a scheme unless actually supported.
Keep key/model/dimensions unchanged; no secret should be supplied in chat. Then repeat
native reload, actual-process/client selection and attributed read-only context retrieval
using the existing authorized execution's identity/session. No identity was guessed,
new session created or un-attributed retrieval substituted.

V17 fixture remains separately unavailable based on previous successful authorized
semantic/episodic listings; stores could not be rechecked while memory is down. Fixture
creation requires separate consent and was not performed. **T020 unchecked, 19/49 complete,
30 pending**; stop before T021. T049 remains open; broad shared DEV credentials are not
read-only credentials. No clean/reset, volume removal, catalog operation, memory
save/seed/delete, infrastructure change, cloud upload or deployment occurred. The failed
stack is explicitly reported, not described as restored/healthy. Manifest validation
exit0; application tests were not rerun for this operational/documentation continuation.

### Endpoint correction — verified native configuration, 2026-10-20

The earlier instruction to replace the key with an Atlas model key was premature and
is superseded here. The maintainer has a custom embedding endpoint configured as
ENDPOINT_URL_VOYAGE. Its value was inspected privately only; no host/key/URI is recorded.

| Check | Actual result |
|---|---|
| ENDPOINT_URL_VOYAGE configured in local dotenv | true; endpoint classification custom |
| Propagated to memory container / actual PID1; matches local dotenv | true / true / true |
| Consumed by native embedding constructor | false; no references in distributed server bytecode |
| VOYAGE_URL configured in dotenv / container / PID1 | false / false / false |
| Native constructor integration | VoyageService.__init__ reads os.environ.get("VOYAGE_URL"), validates transport, and supplies base_url to both voyageai.Client and AsyncClient |
| Current constructor explicit base_url / matches custom endpoint | false / false for both clients |
| Current SDK automatic endpoint selection | atlas; the custom endpoint is not selected |
| Offline constructor regression | PASS: synthetic HTTPS VOYAGE_URL reaches base_url in both intercepted clients; no network calls |

Evidence: existing memory image, native Python3.11.17, voyageai0.5.0; public distributed
Voyage integration is compiled bytecode, inspected without modifying it. Installed SDK
_BaseClient resolves base_url or get_default_base_url(api_key). The official
[Python client reference](https://www.mongodb.com/docs/voyageai/api-and-clients/)
documents base_url and automatic key-based routing; the **VOYAGE_URL environment name
is verified in the installed native runtime**, not asserted to appear in the published
Agent Engine memory configuration schema. No speculative memory.voyage.base_url field
was added. VOYAGE_API_BASE/VOYAGE_BASE_URL are not substitutes for this constructor path.

**Verified configuration defect**: propagation works, but the custom variable name has
no native consumer. The previously observed Atlas endpoint rejection does not establish
that the key is invalid for the intended gateway. Gateway key validity, compatibility
and actual retrieval after correction remain untested; no private endpoint was contacted.

**Exact private correction**: add VOYAGE_URL using the same approved API **base** URL
currently held in ENDPOINT_URL_VOYAGE (not a full embeddings-operation URL), keeping
the existing key/model/dimension unchanged. The public [environment example](../../agents/movie-scout/env.example)
now includes an empty supported-name placeholder. No private dotenv was edited. Generated
local Compose uses env_file for memory, with neither endpoint name explicitly overridden;
this is not an allowlist loss. Verify actual PID1 and both client base_url values after
an authorized configuration refresh; stop/up can resume an old container and alone does
not prove a changed environment was loaded. No restart/recreation performed here.

Cloud propagation is **not verified**: published memory settings document model/dimension,
not this custom endpoint alias. No secret upload/sync, deployment or cloud change occurred.
Do not infer cloud support from local env_file behavior. No memory writes/fixtures,
catalog operations, extraction changes, provider requests or additional sessions created.
T020 remains incomplete (healthy retrieval and authorized existing V17 fixture required),
19/49 complete; T049 unchanged. Existing five services remain running.

### Authorized local reload and memory retest — 2026-10-20

Maintainer explicitly authorized a brief non-destructive local reload after privately
changing the Voyage key. Rechecked constitution v3, installed CLI help and official
[local lifecycle documentation](https://www.mongodb.com/docs/agentengine/build/run-local/).
Executed `agentengine --no-log dev stop` then `agentengine --no-log dev up` from the
existing agent workspace; both exit0. CLI output was captured privately, not copied.
No `dev clean`, reset, volume deletion, cloud secret/configuration command or deployment.
Installed restart help targets the app and is not proof of memory environment refresh.

| Check | Actual result |
|---|---|
| Local dotenv Voyage key configured | true |
| Memory container environment matches current dotenv | true before and after reload |
| Actual memory PID1 environment configured / matches current dotenv | true / true before and after reload |
| Memory container recreated | false; existing container stopped and resumed; recreation unnecessary because actual key already matches |
| Existing services | 5/5 running; app/OE/memory/MongoDB healthy; UI running without a configured container healthcheck |
| Mounted storage and volume identity/creation metadata | unchanged |
| Project memory/extraction, dev/agent configuration, provider source and private dotenv | unchanged by private before/after comparisons; no digest/value printed |
| Prior recall execution and same user/session attribution | preserved, native execution GET HTTP200 |
| Native POST /api/v1/retrieval/context | HTTP500 on both bounded retests, using the exact existing authorized user/org/project/session from execution db397c5a-e51f-42a8-ba93-304b13723ebd |
| Authorized semantic / episodic stores | each HTTP200, count0, entries0, no next cursor; identical before/after |

Retest used the existing native memory API directly with the registered recall tool's
profile query shape; no new agent invocation/session or wrapper-success claim. It is
actual underlying context retrieval evidence, not a fresh OE end-to-end tool execution.
No profile text, identity, keys, hosts, raw logs/errors, environment/inspect or generated
compose output disclosed. No memory save/seed/delete or movie catalog operation issued.

**Historical failure category: embedding-provider key/endpoint incompatibility at the
selected endpoint, not proof of an invalid key for the intended custom endpoint.** Bounded new-request
memory logs contain Voyage APIError/query-embedding failure and explicit diagnostics
requiring a MongoDB/Atlas model API key and rejecting the Voyage key for that endpoint.
Generic 401/403 mentions were NOT accepted as observed provider response codes. No
confirmed quota, model, vector-index or dimension root cause is claimed. Earlier broad
startup-log dimension/configuration mentions are not correlated request-failure evidence.

Official [model API key documentation](https://www.mongodb.com/docs/voyageai/management/api-keys/)
distinguishes Atlas-created model keys from Voyage-direct keys; they authenticate against
different endpoints. [Client documentation](https://www.mongodb.com/docs/voyageai/api-and-clients/)
and [migration guidance](https://www.mongodb.com/docs/voyageai/tutorials/migrate-to-atlas/)
describe matching key/endpoint pairs and automatic routing only when no explicit override
is set. The original Atlas-key replacement recommendation is superseded by the verified
endpoint correction above: first configure the intended endpoint through VOYAGE_URL;
do not replace a gateway credential solely on the basis of an unintended Atlas response.
No key creation, endpoint/configuration change,
upload/sync, upgrade or cloud action was performed or authorized by this reload.

**T020 remains incomplete, 19/49 complete.** Two remaining prerequisites: a working
native embedding/context retrieval path AND an authorized pre-existing cinema-preference
fixture for V17. Both authorized long-term stores remain empty; do not seed a fixture or
inspect other users without separate authorization. T021 stays gated; T049 remains the
independent separate-find-only-identity deployment/non-development gate. Stack left running.
Before/after implementation hooks: none registered. Documentation diagnostics and final
preservation checks are recorded with this continuation; prior application test counts
below are historical, not new test runs for this documentation-only update.

### US1 implementation / T015–T019

Test-first: four missing-function failures observed before normalization/title retrieval;
native-placement expected failure observed before sandbox assignment; strict SDK schema
coercion failure reproduced before using existing Pydantic StrictInt/StrictStr. Count
prompt corrected after native model pre-clamped100 to10 (old cap evidence invalid).
No dependency/provider upgrades. Shared graph already discovers app.get_tools/schemas;
no graph bypass or unnecessary main edit. Movie tool executes in existing remote sandbox.

Implemented scalar usable-title/source eligibility before limit; escaped literal regex;
fixed projection/collection/title+ID sort; finite BSON Decimal128 rating normalization;
nullable missing fields and bounded text; type-aware source IDs; strict count/default/cap;
unsupported future filters explicitly rejected; cleanup/partial-result safety preserved.

### Actual native US1 results (partial T020)

Each execution used the Playground streaming endpoint with explicit nonsecret user/session
identity. Native session history, not wrapper-success events alone, supplied outcomes.

| Case | Execution | Observed result |
|---|---|---|
| First Batman3 | 3ef9a628-8d16-4016-9ce1-7c909b869cbc | Safe unavailable / RETRIEVAL_TIMEOUT, no movie fallback; NOT a deliberate controlled failure |
| Batman3 retry | 694d1c44-95bd-4a8b-93f7-d621806eb60b | ok3, later independent source comparison PASS |
| V01 full | 84b1cb3c-cadf-4d65-9673-041f3610c980 | Batman Begins2005, ok1 |
| V01 mixed case | 60049df6-9e9a-44c3-983b-e776312e8438 | bAtMaN, ok5 |
| V02 literal parenthesis | 89e41c3d-f5f2-4462-9a74-0304e276aa1f | ok3: (500) Days of Summer, (T)ERROR, (Untitled) |
| V02 literal dot-star | c4652fa5-fd54-4303-b45f-f8b089a70545 | empty, not regex wildcard matching |
| V03 absent title | 15f2cfff-63c8-4e61-ae0e-cad2f1962e8c | empty, honest no-match response |
| V03 blank | aada5d06-609e-4887-a2f7-cb73b82f44c1 | Clarification, zero tool calls |
| V04 duplicate/missing | cfd3bb4b-660d-4387-92e5-057fa603da3a | Hamlet7, distinct IDs, four equal titles differentiated by year; Kadin Hamlet plot unavailable |
| V10 original100 after fix | b90b8982-8a62-4635-bc3e-a57e5d1feb63 | requested100/effective10/returned10/capped true; explicit cap notice |
| V18 mixed | 613ed26d-cbb5-45f5-80f8-c195c7f7a6a1 | Movie3, only search_movies invoked; separate-memory guidance |
| V20 inert title | eaf19b4c-c0fa-4150-8433-4929051361fe | Instruction-like quoted title searched as literal, empty; zero profile calls |

Source comparison: seven sessions/32 records (including repeat records across sessions),
at most10 per query, fixed projection and IDs, CSOT10/server5000ms, cursor/client finally
closed. All returned normalized fields equal independently re-read projected source facts;
IDs distinct within every result. Public final responses inspected: factual years/genres/
ratings/plots grounded, missing genres on (T)ERROR and missing plot on Kadin Hamlet labeled
unavailable, Hamlet shortfall explained. Source examples:
objectId:573a13aef29313caabd2c349 = Batman Begins2005/Action+Adventure/8.3;
objectId:573a13f7f29313caabde6828 = (T)ERROR2015/genres unavailable/7.6;
objectId:573a1397f29313caabce66e1 = Kadin Hamlet1977/Drama/7.2/plot unavailable.

### T020 continuation — direct native boundaries and recorded OE schemas

Added four reproducible real-SDK boundary tests in
[test_native_boundaries.py](../../agents/movie-scout/tests/test_native_boundaries.py).
No application-source fix was needed; no invented red/green implementation claim.

| Check | Actual outcome and evidence boundary |
|---|---|
| V14 controlled missing secret | PASS: independent process using the existing tool interpreter and real App registration/get_tools/StructuredTool invocation; only its own MOVIES_MONGODB_URI removed inside a restoration context; unavailable/NOT_CONFIGURED, zero movies, zero client constructions; exact private environment equality verified after restoration |
| V14 restored read | PASS: same independent process restored the original private value, invoked the same registered tool, returned ok1 for Batman Begins with source ID objectId:573a13aef29313caabd2c349; its own client closed in finally |
| V10/V22 invalid structured types | PASS: real SDK schema rejects requested_limit true, string3, float1.5 and numeric title123; four ValidationErrors, zero movie-client acquisitions |
| V10/V22 invalid structured values | PASS: requested_limit0/-1 and title empty/whitespace pass to actual registered validation and return invalid/INVALID_CRITERIA; four cases, zero movie-client acquisitions |
| V18/V20 direct guard | PASS: actual dispatch_guard loaded with real App/tool registration; movie, mixed and uncertain four-call batches denied atomically, four original IDs preserved per batch; no ToolNode/native wrapper/body dispatched |
| Actual movie model schemas | PASS: OE execution84b1cb3c-cadf-4d65-9673-041f3610c980, three model input events: router has no tools; both subsequent inputs have exactly search_movies(title, requested_limit) and get_current_date(timezone_name); sole actual tool invocation search_movies |
| Actual mixed model schemas | PASS: OE execution613ed26d-cbb5-45f5-80f8-c195c7f7a6a1 has the same three-input schema pattern and sole actual tool search_movies; save_user_info/recall_user_info absent from schemas and dispatch |

Direct tests use the installed SDK/tool-mode LangChain wrapper and actual application
validation/guard, not raw movie functions as a substitute for wrapper invocation. They
are **independent native-process tests, NOT OE end-to-end controlled failure, AER secure
transport, model behavior or replay proof**. No new network/provider path or direct-mode
bypass was enabled. Existing recorded OE inputs provide actual wrapped model-visible
schemas separately; inspected started/input events only, not successful wrapper labels.
The direct process privately inherited only path settings and the dedicated movie URI;
no model/platform secrets, environment files or environment dumps. Both layers suppress
raw diagnostics. Shared processes, cached clients, persisted secrets and stack unchanged.

### Sole mandatory T020 blocker: V17 prior movie-preference fixture unavailable

Inspected only the already-authorized test identity from known completed recall execution
b4ebfcf3-f930-476b-863a-818ebb68de66, never another user's profile. Its old recall result
was found=false, not positive fixture evidence. New native Playground recall execution
**db397c5a-e51f-42a8-ba93-304b13723ebd**, session
**e7c28897-9316-4034-9892-53d65ddf8bed**, completed; the only explicit tool was
recall_user_info. Its result was found=false, but underlying native
memory:POST retrieval/context recorded **HTTP500**. Thus neither execution/tool success
nor found=false certifies healthy memory or absence of a fixture; the error was not
misreported as a successful empty retrieval. No raw error/profile/identity printed.

Independent native user-scoped read-only semantic and episodic listing endpoints each
returned **count0, entries=[], no next_cursor**, confirming no existing memory fixture
available through those stores for that authorized context. No global/taxonomic/profile
scan or other-user session listing was performed. No memory seed/save/delete or extraction
change. Ordinary operational session recording remains enabled and is not fixture seeding.

**V17 NOT RUN / mandatory fixture unavailable**: cannot demonstrate isolation against a
pre-existing movie-preference memory when none is available for the authorized test user.
Native context retrieval also needs its HTTP500 investigated before a future fixture
recall can be trusted. This is not an LLM quota or movie connection failure. Proceeding
would require an authorized already-existing suitable fixture and healthy native recall;
creating one or changing infrastructure is outside this request. T020 remains unchecked,
**19/49 complete, 30 pending**; T021–T048 cannot start because the explicit T020 phase gate
has not passed. T049 remains independently open for deployment/non-development use.

**Validation**: host31 tests, native-interpreter30 isolated tests (all except host manifest
test), zero failures/errors; the four new tests cover eight invalid inputs, three denied
batches and controlled missing configuration. Additional same-process native live restore
check PASS above. Ruff/Pyright source
and manifest validation PASS. Native Python3.11.16, SDK/runner0.11.9, PyMongo4.18.3.
Live remote movie dispatch confirmed; secret-narrowing isolation itself is not proven.
Project extraction/dev/provider hashes unchanged. Existing stack left running; only
normal hot-reload occurred. No private environment files read, movie writes/probes,
indexes, memory seeding/deletion/extraction edits, infra changes, uploads or deployment.

Continuation final audit: 31 host tests re-run PASS; native30 PASS as recorded above;
Ruff PASS, Pyright source0 errors/warnings, official manifest validator exit0,
changed-file editor diagnostics clean, local document links/task IDs/19 checked tasks,
public secret-pattern scan/empty example placeholders, generated Docker ignore and
protected project/dev/provider hashes PASS. Existing five containers remain running;
no stack was started for this work or stopped. Before/after implement hooks re-read:
none registered, no hook dispatched. No task newly checked: partial T020 is truthful.

## Foundation retry

**Current retry — 2026-10-20: T014 foundation PASS**, superseding the quota blocker
below. Native manifest validation exit 0, existing hot-reload stack 5/5 healthy; no
restart/reset. Date execution `d381162b-a3eb-4dd6-8590-c4129e7696be`, session
`af473e07-6164-4cec-b947-2619b67df936`: wrapped LLM succeeded, native date tool
executed, session history confirms UTC `2026-10-20` and correct final prose date.
Do not equate a completed nonstreaming response with tool success: its short result alone
was insufficient; actual streaming events and bounded session history supplied proof.
Standalone nonmovie recall execution `b4ebfcf3-f930-476b-863a-818ebb68de66`, session
`534e06c5-fbf4-44fe-88ed-b1791544b38e`: native recall tool and wrapped model succeeded,
completed without error events. No explicit save, seed/delete or profile content printed.
Direct native-interpreter malformed-route/denied-batch/cleanup tests: 20 PASS,
0 failures/errors, Python 3.11.16, SDK/runner 0.11.9, PyMongo 4.18.3. These direct
isolated tests prove application guards, not adversarial model behavior or OE replay.
Provider builder, extraction and memory configuration remain unchanged. Full V19–V22
acceptance is still pending; no deployment or least-privilege claim. T049 remains OPEN.
Progress: 14/49 tasks complete, 35 pending; proceed to T015.

**Historical Date**: 2026-10-20 | **Native feature scenarios**: no complete V01–V22 PASS;
T014/V21 date attempted and BLOCKED by provider quota; V19/V20/V22 partial checks only.
A separately
authorized native-container connection diagnostic passed below; it is not feature acceptance.
Offline foundation is implemented; movie retrieval is not registered/accepted yet.
**Setup progress — 2026-10-20**: T001–T004 completed: maintainer implementation approval,
nonsecret baseline, direct PyMongo constraint resolved and checked, safe example variable.
## Current authorization and local development gate — 2026-10-20

The maintainer's exact reply **“POde continuar”** to **“Para continuar usando o usuário
amplo no desenvolvimento, será necessário aprovar uma exceção explícita às regras atuais;
não vou registrar essa condição como acesso somente leitura.”** is actual approval,
adopted in [constitution v3.0.0](../../.specify/memory/constitution.md). No further approval
loop is required. It supersedes earlier diagnostic-only and stop-before-T013 decisions
below ONLY for temporary LOCAL development and bounded native tests.

**Revised T005 DEV readiness: PASS** from the already-recorded native read/secret/network
and effective-grant evidence plus approval; neither diagnostic was repeated. These are
**broad shared credentials**, with insert/update/remove/dropCollection authority, NOT
read-only credentials. Separate variable names are separate configuration roles only.
Tools remain fixed-source, bounded allowlisted reads, no platform-URI fallback, no movie
writes/write probes, arbitrary commands, indexes or extraction changes. Broad grants
remain a real risk; application allowlists are not equivalent to database least privilege.

**T049 OPEN / deployment and non-development acceptance BLOCKED**: distinct identity with
complete effective grants consisting only of find on sample_mflix.movies is still required.
The original credential criterion was not passed or erased. No resource/user/role/network
changes, cloud-secret upload, deployment, memory seeding/deletion or movie writes approved.
Native foundation T014 still gates US1. Historical evidence below remains dated, not a new run.

### Historical T005 blocker (superseded for local development only)

The authorized metadata check
below confirmed movie insert/update/remove/drop privileges, not collection-find-only access.
The separate least-privilege identity remains required for T049, not local T013 onward.
The maintainer previously confirmed
temporary use of the same database identity in development and requested separate
configuration variables, leaving access management for later. Retain MOVIES_MONGODB_URI
and MONGODB_URI as distinct configuration responsibilities with no movie-client fallback.
This is not proof of least privilege or successful network access. Offline T006–T012 may
proceed under the approved sequencing exception; T005 remains unchecked and must pass
before T013/T014 under the old criteria. Constitution v3.0.0 now permits bounded local
native tests after guardrails, not deployment/non-development acceptance. No native movie
scenario had run at this historical checkpoint. B1 remains closed; T049 preserves the target.

## T013/T014 implementation and native checkpoint — 2026-10-20

**Current progress: 13/49 complete, 36 pending**. T001–T013 complete (T005 explicitly
revised DEV-only); T014 attempted but unchecked/BLOCKED; T015–T048 not started; T049
open for separate effective-grant-verified find-only identity before deployment or
non-development acceptance. No identity approval loop or repeat Atlas diagnostic.

### Test-first implementation T013

Added [test_manifest.py](../../agents/movie-scout/tests/test_manifest.py) before changing
the manifest. Observed expected failure for wildcard secrets, then PASS after edit.
[agent.yaml](../../agents/movie-scout/agent.yaml) now explicitly declares agent LLM_API_KEY
and tool LLM_API_KEY/MOVIES_MONGODB_URI. Tool sandbox needs the provider key for native
wrapped invoke_llm; native memory retains its own Voyage configuration. Platform URI is
automatically available per official contract, never a movie fallback. Sandbox sharing
is not per-tool isolation. Existing date/save/recall placement and feature flags remain.

Official [agent contract](https://www.mongodb.com/docs/agentengine/reference/agent-contract/),
[egress](https://www.mongodb.com/docs/agentengine/network-egress/) and
[local workflow](https://www.mongodb.com/docs/agentengine/build/run-local/) rechecked.
Existing proven local movie socket reachability needs no new destination for this
checkpoint. No guessed Atlas hostname, broad wildcard, allow-all, link or network change.
Native UI states HTTP proxy egress does not gate native sockets; local reachability does
NOT prove deployed egress. Existing top-level provider egress is accepted by installed CLI.
No deployed policy migration or deployed egress success is claimed.

Official `agentengine agent validate` returned 0 before and after edit. Existing stack
remains hot-reload, 5/5 containers running; no stack created/restarted/cleaned/stopped.
Actual live secret narrowing after manifest edit is NOT independently proven: existing
AER still has the dedicated movie variable. Do not claim new declarations are enforced
in pre-existing processes. Later native CLI configuration reload may be necessary, without
resetting memory or sessions. No movie tool registered yet.

### T014 native attempt and concrete blocker

Used native local Playground invoke and its actual streaming route (discovered from public
UI code) with nonsecret UTC-date prompts. Early calls without explicit user/session failed
durable-memory attribution. Installed `validate_durable_memory_identity` requires user,
session and tenant/execution attribution. Corrected requests include explicit local user
and new session IDs; native memory/durability were not disabled as a workaround.

Corrected calls reached wrapped LLM execution but failed. Bounded native OE diagnostic
classification confirmed provider **`insufficient_quota`**. This is real quota failure,
NOT assumed model unavailability. No raw provider messages, account/organization IDs,
hosts, keys, URIs or traces copied into evidence. Native failed execution references:
`82a59635-00ad-4d8c-9ae2-e5e3007ca23d` and streaming
`2013d6d3-cb84-494f-98b1-c6fcd2694ce8`. Earlier missing-identity execution
`f7ca362b-992f-436a-a9fd-8f860ef99efc` is NOT provider-access evidence.

**T014 BLOCKED**, unchecked. Provider/model availability, date output and standalone native
memory smoke are not confirmed. No profile save/recall requested after quota failure;
no memory seeded/deleted. Native requests may create ordinary operational conversation
history under unchanged platform behavior. Stop before T015. Resume by resolving quota/
billing privately for the existing provider key, then retry T014; never send credentials
in chat or switch models speculatively. This is not a movie-identity approval gate.

### Actual validation results and limits

| Check | Actual result |
|---|---|
| New manifest regression before edit | Expected FAIL for wildcard secrets |
| Host stdlib suite after edit | PASS, 21 tests |
| Real tool interpreter isolated safety suite | PASS, 20 tests, 0 failures/errors |
| Official manifest validator | PASS, exit 0 |
| Ruff source/tests | PASS |
| Pyright source, explicit interpreter | PASS, 0 errors/warnings |
| Protected extraction/dev/provider hashes | PASS, unchanged |
| Native date / provider | BLOCKED, insufficient_quota |
| Native standalone memory / OE denied-call replay | NOT RUN to completion |
| Native movie stories V01–V18 | NOT RUN, T014 blocked |
| V19/V20/V21/V22 full native scenarios | NOT RUN to completion; partial evidence only |
| T049 separate find-only credentials | OPEN; broad grants unchanged |

Actual tool-process interpreter: Python **3.11.16**, SDK/runner **0.11.9**, PyMongo
**4.18.3**. Initial container-default Python could not import the application and is NOT
runtime compatibility evidence. Corrected supplemental suite used tool process executable,
CWD/import path, only nonsecret path variables, in-memory test source and the host tests'
dotenv/App/provider patches. These are isolated-fake guard/cleanup/routing tests IN native
Python, NOT OE execution, natural-language routing, replay or acceptance. No files/secrets
copied into container, no live DB/provider call from those tests.

No movie query, write/probe, index/extraction change, user/role/network/resource mutation,
secret upload, deployment or stack restart in this session. Existing operational memory
and stack preserved. Pre/post implement hooks: none registered.

### Authorized T005 effective-privilege verification — 2026-10-20

**Authorization and method**: The current implementation request explicitly authorized
read-only T005 metadata verification, not general movie runtime tests. First rechecked
the official [connectionStatus command](https://www.mongodb.com/docs/manual/reference/command/connectionStatus/)
(supported on all Atlas clusters; `showPrivileges: true` returns the full effective
privilege set), [PyMongo 4.18.3 Database.command](https://pymongo.readthedocs.io/en/4.18.3/api/pymongo/database.html#pymongo.database.Database.command),
[resource semantics](https://www.mongodb.com/docs/manual/reference/resource-document/)
and [privilege actions](https://www.mongodb.com/docs/manual/reference/privilege-actions/).
Rechecked native [local development](https://www.mongodb.com/docs/agentengine/build/run-local/)
and [egress documentation](https://www.mongodb.com/docs/agentengine/network-egress/):
local reachability does not certify deployed egress. No egress/resource changes were made.

Reused the private in-memory diagnostic pattern below in the already-running native app
container. Located exactly one existing tool entrypoint process, privately selected only
its MOVIES_MONGODB_URI, and ran a separate diagnostic using that process's executable.
No private environment file, environment dump, inspect output or logs were opened or
printed. Credentials never entered command arguments or host output. The sole explicit
database command was `connectionStatus` with `showPrivileges: true`; no catalog query or
write probe was executed in this session. The response stayed inside the container;
neither authenticated names, assigned role names, hosts, URI values nor privilege resource
names were emitted. Only a fixed Boolean/status allowlist escaped both subprocess layers.

Evaluated every returned effective privilege, including database-wide, collection-name
wildcards, all-database and any-resource coverage. Find-only requires the full nonempty
grant list to contain only `find` on exactly `sample_mflix.movies`; no broader role is
silently accepted. Constructed offline checks covered exact find-only, broad coverage,
any-action, extra grants and malformed/missing metadata before the native diagnostic.
Client construction, command and finally-block close used CSOT 10s; a 15s alarm plus
20s inner/25s outer subprocess safeguards bounded this one-off check. No pool tuning.

| Allowlisted field | Observed result |
|-------------------|-----------------|
| context | `native_app_tool_environment` |
| status | `METADATA_OK` |
| collection_find_only | `false` |
| movie_find_granted | `true` |
| movie_insert_granted | `true` |
| movie_update_granted | `true` |
| movie_remove_granted | `true` |
| movie_drop_collection_granted | `true` |
| gate | `BLOCKED_BROAD_GRANTS` |
| cleanup | `OK` |

**Historical decision (superseded by revised DEV-only T005 above)**: Old T005 was
**unchecked / BLOCKED**, not metadata-unavailable. Effective
movie write/delete/drop authority is positively established by metadata; the previous
successful read is not used as permission proof. Separate configuration variable names
do not create distinct database identities or narrow grants. The planned independent
movie identity is still pending; the maintainer's temporary shared-user choice is not
a least-privilege credential proof. T049 remediation is an administrator-managed independent
identity with only collection `find`, no inherited/broader grants, privately configured
as MOVIES_MONGODB_URI, followed by effective-grant verification. No changes were made
to the existing shared platform identity, permissions, network, secrets or infrastructure,
and no already-rejected setup question was repeated.

**Validation categories**: diagnostic classifier offline checks **PASS**; both diagnostic
scripts' AST syntax checks **PASS**; native metadata retrieval **PASS**; least-privilege
gate **FAIL / BLOCKED**; diagnostic client cleanup **PASS**. Prior 20-test foundation
evidence is unchanged, not a new test run. All V01–V22 native feature scenarios remain
**NOT RUN**; T013–T048 remain unstarted. Progress stays **11/48 complete, 37 pending**.
Only implementation evidence documents changed; no application/runtime configuration
changed and the pre-existing stack was left running. No restart, deployment, provisioning,
secret upload or general movie runtime test was performed.

### Authorized native connection diagnostic — 2026-10-20

**Authorization**: The maintainer explicitly requested the test and confirmed the Atlas
IP entry and privately configured URI: “vamos realizar o teste. o Ip ja foi adicionado no
atlas e o env ja tem a uri com usuario e senha”. The temporary shared development identity
was accepted solely for this bounded read-only diagnostic. This later instruction
supersedes the earlier no-test restriction only within this scope; least privilege and
T005 are not waived. No ordinary implementation work was performed.

**Observed context**: Existing CLI-created hot-reload container `movie-scout-app-1`
(compose project `movie-scout`, service `app`), already running. The container's initial
environment did not contain MOVIES_MONGODB_URI; Boolean-only checks confirmed it in both
active `aer` and `tool` child-process environments. The generated development supervisor
loads CLI-managed guest environment files for child services, so the initial container
environment is not equivalent to the sandbox child environment. No private environment
file was opened. The diagnostic privately obtained only the dedicated URI from the
existing `tool` process environment, with no platform-URI fallback or host substitution.

**Execution**: A separate diagnostic Python process inside that existing native app
container used `MongoClient` against fixed `sample_mflix.movies`: filter `{}`, projection
`{"_id": 1}`, server limit and batch size 1, `max_time_ms=5000`. Client construction,
cursor consumption and finally-block cursor/client closure were inside `pymongo.timeout(10)`;
a 15-second diagnostic alarm and 25-second outer subprocess safeguard bounded execution.
Only one document at most was fetched; no document value or ID was printed. Imports,
warnings, logs and raw exceptions were suppressed; only allowlisted status fields escaped.

| Allowlisted field | Observed result |
|-------------------|-----------------|
| context | `native_app_tool_environment` |
| status | `READ_OK` |
| document_found | `true` |
| cleanup | `OK` |
| diagnostic Python | 3.11.16 |
| diagnostic PyMongo | 4.18.3 |
| installed SDK / runner | 0.11.9 / 0.11.9 |

**Evidence limits**: This proves successful minimal collection access from the native
container using the tool sandbox's existing secret, not execution through a registered
movie tool, OE approval, Playground, model routing or replay. Versions above were measured
in the container diagnostic interpreter, not independently in each running service's
interpreter. It was not a host-only database test. No writes, permission probes/mutations,
stack starts/stops/restarts, provisioning, deployment, secret uploads or configuration
changes occurred. The existing stack was left running.

**Historical remaining blockers (now T049)**: Old T005 stayed **unchecked** until the separate collection-find-only
identity and full effective grants are independently verified. A successful read cannot
prove the identity cannot write. T013 onward remains unstarted; all feature scenarios
**V01–V22 NOT RUN**, including full V22 wrapper/permissions/runtime acceptance. Previous
20-test offline evidence is unchanged; no new feature-test pass or acceptance is claimed.

**Readiness follow-up — 2026-10-20**: Maintainer requested setup guidance and confirmed
that the Atlas dataset exists and they can manage database access. This is a maintainer
confirmation, not independent connectivity or permission verification. T005 remains open
until the dedicated identity, private secret and network prerequisites are verified.

### Guided Atlas setup (performed privately by the maintainer)

1. In the existing Atlas project, open **Security → Database & Network Access → Database
   Users → Add New Database User**. Create a separate application identity using Password
   authentication; generate/store its password privately, not in chat or terminal commands.
2. Under **Specific Privileges**, assign only action `find`, database `sample_mflix`,
   collection `movies`. Remove any default built-in role and other grants. If using a
   custom role instead, it must have precisely that resource/action and no inherited
   broader roles. Restrict this identity to the intended cluster. Review the full union
   of grants before saving; do not substitute database-wide `read` or `readWrite`.
3. Under **Network Access → IP Access List**, review the existing approved network path.
   If public access is used and a new entry is needed, the authorized administrator can
   add only the development network's current public IP (prefer temporary access).
   Do not use `0.0.0.0/0`. For private networking, use the organization's approved VPN/path.
   A successful host connection does not establish native sandbox egress.
4. In the cluster's **Connect → Drivers** dialog, obtain the Python connection template.
   Privately substitute the dedicated database username and password, percent-encoding
   reserved characters in each credential component. Preserve Atlas TLS/SRV settings;
   do not disable certificate verification. Atlas password users authenticate against
   `admin`; retain the appropriate authentication source if changing the default database.
5. In the agent directory's ignored local environment file, add the completed value as
   `MOVIES_MONGODB_URI`, using [env.example](../../agents/movie-scout/env.example) only as
   a variable-name reference. Preserve existing platform/provider values. Do not put
   the real value in the example, chat, a command argument, a screenshot or a tracked file.
   No MCP credentials, cloud secret upload or platform database replacement are needed.
6. Return only a nonsecret readiness confirmation: dataset present; dedicated identity
   has only collection `find`; secret saved locally; approved network path ready. Any
   connection test must be bounded and read-only, suppress raw exception details, and
   never attempt a write to test authorization. Native runtime proof remains pending.

Sources: [Atlas database users](https://www.mongodb.com/docs/atlas/security-add-mongodb-users/),
[custom roles](https://www.mongodb.com/docs/atlas/security-add-mongodb-roles/),
[IP access lists](https://www.mongodb.com/docs/atlas/security/ip-access-list/),
[Agent Engine local environment](https://www.mongodb.com/docs/agentengine/build/run-local/).

### Deployment/non-development credential readiness (T049; not local resume)

- Use an existing Atlas cluster containing `sample_mflix.movies`; confirm availability
   with your authorized database administrator. Do not substitute the local platform store.
- Have the administrator supply a separate identity whose reviewed role grants only the
   required `find` privilege on that collection. Do not use platform-wide read/write credentials
   and do not attempt writes to test permissions. Creating users/roles/resources requires
   separate authorization; no such changes were made by this implementation session.
- Privately set MOVIES_MONGODB_URI in the agent's ignored local environment, keeping the
   existing platform URI intact. Never send the value through chat or commit it. No cloud
   secret upload is needed for local setup, and none was performed.
- Verify the local development network and eventual native sandbox egress can reach the
   selected cluster using documented controls without global access or changing cluster links.
   Record only redacted role/data/network confirmation, not credentials, hostnames or URI.
- Complete T049 after readiness is confirmed. Native sandbox version/import checks and
   end-to-end movie reads remain later validation tasks, not claims earned by configuration.

Run after executable tasks implement [the plan](plan.md). Contracts and field rules are
in [movie-tools.md](contracts/movie-tools.md) and [data-model.md](data-model.md).

## Offline foundation expectations — T006 (before implementation)

These supplemental stdlib checks use isolated fakes, never catalog fixtures or native
acceptance evidence. All V01–V22 native scenarios remain NOT RUN. T005 gates T013/T014.

- T007: old messages-only checkpoints remain readable; missing criteria/route/permissions
   default to empty/uncertain/none; all added state values are JSON serializable.
- T008: importing/registering tools creates no movie client or connection. Concurrent
   first calls reuse one client, only the dedicated variable is read, missing configuration
   fails safely, a child resets client AND inherited lock, shutdown close is best effort.
- T009 / V07/V14/V22: reject unknown/operator keys, nulls, booleans-as-numbers,
   strings/arrays/nonfinite ratings, invalid ranges/enums/counts before client access.
   Default five, positive requests capped at ten, strict JSON envelopes; invalid and
   unavailable never mean empty success. Keep full cursor consumption and close inside
   CSOT 10s; set server max_time_ms 5000, sort and positive server limit <=10. Failures
   at find/configuration/iteration/normalization/close discard every partial movie and
   expose only stable codes/guidance, never exception text. Full story predicates,
   normalization and registered movie tool are later tasks, not foundation acceptance.
- T010–T012 / V17–V21: fixed-schema wrapped router exposes no tools and accepts only
   one exact route object; malformed/failed/tool-calling responses fail closed. Recompute
   on each user turn. Movie/mixed: movie/date only; nonmovie_memory: profile/date only;
   other: date only; uncertain: no tools, clarify. Previous profile output must not enter
   movie/router prompts or supply movie criteria. Mixed turns defer all profile operations.
   Independently guard before ToolNode/wrapper execution, preserving every denied call ID,
   including mixed multi-call batches, with no denied wrapper side effects. Keep native
   app.llm/get_tools/checkpointer paths and unchanged automatic extraction.

## Offline foundation results — 2026-10-20 (T006–T012)

**PASS (host-only)**: 20 stdlib `unittest` methods, including parameterized negative
matrices, in [test_foundation.py](../../agents/movie-scout/tests/test_foundation.py) and
[test_routing.py](../../agents/movie-scout/tests/test_routing.py). All assertions use
constructed values/fakes, not catalog fixtures. Graph tests compile the actual LangGraph
with fake App/LLM and instrumented ToolNode inputs; they prove application-side dispatch,
not native OE/replay, model interpretation, provider or sandbox execution.

Verified: no client at import/registration; threaded reuse, dedicated-variable-only access,
missing configuration, PID/fork reset and best-effort close; strict invalid-before-client
checks, defaults/cap/JSON safety; fixed source/projection/server limit/5000ms budget;
consumption inside real installed CSOT plus instrumented full-scope cleanup; failures in
find/options/iteration/normalization/close discard partial results and sanitize codes.
Graph checks cover exact route parsing, duplicate/unknown/malformed labels and router
failures, all route schema sets, allowed date/nonmovie-memory calls, blocked movie calls
on memory routes, forged persisted permissions, uncertain forced calls, per-turn reset,
and exclusion of prior profile output/assistant summaries. Multi-call batches containing
any denied call are rejected atomically with every original call ID and zero wrapper
effects; an allowed-only retry can proceed. This is deliberately stricter than selectively
dispatching siblings and avoids orphan tool IDs or rewriting historical AI messages.

T007 optional state fields preserve messages-only checkpoints; fresh route defaults deny
all tools. Router sees only same-session human messages, never assistant/profile output.
Responder sees those human turns plus current-turn tool round trips, not historical
assistant summaries. Actual natural-language classification remains a native model risk
for T014/V17–V21. Native state/checkpoint replay compatibility is NOT RUN.

**Tooling PASS**: locked host `uv sync --locked` (no upgrade), `uv lock --check` (125
resolved packages), Ruff 0.17.0 on source/tests, Pyright 1.1.414 on source with explicit
local-venv interpreter (0 errors/warnings), and Python byte-compilation of source/tests.
Host CPython 3.13.13; SDK/runner 0.11.9, PyMongo 4.18.3, LangGraph 1.2.14,
langchain-core 1.6.10. Existing editor-wide Pylance still reports its baseline SDK
`reportMissingImports` and test-package resolution warnings; explicit-interpreter CLI
Pyright passes. No source suppressions or provider changes were used to hide warnings.

Corrected during checks: postponed annotations made runtime TypedDict optional-key
metadata empty; immediate annotations now preserve `NotRequired`. Fixed one inferred
message-list return type; corrected a supplemental test's schema representation to the
observed SDK StructuredTool representation. Final suite has no failing tests.

Protected project/agent/dev configuration and provider-builder hashes match the T002
baseline exactly. Existing date/profile bodies, native feature flags and extraction are
unchanged. Ignore files already cover this Python-only setup; no new ignore file needed.
Private environment/example values were not inspected; no movie/database/provider call,
native CLI/start/stop/restart, provisioning, upload, deployment or running-stack change
was performed. No stack was started for validation; pre-existing sessions are left alone.

**Historical STOP before T013 (superseded by v3.0.0 DEV exception)**: Old T005 required independent find-only role/network/private
secret readiness verification. No movie tool is registered yet (T018/T019), full genre
vocabulary/predicates/normalization remain story tasks, and T032/T034 own criteria merging.
All native V01–V22 remain **NOT RUN**. No native acceptance or full foundation checkpoint
is claimed. Revised DEV T005 now passes; T014 still precedes story implementation.

## Prerequisites and safety

1. Existing CLI-generated Movie Scout project; official CLI authenticated, Docker Desktop
   running, Python >=3.11. Do not regenerate it. Use the existing dependency tooling to
   resolve the direct PyMongo 4.x constraint with SDK constraints; record actual native
   Python, SDK, runner, driver and CLI versions, checking official compatibility for those
   exact versions. Host Python/CLI or successful startup alone is not runtime verification.
2. Existing Atlas `sample_mflix.movies`; local development may use the approved v3.0.0
   broad shared identity with the guardrails above. A separate verified collection-find-only
   identity is mandatory for T049 before deployment/non-development acceptance. Review roles without logging credentials; never
   attempt a write to prove read-only access. Do not provision/load/modify a dataset merely
   to manufacture validation fixtures. Local platform MongoDB is not the movie source.
3. Configure `MOVIES_MONGODB_URI` privately through the documented local environment;
   never paste it into chat, tracked files, commands, screenshots or traces. Preserve the
   platform `MONGODB_URI`. Confirm movie tool reads only its dedicated secret with no fallback.
   For a later approved deployment, `agentengine secret set MOVIES_MONGODB_URI --workspace-scope`
   prompts securely; deployment/secret upload is not required or authorized by this planning run.
4. Verify existing provider/model access and native memory provider requirements. Keep
   `features.memory` and project extraction settings unchanged. Narrow wildcard secret
   declarations to required names without breaking those native features; sandbox secrets
   remain shared and platform URI may remain automatically available.
5. Verify actual movie Atlas network access with documented egress/access controls.
   A linked cluster is in base egress; another cluster requires explicit reachability.
   Do not change platform cluster links or open global access merely to run a test.

Official references: [local development](https://www.mongodb.com/docs/agentengine/build/run-local/),
[testing](https://www.mongodb.com/docs/agentengine/deploy/test/),
[secrets](https://www.mongodb.com/docs/agentengine/deploy/provision-secrets/),
[cluster egress](https://www.mongodb.com/docs/agentengine/network-egress/atlas-cluster-link/),
[monitoring](https://www.mongodb.com/docs/agentengine/manage/monitor/).

## Start and observe (run from repository root)

```bash
cd agents/movie-scout
agentengine --version
agentengine agent validate
agentengine dev up
```

Use the Playground URL printed by startup (configured default port 3000), not an assumed
URL if the CLI reports another port. Submit the cases below through the native interface
and inspect native traces/tool input-output. Inspect runtime package metadata through the
native development environment without printing environment variables or connection strings.
Do not use a host-only driver import as proof of tool-sandbox compatibility.

```bash
agentengine dev logs
```

Logs/traces must contain no raw driver exception strings, secrets or internal hostnames.
If they do, redact evidence and fix disclosure before acceptance; do not copy them into chat.
Supplemental existing Ruff/Pyright or standard-library validation may run during tasks,
but native checks remain mandatory. No external testing/tracing service is needed.

## Select read-only evidence fixtures

Use bounded native movie retrieval and inspect returned projected facts/source IDs.
Select actual full title, fragment, literal punctuation, duplicate-title distinct IDs,
year/rating endpoints and genre combinations present in the catalog. Expected IDs/facts
must be checked against retrieved records, not LLM recollection. An example like Batman is
not evidence that a fixture exists. For missing/nonnumeric/unrated cases, select existing
records if available. No fixture writes. If a necessary edge fixture is absent, record
NOT RUN/fixture unavailable and use clearly labeled supplemental isolated validation checks;
do not claim native coverage or full acceptance until required coverage is satisfied.

## US1 test-first expectations — T015

Before implementation, select bounded existing records through the native registered tool:
start with literal `Batman` (candidate, not assumed present), then use a returned complete
title and mixed-case fragment for V01. For V02 use `(` and `.*` as literal fragments;
only assert positive punctuation coverage if an actual matching record is returned.
Use `__movie_scout_missing_8fd774b6__` for a candidate no-match V03; verify empty rather
than assume absence. Direct blank title must be invalid before client access.
For V04 try a bounded `Hamlet` title request for distinct same-title IDs; inspect returned
optional fields for existing missing metadata. Absent duplicate/missing-field/punctuation
fixtures stay NOT RUN, never manufactured. No unbounded fixture scan or catalog writes.

V10: direct counts omitted/1/10/100 yield effective 5/1/10/10, capped notice only for100;
zero/negative/fractional/bool counts are invalid before client use. V14: isolated direct
missing-secret/iteration-failure checks first, then a native tool invocation under a safe
local control if possible without disrupting existing sessions. Otherwise native V14 is
NOT RUN and T020 remains incomplete. V17/V18/V20: movie/mixed requests expose only movie/
date schemas and never invoke profile tools; punctuation/injected text stays inert.
V22: confirm native remote search_movies registration, source projection, bounded output,
CSOT cleanup and native versions. Compare native tool results' source IDs and every
displayed fact to independently projected fixed-source reads under the same bounds;
model answers must contain only retrieved facts. Supplemental fake-record normalization
tests are explicitly NOT catalog fixtures and do not earn native acceptance.

## Scenario matrix

| ID | Native request/check | Required outcome |
|----|----------------------|------------------|
| V01 US1 | Existing full title, shared fragment, mixed case | Matching retrieved distinct IDs; facts equal source; <=effective limit |
| V02 US1 | Existing punctuation-containing fragment; regex-like title text | Literal case-insensitive containment, never executable query syntax/fuzzy matching |
| V03 US1 | Confirmed nonexistent title; blank title/blank user input | Honest empty result versus clarification, no unrestricted blank-title query |
| V04 US1 | Existing missing metadata and same-title/different-ID records | Missing labeled unavailable, zero not substituted, identities distinct/no duplicates |
| V05 US2 | Science fiction after 2010 and IMDb above 7 | `Sci-Fi`, strict year/rating, all criteria satisfied |
| V06 US2 | Title + genre AND/OR + exact/inclusive year range + at-least rating | All active predicates correct; exact endpoints included, alternatives honored |
| V07 US2 | Reversed/equal-strict conflicting ranges, years outside 1–9999, ratings outside 0–10, strings/bools/arrays/nonfinite numerics | Correction/invalid result, no database call for invalid structured input |
| V08 US2 | Unknown genre, ambiguous date, unsupported operator-shaped input | Concise clarification/rejection, no invented alias or raw MQL passthrough |
| V09 US3 | Three highly rated comedies from 2000s with >=3 verified matches | Exactly 3, numeric ratings descending, 2000–2009, fact-grounded fit explanation |
| V10 US3 | No count, count 1/10/100; zero/negative/fractional count | Default 5; honor 1/10; cap100 at10 with notice; invalid others rejected |
| V11 US3 | Fewer eligible matches; two rated plus unrated; all-unrated matches | Explained shortfall; rated-only high-rating output; no unrated fill; honest no eligible rated matches |
| V12 US3 | Ordinary discovery with unrated records and no rating criterion/order | Otherwise matching unrated eligible, rating unavailable; no hidden rating threshold |
| V13 US3 | Valid combined criteria with no matches | Successful empty, suggest adjustment without silent relaxation |
| V14 Failure | Temporarily unavailable movie connection using safe local control below | `unavailable`, retry guidance, no partial/remembered movie fallback, no empty-success claim or secret leakage |
| V15 US4 | Same-session action request, then “only after 2015”, then replace year | Preserve action, strict boundary, replace only year; recorded active criteria agree |
| V16 US4 | New conversation or unavailable context, incomplete follow-up | Ask missing criteria; no invented cross-session preference memory |
| V17 Memory | Movie request when native profile already has preferences | No explicit save/recall calls; use current-conversation criteria only; no zero-retention claim |
| V18 Memory | “Remember my location and recommend three comedies” plus reordered/adversarial mixed wording | Complete movie portion where possible; zero explicit profile saves/lookups; request memory separately; both schemas and dispatch enforce |
| V19 Regression | Separate standalone nonmovie save/recall after mixed turn; then new movie turn | Compatible memory operations work separately; route resets; movie turn has no profile operations/profile-derived criteria |
| V20 Security | Write/credential requests, instructions in title/retrieved plot, attempted disallowed multi-tool calls | Decline/ignore as data, no mutation or secret disclosure, dispatch blocks before side effects |
| V21 Regression | Existing date lookup and unchanged native memory/extraction settings | Date remains functional; memory/extraction not disabled or rewritten |
| V22 Runtime | Inspect sandbox trace, result bounds, role metadata, resolved versions | Native wrapper/tool sandbox path works, fixed source/find only, <=10 projected results, compatible versions recorded |

V07 includes direct structured-tool validation inside supported local tooling, since the
conversational model may correct an invalid value before generating any tool call. Native
trace validation must distinguish model clarification from actual argument rejection.

## Safe local failure control

Only in a disposable local development session, privately unset the dedicated movie secret
or supply a deliberately nonsecret invalid local value; restart using the native workflow
and submit a movie request. Never modify platform URI, Atlas users/roles, production secrets,
dataset records or shared network policies. Restore the original private configuration and
restart afterward. Confirm `NOT_CONFIGURED`/safe unavailable handling, then verify a successful
read. Dependency/timeout/authorization branches may need supplemental isolated checks when
they cannot be reproduced safely; label those checks separately, never invent live results.

## Evidence and exit criteria

For each case record ID, timestamp, native session/trace reference, redacted input, effective
criteria, returned source IDs and projected supporting facts, safe outcome, expected/actual
result and PASS/FAIL/NOT RUN. Record both model-visible schemas and actual tool dispatch for
memory cases. No URI, environment dump, internal error/host or secret may enter evidence.
A local versioned evidence artifact can be added during implementation; no fake evidence is
created here. Catalog/source metadata is evidence, not a new persistent application store.

Local validation requires all applicable mandatory native scenarios, compatible resolved
versions, disclosed broad-role risk, source-grounded results, unchanged extraction and
regressions to pass. Deployment/non-development acceptance additionally requires T049
verified separate find-only identity; local success never satisfies that gate.
Supplemental checks do not replace native end-to-end proof. Fix failures before claiming
completion; fixture/provider/network gaps remain explicit NOT RUN, not new B1 documentation
blocks. Builds/deployment follow official workflows only when separately requested.

Stop the local environment when finished:

```bash
agentengine dev stop
```