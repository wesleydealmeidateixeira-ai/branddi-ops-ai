# PROJETO — Branddi Ops AI

## 1. Escopo e premissas

Case fictício de proteção de marcas. N1 executa tratativas padronizadas; N2 realiza análises complexas, mediações e exceções. A decisão em avaliação é reduzir N1 de 12 para 7 analistas e N2 de 9 para 7, preservando ao menos 90% de conclusões dentro do SLA, 97% de conformidade de qualidade e nenhuma hora extra adicional.

Premissas do enunciado: 40 h/semana por analista, 65% de disponibilidade produtiva, 1,8 ações humanas por caso N1 e 3,0 no N2; entradas semanais N1=800, N2=420; fila inicial N1=140, N2=180; crescimento hipotético de 20% das entradas. As entradas N2 já incluem transferências de N1 e reaberturas: **não somar N1 e N2 como casos únicos**. Tempos futuros são hipóteses, não ganhos realizados.

## 2. Dimensionamento e memória de cálculo

Minutos produtivos/analista/semana = 40 h × 60 min/h × 65% = **1.560 min**.

Capacidade teórica (casos/semana) = `analistas × 1.560 / (ações humanas por caso × minutos por ação)`.

Saldo (casos/semana) = capacidade − entradas. Saldo negativo aumenta a fila. Capacidade abaixo expressa com duas casas decimais; a fila é uma projeção contínua aproximada, não contagem literal de frações de chamados.

| Cenário | Nível | Analistas | Min/ação | Entradas/semana | Capacidade/semana | Saldo/semana |
|---|---|---:|---:|---:|---:|---:|
| Atual | N1 | 12 | 9 | 800 | 1.155,56 | +355,56 |
| Atual | N2 | 9 | 12 | 420 | 390,00 | −30,00 |
| Atual +20% | N1 | 12 | 9 | 960 | 1.155,56 | +195,56 |
| Atual +20% | N2 | 9 | 12 | 504 | 390,00 | −114,00 |
| Proposta com tempos futuros | N1 | 7 | 5 | 800 | 1.213,33 | +413,33 |
| Proposta com tempos futuros | N2 | 7 | 9 | 420 | 404,44 | −15,56 |
| Proposta +20% | N1 | 7 | 5 | 960 | 1.213,33 | +253,33 |
| Proposta +20% | N2 | 7 | 9 | 504 | 404,44 | −99,56 |

Fila após `t` semanas, supondo fluxos constantes e sem restrições de prioridade: `max(0, fila_inicial + t × (entradas − capacidade))`. Com proposta 7/7, tempos futuros e +20% de demanda, em quatro semanas: N1=0 (capacidade ociosa após zerar a fila); N2≈578,22 casos. A fórmula não estima pontualidade de SLA nem variabilidade.

Para N2 **atual**, recuperar fila de 180 em quatro semanas com entrada de 420/semana exige 420 + 180/4 = **465 casos/semana**, 75 acima da capacidade atual de 390. São alternativas **independentes** no simulador: aproximadamente 2 analistas adicionais; reduzir tempo médio por ação de 12 para ≈10,06 min (−16,13%); ou automatizar 75 casos elegíveis por semana sem repasse de trabalho equivalente. Contratação requer dimensionamento inteiro; automação depende de elegibilidade, revisão e taxa de sucesso. Essas alternativas não podem ser somadas como ganhos comprovados.

### Recomendação de quadro

**Não aprovar a redução imediata para 7 N2.** Mesmo supondo o tempo futuro de 9 min/ação, sete N2 não atendem 420/semana nem 504/semana. Nove N2 a 9 min/ação teriam capacidade teórica de 520/semana e apenas 16/semana de margem ante 504, insuficiente para afirmar resiliência ou redução rápida da fila. Manter capacidade de N2 e avaliar reforço temporário, automação elegível ou melhoria comprovada. A decisão de N1 também é **condicionada** à medição dos tempos futuros, qualidade, variabilidade e efeitos da transferência N1→N2; não cortar equipe com base em hipótese.

