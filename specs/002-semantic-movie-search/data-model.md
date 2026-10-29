# Data model — conditional semantic search design

## Active embedding migration — 2026-10-27

The active semantic path uses `voyage-4-large` query embeddings with 2048
finite float values and `truncation=False`. New document embeddings belong in
`plot_embedding_voyage_4_large`; `plot_embedding_voyage_3_large` remains
historical evidence and is not queried by the implementation. The corresponding
vector index must be prepared and verified manually before native acceptance.

**Status**: desenho local revisado pela aprovação exata “sim, aprovo” de2026-10-23, conforme [plano](plan.md). G1/G2 preservados com amostra limitada/atestado; caminho de embedding documentado selecionado. G4-B é aceitação nativa obrigatória NOT RUN, não bloqueio circular pré-código. Esta invocação é documental, sem implementação ou alteração de esquema/dados.

## FR-017 — Observed source inventory, 2026-10-23

Namespace sample_mflix.embedded_movies no mesmo cluster atestado pelo mantenedor. Diagnóstico no interpretador/ambiente TOOL após reconfirmar G1; find com projeção positiva, limite101 (100+sentinela), maxTimeMS5000, CSOT limitado e cursor fechado. Primeiros100 em ordem natural analisados; existe continuação. Segunda leitura dos primeiros100 para decodificação interna de vetores. Amostra não aleatória/não exaustiva: não prova uniformidade, cobertura global ou alinhamento das ausências entre campos. Nenhum vetor/texto/ID/URL bruto emitido.

| Caminho exato | Tipo observado | Presença/ausências e limites da amostra | Papel |
|---|---|---|---|
| _id | ObjectId | 100/100 | identidade/retorno |
| title | string | 100/100 não vazios;4–36 caracteres | apresentação |
| plot | string | 98/100 não vazios;50–203 caracteres;2 ausentes | apresentação obrigatória e texto-fonte documentado dos embeddings |
| fullplot | string | 96/100;4 ausentes;126–1838 caracteres | observado, NÃO fallback nem campo ativo |
| genres | array de strings | 100/100;1–3 itens,285 elementos sem inválidos | filtro AND/OR e apresentação |
| year | inteiro decodificado, sem distinguir aqui BSON int32/int64 | 100/100;1914–1975;zero inválidos na amostra | filtro de intervalo e apresentação |
| imdb.rating | double no objeto aninhado imdb | 100/100;4.3–8.3;zero inválidos | filtro de intervalo e apresentação |
| plot_embedding_voyage_3_large | BSON binData subtipo9, FLOAT32 | 98/100;2 ausentes;2048 dimensões/padding0 em98 decodificados;zero inválidos | vector interno, nunca apresentação |
| poster | string | 92/100;8 ausentes;HTTPS sem credenciais apenas sintaticamente | imagem opcional INATIVA, não prova URL pública/segura/renderizável |

98/100 tinham simultaneamente ObjectId/título/plot utilizáveis. Vetores apresentaram norma aproximadamente1; não inferir normalização global/modelo só disso. Dois plots ausentes reforçam exclusão semântica U1 sem refill/fullplot; regra tradicional permanece. Não houve fullscan.

Definição atual/mapeamento e atestado Ready/Queryable em [contrato](contracts/semantic-movie-tools.md). Proveniência corroborada e parâmetros históricos não conhecidos em [research](research.md).

## Phase 2 — T005 inventory reconciliation, 2026-10-23

Após T004, conferidos o inventário FR-017 acima e o recibo sanitizado G2 já fornecidos pelo mantenedor. Método desta tarefa: cruzamento documental, sem nova inspeção. Ambiente da evidência original: TOOL local/configuração G1, namespace exato no mesmo cluster atestado; primeira leitura limitada a100+sentinela e segunda dos primeiros100 para decodificação vetorial, não amostragem aleatória nem schema completo. Identidade/título/plot, arrays de gêneros, year e imdb.rating aninhado, binData vetorial e poster opcional têm caminhos/tipos/cobertura explícitos na tabela. Não promover o inteiro decodificado de year a um subtipo BSON específico, inferir coincidência das ausências plot/vetor ou tratar sintaxe HTTPS como prova de segurança de imagem.

