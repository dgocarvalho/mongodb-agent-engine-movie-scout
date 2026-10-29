# Feature Specification: Busca semântica de filmes pelo enredo

**Feature Branch**: `master` (branch atual; nenhum hook de criação de branch registrado)

**Created**: 2026-10-22

**Status**: Revisão local aprovada documentalmente em2026-10-23 (“sim, aprovo”); G1/G2 preservados no escopo registrado, caminho documentado selecionado no plano; aceitação nativa G4-B NOT RUN. Esta invocação não implementa nem opera serviços.

**Input**: User description: "Vamos adicionar a feature para buscar semantica. Ja existe hoje um vector index, chamado plot_vector_index, tipo vectorSearch, index fields plot_embedding_voyage_3_large na collection [embedded_movies]. A ideia e apenas permitir buscar filme de forma semanatica. Nao vamos mudar nenhuma funcionalidade existente, apenas adicionar e alterr o minimo necessario para isso. Se possivel, utilizando o agent engine, seria legarl trazer e apresentar a imagem do filme tambem, epnas se for recurso nativo do chat da plataforma"

**Governance**: A constituição vigente é v4.0.0. Na clarificação de 2026-10-22, o
mantenedor respondeu “A” e aprovou uma emenda limitada: autorizar também
`sample_mflix.embedded_movies` exclusivamente para busca semântica somente leitura,
em ferramenta nativa com PyMongo oficial, exigindo privilégios mínimos verificados
nas duas coleções, sem escrita, alteração automática de índice ou nova infraestrutura.
Esta aprovação foi formalizada na [constituição v4.0.0](../../.specify/memory/constitution.md)
em 2026-10-22, com sincronização dos templates e orientações. O bloqueio de autorização
da fonte está resolvido; o plano revisado registra a aprovação local de2026-10-23,
as evidências técnicas e os limites ainda sujeitos à aceitação nativa. Nenhum suporte ou acesso
à nova coleção é comprovado apenas pela emenda.
A exceção oficial-PyMongo já aprovada permanece válida em seu escopo, sem reabrir B1.
Nenhuma execução, alteração de credenciais, catálogo, índices ou infraestrutura está
autorizada pela criação desta especificação.

**Decisão aprovada2026-10-23**: resposta exata **“sim, aprovo”** à simplificação para
LOCAL TEST DEVELOPMENT. SC-005 passa a meta medida, sem garantia global rígida30s
ou promessa de cancelamento de trabalho no servidor. Mantêm-se limites de entrada/saída,
timeouts explícitos de provedor/MongoDB, zero retries aplicativos e segurança integral.
Constituição v4.0.0 inalterada: compatibilidade oficial documentada antes do código,
validação nativa antes do aceite. Nenhuma emenda é necessária para retirar uma garantia
que não é constitucional. Seleção documentada no [plano](plan.md); comprovações de
resolução, entrega/segregação de secrets, endpoint/egress/conectividade e funcionamento
ocorrem durante implementação e são obrigatórias antes de aceite pela checklist única
G4-B, atualmente NOT RUN. Não são resultados circulares pré-código nem PASS presumido.
As55 tarefas existentes permanecem desmarcadas; esta aprovação permite revisão documental
e handoff para workflow separado, não implementação/runtime nesta invocação. Não pedir
a mesma aprovação novamente; restart continua exigindo autorização operacional separada.

**Checkpoint2026-10-23**: [research.md](research.md) registra metadados nativos G1,
inventário limitado G2 e atestado do mantenedor sobre filtros/Ready/Queryable/MongoDB9.0.4.
Proveniência oficial plot/voyage-3-large/2048 corroborada após confirmação Load Sample Dataset.
Chave/endpoint existentes preservados, sem nova solicitação. Caminho de query documentado
selecionado/aprovado, não instalado nem validado nativamente; binding/egress reais pendentes.
Política de duração não interrompe in-flight. A revisão aprovada substitui a garantia de
tempo por meta operacional medida, preservando fontes, segurança, histórias e IDs das tarefas.

## Clarifications

### Session 2026-10-23

- Q: Aprova simplificar o plano para desenvolvimento/teste LOCAL, trocando a garantia global30s por meta medida, mantendo timeouts explícitos/limites/zero retries, selecionando o cliente oficial documentado e verificando dependências/binding/egress/funcionamento durante implementação antes do aceite? → A: **sim, aprovo**. Escopo: revisão documental, sem executar código/runtime nesta invocação; plano registra a seleção e checklist nativa obrigatória NOT RUN, sem dispensar a constituição ou autorizar restart/infra/cloud.

