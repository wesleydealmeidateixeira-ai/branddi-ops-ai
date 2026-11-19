# TESTES — Branddi Ops AI

## 1. Escopo, evidências e critérios

Este documento apresenta os testes funcionais do protótipo Branddi Ops AI, desenvolvido com dados fictícios do case da Branddi.

Os resultados distinguem evidências observadas na interface, simulações controladas de falha e limitações ainda não validadas.

**Critérios de aceitação:**
- Cálculos determinísticos e matematicamente coerentes.
- Tratamento de entradas inválidas.
- Revisão e registro de decisões humanas.
- Continuidade do simulador quando o LLM estiver indisponível.
- Separação dos indicadores de N1 e N2.
- Nenhuma implementação operacional automática.
- Preservação das metas de SLA ≥ 90% e qualidade ≥ 97% no piloto.

Os limites de SLA e qualidade são critérios para avaliação futura, não resultados comprovados pelo protótipo.

## 2. Cenários de testes funcionais

### T1 — Cenário padrão: capacidade operacional N2

**Entrada:**
- 9 analistas.
- 40 horas semanais por analista.
- Disponibilidade produtiva de 65%.
- 3 ações por caso.
- 12 minutos por ação.
- Demanda de 420 casos/semana.
- Fila inicial de 180 casos.

**Resultado esperado:**
- Capacidade semanal: 390 casos.
- Utilização: 107,69%.
- Déficit: 30 casos/semana.
- Fila projetada após uma semana: 210 casos.

**Resultado observado:**

A aplicação apresentou capacidade de 390 casos/semana, utilização de 107,69% e fila projetada de 210 casos.

**Situação: APROVADO — Observação visual.**

### T2 — Validação de entrada inválida

**Entrada:**

No simulador de capacidade operacional, alterar o campo "Tempo médio por caso (minutos)" de 30 para 0.

**Resultado esperado:**

O sistema deve identificar a entrada inválida e impedir que o valor zero seja aceito para o cálculo, evitando divisão por zero.

**Resultado observado:**

O campo foi destacado em vermelho e apresentou a mensagem:

"Error: Number is below the allowed range. Please enter a value greater than or equal to 1."

O arquivo `app.py` estabelece `min_value=1` para esse campo.

Após o teste, o valor original de 30 minutos foi restaurado.

**Situação: APROVADO — Validação da interface.**

**Limitação:** não foi realizado teste direto da função matemática com entrada zero fora da interface Streamlit.

### T3 — Exceção com decisão humana

**Entrada:**

Cenário operacional N2 com capacidade de 390 casos/semana, demanda de 420 casos/semana, fila inicial de 180 casos e prazo de recuperação de quatro semanas.

Decisão selecionada: "Solicitar ajustes".

Justificativa: revisar o dimensionamento do N2 antes de qualquer implementação e validar SLA, qualidade e capacidade operacional.

Responsável: identificação de teste T3.

**Resultado esperado:**
- Registrar decisão, justificativa e responsável.
- Associar a decisão aos parâmetros operacionais.
- Exibir o registro no histórico.
- Não executar mudanças operacionais automaticamente.

**Resultado observado:**

A aplicação apresentou:

"Decisão registrada com sucesso! Registro nº 1."

O histórico exibiu um registro contendo:
- ID: 1.
- Decisão: Solicitar ajustes.
- Justificativa informada.
- Responsável identificado.
- Capacidade semanal: 390.
- Demanda semanal: 420.
- Fila inicial: 180.
- Prazo: 4 semanas.

**Situação: APROVADO — Registro e consulta observados na sessão.**

**Limitação:** a durabilidade do registro após reinicialização do ambiente Streamlit Community Cloud não foi testada.

### T4 — Indisponibilidade do Gemini

**Entrada:**

Simulação controlada de indisponibilidade da API Gemini.

**Procedimento 1 — Teste isolado:**

Criado o arquivo `teste_falha_gemini.py`, utilizando `unittest.mock.patch` para substituir temporariamente a chamada à API por uma exceção `ConnectionError`.

**Resultado esperado:**

A falha deve ser detectada pelo script de teste sem necessidade de indisponibilizar o serviço real.

**Resultado observado:**

O terminal apresentou:

```text
TESTE T4 - INDISPONIBILIDADE DO GEMINI
Indisponibilidade detectada: Falha simulada: API Gemini indisponivel
A chamada da IA falhou de forma controlada no teste.
```

**Procedimento 2 — Teste de integração local:**

No ambiente local, a chamada `analisar_operacao(dados_para_ia)` foi substituída temporariamente por uma exceção `ConnectionError`, para verificar o tratamento de erro existente no `app.py`.

**Resultado esperado:**
- Apresentar mensagem de erro compreensível.
- Manter os cálculos operacionais disponíveis.
- Não executar decisões automaticamente.

