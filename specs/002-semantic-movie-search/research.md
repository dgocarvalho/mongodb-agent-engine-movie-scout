# Research — semantic movie search

## T027 — evidência nativa final, 2026-10-28

O índice ativo foi confirmado como READY/QUERYABLE: `plot_vector_index` em
`sample_mflix.embedded_movies`, path `plot_embedding_voyage_4_large`, 2048
dimensões, cosine, com filtros `genres`, `year` e `imdb.rating`. Após rebuild
local saudável, D01–D10 PT/EN passaram no catálogo real com uma chamada
semântica por sessão, sem perfil, fonte e grounding confirmados e 5 resultados
por caso. AND/OR, limites estritos/inclusivos e o caso vazio também passaram;
o vazio retornou `empty`, `returned_count=0`, `shortfall=5`, sem fallback.

Durante a prova foram corrigidos o roteamento de gêneros/temas para a busca
semântica e a normalização de intervalos opcionais antes da validação. A suíte
local final passou `118 passed, 266 subtests passed`. Nenhuma escrita de
catálogo/índice/role/rede foi feita e nenhum segredo foi registrado.

## T044/T045 — text-only image decision and safeguards, 2026-10-27

The reviewed Agent Engine contract/SDK references document native tools and
artifacts but do not establish native chat rendering for a poster URL. No native
rendering demonstration is available. The feature therefore remains text-only:
the system prompt forbids image insertion, poster fetching and external record
enrichment, while semantic normalization uses a positive allowlist that excludes
`poster` and unknown fields. `test_semantic_images.py` covers these safeguards,
including a no-fetch assertion. Image support is not enabled and no image
endpoint, downloader or proxy was added.

## T046-T048 — image branch skipped, 2026-10-27

Because T044 found no documented native poster-rendering support, T046 and T047
take the text-only branch: no contract projection, tool field, prompt extension,
image renderer, URL validator, backend fetch or enrichment is enabled. T048 is
covered by `test_semantic_images.py` plus the full local regression suite; all
semantic output remains textual and the image branch cannot affect it. Native
text acceptance is still separately blocked by T027 and is not inferred from
these local tests.

## T049 — optional image scenarios recorded as text-only SKIP, 2026-10-28

No native chat renderer for poster references was established. The safe,
missing/invalid, and load-failure image scenarios are therefore explicitly
`SKIP — support not demonstrated`; no image code, URL validation, downloader,
proxy, or external enrichment was added. The text-only branch was executed by
`test_semantic_images.py` (3/3), including the no-fetch assertion. This is the
optional SC-007 path and does not close the separate G4-B limitations.

## T052 — static implementation/allowlist audit, 2026-10-28

The permitted public files were audited without reading private environment
values or performing writes/probes. `agent.yaml` keeps the explicit four
configuration names in the TOOL sandbox, the five intended native tools, and
the three previously configured egress destinations. `MOVIES_MONGODB_URI` is
used by the movie client; the platform `MONGODB_URI` is not a fallback.

The source audit confirms separate traditional and semantic route allowlists,
profile blocking on movie/mixed routes, explicit Voyage `api_key`/`base_url`
binding, `voyageai==0.5.0`, Python `>=3.11,<3.15`, zero provider retries,
provider timeout capped at six seconds, bounded MongoDB budgets, and sanitized
failure envelopes. Semantic normalization does not project `poster` or unknown
fields and performs no URL opening/fetching. `git diff --check` passed; no
credentials, URI values, raw exceptions or private hosts were added to the
audited public files. Cloud/deploy readiness remains outside this local audit.

## T027 — revalidation reaches semantic tool but MongoDB connection fails, 2026-10-28

One authorized local `agentengine dev up --no-artifact-auth` regenerated the
public artifacts successfully and reported a healthy local stack. The public
TOOL registration included `search_semantic_movies`; no private values or raw
error payloads were retained.

A fresh frozen D01 invocation with a non-secret synthetic `user_id` completed
normally. The earlier `runtime_lost` was caused by incomplete durable-memory
identity in the request, before the conversation. The allowlisted observer
passed and confirmed one `search_semantic_movies` call, zero profile calls,
source `sample_mflix.embedded_movies`, status `unavailable`, zero results and
`shortfall=0`.

The sanitized worker diagnostic now classifies the failure precisely as
`stage=database_aggregate code=network_timeout`. Provider access and the
runtime reached the MongoDB read, but semantic retrieval, grounding, filters
and timing remain unproven. T027 remains open; no retry, D02-D10, T028 or T029
was executed. Read-only diagnostics from the TOOL container resolved the
MongoDB SRV record to all three shard hosts and opened TCP `27017` successfully
to each one. Basic DNS/egress routing is therefore working. The remaining
timeout occurs after TCP reachability, during MongoDB protocol/server
selection or the bounded `$vectorSearch` operation. The next evidence must be
a sanitized driver/Atlas-side classification; no URI or credential should be
exposed.

An additional bounded native traditional read found `Batman Begins` using the
same movie connection and returned one record. This isolates URI, credentials,
Atlas access and general MongoDB routing as working. The remaining failure is
specific to the semantic aggregation/vector path (`plot_vector_index`, active
embedding field/dimension or bounded `$vectorSearch` execution); T027 remains
open until that path returns a real `ok` or `empty` outcome.

## Voyage 4 migration — 2026-10-27

Native runtime diagnostics identified the provider-stage failure: the configured
`voyage-3-large` model was rejected by the active endpoint. The implementation
therefore migrated the query embedding request to the documented
`voyage-4-large` model with the same approved 2048/query/float/no-truncation
shape. Because stored vectors are model-specific, the active MongoDB field is
`plot_embedding_voyage_4_large`; the existing Voyage 3 field and index remain
historical and are not used by the consumer. The manual seed script at
`agents/movie-scout/scripts/seed_voyage4_embeddings.py` is dry-run by default,
does not create indexes, and was not executed by the agent. T027/G4-B remain
open until the maintainer seeds the field, prepares a compatible vector index,
and obtains native evidence of provider access and semantic retrieval.

## T027 — nova sessao D01: indisponibilidade semantica, 2026-10-27

Uma sessao nova submeteu uma unica vez o D01 congelado. O endpoint respondeu
HTTP 200; a trace sanitizada mostrou exatamente uma chamada
`search_semantic_movies`, nenhuma chamada de perfil e o envelope fixo
`sample_mflix.embedded_movies` como `unavailable/semantic_unavailable`, com
zero resultados e `shortfall=0`. O runtime nao forneceu `stage/code`.

Sem `ok` ou `empty`, a matriz foi interrompida conforme T027: sem retry,
D02-D10, filtros, T028 ou T029. O resultado confirma apenas o fail-closed da
fronteira semantica nativa; readiness, provider, database e grounding ficam
sem classificacao adicional. T027/G4-B ficam abertos.

## T027 — single authorized diagnostic attempt stopped at native attribution, 2026-10-27

A única tentativa com o prompt D01 congelado usou o helper nativo existente e
parou antes da invocação semântica porque a atribuição da sessão-base retornou
HTTP 404 (`NATIVE_ATTRIBUTION_NOT_FOUND`). Nenhuma chamada de ferramenta,
perfil, provedor ou banco ocorreu; não houve retry. O runtime não expôs o novo
logger `stage/code`, portanto a classificação readiness/provider/database é
`UNKNOWN`. A evidência não permite atribuir causa a secrets, endpoint, egress,
modelo, índice ou MongoDB. T027 continua aberta e T028/T029 permanecem sem
execução.

## T027 — post-up native preflight revalidation, 2026-10-27

Depois da única execução autorizada de `agentengine dev up --no-artifact-auth` no cwd `agents/movie-scout`, foi feita uma única sessão nova D01. A resposta HTTP 200 produziu trace sanitizada com 8 eventos, uma única chamada `search_semantic_movies`, zero chamadas de perfil (`save_user_info`/`recall_user_info`) e envelope fixo `sample_mflix.embedded_movies`: `unavailable`, `semantic_unavailable`, zero resultados e shortfall zero. Nenhum conteúdo de modelo, plot, vetor, segredo ou erro bruto foi retido.

Essa evidência confirma apenas o bloqueio funcional fail-closed na fronteira nativa. Não comprova acesso ao modelo/endpoint, egress efetivo, conectividade MongoDB, consulta vetorial, filtros, grounding, relevância ou timing; nenhuma causa interna mais específica foi inferida. T027/G4-B permanecem abertos, sem retry, D02–D10, filtros, T028/T029 ou lifecycle adicional.