### Session 2026-10-22

- Q: A busca semântica deve aceitar filtros adicionais de gênero, ano e nota? → A: Sim, os filtros são obrigatórios quando solicitados; se necessário, o mantenedor alterará manualmente o índice existente após receber o mapeamento verificado de campos, tipos e associações. O agente não altera o índice.
- Q: Em qual banco e cluster está embedded_movies? → A: No banco sample_mflix, no mesmo cluster do catálogo atual; somente a coleção muda para embedded_movies.
- Q: Como funciona um refinamento como “agora só depois de 2000” após uma busca semântica? → A: Mantém o tema e atualiza os filtros semânticos na mesma sessão; reset limpa esse contexto, separado dos critérios tradicionais e sem perfil persistente.
- Q: Aprova a emenda para autorizar a nova fonte de filmes? → A: A — autorizar também sample_mflix.embedded_movies exclusivamente para busca semântica somente leitura em ferramenta nativa com PyMongo oficial, com privilégios mínimos verificados nas duas coleções, sem escrita, alteração automática de índice ou nova infraestrutura; formalização constitucional pendente.

**Resolução de governança (2026-10-22)**: a pendência de formalização registrada na
resposta acima foi resolvida pela constituição v4.0.0; a resposta original é preservada
como histórico, sem reabrir a autorização.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Descobrir filmes descrevendo uma história (Priority: P1)

Como pessoa buscando um filme sem saber seu título, quero descrever um tema, situação
ou enredo e receber filmes semanticamente próximos, com uma explicação curta baseada
nos dados recuperados.

**Why this priority**: É o único novo fluxo obrigatório; permite descobrir filmes por
significado, sem depender da ocorrência literal das palavras do pedido no enredo.

**Independent Test**: Em uma conversa nova no chat nativo, enviar uma descrição como
“Busque filmes sobre alguém que descobre viver em uma realidade simulada” e comparar
os resultados com os registros e enredos da fonte semântica aprovada.

**Acceptance Scenarios**:

1. **Given** uma fonte semântica disponível e autorizada, **When** o usuário descreve
   um enredo em português, **Then** recebe até cinco filmes por padrão, priorizados
   por proximidade semântica, sem precisar fornecer um título.
2. **Given** a mesma intenção expressa com palavras diferentes, **When** o usuário
   faz a busca, **Then** a relevância é avaliada pelo significado, sem exigir igualdade
   de listas ou posições entre execuções.
3. **Given** resultados recuperados, **When** o agente recomenda filmes, **Then**
   cada filme e cada fato apresentado correspondem ao registro recuperado; a explicação
   de afinidade é distinguida de metadados factuais.
4. **Given** um pedido de cem resultados, **When** a busca é atendida, **Then** no
   máximo dez filmes são apresentados, com aviso do limite e de eventual falta de opções.
5. **Given** uma busca sem resultados elegíveis ou resultados sem relação clara com
   a descrição, **When** o agente responde, **Then** informa a ausência ou baixa
   correspondência e pode pedir uma descrição melhor, sem inventar filmes nem afirmar
   que uma proximidade numérica garante aderência temática.
6. **Given** uma descrição acompanhada de gênero, ano ou nota IMDb, **When** a busca
  semântica é executada, **Then** todos os filmes apresentados satisfazem as restrições
  explícitas, preservando AND/OR entre gêneros e limites estritos/inclusivos existentes;
  os elegíveis continuam ordenados por proximidade semântica.
7. **Given** suporte insuficiente do índice aos filtros requeridos, **When** a feature
  é preparada para aceitação, **Then** o mantenedor recebe o mapeamento verificado
  necessário para sua alteração manual; o agente não modifica o índice nem omite filtros.
8. **Given** candidatos com ID/título inutilizáveis ou plot ausente, null, não string,
   vazio ou somente whitespace, **When** a lista semântica é normalizada, **Then** esses
   candidatos são excluídos da apresentação, preservando a ordem relativa dos demais;
   informa-se shortfall (ou empty se nenhum elegível), sem fabricar enredo/afinidade,
   fallback ou consulta de reposição. Metadados ausentes no fluxo tradicional mantêm
   o comportamento existente.

---

### User Story 2 - Continuar usando o agente sem regressões (Priority: P1)

