# Implementation Plan: Busca semântica de filmes pelo enredo

## Migration amendment — Voyage 4, 2026-10-27

The active implementation now uses `voyage-4-large` with query input, 2048
dimensions, float output and `truncation=False`. The active MongoDB vector
field is `plot_embedding_voyage_4_large`; Voyage 3 references remain historical
dataset evidence only. A maintainer must manually seed the new field and create
and validate its vector index before native acceptance. T027 remains open.

## T027 — nova sessao D01 bloqueada, 2026-10-27

O preflight nativo autorizado usou uma sessao nova e o prompt D01 congelado.
Houve HTTP 200, uma unica chamada `search_semantic_movies`, zero chamadas de
perfil e envelope `sample_mflix.embedded_movies` com
`unavailable/semantic_unavailable`, `returned_count=0` e `shortfall=0`.
Nenhum `stage/code` foi exposto. Como nao houve `ok`/`empty`, nao seguir para
D02-D10, filtros, T028 ou T029; T027 e G4-B continuam abertos, sem retry ou
lifecycle adicional.

## T027 — diagnostic attempt blocked before semantic invocation, 2026-10-27

A única tentativa autorizada com o D01 congelado terminou na atribuição da
sessão-base do helper nativo existente, com HTTP 404
(`NATIVE_ATTRIBUTION_NOT_FOUND`). Não houve `search_semantic_movies`, perfil,
provider, banco ou retry; `stage/code` não foi exposto. Readiness/provider/
database permanecem `UNKNOWN`, sem causa interna inferida. T027 continua `[ ]`
e não libera T028/T029.

## T027 — post-up native preflight revalidation, 2026-10-27

O único `agentengine dev up --no-artifact-auth` autorizado foi executado a partir de `agents/movie-scout` e concluiu com os serviços locais saudáveis. Uma única sessão nova D01 posterior respondeu HTTP 200; a trace sanitizada registrou uma chamada `search_semantic_movies`, nenhuma chamada de perfil e o envelope `sample_mflix.embedded_movies` como `unavailable/semantic_unavailable`, com zero resultados e shortfall zero. A observação não reteve stream bruto, plots, vetores, segredos ou erros.

T027 não atende os critérios de G4-B: busca, filtros, grounding, segurança funcional, conectividade/modelo e tempos permanecem sem prova. Não iniciar T028/T029, não repetir a chamada e não executar lifecycle adicional; T017 permanece congelada e T027 continua desmarcada.

**Branch**: `master` | **Date**: 2026-10-23 | **Spec**: [spec.md](spec.md)

**Input**: [spec.md](spec.md), constituição v4.0.0 e implementação tradicional existente.

**Checkpoint atual T026 concluída / T027 BLOQUEADA,2026-10-27**:26/55 concluídas,29 pendentes. A nova autorização exata foi consumida por UMA execução correta de `agentengine dev up --no-artifact-auth` dentro de `agents/movie-scout`; os artefatos foram regenerados/aplicados e a stack local terminou saudável. Manifesto público, tool list e versões nativas esperadas foram confirmados sem valores privados. O único preflight D01 chamou `search_semantic_movies` uma vez, sem perfil, e retornou fail-closed `unavailable/semantic_unavailable`, zero resultados. Sem retry, D02, filtros, T028/T029 ou outro lifecycle. T027 e G4-B7 permanecem abertos; campanhas D/H/F não foram iniciadas como avaliação e o canônico T017 está intacto.