**Resultado observado:**

A aplicação Streamlit apresentou:

"Não foi possível consultar o Gemini. Verifique a conexão ou tente novamente. Os cálculos operacionais continuam disponíveis."

Os resultados de recuperação permaneceram visíveis:
- Fila acumulada: 180 casos.
- Capacidade necessária: 465 casos/semana.
- Prazo: 4 semanas.
- Analistas adicionais: 2.
- Redução do tempo médio: 16,13%.
- Casos para automatizar: 75 por semana.

**Restauração:**

Após a simulação, a chamada original ao Gemini foi restaurada no `app.py`.

Uma nova execução local gerou o diagnóstico executivo completo, demonstrando o retorno do funcionamento normal da integração.

**Situação: APROVADO — Falha simulada e recuperação funcional observadas.**

**Limitação:** não foi realizado teste de indisponibilidade real do serviço Google Gemini.

### T5 — Cenário de maior volume: crescimento de 20%

**Entrada:**

Crescimento de 20% na demanda semanal:
- N1: 800 para 960 casos.
- N2: 420 para 504 casos.

Equipe proposta:
- N1: 7 analistas, 1,8 ação/caso e 5 minutos/ação.
- N2: 7 analistas, 3 ações/caso e 9 minutos/ação.

Disponibilidade produtiva: 65%.

**Resultado esperado:**
- Capacidade N1: 1.213,33 casos/semana.
- Utilização N1: 79,12%.
- Capacidade N2: 404,44 casos/semana.
- Utilização N2: 124,62%.
- Déficit N2: aproximadamente 99,56 casos/semana.
- Fila N2 após uma semana: aproximadamente 280 casos.

**Resultado observado:**

As capturas da aplicação apresentaram os indicadores de capacidade e utilização de N1 e N2 separadamente, incluindo a fila projetada do N2.

**Situação: APROVADO — Observação visual e conferência matemática.**

**Limitação:** os tempos futuros de execução são hipóteses de produtividade, não ganhos medidos em operação real.

### T6 — Plano de recuperação da fila N2

**Entrada:**
- Capacidade atual: 390 casos/semana.
- Demanda: 420 casos/semana.
- Fila inicial: 180 casos.
- Prazo: 4 semanas.

**Resultado esperado:**

Capacidade necessária:

420 + (180 / 4) = 465 casos/semana.

Alternativas independentes:
- Adicionar 2 analistas.
- Reduzir o tempo médio em aproximadamente 16,13%.
- Automatizar 75 casos/semana.

**Resultado observado:**

A aplicação apresentou capacidade necessária de 465 casos/semana e as três alternativas previstas.

**Situação: APROVADO — Observação visual.**

**Limitação:** a recuperação depende da capacidade adicional estar efetivamente disponível durante o período considerado.

### T7 — Diagnóstico executivo com IA

**Entrada:**

Dados estruturados da operação N2, incluindo capacidade, demanda, déficit, fila acumulada, prazo e alternativas de recuperação.

**Resultado esperado:**
- Diagnóstico executivo estruturado em seis seções.
- Indicadores consistentes com o simulador.
- Recomendações condicionadas à viabilidade.
- Ausência de execução operacional automática.
- Declaração padronizada sobre a origem dos indicadores.

**Resultado observado:**

O Gemini produziu diagnóstico contendo:
1. Diagnóstico executivo.
2. Principais riscos.
3. Recomendações priorizadas.
4. Plano de recuperação.
5. Indicadores de acompanhamento.
6. Decisão gerencial.

Os valores principais foram compatíveis com os cálculos do simulador.

A resposta indicou a necessidade de validação técnica, financeira e gerencial antes da implementação.

O sistema apresentou a declaração final:

"Os indicadores apresentados foram fornecidos pela aplicação e utilizados como base para esta análise."

**Situação: APROVADO — Execução observada.**

**Limitação:** a consistência de uma execução não garante que todas as futuras respostas do LLM serão corretas.

## 3. Verificação numérica independente

### Capacidade produtiva

Minutos produtivos por analista por semana:

40 × 60 × 0,65 = 1.560 minutos.

Fórmula:

Capacidade semanal = (analistas × minutos produtivos) / (ações por caso × minutos por ação).

| Cenário | Analistas | Ações/caso | Minutos/ação | Capacidade/semana | Demanda/semana | Saldo/semana |
|---|---:|---:|---:|---:|---:|---:|
| N1 atual | 12 | 1,8 | 9 | 1.155,56 | 800 | +355,56 |
| N1 proposto +20% | 7 | 1,8 | 5 | 1.213,33 | 960 | +253,33 |
| N2 atual | 9 | 3 | 12 | 390,00 | 420 | -30,00 |
| N2 proposto +20% | 7 | 3 | 9 | 404,44 | 504 | -99,56 |

### Projeção da fila N2