Como usuário atual, quero continuar buscando por título, filtrando, pedindo recomendações
bem avaliadas e refinando a conversa com o mesmo comportamento já implementado.

**Why this priority**: O usuário pediu uma adição mínima, sem mudanças nas funcionalidades existentes.

**Independent Test**: Executar a regressão existente e uma sequência intercalando busca
por título, busca semântica e nova busca explícita por título, verificando os critérios
e ferramentas utilizados em cada turno.

**Acceptance Scenarios**:

1. **Given** os cenários atuais de título, filtros, notas e refinamento, **When**
   são repetidos após a adição, **Then** preservam seus contratos, limites e critérios
   de aceitação, inclusive distinção entre vazio e indisponível.
2. **Given** um pedido explícito de busca por título, **When** o agente o atende,
   **Then** não o substitui silenciosamente por busca semântica ou por outra fonte.
3. **Given** uma busca semântica anterior, **When** o usuário inicia uma nova busca
   por título ou pede reset, **Then** a descrição temática não se torna um filtro oculto
   e a busca anterior não sobrescreve os critérios estruturados já confirmados.
4. **Given** uma frase ambígua como “Matrix”, sem intenção suficiente no contexto,
   **When** a rota não puder ser determinada com segurança, **Then** o agente esclarece
   se o usuário deseja título ou semelhança temática, em vez de adivinhar critérios.
5. **Given** uma solicitação cinematográfica ou mista, **When** a busca semântica é
   considerada, **Then** mantém o bloqueio de chamadas explícitas de perfil e não usa
   preferências entre conversas para completar a descrição.
6. **Given** uma busca semântica confirmada sobre viagens no tempo, **When** o usuário
  pede “agora só depois de 2000”, **Then** o tema é mantido e a dimensão de ano é
  substituída pelo limite estrito solicitado, preservando os demais filtros semânticos.
7. **Given** contexto semântico confirmado, **When** uma proposta de refinamento é
  inválida ou a consulta falha, **Then** o último contexto válido não é sobrescrito;
  um reset explícito limpa o contexto semântico e impede sua herança na próxima busca.

---

### User Story 3 - Ver uma imagem quando o chat nativo permitir (Priority: P3)

Como usuário, gostaria de visualizar o pôster do filme junto ao resultado, mas somente
se o próprio chat da plataforma suportar esse recurso sem uma interface adicional.

**Why this priority**: É um complemento opcional e não pode bloquear a busca semântica.

**Independent Test**: Após comprovar suporte nativo, apresentar um resultado com imagem
disponível e outro sem imagem; na ausência de suporte, verificar a resposta textual normal.

**Acceptance Scenarios**:

1. **Given** suporte nativo documentado e demonstrado no chat e uma referência de imagem
   segura no registro recuperado, **When** o filme é apresentado, **Then** sua imagem
   pode aparecer pelo mecanismo nativo, sem frontend, proxy ou serviço adicional.
2. **Given** suporte não confirmado, imagem ausente, endereço inadequado ou falha de
   carregamento, **When** o filme é apresentado, **Then** os dados textuais continuam
   disponíveis, sem imagem inventada ou busca externa de pôsteres.
3. **Given** uma imagem com falha, **When** os resultados textuais são corretos,
   **Then** a busca continua sendo considerada funcional; a imagem permanece opcional.

### Edge Cases

- Descrição vazia, somente espaços ou sem intenção cinematográfica: pedir esclarecimento
  sem executar uma busca ampla arbitrária.
- Descrição excessiva: informar o limite de entrada definido no plano, sem truncar
  silenciosamente elementos essenciais do pedido.
- Nenhum candidato ou poucos candidatos: informar insuficiência sem fabricar substitutos.
  Na apresentação SEMÂNTICA, excluir candidatos sem ID/título utilizáveis ou plot
  recuperado utilizável (ausente/null/não string/vazio/somente whitespace); preservar
  ordem, informar shortfall/empty e não executar fallback ou consulta de reposição.
  Outras ausências ficam explícitas; o tratamento tradicional de metadados não muda.
- Vetores ausentes/inválidos, índice indisponível, incompatibilidade de embeddings,
  erro de autorização, falha do provedor ou timeout: informar indisponibilidade sem
  apresentar o erro como “nenhum filme encontrado” nem expor detalhes privados.
- Similaridade alta, mas aderência temática fraca: não descrever o resultado como
  correspondência exata nem converter score em probabilidade de satisfação.