As contagens de strings/vetores válidos e ausências descrevem somente os100 registros observados; não são garantia global de ausência de null, tipos mistos, strings vazias/whitespace, valores fora de faixa ou vetores inválidos. Normalização defensiva deve cobrir essas categorias mesmo quando não ocorreram na amostra. fullplot permanece inativo/sem fallback; poster inativo. Prova de query/filtros e normalização real continua G4-B NOT RUN. T005 concluída pela conferência da evidência existente, não por fullscan ou nova aceitação.

## SemanticRequest and SemanticCriteria

Representação lógica, não implementação. Entrada controlada e serializável; propriedades desconhecidas inválidas.

| Campo | Tipo / regra |
|---|---|
| description | string com1–2000 caracteres após trim; omitida só em refinamento com tema semântico confirmado; nunca truncar silenciosamente |
| genres | lista de strings não vazias, <=10 itens, cada um<=80 caracteres; aliases já validados no fluxo existente; lista vazia limpa dimensão |
| genre_mode | all/any, padrão all; AND/OR explícito preservado |
| year | dimensão opcional: min/max inteiros1–9999, min_inclusive/max_inclusive booleanos; null limpa dimensão |
| rating | dimensão opcional: min/max finitos0–10, min_inclusive/max_inclusive booleanos; null limpa dimensão |
| requested_limit | inteiro positivo não booleano; padrão5, efetivo min(solicitado,10); registrar cap |

Dimensão de intervalo é substituída inteira quando fornecida: ambos os extremos e flags. Extremo omitido nessa dimensão vira ausente, não herda extremo antigo. Flags default inclusivas para extremos fornecidos. Min>max ou extremos iguais com exclusão tornam intervalo inválido. Não descartar nota0 por truthiness. Números string/bool, NaN e infinito inválidos. `genre_mode` isolado mantém gêneros confirmados; sem gêneros resultantes é inválido.

Propriedade ausente preserva dimensão em refinamento. Limpar explicitamente não equivale a omitir. Busca nova explícita parte de contexto semântico vazio; refinamento parte somente do contexto semântico. Não importar título/limites tradicionais.

## SemanticSessionContext

- Tema, gêneros/modo, intervalo de ano/nota e quantidade confirmados, somente no estado/checkpointer nativo da conversa, separados de `active_movie_criteria`.
- Sessão antiga sem o campo começa vazia/permissões incertas; não reconstruir pelo perfil persistente.
- Vetores, secrets, URI, erros internos e prova de grants nunca integram contexto de conversa.
- Proposta e confirmado são cópias independentes; não mutar antecipadamente o estado.

| Evento | Transição semântica | Efeito tradicional |
|---|---|---|
| Busca/refinamento validado | criar proposta, sem confirmar | nenhum |
| Retorno real ok | confirmar proposta correlacionada à chamada | nenhum |
| Retorno real empty | confirmar mesmo sem filmes | nenhum |
| Invalid/unavailable | preservar último confirmado | nenhum |
| Reset explícito | limpar tema e dimensões semânticas imediatamente | preservar semântica tradicional existente de reset |
| Nova busca tradicional | não aplicar tema nem sobrescrever critérios tradicionais | comportamento existente |
| Ambiguidade | esclarecer, sem consulta/commit | nenhum |

Alternância de intenção não reativa contexto oculto: retomar tema anterior exige intenção de refinamento semântico suficientemente explícita. Reset impede recuperação do tema inclusive a partir de mensagens antigas.

## RetrievedSemanticMovie

Identidade composta por namespace fixo + identificador serializado. `_id` igual entre coleções não significa mesmo filme. Sem join/enriquecimento.