Fila inicial: 180 casos.

**N2 atual, após uma semana:**

180 + 420 - 390 = 210 casos.

**N2 proposto com demanda +20%, após uma semana:**

180 + 504 - 404,44 ≈ 280 casos.

**N2 proposto com demanda +20%, após quatro semanas:**

180 + 4 × (504 - 404,44...) ≈ 578,22 casos.

As projeções consideram demanda e capacidade constantes, sem alterações na composição ou complexidade dos chamados.

N1 e N2 são calculados separadamente. Os casos transferidos entre níveis não devem ser somados como novos clientes únicos.

## 4. Comparação antes/depois e esforço humano residual

**Amostra cronometrada de tarefas manuais versus assistidas: n = 0.**

Não foi realizada medição pareada de tempo, esforço humano residual, retrabalho ou qualidade operacional.

Portanto, não existe percentual de produtividade real comprovado.

A comparação disponível representa cenários teóricos:

| Indicador | N2 atual | N2 proposto |
|---|---:|---:|
| Analistas | 9 | 7 |
| Ações por caso | 3 | 3 |
| Tempo por ação | 12 min | 9 min |
| Capacidade teórica semanal | 390 | 404,44 |
| Demanda atual | 420 | 420 |
| Saldo na demanda atual | -30 | -15,56 |
| Demanda com +20% | 504 | 504 |
| Saldo com +20% | -114 | -99,56 |

O ganho hipotético considera exclusivamente a redução de tempo por ação, mantendo constante a quantidade de ações por caso. Não há soma de ganhos sobrepostos.

### Medição proposta para o piloto

Selecionar amostras comparáveis por tipo e complexidade de chamado.

Registrar:
- Quantidade de casos avaliados.
- Tempo total de execução manual.
- Tempo total de execução assistida.
- Tempo de revisão humana.
- Correções e retrabalho.
- Qualidade das entregas.

Calcular o ganho líquido incluindo o esforço humano residual.

Não extrapolar resultados de amostras pequenas para toda a operação.

## 5. Falhas, correções e retestes

| Ocorrência | Tratamento | Reteste |
|---|---|---|
| Possibilidade de afirmações financeiras ou prazos sem comprovação | Regras de validação reforçadas no `ai_agent.py` | Nova resposta inspecionada visualmente |
| Risco de o parecer afirmar auditoria externa inexistente | Declaração final padronizada pela aplicação | Rodapé observado no diagnóstico |
| Entrada inválida no tempo médio | Restrição `min_value=1` no Streamlit | T2 validado |
| Necessidade de registrar decisão humana | Formulário e histórico SQLite | T3 validado na sessão |
| Indisponibilidade do Gemini | Tratamento de exceção no `app.py` | T4 validado com falha simulada e restauração |

## 6. Critérios para seguir, revisar ou interromper

**Seguir para piloto controlado quando:**
- Os cálculos forem consistentes.
- A revisão humana estiver funcional.
- As exceções forem tratadas.
- As integrações simuladas estiverem identificadas.
- Existirem responsáveis definidos para aprovação e acompanhamento.

**Revisar a solução quando:**
- A IA produzir recomendações inconsistentes.
- O esforço de revisão eliminar o ganho operacional.
- A automação transferir trabalho indevidamente do N1 para o N2.
- Os tempos de execução projetados não forem alcançados.

**Interromper a automação quando:**
- Houver risco de descumprimento de SLA ou qualidade.
- Forem identificadas decisões incorretas com impacto operacional.
- Ocorrer falha de rastreabilidade ou perda de histórico.
- Não existir mecanismo seguro de reversão.

Metas do piloto:
- SLA ≥ 90%.
- Qualidade ≥ 97%.
- Sem horas extras.
- Preservação da revisão humana.
- Monitoramento da capacidade, fila e esforço humano residual.

Esses critérios são propostos para uma operação real e ainda não foram validados com dados de produção.

## 7. Limitações e próximos passos

O protótipo utiliza dados fictícios e não possui integração com os sistemas internos reais da Branddi.

A integração com a API Gemini é real, mas a falha T4 foi induzida artificialmente em ambiente local.

O armazenamento SQLite utilizado no Streamlit Community Cloud pode ser efêmero. A persistência após reinicializações não foi comprovada.

Não foram realizados testes de:
- Carga simultânea e desempenho sob alto volume de usuários.
- Segurança de acesso e autenticação.
- Durabilidade de registros após reinicialização.
- Qualidade estatística das recomendações em amostras extensas.
- Ganho líquido de produtividade com casos reais.

Nenhuma alteração foi executada em pessoas, acessos ou sistemas operacionais reais.

A evolução para produção dependeria de integração com os sistemas corporativos, banco de dados persistente, controle de acesso, monitoramento, tratamento de exceções e validação de Tecnologia, Produto e Operações.