- Plot contendo instruções maliciosas: tratar como dado não confiável, sem executar
  instruções, revelar segredos ou chamar ferramentas de perfil/escrita.
- Pedido semântico combinado com gênero, ano ou nota: aplicar todas as restrições;
  se o índice ainda não estiver preparado, informar indisponibilidade dessa combinação,
  sem ignorar filtros ou declarar a entrega completa antes da adequação manual e validação.
- Falha semântica seguida de busca tradicional: a capacidade tradicional permanece disponível.
- Imagem externa com redirecionamento suspeito ou endereço privado: não buscar pelo
  backend nem introduzir um downloader; excluir a referência inadequada.

As evidências de aceitação devem identificar a intenção, a fonte realmente consultada,
o resultado observado e a correspondência dos fatos recuperados, usando o ambiente
nativo. Testes sintéticos e dados reais devem ser identificados separadamente.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O agente MUST oferecer descoberta de filmes por descrição de enredo ou
  tema, em português ou inglês, com ordenação por proximidade semântica, não por nota IMDb.
- **FR-002**: A nova busca MUST usar somente a fonte semântica existente aprovada,
  `sample_mflix.embedded_movies`, no mesmo cluster do catálogo atual, sem alterar sua
  coleção ou embeddings; o agente MUST NOT modificar seu índice.
  Eventual adequação do índice cabe exclusivamente ao mantenedor, manualmente.
- **FR-003**: O agente MUST distinguir intenção semântica de busca tradicional e
  esclarecer ambiguidades essenciais, preservando os comportamentos atuais.
- **FR-004**: A busca MUST apresentar cinco resultados por padrão e no máximo dez,
  informando limite aplicado ou insuficiência de opções sem completar artificialmente.
- **FR-005**: Cada filme apresentado MUST corresponder a um registro recuperado;
  na apresentação semântica, ID, título e plot recuperado utilizáveis são obrigatórios.
  Candidatos sem ID/título utilizáveis ou plot ausente, null, não string, vazio ou somente
  whitespace MUST ser excluídos, preservando a ordem relativa dos elegíveis e informando
  shortfall/empty sem fallback ou consulta de reposição. Demais fatos MUST refletir os
  campos disponíveis, com ausências explícitas. Esta elegibilidade é somente semântica;
  o comportamento tradicional de metadados ausentes permanece inalterado.
- **FR-006**: A explicação de relevância MUST ser breve e apoiada no enredo recuperado;
  não deve afirmar que o filme satisfaz detalhes que o registro não sustenta. MUST NOT
  fabricar plot ou afinidade para manter candidato inelegível na apresentação semântica.
- **FR-007**: O agente MUST diferenciar entrada inválida, ausência de candidatos,
  baixa correspondência e falha de consulta/provedor, sem fallback silencioso.
- **FR-008**: O agente MUST limitar entrada e resultados, configurar timeouts explícitos
  de provedor e MongoDB conforme comportamento suportado, manter zero retries aplicativos,
  fechar recursos e sanitizar falhas, sem devolver vetores ou credenciais ao usuário.
  Duração ponta a ponta MUST ser medida conforme SC-005, sem prometer garantia global
  rígida nem equiparar timeout cliente a cancelamento de trabalho no servidor.
- **FR-009**: A nova capacidade MUST manter intactos título, filtros, ranking por nota,
  refinamentos, reset, data e memória não cinematográfica, nos cenários atuais.
- **FR-010**: Busca semântica MUST NOT reutilizar preferências persistentes como
  critérios, salvar explicitamente preferências de cinema ou expor ferramentas de
  perfil em turnos cinematográficos/mistos. Extração automática nativa permanece inalterada.
- **FR-011**: Falhas ou resultados semânticos MUST NOT sobrescrever os critérios
  estruturados da busca tradicional. Mudança explícita de intenção e reset devem ser respeitados.
  Na mesma sessão, refinamentos semânticos MUST manter o tema e substituir apenas as
  dimensões de filtro alteradas, com a mesma semântica de limites do fluxo existente.
  O contexto semântico MUST permanecer separado dos critérios tradicionais, ser confirmado
  somente após consulta bem-sucedida (inclusive vazia) e ser limpo por reset explícito.
  Propostas inválidas ou indisponíveis MUST NOT substituir o último contexto válido.
- **FR-012**: A ferramenta MUST aceitar somente entradas controladas para a operação
  autorizada, sem permitir coleção, índice, comando ou consulta arbitrários pelo usuário.