**Checkpoint atual T026 concluída / T027 BLOQUEADA,2026-10-27**:26/55 concluídas/29 pendentes. [A nova execução única autorizada](quickstart.md#t027--correct-authorized-dev-up-succeeded-semantic-preflight-unavailable-2026-10-27) de `agentengine dev up --no-artifact-auth` foi feita no cwd correto, regenerou/aplicou os artefatos e terminou com stack local saudável. Artefato/tool/dependências nativas esperados foram confirmados sem valores privados. O único preflight D01 chamou `search_semantic_movies` uma vez, sem perfil, e retornou fail-closed `unavailable/semantic_unavailable`, zero resultados. Sem retry, D02, filtros, T028/T029 ou outro lifecycle. T027/G4-B7 permanecem abertos; campanhas congeladas continuam NOT RUN e freeze T017 preservado.

## T018 — authorized dependency and manifest completion, 2026-10-26

Critérios exatos da tarefa satisfeitos no ambiente HOST autorizado, não aceitação nativa: declaração voyageai==0.5.0 sem local/video e faixa>=3.11,<3.15, sandbox.tool.secrets exato LLM_API_KEY/MOVIES_MONGODB_URI/VOYAGE_API_KEY/VOYAGE_URL, comentários e placeholders ainda vazios; resolução/importação reais por uv e verificação das assinaturas instaladas sem construir cliente. Referências oficiais atuais/limites, autorização literal e comparação sanitizada dos processos em [quickstart](quickstart.md#t018--authorized-declarations-and-host-imports-2026-10-26). API api_key/base_url não é campo YAML; seu uso explícito sem fallback será código T019–T021, não antecipado. Secret scope é sandbox compartilhado, não isolamento por ferramenta.

Não alterar egress sem conhecer destino público autorizado, nem ler URL/chave privada para completá-lo. Regra legada existente preservada; binding/entrega/segregação/egress/conectividade/modelo e versões/import nativos continuam G4-B NOT RUN. Nenhuma chamada ao catálogo/provedor ou aplicação importada. uv sync --no-install-project --no-build excluiu a distribuição editable host movie-scout0.1.0 sem apagar fontes; evidência de dependências, não reinstalação/build do projeto. Primeiro cutoff fixo foi substituído por nova geração sob a configuração relativa original, --check PASS; não modificar uv.toml para acomodar resolução. Lock ignorado gerado pelo package manager, não editado manualmente;134 registros não são134 instalações. A autorização de efeito automático não concede operação manual de stack/cloud. T018 marcada somente após estes critérios, STOP T019; resultados anteriores abaixo são históricos.

Auditoria final desta retomada:56 arquivos públicos protegidos byte a byte inalterados; oito arquivos públicos permitidos modificados, mais lock local gerado. Metadados pyproject equivalem exatamente ao baseline mais pin/faixa; manifesto equivale exatamente ao baseline mais dois nomes TOOL, exemplo mantém atribuições vazias.55 linhas de tarefas exatamente iguais exceto caixa T018,18 marcadas/37 pendentes/13[P]; cauda histórica do quickstart/G4-B integralmente preservada, sete caixas NOT RUN e canônico11749 bytes/SHA256 a76dce445350220835eb8320c07feaadc57e200eb0722265ae0a68705ecd50b2.103 destinos locais de links existentes/whitespace/AST/git diff --check PASS; uv pip check:129 distribuições instaladas compatíveis. Primeira auditoria auxiliar usou título G4-B com parênteses inexistentes: corrigido somente o validador, repetição completa PASS. Uma tentativa inicial de patch documental com contexto inexato falhou; conferência posterior confirmou seção atual única e freeze intacto. Hooks YAML final before_implement0/after_implement0 executáveis, nenhum obrigatório a despachar. Não são provas de secretos/runtime nativo/saúde/cloud.

**Date**: 2026-10-26 | **Status**: T017 concluída por pré-registro v1.0 congelado;17/55 concluídas,38 pendentes. [Leitura atual/protocolo](quickstart.md#t017--successful-bounded-read-and-prospective-freeze-2026-10-26): READ_OK10 registros/1746ms/find1/getMore0/cleanup true. Cinco temas locais fundamentam dez prompts5PT/5EN; D/H/F NOT RUN. STOP antes T018. G1/G2 históricos2026-10-23 sem reauditoria; G3/G4-A/aprovação preservados, G4-B sete itens NOT RUN. Sem aceitação/instalação/alteração da stack. Registros anteriores abaixo permanecem históricos.

## T018 — final static verification, 2026-10-26

Auditoria pública:76 arquivos protegidos byte a byte inalterados;55 linhas de tarefas exatamente idênticas,17 marcadas/38 pendentes/13[P], T018 aberta. Histórico do quickstart após o cabeçalho original integralmente preservado, canônico T01711749 bytes/SHA256 a76dce445350220835eb8320c07feaadc57e200eb0722265ae0a68705ecd50b2 intacto e G4-B7 desmarcadas. Atribuições de env.example idênticas/vazias; somente comentários mudaram.98 destinos locais de links existentes/whitespace direto PASS; git diff --check PASS complementar. Primeira comparação auxiliar tentou comparar o quickstart inteiro como sufixo apesar da inserção após o título; corrigido somente o validador para comparar a cauda histórica após o cabeçalho, auditoria repetida PASS. Nenhuma mudança de aplicação para acomodar checks.

Filtro real extraído por AST, somente constantes e duas funções puras, executado isoladamente sem importar/iniciar supervisor: agent.yaml/pyproject.toml/uv.lock=True (observáveis); env.example/quickstart.md=False. Isso verifica o risco estático e a segurança desses comentários/documentos frente a esse filtro, NÃO o estado ativo da stack, outros watchers ou um restart realmente ocorrido. Ignoradores Git/Python/Docker existentes revistos e preservados, sem lacuna crítica identificada. Hooks YAML final parseado: before_implement0/after_implement0 executáveis, nenhum obrigatório a despachar. Nenhum teste aplicativo ou import Voyage, nativo, secret, DB/provedor, build ou lifecycle; resolução pública host descrita no quickstart não é aceitação G4-B.

## T017 — native catalog evidence and frozen preregistration, 2026-10-26

Mantenedor informou “desculpa, o cluster ainda nao tinha sido inicializado.” Retomada interpretada como UMA nova leitura no escopo anterior, sem pedir a mesma permissão/credenciais e sem inicializar/resumir/iniciar/parar/reiniciar/buildar/deployar cluster ou stack. Constituição primeiro, pré-requisitos/checklist16/16 PASS/hooks before_implement0; plano/tarefas/modelo/contrato/spec/quickstart/evidência/helper/factory/skills revistos. Python host3.13.13 configurado, configuração de contêiner obtida, ignoradores públicos preservados e baseline60 arquivos públicos capturado, sem privados. Documentação oficial Agent Engine/find/CSOT conferida. Skill genérico de consulta não autoriza seus probes de schema/índice: namespace/projeção já fixos e inventário existente, nenhuma inspeção MCP ou rota alternativa.

T017-CATALOG-20261026-03:2026-10-26T13:44:41.698007Z–13:44:43.444172Z, **READ_OK**,1746ms incluindo client.close;10 documentos recebidos/10 com ObjectId/título/plot utilizáveis, sem corte local dos plots. LAUNCHER público extraído por AST selecionou um TOOL existente; processo próprio Python3.11.16/PyMongo4.18.3/SDK0.11.9, somente tools/factory real, sem main/App/dotenv/auditoria original. Configuração herdada MOVIES corresponde à factory/principal esperado e difere da operacional, somente booleanos; não comparação fresca com privado, reauditoria de grants ou inspeção de pool longevo. G1 histórico2026-10-23 continua delimitado, não atualizado por sucesso de leitura.

Uma find{} sample_mflix.embedded_movies, ordem natural, projeção positiva _id/title/plot, limit=-10/batch10/max_time_ms5000/CSOT5s/retryReadsFalse, zero retries aplicativos. Monitor: find1/getMore0/inesperados0; namespace/filtro/projeção/limit10/batch10/singleBatch observados corretos, maxTimeMS3557<=5000. Cursor/client fechados em finally. Sem segunda leitura, sentinela/refill/metadados administrativos/vetores/provedor/embedding ou operações. Agora há recuperação pela rota estabelecida, mas o relato de inicialização não prova a causa histórica dos timeouts, nem estado administrativo do cluster. Não inferir isso sem evidência.

Antes de qualquer avaliação semântica, v0.1 preservada integralmente e revisão prospectiva v1.0 registrada: trocar cinco pares temáticos não comprovados por cinco temas sustentados nos plots recebidos. Somente cinco IDs/títulos/resumos necessários retidos no quickstart; não copiar todos os plots. Dois plots de origem têm reticências: usar somente conteúdo explícito, sem completar. Nenhum score/resultado semântico/latência de campanha influenciou a revisão. Campo humano não atribuído do rascunho substituído prospectivamente por avaliador automatizado identificado GitHub Copilot, sem pessoa/consentimento/julgamento humano inventados; eventual revisão humana complementar não substitui rótulos para melhorar nota.

v1.0 autossuficiente: D10/PT5/EN5, H20 em ordem D01–D10 duas vezes, concorrência1, cold/warm UNKNOWN salvo prova, rubrica0/1/2/top5/>=8/10, matriz F10/subcasos, campos de evidência, saudável19/20<=20s e falha TARGET30s, sem garantia/cancelamento global/seleção pós-hoc. Freeze efetivo2026-10-26T13:46:43.689484Z,11749 bytes UTF-8 entre marcadores; SHA256 a76dce445350220835eb8320c07feaadc57e200eb0722265ae0a68705ecd50b2. Cálculo local anterior à marcação T017; primeira checagem auxiliar teve incompatibilidade de encoding Ruby, corrigida somente no validador para UTF-8 e repetida, sem efeito na aplicação ou nova consulta.

T017 [X] por evidência/pré-registro,17/55 concluídas/38 pendentes, STOP antes T018. Todos D/H/F e G4-B7 NOT RUN; find de catálogo não comprova busca semântica/modelo/binding/segregação/egress/relevância/performance/cloud. Nenhum teste aplicativo, produção/testes/dependências/manifestos/privados/serviços alterados; somente quickstart/research/plan/tasks. Histórico anterior não apagado nem reinterpretado como sucesso.

Auditoria final desta continuação:60 hashes públicos protegidos inalterados; somente quatro documentos permitidos modificados.55 linhas de tarefas idênticas ao baseline exceto a caixa T017, IDs sequenciais/histórias/textos/13[P] preservados,17 marcadas/38 pendentes. Hash canônico/11749 bytes e D10/H20/F10 conferidos; v0.1 e todo o restante histórico/G4-B byte a byte preservados, sete caixas NOT RUN; requirements16/16.95 links locais/24 âncoras válidos, whitespace direto e git diff --check PASS; quatro documentos sem diagnósticos do editor. YAML before_implement/after_implement relido/parseado:0 executáveis, nenhum hook obrigatório a despachar. Não é teste aplicativo, hash de privados ou prova de saúde/identidade imutável da stack.

## T017 — renewed read blocked at server selection, 2026-10-26

“podemos continuar” autoriza UMA tentativa renovada no mesmo escopo, não expansão/operação da stack. Revisão inicial de evidência/código: o primeiro timeout não reteve subtipo e não demonstrava causa externa; launcher/factory públicos e serializer limit negativo/batch foram conferidos sem executar auditoria original, main ou privados. Não foi identificado defeito específico que justificasse alterar helper/fonte/timeouts. Pré-requisitos/checklist16/16 PASS, before_implement0, skills/Python/configuração de contêiner e ignoradores existentes conferidos.

Resultado T017-CATALOG-20261026-02,2026-10-26T13:19:57.893594Z–13:20:03.134668Z: **SERVER_SELECTION_TIMEOUT**, ServerSelectionTimeoutError na etapa consume,5241ms incluindo cleanup (241ms acima de5s), find0/getMore0/comandos aplicativos inesperados0/zero registros; cursor e cliente próprios fechados em finally. Um único TOOL existente, Python3.11.16/PyMongo4.18.3/SDK0.11.9, URI dedicada herdada corresponde à factory e difere da operacional/principal esperado true; sem fallback ou reauditoria de grants. G1 histórico não convertido em prova atual. Método/limites/autorização no [registro atual](quickstart.md#t017--renewed-bounded-read-outcome-2026-10-26): uma find{} solicitada em embedded_movies, somente _id/title/plot, limit=-10/batch10/max_time_ms5000/CSOT5s/retryReadsFalse. Nenhum wire find observado; não inventar limites efetivamente transmitidos.

O driver não selecionou servidor disponível antes da consulta; não é falha demonstrada de sintaxe, execução de query, índice ou permissão. Causa específica DNS/TCP/TLS/rota/política/estado externo UNKNOWN; não inspecionada nem inferida, sem probes/erros brutos. A categoria nova não diagnostica retroativamente a primeira tentativa. Nenhum retry após a falha, fonte/rota alternativa, metadado administrativo, vetor/provedor/embedding ou operação da stack. Próximo passo do mantenedor: restaurar/verificar conectividade pela rota nativa existente fora desta execução, ou fornecer extrato sanitizado local de até10 _id/title/plot com proveniência para cinco temas. Sem nova pergunta de aprovação genérica, credenciais solicitadas, timeout ampliado ou ação administrativa pelo assistente.

Somente quatro documentos de evidência/status atualizados; protocolo candidato v0.1 permanece intacto/NOT FROZEN, sem IDs/enredos/avaliador/freeze/hash inventados. T017 [ ],16/55/39 pendentes/13[P]; G4-B sete itens NOT RUN. STOP antes T018. Sem testes aplicativos/produção/testes/dependências/manifestos/privados/serviços alterados; não é busca semântica, G4-B PASS ou prontidão cloud. Os limites de autorização anteriores abaixo descrevem o checkpoint anterior, superado apenas pela tentativa renovada expressamente solicitada.

Auditoria desta retomada:60 hashes públicos protegidos inalterados, quatro documentos permitidos modificados;55 linhas de tarefas/IDs/histórias/caixas exatamente iguais ao baseline,16 marcadas/39 pendentes/13[P]. Protocolo v0.1 e todo o restante do quickstart a partir dele byte a byte preservados, D10/H20/F10/G4-B7 desmarcadas; requirements16/16.94 links locais/24 âncoras válidos, whitespace direto/git diff --check PASS, quatro documentos sem diagnósticos do editor. YAML before_implement/after_implement:0 hooks executáveis, nenhum obrigatório a despachar. Não é teste aplicativo, hash de privados, prova de saúde da stack ou identidade imutável de contêineres.

## T017 — authorized single read blocked, 2026-10-26

O mantenedor autorizou exatamente **“sim, pode seguir”** para UMA leitura de até dez registros de embedded_movies, somente ID/título/plot, sem vetores e timeout5s, para fundamentar T017; não T018 ou operações. Constituição primeiro, instruções/memória/skills de consulta/conexão/Python revisadas, hooks before_implement0, pré-requisitos feature002/checklist16/16 PASS. Python host existente3.13.13 configurado antes dos comandos Python; configuração de contêiner obtida antes de docker. Ignoradores existentes verificados/preservados e baseline de60 arquivos públicos protegidos capturado, sem incluir privados.

Método/evidência completos em [quickstart](quickstart.md#t017--single-authorized-read-outcome-2026-10-26), ID T017-CATALOG-20261026-01. LAUNCHER público extraído por AST, sem rodar a auditoria original/main; um TOOL selecionado, próprio processo com interpretador nativo3.11.16/PyMongo4.18.3/SDK0.11.9. Factory real confirmou booleanamente URI de filmes entregue e distinta da operacional/identidade esperada; nenhum arquivo privado ou valor impresso, nenhuma reauditoria de grants. G1 é histórico2026-10-23 aplicável à configuração registrada, não metadados frescos ou comparação nova ao arquivo privado. A exceção ampla histórica não foi usada para justificar acesso.

Única find solicitada em sample_mflix.embedded_movies, filtro vazio, projeção _id/title/plot, limit=-10 para singleBatch/máximo10, batch10/max_time_ms5000 dentro de CSOT5s, retryReads=False apenas no cliente diagnóstico, zero retries aplicativos. Resultado real2026-10-26T13:13:33.360141Z–13:13:38.591150Z: **READ_TIMEOUT**,5228ms; find0/getMore0/comandos aplicativos inesperados0, nenhum documento. Como não houve find enviado, limites efetivos no wire não foram observados;228ms acima de5s explicitados, sem garantia rígida/cancelamento servidor. Cursor e cliente próprios fechados em finally. Não atribuir causa a grants/rede/índice/modelo sem evidência; nenhum teste adicional para diagnosticá-la autorizado/executado.

Autorização de uma tentativa consumida: sem retry, fonte alternativa, metadados administrativos, vetores/embeddings/provedor, queries adicionais ou operação de serviços. Lacuna temática permanece; candidatos v0.1/ordem H/rubrica/F e campos de freeze preservados sem inventar temas/avaliador/hash. T017 não satisfaz critérios de conclusão e permanece [ ];16 concluídas/39 pendentes/55 IDs e13[P] preservados. Todos D/H/F e sete G4-B NOT RUN, não evidência de busca semântica/secret delivery/binding/modelo/egress operacional ou cloud. Sem testes aplicativos, instalações ou alterações de fontes/testes/dependências/manifestos/privados. STOP antes T018. A seção de rascunho abaixo descreve a etapa anterior à autorização, não um pedido repetido dela.

Auditoria documental desta continuação:60 hashes públicos protegidos inalterados; somente quickstart/research/plan/tasks modificados.55 linhas de tarefas exatamente iguais ao baseline, inclusive todas as caixas (16 marcadas/39 pendentes), histórias e13[P]; protocolo candidato v0.1 até G4-B byte a byte preservado, D10/H20/F10 e G4-B7 desmarcadas.90 links locais/22 âncoras válidos, whitespace direto/git diff --check PASS; quatro documentos sem diagnósticos do editor. YAML final parseado: before_implement0/after_implement0 executáveis, nenhum hook obrigatório. Não é teste aplicativo, prova de integridade de privados ou de saúde/identidade de contêineres; nenhum desses estados foi alegado como revalidado.

## T017 — authorized evidence review and draft only, 2026-10-26

Pedido limitado a T017, constituição lida primeiro, hooks before_implement ausentes, pré-requisitos JSON da feature002 e requirements16/16 PASS. Revisados spec/plano/tarefas/modelo/contrato/pesquisa/quickstart, memória existente e fixtures/helpers públicos como texto, sem imports/execução. Ignoradores Git/Python/Docker existentes conferidos, sem lacuna crítica ou edição. Nenhum novo gate documental/loop de aprovação “sim, aprovo”, B1 ou T049.

Evidência temática insuficiente: G2 original analisou primeiros100 e emitiu apenas inventário/contagens, sem textos/IDs; não derivar temas de gêneros/anos. Fixtures semânticas novas declaram dados sintéticos, incluindo mundo simulado; helper native_movie_checks compara exclusivamente movies e acessa configuração nativa quando executado, portanto não foi reutilizado/lançado para obter catálogo. Títulos tradicionais previamente validados não comprovam sua presença em embedded_movies; nenhuma identidade entre coleções ou mapeamento de subconjunto local foi estabelecida. A confirmação Load Sample Dataset/proveniência de embeddings não preenche essa lacuna temática.

Tentativas públicas oficiais de sample_mflix HTML e variante .md falharam na extração2026-10-26; nenhum plot/documento foi recuperado. “The Great Train Robbery” permanece indicação de possível exemplo documental, não evidência verificada nesta sessão nem presença local. Mesmo recuperar um exemplo oficial não comprovaria a carga local exata. Não se inventou enredo/ID nem se rotulou tema incerto como comprovado.

Trabalho efetivo em [quickstart, seção4](quickstart.md#4-preregister-evaluation-before-running): dez descrições candidatas5PT/5EN com facetas explícitas e prova PENDENTE, vinte pedidos determinísticos, rubrica0/1/2/top5/>=8/10, concorrência1/ordem/cold-warm-UNKNOWN, saudável19/20<=20s, matriz F01–F10 com subcasos/controles sintéticos separados, falha TARGET30s, campos de evidência e regra anti-substituição pós-hoc. Tudo DRAFT/NOT FROZEN/NOT RUN; avaliador/data/hash de freeze ainda pendentes. Não medir antes de provar temas/congelar, não executar tarefas dependentes. T017 permanece [ ],16 marcadas/39 pendentes; sete G4-B intactas.

Próximo passo mínimo proposto, NÃO autorizado/executado: extrato sanitizado fornecido pelo mantenedor ou autorização específica de UMA find nativa em embedded_movies, total<=10/batch10, somente _id/title/plot, CSOT5s/maxTimeMS<=5000/cleanup, sem vetores/provedor/metadados administrativos/paginação/retry/secret reads. Aplicabilidade da configuração G1 deve estar estabelecida por evidência sanitizada, sem presumir validade fresca; divergência exige STOP, não nova inspeção implícita. Procedimento/limites exatos no quickstart. Se insuficiente, manter rascunho sem ampliar leitura. Nenhuma fonte/teste/dependência/manifesto/privado alterado, nenhum teste/import/DB/provedor/runtime/install/build/start/stop/restart/infra/cloud nesta tarefa. STOP antes T018; a falta de prova local específica a T017 não reabre gates documentais superados nem simula aceitação.

Auditoria estática2026-10-26:60 hashes públicos protegidos inalterados;55 linhas de tarefas exatamente idênticas ao baseline,16 marcadas/39 pendentes/13[P]; dez D/vinte H/dez F conferidos, G4-B7 desmarcadas e requirements16/16. Quatro Markdown editados:88 links locais/21 âncoras existentes, whitespace direto e git diff --check PASS; diagnósticos do editor sem erros. YAML relido/parseado, before_implement/after_implement0 executáveis: nenhum hook a despachar. Checagens documentais não são testes aplicativos nem evidência nativa/segredos/runtime; nenhum arquivo fora dos quatro documentos foi editado por esta continuação.

## Phase 1 execution — T001 scope and constitution review, 2026-10-23

**T001 concluída por conferência documental efetiva.** O pedido atual “Start the implementation in phases” inicia o workflow separado previsto no plano e limita esta execução a T001–T003, com STOP antes de T004. Não amplia a aprovação histórica “sim, aprovo” de2026-10-23 para operações: aquela decisão aprovou a simplificação LOCAL TEST DEVELOPMENT e seu handoff, não executou implementação na revisão anterior. Nenhuma nova aprovação foi solicitada; constituição v4.0.0 lida primeiro, sem emenda ou waiver. Requisitos FR-001–FR-017/SC-001–SC-008, plano, pesquisa, modelo, contrato e quickstart atuais conferidos; trechos anteriores “nesta invocação” referem-se às respectivas revisões históricas, não proíbem este novo setup expressamente solicitado.

| Princípio constitucional | Conferência T001 / limite preservado |
|---|---|
| I — plataforma exclusiva | Mesmo agente/CLI/SDK nativos; exceção oficial PyMongo restrita a ferramentas read-only. Cliente Voyage selecionado documentalmente, não instalado nem declarado nativamente compatível por esta conferência. |
| II — fonte de verdade | Tradicional somente sample_mflix.movies; semântica somente sample_mflix.embedded_movies no mesmo cluster. Sem troca silenciosa, join, fallback ou escrita. |
| III — arquitetura mínima | Nenhum projeto novo, frontend/backend/proxy, orquestrador ou infraestrutura adicional. |
| IV — grounding | Semântica exige ID/título/plot recuperados utilizáveis; excluir plot ausente/null/não string/vazio/whitespace, manter ordem e shortfall/empty honestos, sem refill/fabricação. Ausências tradicionais não mudam. |
| V — segurança/configuração | MOVIES_MONGODB_URI separado de MONGODB_URI, sem fallback; nenhuma leitura privada ou operação de banco. Exceção ampla histórica NÃO cobre semântica; preservar G1 find-only exato nas duas coleções. |
| VI — validação/observabilidade | G4-B nativo único continua obrigatório NOT RUN; não substituir por documentos/mocks. Tradicional, estado, filtros, falhas e segurança exigem regressão futura; imagens continuam text-only. |
| VII — entrega por especificação | Implementar em fases conforme lista existente, registrar evidência e marcar somente trabalho efetivo. T001–T003 não liberam automaticamente T004–T011 ou aceitação. |

**Gates conferidos, não reexecutados**: G1 PASS apenas para configuração local nativa registrada/find-only nas duas coleções; T049 da feature001 continua concluído exclusivamente para movies. G2 PASS com primeiros100 documentos e atestado manual dos filtros/Ready/Queryable/MongoDB9.0.4, não schema exaustivo nem consulta vetorial aceita. G3 seleciona voyageai==0.5.0 e voyage-3-large/query/2048/float/truncation=False em Python>=3.11,<3.15; G4-A é viabilidade documental API/runtime/build/secrets/egress, nunca PASS operacional. Binding futuro explícito api_key/base_url dos EXISTENTES VOYAGE_API_KEY/VOYAGE_URL no TOOL necessário; não ler/pedir secrets ou inferir entrega pela memória.

**Critérios preservados**: saudável>=19/20<=20s medido; falha30s é meta, não garantia/cancelamento servidor. Propostas de ferramenta12s/provedor6s/DB5s, timeouts suportados e zero retries aplicativos. Resolução/import, entrega/segregação/binding/egress/conectividade e resultados reais pertencem a G4-B durante implementação/antes do aceite, não resultados circulares exigidos antes do código.

**Entrada do workflow**: pré-requisitos oficiais --json --require-tasks --include-tasks passaram, FEATURE_DIR absoluto aponta feature002; checklist requirements16/16, zero pendentes. Hooks before_implement ausentes. Sem reauditar G1/G2, executar testes, ler privados, instalar/buildar, chamar DB/provedor ou iniciar/parar/reiniciar/deployar serviços. B1 e autorização “A” não reabertos.

## Phase 1 execution — T003 official references and evidence criteria, 2026-10-23

**T003 concluída após T001/T002.** Referências públicas oficiais consultadas diretamente nesta fase e consolidadas abaixo. São evidência de interfaces e viabilidade documental, não instalação, resolução conjunta, entrega de secrets, acesso ao modelo, consulta vetorial ou aceitação nativa. Nenhum comando de instalação/build, import Python, teste ou chamada ao banco/provedor foi executado.

| Tecnologia / combinação proposta | Referência oficial e fato verificável | Critério de evidência e bloqueio preservado |
|---|---|---|
| Agente único, ferramentas e estado nativos | [Getting started](https://www.mongodb.com/docs/agentengine/get-started/), [contrato](https://www.mongodb.com/docs/agentengine/reference/agent-contract.md), [SDK API](https://www.mongodb.com/docs/agentengine/sdk/python/packages/agent-engine-sdk-langgraph/docs/api/): Python>=3.11, estrutura gerada, App.tool/App.llm auditados, checkpointer e estado serializável; sem endpoint HTTP próprio. | Preservar wrappers/estrutura e não guardar clientes/vetores/secrets em estado. Carregamento/roteamento/estado reais são prova futura G4-B; documentação não prova execução. Framework, proxy, agente ou UI alternativos continuam não aprovados. |
| Dependências e runtime combinados | [Build](https://www.mongodb.com/docs/agentengine/deploy/agent-image.md) e [local](https://www.mongodb.com/docs/agentengine/build/run-local.md): caminho oficial de dependências; lock existente implica sincronização frozen. [Voyage0.5.0 metadata](https://pypi.org/pypi/voyageai/0.5.0/json): Python>=3.9,<3.15. Interseção selecionada com plataforma: >=3.11,<3.15. | Resolver versões reais de SDK/runner/PyMongo/Voyage, consistência manifest/lock e imports no runtime nativo durante implementação/antes do aceite. Alterar declaração não comprova instalação. Combinação operacional não verificada bloqueia uso/aceite afetado, não autoria prévia de testes/código. Sem instalar ou alterar manifestos nesta fase. |
| PyMongo e agregação vetorial read-only | [Aggregation](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/aggregation/), [Collection API4.18.3](https://pymongo.readthedocs.io/en/4.18.3/api/pymongo/collection.html), [metadata4.18.3](https://pypi.org/pypi/pymongo/4.18.3/json) e [vectorSearch](https://www.mongodb.com/docs/vector-search/query/aggregation-stages/vector-search-stage/): aggregate retorna CommandCursor, aceita maxTimeMS/batchSize; estágio vetorial primeiro, dimensão compatível e pré-filtros indexados. | Manter intervalo existente pymongo>=4.11,<5;4.18.3 é referência, não versão instalada/pin novo. Construir pipeline fixo allowlisted, limite<=10/numCandidates<=200, projeção sem vetores e cursor fechado. API também permite writes: sua existência não torna pipeline arbitrário seguro. Validar wire/filtros/falhas no nativo com G1/G2 aplicáveis, MOVIES_MONGODB_URI sem fallback. Não reabrir B1 nem reauditar grants aqui. |
| Cliente oficial e query embedding | [API/clientes](https://www.mongodb.com/docs/voyageai/api-and-clients/), [modelos textuais](https://www.mongodb.com/docs/voyageai/models/text-embeddings/) e [fonte oficial v0.5.0](https://raw.githubusercontent.com/voyage-ai/voyageai-python/v0.5.0/voyageai/client.py): Client(api_key,base_url,timeout,max_retries), embed(input_type,truncation,output_dtype,output_dimension); API requer cliente>=0.3.7. | Seleção exata voyageai==0.5.0, voyage-3-large/query/2048/float/truncation=False, timeout positivo<=6s e max_retries=0; validar dimensão/números finitos. Compatibilidade documental não prova acesso real conta/modelo/endpoint ou relevância. Não substituir por modelo de memória, cliente HTTP alternativo, truncamento/fallback ou inferência de proveniência pelo nome do campo. |
| Secrets/endpoint/egress do TOOL | [Contrato por sandbox](https://www.mongodb.com/docs/agentengine/reference/agent-contract.md), [secrets](https://www.mongodb.com/docs/agentengine/deploy/provision-secrets.md), [egress](https://www.mongodb.com/docs/agentengine/network-egress.md): entrega e rede são por sandbox; configuração declarada e aplicação efetiva são distintas. | Binding futuro explícito api_key/base_url dos EXISTENTES VOYAGE_API_KEY/VOYAGE_URL no TOOL necessário pelo mecanismo oficial; ausência/incompatibilidade falha fechada. Matching chave/região/modelo, entrega/segregação e rede reais continuam não comprovados e bloqueiam uso/aceite afetado até G4-B. Memória não é evidência de entrega TOOL. Sem ler/pedir/copiar secrets, autodetectar destino, alterar rede ou operar serviços. |
| Timeouts e duração observada | [SDK](https://www.mongodb.com/docs/agentengine/sdk/python/packages/agent-engine-sdk-langgraph/docs/api/), [policy engine](https://www.mongodb.com/docs/agentengine/manage/governance/policy-engine.md), [invoke](https://www.mongodb.com/docs/agentengine/deploy/invoke-agent.md): timeout por ferramenta; política checa antes da chamada e não interrompe in-flight; timeout cliente não cancela servidor. | Orçamentos propostos ferramenta12s/provedor6s/DB5s segundo suporte, trabalho bounded e zero retries aplicativos. Comprovar comportamento/cleanup e medir >=19/20 saudáveis<=20s; falha30s é TARGET, registrar overrun. Garantia global, propagação OE/modelos e interrupção de thread síncrona permanecem não comprovadas e não podem ser prometidas; não são requisito circular pré-código nem autorização para watchdog próprio. |
| Memória nativa e imagens opcionais | [Contrato](https://www.mongodb.com/docs/agentengine/reference/agent-contract.md) e [SDK](https://www.mongodb.com/docs/agentengine/sdk/python/packages/agent-engine-sdk-langgraph/docs/api/) delimitam ferramentas/estado nativos; não estabelecem, por si, renderização de pôster no chat. | Preservar memória/extraction existentes e separar contexto semântico/perfil explícito. Imagens continuam bloqueadas por falta de evidência oficial específica + demonstração nativa; entrega principal text-only, sem proxy/enriquecimento ou fetch externo. |

**Resultado T003**: caminho documental selecionado G3/G4-A consolidado, sem novo PASS operacional. G1/G2 e proveniência históricos preservados com seus limites; nenhuma inspeção nova de catálogo/índice. Combinações não verificadas ficam explicitamente bloqueadas para uso/aceite correspondente, não convertidas em proibição circular de implementar o caminho aprovado. A checklist única [G4-B](quickstart.md#5-local-acceptance-checklist-g4-b) conserva sete itens NOT RUN. T004–T011 não executadas nesta fase; STOP após a validação documental do Setup.

## Phase 2 execution — foundational documentary review, 2026-10-23

Escopo desta continuação: somente T004–T011, em sequência, com STOP antes de T012/Fase 3. Método: revisão dos registros sanitizados existentes e documentação pública oficial; nenhuma nova auditoria DB, leitura privada, consulta semântica, chamada de embedding, teste aplicativo, instalação, build ou operação de serviços. Os registros de Fase 1 e de planejamento abaixo continuam históricos; não se atribui a esta fase a execução dos diagnósticos anteriores.

### T004 — G1 evidence reconciliation

Conferido o atestado/diagnóstico sanitizado já recebido em2026-10-23, seção [G1](#g1--native-metadata-verification), sem pedi-lo novamente ou reexecutá-lo. Ambiente comprovado: conexão nova pelo interpretador/ambiente de um único processo TOOL local selecionado; factory real `_get_movie_client`, configuração de filmes correspondente e separada da operacional, principal esperado e `connectionStatus(showPrivileges:true)` com concessões efetivas completas, inclusive herdadas: somente find nas coleções exatas sample_mflix.movies e sample_mflix.embedded_movies, sem wildcard/recursos/ações extras. Método/data/configuração/limites são suficientes para o G1 local registrado; T004 concluída documentalmente, não nova prova operacional. Não prova heap/pool do worker longevo, cloud ou permanência dos grants. Mudança de identidade/configuração/grants invalida a evidência e exige STOP antes do uso afetado. Exceção ampla histórica e T049 de movies não foram usados como prova semântica.

### T007 — existing manual preparation receipt and invalidation

Após T005/T006, conferido o recibo sanitizado já recebido em2026-10-23, [G2 histórico](#g2--bounded-inventory-and-manual-preparation-receipt), contra o [mapeamento do contrato](contracts/semantic-movie-tools.md#t006--verified-mapping-and-documentary-operator-cross-check). Namespace fixo sample_mflix.embedded_movies, mesmo cluster/configuração movie G1; índice existente plot_vector_index/vectorSearch, plot_embedding_voyage_3_large/2048/cosine. Diferença manual externa atestada: adição dos três caminhos filter genres/year/imdb.rating; mantenedor confirmou Ready/Queryable e MongoDB9.0.4 após a preparação. Nenhuma nova alteração solicitada ou executada; grants runtime find-only não ampliados. T007 concluída documentalmente por recibo existente, não nova listagem administrativa nem consulta vetorial/filtros aceita.

Readiness fica vinculada à identidade/configuração movie e ao namespace/índice/definição/status/versão inventariados. Troca de configuração/identidade/grants, campo/tipo/dimensão/métrica, filter ausente/alterado, índice recriado/não queryable ou incompatibilidade de servidor/operador invalida o item afetado: STOP até evidência sanitizada correspondente, sem descoberta/gestão runtime, filtro omitido, pós-filtro substituto, fallback ou rotular indisponível como vazio. Não repetir agora G1/G2 ou solicitar o mesmo recibo; resultados reais de busca/filtros continuam G4-B NOT RUN.

### T008 — exact official hosted client selection

Conferência documental2026-10-23 após T003 e proveniência existente, sem instalar/importar/chamar o cliente. Seleção preservada: voyageai==0.5.0, sem extras local/video, Python>=3.11,<3.15. [Metadados versionados](https://pypi.org/pypi/voyageai/0.5.0/json) declaram >=3.9,<3.15 e distribuição wheel; a interseção com Agent Engine>=3.11 é a faixa semântica escolhida, não a versão efetiva já instalada. Dependências transitivas e resolução conjunta com SDK/runner/PyMongo ainda exigem G4-B; wheel não prova resolução/import bem-sucedidos.

APIs verificadas na [fonte oficial Client v0.5.0](https://raw.githubusercontent.com/voyage-ai/voyageai-python/v0.5.0/voyageai/client.py) e [base v0.5.0](https://raw.githubusercontent.com/voyage-ai/voyageai-python/v0.5.0/voyageai/_base.py), em conjunto com [API/clientes MongoDB](https://www.mongodb.com/docs/voyageai/api-and-clients/) e [text embeddings](https://www.mongodb.com/docs/voyageai/models/text-embeddings/):

- Construtor selecionado `voyageai.Client(api_key=..., base_url=..., timeout=..., max_retries=0)`: valores dos EXISTENTES VOYAGE_API_KEY e VOYAGE_URL entregues ao TOOL pelo mecanismo oficial, não inferidos da memória. Validar ambos como strings não vazias/não whitespace ANTES da construção e validar o destino configurado sem substituí-lo. A base0.5.0 usa `api_key or default_api_key()` e `base_url or get_default_base_url(api_key)`; passar argumentos vazios não impede fallback. Ausência/incompatibilidade deve produzir unavailable sem construir/chamar o provedor, nunca autodetecção ou novo destino. Sem ler/copiar/pedir valores nesta fase.
- Uma chamada hospedada `Client.embed` com lista de UMA descrição validada, `model="voyage-3-large"`, `input_type="query"`, `output_dimension=2048`, `output_dtype="float"`, `truncation=False`; sem rewrite/tradução/tokenizer/count_tokens/modelo local/download. Exigir exatamente um vetor2048 de números finitos transitório; não persistir/logar/expor o vetor ou payload bruto.
- `timeout` explícito positivo<=6 segundos, reduzido pelo restante local quando suportado, e `max_retries=0` explícito; zero retries aplicativos e nenhuma segunda tentativa/fallback. O cliente mapeia timeout para request_timeout do transporte: não promover esse parâmetro a deadline rígido da conversa ou cancelamento servidor. Chamadas/tempos reais serão observados em G4-B.
- Proveniência já recebida Load Sample Dataset + documentação oficial histórica: plot/voyage-3-large/2048/binData. O link histórico sample_mflix retornou404 nesta consulta documental e não foi falsamente registrado como reverificado; a evidência anterior é preservada. input_type/pré-processamento históricos continuam desconhecidos; compatibilidade técnica documentada com/sem input_type não é prova do valor histórico nem novo bloqueio pré-código. Query real/relevância ainda NOT RUN.

T008 concluída como seleção documental aprovada, não G3 operacional PASS. Sem alterar o modelo/dimensão da memória, manifesto, dependências ou privados. Entrega/segregação efetiva, normalização/matching do base URL existente com chave/região/modelo, autorização do modelo e egress/conectividade pertencem à checklist única G4-B durante implementação e antes de aceite.

### T009 — G4-A precise native mechanisms and limits

Conferência documental2026-10-23 após T003/T008. G4-A é viabilidade do caminho revisado, NÃO PASS operacional; a decisão exata “sim, aprovo” retirou garantia global30s, não timeouts/segurança. Mecanismos selecionados para implementação futura, sem aplicá-los nesta fase:

| Fronteira | Mecanismo oficial selecionado / localização futura | Limite e prova G4-B ainda necessária |
|---|---|---|
| Ferramenta auditada | [SDK API](https://www.mongodb.com/docs/agentengine/sdk/python/packages/agent-engine-sdk-langgraph/docs/api/): `App.tool(is_local=False, timeout=12)` para execução remota TOOL; `get_tools()` fornece wrappers auditados no AER e `get_tool_schemas()` os schemas originais. Acrescentar search_semantic_movies à lista `sandboxes.tool.tools` pelo [contrato](https://www.mongodb.com/docs/agentengine/reference/agent-contract.md), sem wrapper/I/O paralelo próprio. | Timeout do decorador é inteiro em segundos, por chamada, não deadline global. Preservar integração existente de schemas/dispatch/checkpointer. Verificar registro/carregamento/chamada nativos; não executar provedor no AER por conveniência. |
| Dependências/runtime | [Build](https://www.mongodb.com/docs/agentengine/deploy/agent-image.md) e [local](https://www.mongodb.com/docs/agentengine/build/run-local.md): declaração futura no pyproject do agente, pin voyageai==0.5.0 e faixa semântica>=3.11,<3.15; tooling oficial uv/build do CLI. Lock presente exige consistência com sincronização frozen; reconciliar pelo fluxo oficial no ambiente autorizado, não editar lock manualmente ou usar pip ad hoc como prova de sandbox. | Nenhuma instalação/resolução/build agora. Resolver SDK/runner/PyMongo/Voyage/transitivas conjuntamente e verificar versões/imports reais durante implementação. Build/upload cloud não necessário nem autorizado para aceite LOCAL; etapa que exigir operação de serviços para em autorização separada. |
| Entrega dos valores existentes | [Contrato](https://www.mongodb.com/docs/agentengine/reference/agent-contract.md), [secrets](https://www.mongodb.com/docs/agentengine/deploy/provision-secrets.md) e [local](https://www.mongodb.com/docs/agentengine/build/run-local.md): declarar futuramente os nomes EXISTENTES VOYAGE_API_KEY/VOYAGE_URL em `sandboxes.tool.secrets`; usar entrega local de ambiente suportada pelo CLI e binding explícito T008, não copiar valores da memória. Preservar MOVIES_MONGODB_URI para filmes e MONGODB_URI operacional, sem fallback. | Segregação é por sandbox: TODOS os tools do TOOL compartilham seu ambiente, não há isolamento por ferramenta nem sandbox adicional aprovado. Não acrescentar esses nomes ao AGENT só para facilitar acesso; declarações não provam presença/ausência efetiva em cada processo. Verificar entrega/segregação nativas sem divulgar valores; não provisionar/uploadar cloud secrets, ler privados ou pedir secrets agora. |
| Destino e egress | [Network egress](https://www.mongodb.com/docs/agentengine/network-egress.md): mecanismo atual por `sandboxes.tool.network.egress` e `egress_mode`, allow_list de FQDN/portas exatos do destino já configurado em VOYAGE_URL. Vincular futuramente o base URL válido à regra documentada, preservando regras existentes necessárias; nenhum host adivinhado, wildcard, allow_all ou rota alternativa. | Manifesto atual contém egress legado top-level para outro provedor; não é prova de regra semântica. Não executar migração/alterar manifesto/rede aqui. Regras são aplicadas no deploy documentado, não prova de enforcement/conectividade local; compatibilidade da estrutura CLI e aplicação local efetiva devem ser verificadas em G4-B, sem deploy ou mudança de rede presumidos. Matching chave/região/base URL/modelo e acesso reais continuam não verificados. |
| MongoDB bounded | [Collection API](https://pymongo.readthedocs.io/en/4.18.3/api/pymongo/collection.html), [CSOT](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/connection-options/csot/): Collection.aggregate com pipeline allowlisted, maxTimeMS<=5000 e batchSize<=10; contexto `pymongo.timeout` em segundos limita trabalho DB/consumo segundo suporte, preservando cache/cleanup por processo e URI dedicada. | Proposta DB<=5s com restante local quando suportado e zero retries aplicativos; observar CSOT/maxTimeMS efetivo no wire e fechamento inclusive falhas. Um retry interno do driver não é retry aplicativo: comportamento efetivo/configuração existentes devem ser conferidos, não inventar ajuste de conexão ou garantia de cancelamento servidor. Sem novos probes/auditoria DB nesta fase. |
| Duração, erros e exposição | Propostas ferramenta12s/provedor6s/DB5s, checar restante local antes do próximo trabalho onde suportado; uma descrição/embedding/agregação e zero retries aplicativos. [Políticas](https://www.mongodb.com/docs/agentengine/manage/governance/policy-engine.md) checam antes das chamadas, não interrompem in-flight; [invoke](https://www.mongodb.com/docs/agentengine/deploy/invoke-agent.md) não equipara timeout cliente a cancelamento servidor. | Não assumir propagação OE/modelos/final response, interrupção de thread síncrona ou watchdog próprio. `redact_fields` do SDK cobre inputs, NÃO é proteção universal de outputs/artifacts: não incluir secrets/vetores/payloads brutos em envelopes, estado, logs ou artifacts. Falhas sanitizadas, cleanup e overruns precisam de observação nativa. |

SC-005 permanece medição submissão→resposta final:20 pedidos saudáveis pré-registrados,>=19/20<=20s; explicação sanitizada de falha com TARGET<=30s, não hard cap. Registrar cold/warm/concorrência, todos overruns/desvios e casos não executados; não descartar casos ou marcar meta não atingida PASS. Resolução/import/entrega/segregação/binding/egress/conectividade e busca/filtros/estado/segurança/regressão/relevância/tempos ficam na [checklist única G4-B](quickstart.md#5-local-acceptance-checklist-g4-b), sete itens NOT RUN. Sua evidência é coletada durante/após implementação e antes do aceite, não exigência circular de resultados pré-código. T009 concluída documentalmente; nenhuma operação/runtime/API privada foi executada.

### T010/T011 — closure and STOP checkpoint

Reconciliação efetiva dos sete princípios e aprovação/handoff registrados no [plano](plan.md#t010--actual-plan-and-seven-principle-reconciliation-2026-10-23) e [T011](plan.md#t011--recorded-decision-and-phased-handoff-verified-2026-10-23). Somente T004–T011 concluídas nesta continuação; onze tarefas documentais concluídas no total,44 pendentes. **STOP antes T012/Fase 3, testes-first em continuação separada.** G4-B sete caixas NOT RUN, nenhuma aceitação semântica, regressão ou prova operacional fabricada. Aprovação exata “sim, aprovo”2026-10-23 não foi solicitada novamente, nem ampliada para operações; constituição/fontes/manifestos/dependências preservados, sem privados/DB/provedor/instalação/build/start/stop/restart/deploy/mutações.

## Approved local simplification — 2026-10-23

**Decision**: o mantenedor respondeu exatamente **“sim, aprovo”** à proposta para LOCAL TEST DEVELOPMENT: substituir garantia rígida global30s por meta operacional medida, conservar timeouts explícitos/limites/zero retries, selecionar `voyageai==0.5.0` com `voyage-3-large`/query/2048/float/truncation=False e os valores EXISTENTES de VOYAGE_API_KEY/VOYAGE_URL. Resolução de dependências, entrega/segregação de secrets, endpoint-binding, egress/conectividade e funcionamento serão verificados durante implementação e obrigatoriamente antes do aceite pela [checklist única G4-B](quickstart.md#5-local-acceptance-checklist-g4-b). Aprovação é de revisão documental e decisão do plano local; execução fica para workflow separado. Não repetir a mesma aprovação, nem pedir/ler secrets; restart exige autorização operacional separada.

**Rationale / constitution assessment**: constituição v4.0.0 exige tecnologia oficialmente documentada antes do código e validação nativa antes do aceite, não garantia rígida global30s. Não há desvio constitucional nem emenda necessária; nenhuma cláusula constitucional foi alterada/dispensada. [Cliente oficial MongoDB](https://www.mongodb.com/docs/voyageai/api-and-clients/) exige voyageai>=0.3.7 e documenta api_key/base_url/timeout/max_retries. [v0.5.0](https://raw.githubusercontent.com/voyage-ai/voyageai-python/v0.5.0/voyageai/client.py) documenta os mesmos argumentos e embed com input_type/output_dimension/output_dtype/truncation. [Metadados versionados](https://pypi.org/pypi/voyageai/0.5.0/json) delimitam Python>=3.9,<3.15; interseção com [Agent Engine](https://www.mongodb.com/docs/agentengine/get-started/) >=3.11 é >=3.11,<3.15. Sem extras local/video ou bibliotecas alternativas. [Build oficial](https://www.mongodb.com/docs/agentengine/deploy/agent-image.md), [local](https://www.mongodb.com/docs/agentengine/build/run-local.md), [contrato/secrets por sandbox](https://www.mongodb.com/docs/agentengine/reference/agent-contract.md), [secrets](https://www.mongodb.com/docs/agentengine/deploy/provision-secrets.md) e [egress](https://www.mongodb.com/docs/agentengine/network-egress.md) estabelecem o caminho de dependências/configuração, NÃO sua aplicação efetiva. Nenhum build/upload agora; build cloud não é requisito de aceite local nem permissão operacional.

**Compatibility**: [text embeddings](https://www.mongodb.com/docs/voyageai/models/text-embeddings/) documenta voyage-3-large multilíngue,2048,float,truncation=False e compatibilidade técnica com/sem input_type. Corpus plot/voyage-3-large/2048 corroborado pelo sample_mflix e Load Sample Dataset abaixo. `input_type` histórico/preprocessamento permanecem desconhecidos, sem inventá-los ou transformá-los em bloqueio documental adicional. Binding projetado é explícito: api_key do VOYAGE_API_KEY e base_url do VOYAGE_URL EXISTENTES, somente no sandbox TOOL necessário pelo mecanismo oficial; falhar fechado se ausentes/incompatíveis, nunca recorrer a autodetecção de destino ou presumir entrega da memória. Endpoint privado, matching de chave/região, acesso ao modelo e egress efetivos NÃO verificados nesta revisão; a documentação genérica não os prova. Não registrar G3 operacional PASS.

**Timing**: medir ponta a ponta>=19/20 saudáveis<=20s e explicação de falha com meta30s. Orçamentos propostos ferramenta<=12s/provedor<=6s/DB<=5s conforme suporte, timeout positivo explícito e max_retries=0, zero retries aplicativos; limitar restante local quando suportado. [Políticas](https://www.mongodb.com/docs/agentengine/manage/governance/policy-engine.md) checam antes das chamadas, não interrompem in-flight; [invoke](https://www.mongodb.com/docs/agentengine/deploy/invoke-agent.md) distingue timeout cliente de cancelamento servidor. Não exigir nem afirmar garantia/cancelamento global, propagação OE/modelos ou watchdog próprio. Medir overrun/cleanup/wire maxTimeMS; desvio ou caso não executado não vira PASS, segurança não pode ser dispensada.

**Alternatives considered**: manter o requisito global não documentado rejeitado pela revisão explicitamente aprovada; inventar cancelamento ou introduzir serviço externo rejeitados. Waiver constitucional genérico, presumir egress/instalação, trocar modelo/endpoint/memória, ampliar grants e usar aceitação futura como bloqueio circular de código rejeitados. G1/G2 continuam válidos só na configuração/evidência registrada; falha ou mudança exige parar o uso afetado, não contornar. G4-B único checklist LOCAL ainda NOT RUN, sem cloud readiness.

## Evidence ledger and stop conditions

O registro de 2026-10-23 abaixo distingue observação técnica nativa, atestado do mantenedor e pesquisa documental. As seções históricas descrevem revisões anteriores e não anulam essa evidência. Nesta revisão de planejamento não houve nova leitura de catálogo, acesso a secrets, chamada ao provedor, instalação ou alteração operacional; as inspeções limitadas anteriores estão registradas separadamente.

| Gate | Conhecido | Evidência ainda necessária / responsável |
|---|---|---|
| G1 — identity / PASS local | Diagnóstico nativo de 2026-10-23: configuração privada corresponde ao processo TOOL selecionado e à factory real; principal autenticado esperado; grants completos somente find nas duas coleções exatas; URI/papel operacional separado | Concluído para essa configuração local, não cloud nem inspeção do pool do worker longevo. Invalidar se identidade/configuração/grants mudarem. Não repetir T049 nem usar a exceção ampla. |
| G2 — source/index / PASS com atestado | Amostra nativa limitada, schema/tipos/dtype/dimensão observados; definição inicial fornecida; mantenedor aplicou os três filtros e confirmou Ready/Queryable e MongoDB9.0.4 | Evidência administrativa final é atestado do mantenedor, não listagem independente. Amostra não aleatória não prova uniformidade, cobertura global ou sucesso de busca; filtros reais e compatibilidade servidor/consulta serão testados em G4-B. |
| G3 — documented embedding path selected/approved | Origem Load Sample Dataset corroborada: plot → voyage-3-large,2048,binData; FLOAT32 observado. Cliente oficial voyageai==0.5.0 e query documentados/selecionados pela decisão acima | Resolução/import/runtime, matching endpoint/chave/modelo, binding/segregação e egress/conectividade efetivos serão comprovados durante implementação/antes do aceite em G4-B; nenhum PASS operacional presumido. Não pedir/ler secrets nem copiar memória. |
| G4-A — documentary feasibility, revised local scope | App/tool/checkpointer, PyMongo, cliente oficial e caminho build/dependências/secrets/egress documentados; garantia global retirada por aprovação explícita | Nenhum bloqueio pré-código por ausência de cancelamento/deadline global. Isto não prova instalação/entrega/rede; discrepâncias reais param uso/aceite afetados. Orçamentos e limites continuam explícitos. |
| G4-B — single LOCAL acceptance checklist / NOT RUN | Matriz futura definida; nenhum sucesso semântico nativo observado | Durante/após implementação: versões resolvidas, segregação/binding/egress/conectividade, busca real e filtros, falhas sanitizadas, estado/segurança/regressão/relevância/tempos. Bloqueia aceitação final, não autorização pré-código. |

G1/G2 estão resolvidos no escopo indicado; seleção G3 e caminho documental G4-A aprovados no plano local revisado. T010/T011 conferem o registro “sim, aprovo”, sem novo loop. G4-B permanece NOT RUN até implementação e validação nativa autorizadas; não exigir resultados futuros para liberar código. Erros de resolução/acesso/segurança impedem uso/aceite do item afetado, não autorizam contorno. Sem repetir “A”, a exceção histórica, B1 ou T049 de movies. Nenhuma tarefa marcada ou implementação executada nesta revisão.

## Evidence update — 2026-10-23 (authoritative current checkpoint)

G1/G2 e fatos observados abaixo continuam autoritativos nos limites indicados. O status
de candidato/bloqueio dos subitens G3/G4-A pertence ao checkpoint ANTERIOR à aprovação
“sim, aprovo”; para a decisão normativa atual, usar a seção Approved local simplification
e o ledger acima. Nenhuma observação técnica antiga foi convertida em sucesso operacional.

### G1 — native metadata verification

Depois do ajuste manual de grants informado pelo mantenedor, um diagnóstico isolado selecionou um único processo TOOL da stack existente e usou seu interpretador/ambiente. Comparações privadas ficaram em memória; saída somente categorias/booleanos. A factory `_get_movie_client` confirmou a identidade esperada, e `connectionStatus(showPrivileges:true)` mostrou exatamente `find` em `sample_mflix.movies` e `sample_mflix.embedded_movies`, sem wildcard, recursos ou ações extras. Configuração movie correspondeu ao arquivo privado e permaneceu distinta da operacional (serviço local nativo). Não houve documento lido nessa checagem, write probe, alteração ou restart. É prova de uma conexão nova nessa configuração, não do heap/pool longevo ou de cloud.

### G2 — bounded inventory and manual preparation receipt

Após reconfirmar G1, leitura autorizada dos primeiros100 documentos em ordem natural, mais um sentinela para detectar corte, projeção positiva, cursor fechado e maxTimeMS5000 dentro de CSOT limitado. Há mais documentos; amostra não aleatória/não exaustiva. Segunda leitura limitada dos mesmos primeiros100 decodificou internamente o campo vetorial; nenhum texto de catálogo, ID, URL ou vetor foi emitido. Inventário em [data-model.md](data-model.md).

Mantenedor forneceu definição inicial de `plot_vector_index` com vector path `plot_embedding_voyage_3_large`, numDimensions2048 e cosine. Depois do inventário, recebeu mapeamento exato e confirmou aplicação MANUAL dos campos filter `genres`, `year`, `imdb.rating`, MongoDB9.0.4 e, finalmente, Ready/Queryable. Aceito como atestado sanitizado de preparação externa na mesma coleção/cluster; não houve listagem administrativa independente ou consulta vetorial. A identidade runtime não recebeu grants de gestão. Mudança de coleção/índice/definição/status invalida readiness até reconfirmação.

### G3 — provenance and existing configuration decision (prior checkpoint; candidate status superseded above)

Mantenedor confirmou Load Sample Dataset do Atlas. A [documentação oficial sample_mflix](https://www.mongodb.com/docs/atlas/sample-data/sample-mflix/) explicita que `plot_embedding_voyage_3_large` contém embeddings2048 de `plot` gerados com `voyage-3-large` e convertidos em binData. Amostra:98 FLOAT32/2048/padding0 decodificados, zero inválidos; norma L2 aproximadamente1 (1.000000065–1.000000309). Essa observação não prova transformação de normalização universal. `input_type` histórico, versão do carregamento e pré-processamento detalhado não foram documentados e não serão inventados. A documentação de embeddings declara compatibilidade técnica com/sem input_type; isso não prova o valor histórico.

Decisão explícita do mantenedor: conservar `VOYAGE_API_KEY` e destino `VOYAGE_URL` já configurados, chave informada como criada no Atlas. Não solicitar valores novamente, publicar host privado, auto-rotear a outro destino, ler/copiar secrets da memória ou alterar seu voyage-4-large/1024. Essa decisão não comprova entrega ao TOOL nem autorização/egress efetivos.

Candidato documental: `voyageai==0.5.0`, API oficial >=0.3.7; [metadados versionados](https://pypi.org/pypi/voyageai/0.5.0/json) declaram Python>=3.9,<3.15. É candidato para runtime3.11–3.14, não pacote instalado/aprovado nem suporte irrestrito ao >=3.11 do projeto. [Cliente versionado](https://raw.githubusercontent.com/voyage-ai/voyageai-python/v0.5.0/voyageai/client.py) e [API oficial](https://www.mongodb.com/docs/voyageai/api-and-clients.md) documentam api_key/base_url/timeout/max_retries. Query: voyage-3-large, input_type=query, output_dimension2048, output_dtype=float, truncation=false, retries0, timeout positivo<=6s e<=prazo restante. Sem nova dependência selecionada/instalada, endpoint alternativo ou chamada para testar a chave nesta revisão.

Manifesto público atual declara apenas LLM_API_KEY/MOVIES_MONGODB_URI no TOOL; voyageai não é dependência direta. Isso não prova ausência real do segredo, mas impede assumir que a configuração da memória basta. Futuro desenho precisa vincular os valores existentes somente ao sandbox necessário pelo mecanismo oficial, sem upload/restart nesta revisão; isolamento é por sandbox, não por ferramenta. Egress legado lista api.openai.com:443, não comprova destino semântico. Nenhum hostname será adivinhado ou allowlist ampliada automaticamente.

### G4-A — documented limitation, not platform impossibility (historical hard-deadline assessment)

Pesquisa read-only de dois subagentes nesta revisão confirmou build/dependências pelo fluxo CLI e limites das APIs documentadas:

- [Governance policies](https://www.mongodb.com/docs/agentengine/manage/governance/policy-engine.md): OE verifica duração antes de tool/LLM; **não interrompe chamada já em andamento** e pode exceder cap por uma chamada. MAX_EXECUTION_DURATION_MS não comprova hard deadline30s.
- [Invoke/cancellation](https://www.mongodb.com/docs/agentengine/deploy/invoke-agent.md): timeout do cliente fecha somente sua conexão; execução continua. Cancelar sessão cancela chamadas e teardown dos sandboxes, mas é ação explícita com efeitos na sessão, não scheduler global documentado. Ferramentas síncronas em threads não são interrompíveis enquanto rodam; assíncronas recebem CancelledError no próximo await.
- [SDK](https://www.mongodb.com/docs/agentengine/sdk/python/packages/agent-engine-sdk-langgraph/docs/api.md): timeout de App.tool é por chamada; finish_session permite ao turno atual terminar normalmente. [Drain](https://www.mongodb.com/docs/agentengine/sdk/python/packages/agent-engine-runner-shared.md) deadline_at_ms limita drenagem após cancelamento, não o turno original.
- Não se comprovou API pública suportada que propague prazo restante do roteamento à resposta final e cancele in-flight garantindo terminal<=30s. Não substituir por watchdog/serviço próprio, timeout isolado ou garantia presumida. Obter contrato oficial verificável ou submeter revisão explícita do requisito/plano ao mantenedor; não relaxar orçamento unilateralmente.
- [Build](https://www.mongodb.com/docs/agentengine/deploy/agent-image.md)/[local](https://www.mongodb.com/docs/agentengine/build/run-local.md) documentam dependências públicas e lockfile frozen; compatibilidade futura exige manifest/lock consistentes. [Egress](https://www.mongodb.com/docs/agentengine/network-egress.md) é por sandbox e aplicado no deploy; [limitações](https://www.mongodb.com/docs/agentengine/reference/limitations.md) não oferecem isolamento de secret/rede por ferramenta. Nenhuma política/secret/lock foi alterada.

**STOP histórico, anterior ao “sim, aprovo”**: naquele checkpoint G3 era parcial/G4-A BLOCKED e faltava aprovação. A decisão atual acima supera esse bloqueio de planejamento, não as limitações técnicas observadas; G4-B continua NOT RUN. Evidências G1/G2 nunca autorizam infraestrutura. Os parágrafos G3/G4-A deste checkpoint preservam a trilha de auditoria, não são gates normativos atuais.

## R1 — Native architecture

**Decision**: manter um agente, ferramentas `App.tool`, wrappers auditados e checkpointer nativos existentes. Desenho semântico separado do fluxo tradicional, sem serviço externo próprio.

**Rationale**: [getting started](https://www.mongodb.com/docs/agentengine/get-started/), [agent contract](https://www.mongodb.com/docs/agentengine/reference/agent-contract.md) e [SDK API](https://www.mongodb.com/docs/agentengine/sdk/python/packages/agent-engine-sdk-langgraph/docs/api/) documentam Python >=3.11 e interfaces nativas. [Local](https://www.mongodb.com/docs/agentengine/build/run-local.md), [build](https://www.mongodb.com/docs/agentengine/deploy/agent-image.md), [secrets](https://www.mongodb.com/docs/agentengine/deploy/provision-secrets.md) e [egress](https://www.mongodb.com/docs/agentengine/network-egress.md) cobrem o contêiner, não certificam qualquer biblioteca nova. Configuração declarada não comprova rede acessível. Public Preview não equivale a prontidão de produção.

**Alternatives considered**: backend/frontend/proxy próprio, MCP de produção e segundo agente rejeitados pela constituição. Nenhuma dependência de embedding implicitamente aprovada pelo starter.

## R2 — Official driver and fixed pipeline

**Decision**: manter `pymongo>=4.11,<5` dentro da exceção constitucional; propor `Collection.aggregate` com pipeline controlado somente leitura. Sem `$out`, `$merge`, `$lookup`, `$unionWith`, comandos arbitrários ou gestão de índice.

**Rationale**: [PyMongo aggregation](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/aggregation/) e [API 4.18.3](https://pymongo.readthedocs.io/en/4.18.3/api/pymongo/collection.html) documentam aggregate, maxTimeMS, batchSize e fechamento de cursor. [Metadados oficiais PyPI 4.18.3](https://pypi.org/pypi/pymongo/4.18.3/json) identificam MongoDB Python Team e Python>=3.9, incluindo3.11. Essa versão é referência documental dentro do intervalo, não versão instalada observada ou pin selecionado.

**Alternatives considered**: driver alternativo e exigência de tutorial nominal PyMongo/Agent Engine rejeitados; B1 já aposentado. Instalar/atualizar pacote agora está fora do escopo.

## R3 — Search/index/filter behavior

**Decision**: usar o índice existente com G2 concluído pelo inventário e atestado acima; `$vectorSearch` primeiro, queryVector explícito compatível e filtros solicitados como pré-filtros indexados. ANN inicial `numCandidates=20*limit`, no máximo200; sem tuning automático ou alteração de índice.

**Rationale**: [stage](https://www.mongodb.com/docs/vector-search/query/aggregation-stages/vector-search-stage/) documenta posição inicial, dimensões compatíveis, numCandidates e operadores limitados. [Index type](https://www.mongodb.com/docs/vector-search/indexes/vector-search-type.md) distingue vector/filter, numDimensions, similarity e queryable. Exemplos oficiais de embedded_movies usam2048 dimensões, mas NÃO provam a configuração deste catálogo. Gênero AND pode usar conjunções de igualdade suportadas; não presumir `$all`. Ano/IMDb preservam `$gt`/`$gte`/`$lt`/`$lte`; OR usa combinação suportada. Campo não indexado para filtro obrigatório bloqueia a combinação: não omitir filtro nem substituí-lo por pós-filtro limitado que falseie topK.

Índice ausente/nome incorreto pode aparentar zero resultados; readiness deve ser comprovada separadamente. Não solicitar permissões de listagem/gestão à identidade find-only. Obter evidência do mantenedor e invalidar readiness diante de divergência. Versão do cluster e suporte documental à consulta entram em G2/G4-A; observação real pós-código entra em G4-B.

**Alternatives considered**: AutoEmbed/voyage4, híbrida, regex no fluxo novo, ENN automático, pós-filtro aproximado e fallback tradicional rejeitados nesta entrega. Regex tradicional permanece intacta.

## R4 — Query embeddings: official client selected

**Decision**: gerar apenas vetor transitório da descrição com voyage-3-large/query/2048/float/truncation=False; cliente oficial voyageai==0.5.0 selecionado/aprovado documentalmente em2026-10-23, sem instalação agora. Manter chave/destino existentes por api_key/base_url explícitos; ausência/incompatibilidade => indisponível, não fallback/autodetecção. Não escrever vetores, trocar modelo do catálogo ou reconfigurar memória.

**Rationale**: [modelos](https://www.mongodb.com/docs/voyageai/models/) e [text embeddings](https://www.mongodb.com/docs/voyageai/models/text-embeddings/) descrevem voyage-3-large multilíngue, input_type=query/document, dimensão padrão1024 e opções256/512/1024/2048. Não assumir2048 pelo nome do campo, nem1024 pelo default. Exigir parâmetros explícitos compatíveis, valores finitos e dimensão exata; desabilitar truncamento do provedor.

[API and clients](https://www.mongodb.com/docs/voyageai/api-and-clients/) documenta cliente oficial voyageai>=0.3.7 para Atlas Embedding/Reranking API e endpoint ai.mongodb.com/v1/embeddings, variantes geográficas, timeout e retries explícitos. Com os metadados/API versionados e proveniência acima, fundamenta a seleção documental; NÃO prova acesso ao modelo nesta conta/endpoint nem resolução conjunta do sandbox. Esses resultados integram G4-B antes do aceite. Configuração da memória VOYAGE_API_KEY/VOYAGE_URL não deve ser lida, copiada, alterada ou presumida suficiente; usar valores já existentes pelo mecanismo oficial no TOOL quando autorizado, sem novos pedidos.

**Alternatives considered**: reutilizar embedding de memória, trocar para modelo atual recomendado, inferir modelo pela dimensão e biblioteca HTTP não verificada rejeitados. Nenhum fallback entre modelos/provedores/endpoints.

## R5 — Session, grounding and failures

**Decision**: contexto semântico separado, confirmado somente após resultado real `ok`/`empty`; inválido/indisponível não sobrescrevem estado. Reset limpa diretamente. Perfis explícitos indisponíveis em cinema/misto; extração automática inalterada.

**Rationale**: preserva FR-005/FR-006 e FR-009–FR-012 e guards nativos existentes. U1 exige ID/título e plot recuperado utilizáveis antes da apresentação semântica: excluir plot ausente/null/não string/vazio/somente whitespace, sem coerção/fabricação de enredo ou afinidade. Preservar ordem relativa dos elegíveis, informar shortfall/empty após descarte, sem fallback, refill query ou aumento do limite para repor candidatos. Outras ausências explícitas e comportamento tradicional de metadados permanecem inalterados. Relevância fraca exige plot utilizável, não equivale a plot ausente.

Manter descrição2000 caracteres, orçamentos propostos ferramenta12s/provedor6s/DB5s segundo comportamento suportado, timeouts explícitos e zero retry aplicativo; fechar cursor e sanitizar exceções. Meta medida ponta a ponta saudável>=19/20<=20s e falha30s, não garantia rígida/cancelamento servidor. G4-A tem caminho documental revisado; G4-B comprovará resolução/segregação/egress/funcionamento e tempos reais durante/após implementação antes do aceite. Não declarar precisão por score nem PASS por documentação.

**Alternatives considered**: critérios compartilhados com tradicional, perfil persistente, commit antes da consulta, apresentar candidato sem plot e preenchimento com conhecimento do modelo rejeitados. A regra U1 não redefine elegibilidade tradicional.

## R6 — Images

**Decision**: texto apenas. Imagem só será habilitada com documentação oficial específica e demonstração no chat nativo, referência segura do registro e tratamento de falha.

**Rationale**: material consultado não estabeleceu renderização nativa de pôster. Artefatos/tool responses não provam renderização de imagem. Não buscar, baixar, proxyar ou enriquecer pôsteres.

**Alternatives considered**: UI própria, Markdown presumido, downloader e API de imagem rejeitados. Ausência de imagem não bloqueia busca principal.

## FR-017 — Required inventory before manual index guidance

Solicitar evidência sanitizada com data, namespace e método: caminhos exatos; tipos BSON/arrays; ausentes/null/inválidos; amostra limitada e cobertura; relações aninhadas; título/identidade/plot; gêneros/ano/IMDb; campos vetoriais e dimensões; referência opcional de imagem. Não imprimir vetores completos. Amostra não prova uniformidade global; registrar limitações e normalizar defensivamente.

Cruzar inventário com índice efetivo: campos vector, filter e apenas retornados. Esse cruzamento ocorreu no checkpoint2026-10-23 e fundamentou a adição manual dos três filtros atestada acima, preservando métrica/dimensão/vetores. Não emitir novos ajustes com campos adivinhados nem gerir índice pelo runtime.

## Security evidence procedure (normative; G1 completed in checkpoint above)

[connectionStatus](https://www.mongodb.com/docs/manual/reference/command/connectionStatus/) documenta `showPrivileges:true`. Prova deve corresponder à identidade efetivamente resolvida por MOVIES_MONGODB_URI no sandbox, incluindo concessões herdadas. Não publicar usuário/host/URI/segredo; manter atestado sanitizado. Conexão MCP ou identidade de inspeção não prova grants nativos. Não tentar escrita para provar ausência de permissão. Sem evidência suficiente, parar sem leitura semântica.

## Documentation execution record — approved simplification, 2026-10-23

- Constituição lida PRIMEIRO e mantida byte a byte v4.0.0; nenhuma emenda/waiver necessária. Fluxos agent/prompt e hooks inspecionados antes do setup. Setup oficial executado com --json após conferir o script: plano já existente preservado, sem cópia de template; FEATURE_SPEC/IMPL_PLAN/SPECS_DIR apontam feature002, BRANCH JSON vazio, branch Git efetivo master inalterado.
- Pesquisa direta somente de documentação pública oficial/API versionada: Agent Engine getting-started/build, Voyage API/text embeddings, metadados0.5.0/cliente versionado, políticas/invoke. Sem subagentes novos ou consulta ao endpoint privado; documentação não foi confundida com resolução/binding/rede nativos.
- Nove Markdown existentes revisados in-place: spec, plan, research, data-model, contrato semântico, quickstart, tasks, checklist de requisitos e contexto Copilot. Referência gerenciada ao plano conferida/preservada; atualização manual por patch, sem rodar atualizador opcional. Nenhum template substituído ou tarefa regenerada/marcada; cláusulas conflitantes emendadas pela aprovação exata “sim, aprovo”2026-10-23.
- Auditoria documental passou:55 IDs únicos/sequenciais desmarcados, formato estrito/caminho por tarefa, mesmas histórias e13[P] nos IDs originais; cobertura17FR+8SC;51 links locais/6 âncoras existentes; whitespace direto limpo;16 itens de qualidade mantidos e7 itens de aceitação LOCAL desmarcados/NOT RUN. Primeiro validador auxiliar rejeitou T051 por aceitar somente subdiretórios, embora README da raiz seja válido; corrigido o validador, não a tarefa, e auditoria repetida com sucesso.
- Diagnósticos do editor limpos nos nove documentos. git diff --check passou, mas o workspace está não rastreado: esse comando não cobre sozinho os Markdown; a checagem direta de whitespace/links/formato acima cobre os arquivos editados. Comparação SHA256 com baseline confirmou constituição, feature-state e cinco templates inalterados (7 arquivos); não é alegação de hash de secrets ou de runtime.
- Hooks YAML parseados: before_plan=0; after_plan somente agent-context/speckit.agent-context.update, habilitado/opcional/condition=null, anunciado como opcional, não executado. Nenhum hook obrigatório. Referência do contexto já aponta para o plano revisado.
- NÃO executados: código/implementação, testes aplicativos/nativos/provedor/DB, leitura de secrets/ambiente privado, instalação/resolução/build, start/stop/restart/deploy ou mutação de catálogo/índice/roles/rede/infra. G1/G2 não repetidos; G4-B permanece NOT RUN. Handoff de implementação é separado e não exige repetir a aprovação documental; operações seguem autorização separada.

## Planning execution record — historical initial delivery

- Setup executado anteriormente: `.specify/scripts/bash/setup-plan.sh --json`; feature002/template. BRANCH retornou vazio; `git branch --show-current` confirmou master, sem troca de branch. `git status --short` e `command -v jq` também executados.
- Inspeções de governança, scripts, fontes existentes e manifests; pesquisa oficial acima. Nenhum subagente utilizado.
- Não executados: testes semânticos, leitura semântica, instalação, build, restart, deploy, alterações de catálogo/índice/roles/rede/secrets. T049 não foi repetido.
- Artefatos são condicionais; não declarar todos os NEEDS CLARIFICATION resolvidos, inventário verificado ou plano aprovado.
- Atualizador documental executado com Python de sistema3.9.6; pulou atualização porque PyYAML não está disponível. Nenhuma dependência instalada. Referência gerenciada atualizada por patch mínimo preservando as demais regras. Esse interpretador auxiliar não é escolha do runtime Agent Engine>=3.11.

## Historical planning revision — 2026-10-22, U1 / I1

- Constituição lida primeiro; before_plan sem hooks. Setup inspecionado: preserva plano existente, sem cópia de template. Backup integral dos Markdown em memória do processo antes do setup; comparação após execução confirmou conteúdo byte a byte preservado e 55 IDs desmarcados. JSON retornou FEATURE_SPEC/IMPL_PLAN/SPECS_DIR da feature002, BRANCH vazio; branch Git efetivo master, inalterado.
- Duas frentes de pesquisa read-only foram enviadas em paralelo para revisão de documentação oficial: (1) viabilidade G4-A deadline/runtime/dependências/secrets/egress; (2) limites vector/embedding e grounding U1. Não há ferramenta de subagentes disponível; revisão direta é a limitação registrada, não um despacho de agentes inventado.
- Guia oficial confirma Python>=3.11 e fluxo CLI; SDK documenta App.tool timeout e wrappers auditados, não estabelece por isso deadline global de conversa. Egress é por sandbox e configuração declarada não prova aplicação/acesso; nenhuma política foi inspecionada ou alterada. G4-A continua BLOCKED, sem afirmar que mecanismo global é impossível.
- Vector Search oficial confirma estágio inicial, filtros indexados, projeção sem vetores e limite de candidatos; API Voyage documenta timeout/retries explícitos e endpoint compatível com região da chave. Exemplos não comprovam grants, campos, índice, modelo/dimensão ou cliente final deste ambiente: G1/G2/G3 continuam BLOCKED. U1 é decisão aprovada de apresentação, não evidência de uniformidade do catálogo.
- Artefatos detalhados revisados in-place e 55 tarefas existentes preservadas, inclusive dependências/claúsulas aprovadas. G4-A pré-código separado de G4-B pós-implementação NOT RUN; aprovação U1/I1 não é aprovação do plano para código.
- Atualizador oficial de contexto executado com caminho exato specs/002-semantic-movie-search/plan.md e venv auxiliar existente/configurada (Python3.13.13), sem instalação. Sucesso explícito confirmado e conteúdo externo ao bloco gerenciado preservado byte a byte pelo script. Esse Python auxiliar não comprova versão do runtime semântico.
- Checagens documentais: 55 IDs únicos/sequenciais T001–T055, zero caixas marcadas, 13[P], cobertura FR-001–FR-017/SC-001–SC-008; alvos relativos Markdown existentes, ausência de whitespace no fim de linhas e git diff --check limpo; branch master inalterado. Diagnósticos do editor sem erros nos oito arquivos. Uma checagem auxiliar de newline EOF não passou porque seis documentos preservam a ausência de newline final; não é falha funcional nem teste aplicativo, e não motivou reformatar artefatos.
- after_plan relido e parseado: somente hook opcional habilitado agent-context / speckit.agent-context.update, condição null. Stanza opcional será reportada; nenhum hook obrigatório e nenhum before_plan executável.
- Nenhum acesso a fontes de aplicação, segredos/ambiente privado, provedor, banco ou runtime; nenhum teste aplicativo, embedding, instalação, build, restart, deploy ou mutação de infraestrutura/índice. Imagens seguem text-only. T049 não repetido.
