# T043 public isolation review scaffold

**NOT STARTUP-APPROVED.** These are configuration inputs, not executable fixture coverage.
There is deliberately no project configuration, application source, dependency manifest,
dotenv, generated Compose, private credential or startup script in this directory.
Do not run local startup here: CLI parent discovery could select the production project.

## Supported configuration

- [dev.yaml](dev.yaml) pins only Playground to 3301 and explicitly selects local MongoDB.
  All other host ports remain dynamically assigned. Port 3301 was bindable during the
  2026-10-21 review; availability must be checked again immediately before any later start.
- [agent.yaml](agent.yaml) uses a fresh test-only slug, native durable execution, memory
  disabled, explicit LLM secret names and no movie/profile credentials or profile tools.
  This declares a candidate boundary, not an assertion that fixtures are implemented.
- Official [local settings](https://www.mongodb.com/docs/agentengine/build/run-local/)
  document both settings and memory gating. The production agent remains unchanged.

## Actual resource evidence and remaining gate

The already existing temporary project outside this repository is NOT this scaffold.
On 2026-10-21 it unexpectedly already had generated Compose, four active containers,
three volumes, Playground 33043 and nonempty private credential assignments. None were
created, stopped, copied, changed or used for model requests by this review. Its public
project configuration fails YAML parsing at line 54. Earlier claims of no Compose,
zero resources and zero nonempty assignments are historical and no longer current.

The installed CLI is an arm64 Mach-O Go binary. Embedded module identifiers name
github.com/10gen/agentic-platform/client-libraries/agentengine-cli; unauthenticated
GitHub repository lookup returns 404 (not proof that the repository does not exist).
Binary symbol names alone do not establish credential propagation or startup ordering.

The sanitized generated Compose audit establishes a unique top-level project name,
project-scoped non-external volumes, local MongoDB and internal OE/AER/tool routing.
It also reveals OE dotenv consumption and generated sandbox environment files. Their
effective secret injection, sandbox config and source/fixture provenance remain unreviewed;
resource naming alone is not complete isolation proof. No raw generated config is copied.

Before native tests: establish exclusive ownership/no concurrent modification of a fresh
officially generated temporary project; parse its public project config; review all
resource paths and generated sandbox/env consumers with no operational Atlas URI; verify
runtime-only LLM delivery without persisting secrets; implement labeled synthetic native
fixtures using the production graph/prompt; then run real OE/model cases and audit traces.
Do not amend or clean up the pre-existing temporary stack as an inferred permission.

T043 remains open; T044–T048 remain sequentially gated; T049 remains independently open.
No new permissions check or repeated fixture authorization is required by this scaffold.