- **FR-013**: Imagens MAY ser apresentadas exclusivamente quando houver comprovação
  de suporte nativo e referência segura no registro; sem comprovação, a entrega é textual.
- **FR-014**: Ausência ou falha de imagem MUST NOT impedir resultados textuais nem
  causar consultas externas de enriquecimento, geração de pôster ou nova infraestrutura.
- **FR-015**: A documentação de uso MUST incluir exemplos semânticos, diferenças em
  relação à busca por título, filtros, limites, falhas e a condição opcional de imagens.
- **FR-016**: Busca semântica MUST aceitar os filtros existentes de gênero, ano e nota
  IMDb, preservando sua validação, AND/OR e limites estritos/inclusivos, sem ignorar
  restrições nem usar nota como substituto da ordenação semântica.
- **FR-017**: Antes de solicitar uma adequação manual do índice, o planejamento MUST
  apresentar o inventário verificado dos campos da fonte, seus tipos e ausências,
  associando cada filtro ao caminho correto e cada metadado ao campo de apresentação.
  MUST distinguir campos vetoriais, campos de filtro e campos apenas retornados, documentar
  compatibilidade dos embeddings e apontar precisamente as alterações necessárias.

### Key Entities *(include if feature involves data)*

- **Pedido semântico**: descrição livre da intenção cinematográfica, idioma, quantidade
  desejada e filtros opcionais de gênero, ano e nota; não constitui perfil persistente.
- **Contexto semântico da sessão**: tema e critérios confirmados para refinamento
  na conversa atual, separados dos critérios tradicionais; reset os limpa e nenhuma
  preferência entre conversas é usada para reconstruí-los.
- **Filme semântico recuperado**: identidade da fonte, título, enredo e metadados
  disponíveis; pode conter uma referência opcional de imagem. Vetores não fazem parte
  da apresentação ao usuário.
- **Correspondência semântica**: relação ordenada entre um pedido e um filme, acompanhada
  de explicação fundamentada; não é uma nota IMDb nem probabilidade de satisfação.
- **Capacidade nativa de imagem**: evidência de suporte do chat e demonstração de
  apresentação; sua ausência resulta em experiência somente textual.

### Constitutional Constraints *(mandatory)*

- Manter um único agente e execução/orquestração exclusivamente no Atlas Agent Engine,
  sem frontend/backend próprios, agentes adicionais ou serviços de enriquecimento.
- Preservar a busca tradicional em `sample_mflix.movies` e a configuração existente.
- O mantenedor aprovou explicitamente a emenda limitada à leitura semântica de
  `sample_mflix.embedded_movies`, além da fonte tradicional. A constituição v4.0.0
  formaliza essa autorização; evidências oficiais, permissões e validação no runtime
  continuam obrigatórias, sem presumir suporte ou acesso efetivo.
- Preservar `MOVIES_MONGODB_URI` como papel de acesso a filmes e `MONGODB_URI` como
  configuração operacional, sem fallback ou troca de papéis. A escolha de configuração
  para a nova fonte pertence ao plano, após aprovação do escopo.
- A evidência T049 existente prova somente os privilégios da coleção antiga; não prova
  autorização na nova coleção. A ampliação mínima necessária deve ser verificada
  independentemente, sem reutilizar automaticamente a exceção histórica de identidade ampla.
- Nenhuma escrita, geração/regravação de embeddings do catálogo, criação de índice,
  mutação de usuário/papel/rede, upload de segredos ou deploy está incluída nesta feature.
  O mantenedor poderá adequar manualmente o índice existente como preparação externa,
  com base no inventário verificado; isso não autoriza mutações pelo agente ou assistente.
- Verificar no plano dependências, embeddings, permissões e mecanismo nativo opcional
  de imagens com documentação oficial e validação no runtime; sem presunção de suporte.
- Validar dados reais e segurança pelo fluxo nativo e preservar a distinção entre
  validação local e aceitação em ambiente implantado.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Em pelo menos 8 de 10 descrições de referência, cobrindo português e
  inglês e temas realmente representados no catálogo, um avaliador encontra ao menos
  um filme relevante entre os cinco primeiros. Pedidos e critérios de relevância devem
  ser fixados antes de executar a avaliação, sem exigir um título único.
- **SC-002**: 100% dos filmes e fatos apresentados nos cenários de aceitação são
  rastreáveis a registros recuperados; nenhuma ausência é preenchida com fato inventado.