Antes de mudar quadro: medir distribuição real dos tempos, sazonalidade, mix de complexidade, ações por caso, retrabalho, reaberturas já embutidas, escalonamentos, produtividade líquida, fila por idade, SLA e qualidade por tipo de demanda. Separar capacidade de operação estável e esforço extraordinário para esvaziar a fila.

## 3. Redesenho do fluxo

**Fluxo de análise de capacidade/decisão, recorte implementado:** parâmetros operacionais fictícios → validação de entradas → cálculo determinístico N1/N2 → comparação com demanda e crescimento → alternativas de recuperação N2 → parecer executivo por IA → revisão humana (aprovar, solicitar ajustes ou rejeitar) → registro da decisão em SQLite.

**Processo de tratamento de casos, evolução proposta (não implementada no protótipo):** recebimento de denúncia → deduplicação por identificador/URL/marca → conferência de evidência → classificação de risco e complexidade → N1 para rotinas padronizadas → N2 para disputas, mediação, evidência insuficiente ou exceções → revisão humana em casos de risco → conclusão com trilha de auditoria. Eliminar reentrada manual de dados e controles duplicados; simplificar preenchimento; automatizar checagens e sugestão de rota; manter julgamento humano em exceções e atos com efeito externo.

Não contar simultaneamente redução de ações/caso e tempo/ação sem medir componentes independentes. Medir também taxa de transferência N1→N2, tempo de retrabalho e esforço humano residual para evitar apenas deslocar gargalo.

## 4. Duas melhorias prioritárias

### A. Simulador determinístico com parecer gerencial por IA — implementado

- **Problema:** proposta de dimensionamento sem validação de capacidade, crescimento e fila.
- **Entradas:** analistas, jornada, disponibilidade, tempo médio por caso/ação, entradas, backlog e prazo-alvo, conforme telas do protótipo.
- **Saídas:** capacidade, utilização, saldo, projeção de fila, alternativas independentes de recuperação e diagnóstico textual por Gemini.
- **Integração:** hoje interface Streamlit, Gemini via API e registro SQLite; integração ao sistema próprio é futura.
- **Ganho esperado:** menor esforço de simulação e comparação de cenários; **não medido como ganho de produtividade real**.
- **Revisão:** decisão humana obrigatória para aprovar, ajustar ou rejeitar; não executa contratação, automação de chamados ou mudanças de quadro.
- **Exceções:** indisponibilidade da IA não deve alterar o cálculo determinístico; exigir leitura do alerta/erro e preservar a decisão humana. Verificar comportamento real da aplicação antes da demonstração.

### B. Triagem assistida e deduplicação de evidências — proposta futura

- **Problema:** triagem repetitiva, retrabalho, transferência indevida e risco de duplicidade na migração.
- **Entrada:** identificador do caso, marca, URL, evidência, tipo de violação, criticidade, histórico e SLA.
- **Saída:** sugestão explicável de N1/N2, duplicidade provável, campos faltantes e nível de confiança.
- **Integração:** evento no sistema próprio, sem escrita direta em produção durante piloto; decisão humana registra aceite/correção.
- **Ganho esperado:** menos minutos humanos de triagem, condicionado a teste A/B ou amostra pareada; não prometer percentual sem medição.
- **Exceções:** disputas, baixa confiança, evidência ausente e risco jurídico são encaminhados à revisão especializada.

**Priorização com Produto/Tecnologia:** especificar problema e métrica, contrato de dados, critérios de aceite, riscos, esforço estimado, dependências, dono técnico e janela de rollback; priorizar valor operacional e redução de risco, não apenas rapidez de desenvolvimento.

## 5. Migração do workflow externo para o sistema próprio