**Status**: T017 concluída por pré-registro congelado v1.0,2026-10-26; [tasks.md](tasks.md):17/55 concluídas,38 pendentes. [Leitura atual e revisão prospectiva](quickstart.md#t017--successful-bounded-read-and-prospective-freeze-2026-10-26), após relato de cluster não inicializado: UMA tentativa READ_OK,10 registros utilizáveis/1746ms/find1/getMore0/maxTimeMS3557/cleanup true. Cinco plots locais sustentam dez prompts5PT/5EN; H20/rubrica/F10/campos/concorrência/cold-warm/regras anti-pós-hoc congelados antes de medir, versão/UTC/hash efetivos registrados. Avaliador automatizado identificado, sem humano ou aprovação inventados. Causa histórica dos timeouts não comprovada. STOP antes T018. Sem alteração de produção/testes/dependências/manifestos/privados/stack ou operações do cluster; G1/G2 históricos não reauditados, D/H/F e sete G4-B NOT RUN. Find não é aceitação semântica/binding/modelo/egress/cloud. Aprovação anterior preservada sem novo loop; registros anteriores permanecem históricos.

## Decisão local aprovada — 2026-10-23

- **Aprovação**: resposta literal **“sim, aprovo”** à proposta de simplificação para LOCAL TEST DEVELOPMENT. Substituir garantia rígida global30s por meta medida; manter timeouts explícitos, limites, zero retries aplicativos e nenhuma promessa de cancelamento global de trabalho no servidor. Não solicitar novamente a mesma aprovação.
- **Seleção documentada**: cliente oficial `voyageai==0.5.0`, `voyage-3-large`, `input_type=query`, `output_dimension=2048`, `output_dtype=float`, `truncation=False`, preservando os valores EXISTENTES de `VOYAGE_API_KEY`/`VOYAGE_URL` por binding explícito `api_key`/`base_url` no TOOL necessário. Sem fallback automático, novas credenciais ou alteração da memória. Referências e limites em [research.md](research.md#approved-local-simplification--2026-10-23).
- **Constituição**: nenhuma emenda necessária nem aplicada. Princípios I/V/VI/VII e Technology Approval and Scope continuam exigindo compatibilidade oficial documentada antes do código e prova nativa antes do aceite. A constituição não exige garantia global30s; sua retirada é revisão aprovada de SC-005/contrato, não dispensa de segurança ou de tecnologia verificada.
- **Separação de evidências**: G1/G2 continuam fechados apenas no escopo local registrado. G3 é seleção/compatibilidade documental aprovada; G4-A é viabilidade documental API/build/secrets/egress, não PASS operacional. Resolução de dependências, entrega/segregação efetiva dos secrets, endpoint-binding, egress, conectividade e funcionamento serão verificados DURANTE implementação e obrigatoriamente ANTES da aceitação pela [checklist única G4-B](quickstart.md#5-local-acceptance-checklist-g4-b). Nenhum resultado nativo foi fabricado.
- **Handoff**: não há gate documental aberto de deadline nem nova rodada de aprovação desta decisão. Um fluxo separado de implementação pode conferir T001–T011 e iniciar testes-first; esta revisão NÃO o executa. Restart/start/stop/build/deploy continuam sujeitos a autorização operacional separada. Sem nova infraestrutura, mutações ou prontidão cloud.

## Summary

Adicionar busca temática PT/EN ao único Movie Scout por ferramenta nativa e PyMongo oficial, somente em `sample_mflix.embedded_movies`. Preservar integralmente busca tradicional em `sample_mflix.movies`. Pipeline fixo, filtros obrigatórios e contexto semântico independente; sem fallback, join, escrita ou nova infraestrutura. Entrega textual; imagens não habilitadas sem prova oficial/nativa.

A autorização da fonte está resolvida por constituição v4.0.0 e resposta “A”; não reabrir essa aprovação nem B1. G1 concluído por metadados nativos; G2 concluído por inventário limitado e atestado do mantenedor sobre adequação manual/Ready/Queryable. G3 selecionado documentalmente pela decisão acima; comprovações operacionais são pendências obrigatórias de G4-B, não bloqueios circulares pré-código. Evidências G1/G2 e seus limites em [research.md](research.md#evidence-update--2026-10-23-authoritative-current-checkpoint). Nenhuma implementação executada/autorizada nesta invocação documental.

## Technical Context

**Language/Version**: Python >=3.11 declarado no projeto; caminho semântico selecionado dentro de >=3.11,<3.15, interseção documental Agent Engine/voyageai0.5.0. Versão efetivamente resolvida no sandbox ainda não verificada; não alegar suporte do cliente a Python>=3.15 nem mudar configuração nesta revisão.

**Primary Dependencies**: preservar `agent-engine-runner-shared[mongodb]>=0.11.3,<1`, `agent-engine-sdk-langgraph>=0.11.3,<1`, LangChain/LangGraph nativos e `pymongo>=4.11,<5`. Selecionar cliente oficial `voyageai==0.5.0` (Python>=3.9,<3.15; API Atlas exige>=0.3.7), sem extras locais/vídeo. Query voyage-3-large/query/2048/float/truncation=False. Pin aprovado documentalmente, NÃO instalado/resolvido nesta revisão; resolução/importação conjunta no runtime e binding/egress existentes são itens obrigatórios de G4-B, sem leitura/solicitação de secrets agora.

**Storage**: MongoDB Atlas `sample_mflix.movies` (traditional read-only access);
`sample_mflix.embedded_movies` only for specified semantic access under constitution 4.0.0;
estado/checkpointer e memória automáticos nativos existentes, sem nova persistência nem reconfiguração da extração.

**Testing**: regressão local determinística e futura validação semântica obrigatória no chat/ferramentas/traces nativos. Procedimento em [quickstart.md](quickstart.md); nenhuma aceitação semântica executada.

**Target Platform**: MongoDB Atlas Agent Engine; official `agentengine` CLI local/build/deploy workflows

**Project Type**: Single educational conversational movie-recommendation agent

**Official References**: [guia](https://www.mongodb.com/docs/agentengine/get-started/), [contrato](https://www.mongodb.com/docs/agentengine/reference/agent-contract.md), [SDK](https://www.mongodb.com/docs/agentengine/sdk/python/packages/agent-engine-sdk-langgraph/docs/api/), [local](https://www.mongodb.com/docs/agentengine/build/run-local.md), [secrets](https://www.mongodb.com/docs/agentengine/deploy/provision-secrets.md), [egress](https://www.mongodb.com/docs/agentengine/network-egress.md), [build](https://www.mongodb.com/docs/agentengine/deploy/agent-image.md), [PyMongo](https://pymongo.readthedocs.io/en/4.18.3/api/pymongo/collection.html), [Vector Search](https://www.mongodb.com/docs/vector-search/query/aggregation-stages/vector-search-stage/). Registro detalhado em [research.md](research.md).

**Performance Goals**: >=8/10 descrições com relevante no top5; medir >=19/20 respostas saudáveis em até20s, da submissão à resposta final. Falha: meta operacional de explicação em até30s, NÃO garantia rígida/global nem cancelamento servidor. Orçamentos propostos ferramenta<=12s, provedor<=6s e MongoDB<=5s com timeouts explícitos segundo comportamento suportado; nenhum retry aplicativo. Aplicar orçamento local restante quando suportado, sem alegar propagação global pelo OE/modelos. Medir tempos, overrun, cleanup e efeitos dos timeouts em G4-B NOT RUN; desvio não pode ser ocultado ou convertido em PASS.

**Constraints**: Preserve CLI-generated configuration; no custom servers/frontends/APIs,
external orchestration, alternative deployment platforms, or unverified dependencies

Descrição<=2000 caracteres Unicode sem truncamento silencioso; padrão5/máximo10 resultados; <=10 gêneros. URI de filmes somente MOVIES_MONGODB_URI, sem fallback operacional. Nenhum namespace, índice, modelo ou pipeline arbitrário. Sem build/restart/deploy nesta sessão.

**Scale/Scope**: descoberta temática, filtros existentes e refinamento/reset da mesma sessão; sem híbrida, paginação, similaridade por filme ou novas dimensões.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Use `.specify/memory/constitution.md` as the authority. Record PASS/FAIL and evidence
for each gate; unresolved technology support is a FAIL, not implicit approval.

- **I — Platform exclusivity**: Official documentation establishes support for every
  technology choice and the Python runtime; use only Agent Engine development, execution,
  orchestration, and deployment. Preserve CLI-generated configuration structure.
  Constitution v2.0.0 permits official PyMongo inside native read-only movie tools using
  official driver compatibility/API evidence plus Agent Engine tool/build/secret/egress evidence;
  require resolved-version and native runtime verification before acceptance.
- **II — Source of truth**: Preserve traditional access to Atlas `sample_mflix.movies`;
  constitution 4.0.0 also permits semantic-only reads of `sample_mflix.embedded_movies`
  in the same cluster. Fixed namespaces, no silent substitution, writes or other databases.
  Verify index/schema, embedding compatibility and genre/year/IMDb filter mapping before
  semantic implementation approval; document any external manual index prerequisite.
- **III — Minimal architecture**: One conversational agent using supported behavior/tool
  interfaces; no custom APIs, servers, frontends, external orchestrators, or extra infrastructure.
- **IV — Grounding**: Tie recommendations to retrieved records; use preferences when provided,
  distinguish facts from opinions, and handle missing metadata and empty results explicitly.
- **V — Security**: Use documented secret mechanisms, exclude credentials from source control,
  and enforce read-only movie operations separately from platform permissions. Constitution
  v3.0.0 permits only the explicitly approved temporary broad shared identity in LOCAL
  development with separate URI roles/no fallback/allowlisted bounded reads. Disclose its
  write grants; require a separate effective-grant-verified collection-find-only identity
  before deployment/non-development acceptance. Local code guards are not least privilege.
  The historical exception does not cover semantic access: verify effective `find`-only
  grants for the required exact collections first. T049 covers movies only; do not reopen
  it or infer new-source privileges. No automated index/role/network/catalog mutation.
- **VI — Validation**: Plan platform-supported local tests for success, empty results,
  invalid requests, missing metadata, and tool failures; use native debugging/monitoring.
  Semantic features require filter correctness, separate session context/reset, profile
  isolation and existing-feature regression. Images require official native support plus
  a runtime demonstration; otherwise keep text without added UI/proxy/enrichment.
- **VII — Spec-driven delivery**: Approved specification precedes implementation; tasks
  trace to requirements, cite official technology references, and prefer native capabilities.

Any scope deviation requires an approved constitution amendment before implementation;
the Complexity Tracking section cannot authorize an exception.

### Resultado efetivo após pesquisa e desenho revisados

| Princípio | Antes | Após | Evidência / pendência |
|---|---|---|---|
| I | Compatibilidade documental | Compatibilidade documental aprovada | Interfaces nativas/PyMongo/cliente Voyage e build documentados; pin selecionado e faixa Python delimitada. Resolução/import/runtime reais NOT RUN em G4-B. |
| II | G1/G2 no escopo registrado | Conforme desenho | Proveniência plot/voyage-3-large/2048 e query documentadas; amostra/atestado não provam consulta real. G4-B exige prova nativa. |
| III | PASS | PASS | Mesmo agente e ferramentas; nenhuma infraestrutura nova. |
| IV | PASS de desenho | PASS de desenho | ID/título/plot utilizáveis obrigatórios na apresentação semântica; shortfall sem reposição/fabricação; prova real G4-B ainda devida. |
| V | G1 PASS local | Conforme desenho, operação pendente | Find-only nas duas coleções/URI separada; mecanismo oficial de secrets/egress documentado, aplicação efetiva NOT RUN em G4-B. T049 histórico só movies. |
| VI | Plano de validação | Conforme desenho, aceitação pendente | SC-005 revisado por aprovação explícita; checklist local nativa obrigatória NOT RUN, sem cancelamento global prometido. Imagens desabilitadas. |
| VII | PASS documental | PASS documental | Spec/plano revisados pela decisão “sim, aprovo”;55 tarefas preservadas. Handoff separado, não execução agora. |

**Revisão constitucional documental conforme, não “todos os gates PASS”.** Phase 0/1 têm decisões documentadas para o escopo local revisado; não existe aceitação nativa nem prova de instalação/segregação/egress efetivos. G4-B permanece NOT RUN e bloqueia aceite. Evidência nova incompatível com documentação ou grants invalida o item dependente, sem contorno; a exceção ampla histórica não se aplica ao acesso semântico.

### I1 — Liberação pré-código versus aceitação pós-implementação

- **G1/G2: PASS no escopo local documentado; G3: caminho documentado selecionado/aprovado; G4-A: viabilidade documental do caminho revisado**. O antigo bloqueio por hard deadline foi retirado pela aprovação explícita de 2026-10-23, não resolvido por uma API inexistente. Políticas checam antes da chamada e não interrompem in-flight; timeout cliente não cancela servidor. Runtime/build/API/secrets/egress têm caminho oficial documentado; sua aplicação efetiva integra G4-B, não PASS pré-código fabricado.
- **Aprovação do plano revisado registrada e conferida em T010/T011**: “sim, aprovo”, escopo LOCAL TEST DEVELOPMENT descrito acima, para revisão documental e handoff. Não pedir a mesma aprovação novamente. Esta fase não implementa nem opera a stack; STOP antes de T012.
- **G4-B: NOT RUN**, checklist única obrigatória antes do aceite: coletar resolução/versões/entrega/segregação/binding/egress/conectividade durante implementação; depois executar aceitação real nativa, grounding/filtros/segurança/estado, regressão, relevância e performance. NOT RUN/FAIL bloqueia aceitação final, NÃO é pré-requisito circular de autorização de código. Testes isolados não substituem G4-B.
- Não repetir acessos/testes/operações nesta revisão documental. Inspeções G1/G2 previamente autorizadas em2026-10-23 ficam registradas, não são testes semânticos. A emenda “A”, B1 e T049 de movies não são reabertos; imagens continuam text-only.

## Project Structure

### Documentation (this feature)

```text
specs/002-semantic-movie-search/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── tasks.md             # 55 tarefas; T001–T018 concluídas (T012–T016 testes RED), T019–T055 pendentes
└── contracts/
  └── semantic-movie-tools.md # contrato local revisado, sem implementação/aceite
```

### Source Code (repository root)

```text
project-config.yaml
agents/
└── movie-scout/
    ├── agent.yaml
    ├── dev.yaml
    ├── env.example
    ├── pyproject.toml
    ├── README.md
    └── src/
        └── agent_movie_scout/
            ├── main.py
            ├── llm.py
            ├── state.py
            ├── system_message.py
            └── tools.py
```

**Structure Decision**: preservar estrutura CLI existente; nenhuma edição de fontes agora. Futuras mudanças mínimas: [state.py](../../agents/movie-scout/src/agent_movie_scout/state.py) para contexto separado, [main.py](../../agents/movie-scout/src/agent_movie_scout/main.py) para intenção/allowlists/commit real, [tools.py](../../agents/movie-scout/src/agent_movie_scout/tools.py) para ferramenta auditada e pipeline fixo, [system_message.py](../../agents/movie-scout/src/agent_movie_scout/system_message.py) para grounding e isolamento. Acrescentar testes em [tests](../../agents/movie-scout/tests), sem substituir regressões. Preservar cliente/cache/cleanup existentes, contratos, regex, ranking e critérios tradicionais. Pin de embedding selecionado acima; declaração/resolução somente no fluxo separado de implementação.

## Phase 0 — Research and prerequisites

O checkpoint anterior2026-10-23 registrou pesquisa de duas frentes e o bloqueio então vigente, preservados como histórico em [research.md](research.md). A decisão aprovada nesta revisão resolve a seleção documental e retira o requisito não suportado de garantia global; não transforma lacunas operacionais em sucesso. Inspeção anterior G2 somente após G1 e autorização, sem grants adicionais; FR-017 fundamentou ajuste manual externo, nenhum índice alterado pelo assistente. G4-B continua validação obrigatória durante/após implementação, não pesquisa circular pré-código. Nenhum subagente ou teste nativo novo nesta revisão.

## Phase 1 — Revised local design

1. Determinar intenção no contexto corrente sem perfil persistente. Título explícito permanece tradicional; ambiguidade pede esclarecimento.
2. Propor contexto semântico independente. Preservar tema/dimensões não alteradas; mudança de ano/nota substitui ambos os extremos e flags antigos. Reset limpa diretamente, sem consulta.
3. Exigir readiness previamente verificada para identidade/índice/configuração exatos. Não descobrir/gerir índices por ferramenta runtime. Não pronto é indisponível, nunca vazio.
4. Validar descrição/filtros e gerar somente embedding transitório compatível após G3, sem tradução/rewrite/truncamento silencioso.
5. Pipeline com `$vectorSearch` primeiro; filtros solicitados em `filter` somente para caminhos indexados verificados. ANN inicial `numCandidates=20*effective_limit` (100 padrão,200 máximo), não garantia de recall. Projeção positiva exclui vetores; score semântico não é IMDb nem probabilidade.
6. Excluir da apresentação SEMÂNTICA candidatos sem ID/título utilizáveis OU sem plot recuperado utilizável (ausente/null/não string/vazio/somente whitespace). Preservar ordem relativa, informar shortfall/empty, sem fabricar plot/afinidade, fallback, consulta de reposição ou aumento do limite para repor descartes. Outras ausências explícitas e tratamento tradicional de metadados permanecem inalterados.
7. Confirmar contexto somente em `ok`/`empty` reais correlacionados à chamada. Falhas preservam estado; guard de lote bloqueia perfil em cinema/misto, sem alterar extração automática.
8. Renderizar texto factual e explicação curta apoiada no plot. Correspondência fraca não vira alegação exata.

Detalhes em [data-model.md](data-model.md) e [contracts/semantic-movie-tools.md](contracts/semantic-movie-tools.md). Contexto do agente deve apontar a este plano, preservando governança externa ao bloco gerenciado.

## Phase 2 — Foundational documentary reconciliation

### T010 — actual plan and seven-principle reconciliation, 2026-10-23

Após T004–T009, conferidas as evidências e decisões existentes contra este plano, requisitos, modelo e contrato. Não houve nova auditoria DB: G1 permanece conexão nova/configuração TOOL local/find-only exato nas duas coleções, não worker longevo/cloud; G2 permanece primeiros100 + atestado manual dos três filtros/Ready/Queryable/MongoDB9.0.4, não schema exaustivo ou consulta vetorial aceita. Revisões efetivas e mecanismos exatos em [T004–T009](research.md#phase-2-execution--foundational-documentary-review-2026-10-23), [inventário T005](data-model.md#phase-2--t005-inventory-reconciliation-2026-10-23) e [mapeamento T006](contracts/semantic-movie-tools.md#t006--verified-mapping-and-documentary-operator-cross-check).

| Princípio | Resultado T010 / requisito preservado |
|---|---|
| I — exclusividade | Conforme documentalmente: agente/CLI/SDK nativos, PyMongo na exceção scoped e cliente oficial pin voyageai==0.5.0 sem extras local/video; Python semântico>=3.11,<3.15. Resolução conjunta/import/runtime ainda G4-B NOT RUN. Sem biblioteca HTTP/UI/proxy/orquestrador próprios. |
| II — fonte | Conforme desenho: movies tradicional, embedded_movies semântico no mesmo cluster; plot_vector_index/plot_embedding_voyage_3_large/2048/cosine; pré-filtros genres/year/imdb.rating. AND de igualdades/any via in/ranges estritos-inclusivos documentados; consulta real pendente. Sem AutoEmbed/fallback/join/escrita/gestão. |
| III — mínimo | PASS documental: um agente, ferramenta nativa remota TOOL com wrappers auditados, sem infraestrutura adicional. Nenhuma implementação nesta fase. |
| IV — grounding | Conforme desenho: ID/título E plot recuperados utilizáveis, excluir plot ausente/null/não string/vazio/whitespace, preservar ordem relativa/count/shortfall/empty sem refill/fabricação. Outras ausências e tradicional inalterados; prova real pendente. |
| V — segurança | G1 PASS local delimitado; configuração de filmes separada da operacional, sem fallback. Seleção de secrets por sandboxes.tool.secrets, Client api_key/base_url explícitos dos valores EXISTENTES e não vazios antes de construir para evitar defaults do SDK. Isolamento é por sandbox, não por tool; entrega/segregação e matching/egress/conectividade ainda não provados. Sem ampliar exceção histórica ou reabrir T049. |
| VI — validação | Plano conforme, NÃO aceitação: orçamentos propostos12/6/5s, timeouts suportados/zero retries aplicativos, sem garantia/cancelamento global. G4-B único LOCAL com sete itens NOT RUN continua obrigatório antes do aceite; testes-first e regressão futura. Imagens text-only até prova oficial+nativa. |
| VII — especificação | PASS documental: decisão exata “sim, aprovo”2026-10-23 preservada sem novo loop/emenda; tarefas existentes com IDs/textos/histórias/13[P] preservados. Escopo atual T004–T011, STOP antes T012; sem tarefas regeneradas. |

Configuração/implementação futura selecionada: Client.embed hospedado voyage-3-large/query/2048/float/truncation=False, uma descrição/vetor transitório; App.tool remoto timeout12 segundos e lista sandboxes.tool.tools; dependência no pyproject via tooling oficial/lock consistente; secrets EXISTENTES somente no TOOL necessário por mecanismo oficial; esquema atual de egress sandboxes.tool.network.egress/egress_mode com allow_list de destino/portas exatos já configurados, nunca adivinhados. Manifesto legado não prova compatibilidade/aplicação local. Nenhum desses arquivos/configurações foi editado; aplicação efetiva/versões/secret delivery/endpoint/modelo/rede ficam G4-B durante implementação, antes de uso/aceite afetados. Sem cloud build/upload/deploy obrigatório ou autorizado para aceite LOCAL.

T010 concluída por esta reconciliação, não por declarar todos os gates PASS: G3 seleção documental aprovada/G4-A viabilidade documental; G4-B permanece [NOT RUN](quickstart.md#5-local-acceptance-checklist-g4-b). Medir>=19/20 de20 saudáveis<=20s submissão→resposta final; falha TARGET30s, registrar overruns e comportamento de cleanup/timeouts. Incompatibilidade real/grants/índice alterados impedem uso afetado, sem contorno; pendências futuras de G4-B não são bloqueio circular de autoria de código. T011 confere o handoff abaixo antes de encerrar a fase.

### T011 — recorded decision and phased handoff verified, 2026-10-23

Conferida após T010 a decisão literal **“sim, aprovo”**,2026-10-23, registrada nesta seção de decisão local e na pesquisa: aprovação da simplificação documental LOCAL TEST DEVELOPMENT, não emenda/waiver constitucional nem aprovação operacional irrestrita. O pedido posterior de implementação em fases abriu o workflow separado; a continuação atual está limitada a T004–T011, após T001–T003. T011 concluída por essa conferência/handoff, sem pedir novamente a mesma aprovação, reabrir “A”, B1 ou T049, exigir resultado G4-B pré-código ou alegar aceitação.

**STOP CHECKPOINT ANTES DA FASE 3/T012.** T001–T011 concluídas documentalmente; T012–T055 permanecem pendentes. Próxima fase, somente em continuação separada: testes isolados T012–T016 PRIMEIRO, depois pré-registro T017 e implementação T018 em diante conforme dependências. Não escrever/executar testes, código, dependências ou manifestos agora. A aprovação histórica não é autorização para reiniciar/operar a stack; start/stop/restart/build/deploy continuam exigindo autorização operacional separada. Nenhuma leitura privada, reauditoria DB, chamada ao provedor, instalação/resolução, teste aplicativo, mutação de catálogo/índice/roles/rede ou infraestrutura nesta fase.

G4-B conserva sete caixas desmarcadas/NOT RUN, obrigatório durante/após implementação e antes do aceite LOCAL, não bloqueio circular de autoria. Divergência nova real de escopo/evidência/constituição ou operação sem autorização exige STOP no trabalho afetado. Sem desvios novos identificados nesta conferência documental; nenhuma alegação de cloud readiness ou de funcionamento nativo semântico. Evidências/limites de G1/G2 não foram ampliados.

## Complexity Tracking

> Record identified violations and their resolution. Justification alone does not
> waive any principle; correction or an approved constitution amendment is required.

| Violation | Resolution or Approved Amendment | Blocking Status |
|-----------|----------------------------------|-----------------|
| Grants semânticos antes ausentes | G1 metadados nativos exatos2026-10-23 sem write probes/role edits pelo assistente | Resolved local; invalidar diante de mudança |
| Inventário/índice antes não verificados | G2 amostra limitada e recibo manual Ready/Queryable, sem inferir uniformidade | Resolved com atestado; query acceptance futura |
| Caminho completo de embeddings | G3 cliente/modelo/parâmetros selecionados por documentação oficial e aprovação; binding/egress efetivos em G4-B | Documentado/aprovado; operação NOT RUN |
| Antiga garantia global30s sem suporte | Retirada pela aprovação “sim, aprovo”2026-10-23; meta medida SC-005, timeouts explícitos e zero retries, sem cancelamento prometido | Revisão local aprovada; nenhuma emenda constitucional necessária |
| Aceitação nativa ainda não executada | G4-B após implementação: versões resolvidas/testes/regressão/performance | NOT RUN; bloqueia aceitação final, não autorização de código |
| Fonte adicional antes proibida | Emenda v4.0.0 já aprovada; não reabrir | Resolved |

## T054 — reconciliação pós-implementação, 2026-10-28

Esta atualização reconciliou o plano com a implementação efetiva e a decisão
text-only de T049. Os sete princípios permanecem atendidos no escopo LOCAL:
agente e interfaces nativas preservados; fontes tradicional/semântica
separadas; grounding e limites sem fabricação; URI/secrets/egress declarados
sem valores privados; validação isolada e nativa registrada; e especificação,
plano e tarefas rastreáveis.

O resultado não declara todos os gates PASS: G4-B permanece aberto pelos
desvios de grounding e pelo controle `unavailable` real não provocado. Não há
garantia global de 30 s, cancelamento servidor, cloud readiness, deploy ou
grants fora do escopo comprovado. A decisão “sim, aprovo” de 2026-10-23 e a
constituição v4.0.0 permanecem inalteradas; nenhuma emenda, waiver ou novo gate
foi criado.