- **SC-003**: 100% dos cenários de regressão anteriores mantêm seus resultados esperados
  e limites funcionais, incluindo memória, refinamento e tratamento de falhas.
- **SC-004**: Em 100% dos testes de quantidade, a lista respeita o máximo de dez e
  comunica corretamente limite e falta de opções.
- **SC-005**: Em pelo menos 95% de 20 pedidos válidos, com dependências saudáveis,
  medir resposta final em até20s (>=19/20). Nos testes de falha, registrar explicação
  sanitizada e tempo total, com meta operacional de até30s, não garantia rígida/global
  ou cancelamento servidor. Registrar todo overrun/NOT RUN e avaliá-lo no aceite local,
  sem excluir casos silenciosamente ou marcar meta não atingida como PASS; timeouts
  explícitos, limites, zero retries e segurança permanecem obrigatórios.
- **SC-006**: 100% dos cenários de entrada inválida, indisponibilidade, ausência de
  candidatos e conteúdo adversarial têm resultado registrado e sem vazamento de segredos,
  chamadas proibidas ou alteração dos dados cinematográficos.
- **SC-007**: Se a imagem nativa for habilitada, os três cenários de imagem passam;
  se não houver comprovação de suporte, a decisão fica registrada e 100% dos resultados
  continuam utilizáveis em texto. A ausência de imagens não bloqueia a entrega principal.
- **SC-008**: Em 100% dos cenários semânticos com filtros de gênero, ano e nota, todos
  os resultados respeitam as restrições; o inventário de campos e a prontidão do índice
  são verificados antes de aprovar esses cenários, sem alteração automática do índice.

## Assumptions

- O usuário informa que já existem a coleção `embedded_movies`, o índice
  `plot_vector_index` do tipo `vectorSearch` e o campo `plot_embedding_voyage_3_large`.
  São informações fornecidas, não uma inspeção executada nesta etapa.
- O mantenedor confirmou que a fonte semântica é `sample_mflix.embedded_movies`, no
  mesmo cluster do catálogo atual. Isso confirma a localização pretendida, não a
  conectividade nem os privilégios efetivos para a coleção adicional.
- O nome do campo sugere uma origem de embeddings, mas não comprova modelo, dimensões,
  métrica, configuração de entrada ou compatibilidade por si só. G2/proveniência foram
  corroborados no checkpoint2026-10-23 com os limites registrados; o plano seleciona
  caminho de query oficialmente documentado e exige funcionamento real em G4-B, sem
  recriar vetores/índices. Não reutilizar automaticamente embeddings da memória nem
  inventar o input_type histórico desconhecido.
- A fonte adicional fornece metadados suficientes para identificar os filmes. Não se
  presume igualdade de identificadores com a coleção original nem se exige um join;
  eventual insuficiência deve ser resolvida no planejamento sem enriquecimento inventado.
  Não se presume plot utilizável uniforme: candidatos sem ID/título/plot utilizáveis
  são excluídos somente da apresentação semântica, conforme FR-005/FR-006.
- A primeira versão aceita descrição, quantidade e os filtros existentes de gênero,
  ano e nota. Busca híbrida, outras dimensões de filtro, paginação e similaridade a
  partir de um filme selecionado ficam fora do escopo. O fluxo tradicional é preservado.
- Caminhos `genres`, `year` e `imdb.rating` foram observados no inventário limitado G2
  e os filtros foram adicionados manualmente pelo mantenedor com atestado Ready/Queryable
  em2026-10-23. Não é inspeção exaustiva nem prova de consulta real; não emitir novos
  ajustes sem inventário correspondente ou alterar o índice pelo assistente.
- Refinamento semântico na mesma sessão faz parte da entrega. Não há perfil temático
  entre conversas; pedidos dependentes de contexto sem informação suficiente devem
  ser esclarecidos, sem importar critérios do fluxo tradicional silenciosamente.
- Imagens são uma oportunidade condicionada, não suporte já confirmado. A documentação
  inicial do Agent Engine comprova chat e traces, mas não comprova renderização de pôsteres.
- G1/G2 têm evidência local delimitada em [research.md](research.md), não cloud.
  Entrega efetiva da configuração existente de embeddings, endpoint-binding/egress e
  consultas reais continuam pendências de implementação/aceitação, não inferências
  da configuração da memória nem bloqueios documentais pré-código já superados.