Migração **não implementada**; desenho proposto: inventariar filas, responsáveis, histórico, timestamps, anexos, regras de SLA e estados; mapear campos e versões; definir IDs estáveis e chaves de idempotência; executar migração por ondas com reconciliação de contagens e amostragem de casos; operar em sombra antes de comutar; proibir dupla escrita não coordenada; manter logs de divergência e plano de reversão. Rollback: suspender novas gravações no destino, reconciliar eventos, restaurar roteamento anterior e comunicar Operações/Produto/Tecnologia. Nenhum dado real é necessário para este case.

## 6. Piloto e primeiros 30 dias

| Janela | Responsável por função | Entrega e dependência | Critério de decisão |
|---|---|---|---|
| Dias 1–7 | Operações + QA | Linha de base de demanda, TMA, fila, SLA, qualidade e esforço residual; taxonomia; amostra | Sem linha de base confiável, não iniciar expansão |
| Dias 8–14 | Tecnologia + Produto | Instrumentação, integração simulada, testes de falha, validação de dados e trilha de auditoria | Sem rastreabilidade, interromper |
| Dias 15–21 | Operações + QA | Execução em sombra e amostra pareada manual/assistida; revisão humana | Não automatizar decisões de alto risco |
| Dias 22–30 | CEO + Operações + Produto + Tecnologia | Comparar ganhos líquidos, estabilidade de fila, SLA e qualidade; decidir ampliar, corrigir ou parar | Avançar apenas com SLA ≥90%, qualidade ≥97%, fila sob controle e sem hora extra adicional |

**SLAs operacionais propostos para o piloto (não fornecidos pelo enunciado):** N1 até 2 dias úteis e N2 até 5 dias úteis, contados da entrada na fila correspondente; formalizar regras de prioridade, pausa e relógio de SLA antes do piloto. **Janela-alvo de redução de backlog:** quatro semanas **após** estabilização e comprovação de capacidade suficiente; para N2, o quadro proposto 7/7 não a sustenta.

### Cinco indicadores — fórmula, fonte, frequência, decisão

| Indicador | Fórmula | Fonte proposta | Frequência | Decisão |
|---|---|---|---|---|
| Produtividade/capacidade | Casos concluídos ÷ horas produtivas; confrontar com entradas | Eventos do sistema + escala | Diário/semanal | Rebalancear capacidade |
| Fila e envelhecimento | Abertos no fechamento; idade p50/p90 | Sistema de casos | Diário | Atuar em backlog e prioridades |
| SLA | Conclusões dentro do prazo ÷ conclusões totais ×100 | Timestamps/SLAs | Diário/semanal | Interromper expansão se <90% |
| Qualidade | Itens conformes ÷ itens auditados ×100 | Auditoria QA | Semanal | Interromper expansão se <97% |
| Esforço humano residual | Minutos efetivos de revisão + correção + execução por caso | Amostra cronometrada + logs | Semanal | Validar ganho líquido |

### Contingência e governança

Se a automação atrasar: manter casos críticos, proteção de SLA e auditoria; reduzir apenas escopo de baixa criticidade; pausar rollout, integrações não essenciais e promessas de redução de equipe. Comunicar CEO e lideranças com capacidade recalculada, riscos, impactos por segmento, responsáveis e prazo de nova decisão. Qualquer decisão de pessoal exige dados reais, análise de variabilidade e governança própria; o protótipo não a executa.

## 7. Conclusão executiva

**Fazer agora:** instrumentar dados, manter revisão humana, executar piloto controlado e corrigir o déficit N2. **Condicionar ao piloto:** automatização adicional, redução de TMA, redesenho de roteamento e eventual dimensionamento. **Não fazer sem evidência:** reduzir N2 para sete, assumir SLA/qualidade por conta teórica, extrapolar teste fictício para operação real ou executar ações automaticamente. Cálculos do simulador são determinísticos; parecer Gemini é interpretação textual; tempos futuros e ganhos de produtividade continuam hipóteses.