| Campo lógico | Saída proposta | Caminho observado na amostra G2, sem garantir uniformidade |
|---|---|---|
| source / id | namespace fixo e identificador utilizável, obrigatório | sample_mflix.embedded_movies / _id |
| title | string utilizável<=300 caracteres; obrigatória para apresentação semântica | title |
| plot | string recuperada não vazia após trim, obrigatória; saída<=500 caracteres, sinalizar truncamento | plot; nenhum fallback para fullplot |
| genres | <=10 strings de até80 caracteres ou null | genres |
| year | inteiro válido ou null | year |
| imdb_rating | número finito0–10 ou null | imdb.rating |
| semantic_score | número finito de $meta vectorSearchScore, não IMDb/probabilidade | metadado de consulta |
| missing_fields / truncated_fields | listas allowlisted de campos lógicos | normalização local |

Texto de catálogo é dado não confiável, nunca instrução. Antes de apresentar, excluir candidatos sem ID/título utilizáveis ou plot recuperado utilizável: ausente, null, não string, vazio ou somente whitespace. Não converter valores não string em texto nem inventar plot/afinidade. Preservar ordem relativa dos elegíveis e calcular returned_count/shortfall após exclusão; se nenhum restar, empty de leitura bem-sucedida, não unavailable. Sem fallback, consulta de reposição ou aumento do limite para repor descartes. Outros metadados inválidos viram ausência explícita; ausente não satisfaz filtro explícito. Validação defensiva final descarta divergências sem relaxar filtros. Esta regra é somente semântica: o tratamento tradicional de metadados ausentes permanece inalterado.

Nenhum vetor/documento bruto/campo fora da projeção positiva é retornado. Imagens ausentes do contrato ativo; extensão futura exige evidência nativa e URL pública HTTPS segura no registro, sem backend fetch/enriquecimento.

## QueryEmbedding and ReadinessEvidence

Vetor transitório interno: voyage-3-large, dimensão2048 verificada G2/proveniência, números finitos, output_dtype=float e input_type=query, truncation=False; sem persistência/log do vetor. Dimensão certa isolada não prova modelo compatível. Cliente oficial selecionado voyageai==0.5.0, API documentada e Python semântico >=3.11,<3.15; resolução conjunta/import/runtime e entrega/egress reais pendentes da checklist G4-B. Chave/destino EXISTENTES VOYAGE_API_KEY/VOYAGE_URL preservados por binding explícito api_key/base_url no TOOL, nunca herdados implicitamente da memória nem auto-roteados. input_type histórico do corpus continua desconhecido; compatibilidade com/sem input_type é documentada, não prova histórica nem novo bloqueio pré-código.

ReadinessEvidence é atestado fora da conversa: ambiente, identidade sanitizada, recursos/ações efetivos, namespace/cluster, índice/queryable/mapeamentos, proveniência/modelo/dimensão/dtype, cliente/versões e endpoint/egress. Mudança em identidade/configuração/índice exige nova verificação; atestado não pode sobreviver silenciosamente à mudança. Não autoriza gestão runtime.

Separar G4-A, caminho documental API/runtime/build/secrets/egress já definido no plano revisado, de G4-B com versões realmente resolvidas, segregação/binding/egress/conectividade e resultados nativos durante/após implementação. Readiness operacional exige prova antes do uso afetado/aceite, não impede escrever código ou testes isolados por faltar teste futuro. Não persistir um PASS inventado em configuração/estado. Mudança dos grants/índice invalida G1/G2. Meta ponta a ponta saudável>=19/20<=20s e falha30s medida, sem garantia/cancelamento global; orçamentos propostos ferramenta12s/provedor6s/DB5s, timeouts explícitos conforme suporte e zero retries aplicativos. Nenhum secret/endpoint foi lido ou solicitado nesta revisão.

## SemanticOutcome and invariants

Estados `ok`, `empty`, `invalid`, `unavailable`, conforme [contrato](contracts/semantic-movie-tools.md). Correspondência fraca é distinção de apresentação apoiada no plot, não limiar global inventado ou falha técnica. Erros não confirmam contexto; reset é operação de estado.

Um pedido propõe um contexto; uma leitura produz zero a10 filmes ordenados por similaridade; cada filme remete a um registro semântico. Critérios tradicionais e semânticos separados, sem perfil cinematográfico explícito persistente. Memória/extração automática nativa e identidade operacional permanecem fora destas entidades.