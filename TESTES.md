# TESTES — Branddi Ops AI

## Escopo, evidência e critérios

Base fictícia do PDF da Branddi. Este arquivo distingue **resultado observado em captura de tela** de **teste ainda pendente**; não se atribui execução automatizada a um teste sem log. Critérios propostos antes do piloto: cálculos matemáticos coerentes, nenhum efeito operacional sem aprovação humana, histórico rastreável, tolerância à falha da IA, SLA ≥90% e qualidade ≥97% quando houver dados reais. SLA e qualidade **não podem ser medidos** apenas com as entradas agregadas deste protótipo.

## Cenários mínimos

| ID | Cenário e entrada | Resultado esperado | Obtido / evidência | Situação |
|---|---|---|---|---|
| T1 | Padrão: N2=9 analistas, 40h, 65%, 3 ações/caso, 12min/ação, demanda 420 | Capacidade 390/sem; déficit 30; uso 107,69% | Capturas da aplicação publicada mostram 390, 107,69% e fila projetada 210 após uma semana | **Observado visualmente** |
| T2 | Inválido: tentar valor de tempo médio igual a zero ou demanda negativa | Entrada recusada ou controlada, sem divisão por zero nem resultado enganoso | Não há registro de execução fornecido | **Pendente de execução** |
| T3 | Exceção gerencial: cenário N2 deficitário; selecionar “Solicitar ajustes”, justificar e registrar | Decisão registrada com responsável e justificativa; sem ação operacional automática | Formulário de revisão humana e histórico foram observados; envio efetivo não comprovado na versão online | **Parcial; reteste pendente** |
| T4 | Indisponibilidade da API Gemini ou resposta incorreta | Cálculos permanecem acessíveis; falha explicitada; nenhuma recomendação tratada como aprovada | Diagnóstico bem-sucedido observado, mas falha induzida não demonstrada | **Pendente de execução** |
| T5 | Maior volume: aumentar demanda N1/N2 em 20% | N1=960/sem; N2=504/sem; recalcular saldo e fila sem misturar níveis | Capturas mostram N1 futuro capacidade 1.213 e uso 79,12%; N2 futuro capacidade 404 e uso 124,62%, fila 280 após uma semana | **Observado visualmente** |
| T6 | Recuperação N2: fila 180, demanda 420, capacidade 390, prazo 4 semanas | Capacidade-alvo 465; alternativas independentes: +2 analistas, −16,13% no tempo ou 75 automações/sem | Capturas mostram 465, 2, 16,13% e 75 | **Observado visualmente** |
| T7 | Parecer Gemini com dados estruturados | Seis seções, números consistentes, recomendação condicional, validação de origem dos dados | Capturas exibem seis seções, números compatíveis e rodapé de validação | **Observado visualmente; sem garantia de todas as execuções** |

## Verificação numérica independente

- Minutos produtivos por analista/semana: `40 × 60 × 0,65 = 1.560`.
- N1 atual: `12 × 1.560 / (1,8 × 9) = 1.155,56` casos/semana.
- N2 atual: `9 × 1.560 / (3 × 12) = 390` casos/semana.
- N1 proposto: `7 × 1.560 / (1,8 × 5) = 1.213,33` casos/semana.
- N2 proposto: `7 × 1.560 / (3 × 9) = 404,44` casos/semana.
- Entradas +20%: N1=960, N2=504. Saldo proposto N2=−99,56/semana; fila após quatro semanas ≈578,22 partindo de 180.
- Recuperação N2 atual em quatro semanas: `420 + 180/4 = 465` casos/semana.

## Comparação antes/depois — estado real da evidência

**Amostra cronometrada de tarefas manuais versus assistidas: n=0.** Nenhuma medição pareada de tempo de execução, esforço humano residual ou conformidade QA foi fornecida até esta versão; portanto **não há percentual de ganho comprovado**. Comparação disponível é de **cenários teóricos**, não produtividade real:

| Medida | Antes: N2 atual | Depois: N2 proposto com tempo hipotético |
|---|---:|---:|
| Analistas | 9 | 7 |
| Tempo/ação | 12 min | 9 min (hipótese) |
| Capacidade teórica/sem | 390 | 404,44 |
| Demanda atual/sem | 420 | 420 |
| Saldo/sem | −30 | −15,56 |
| Demanda +20%/sem | 504 | 504 |
| Saldo com +20%/sem | −114 | −99,56 |

**Procedimento para medição antes/depois em piloto:** selecionar mesma amostra estratificada por tipo e complexidade; registrar tamanho `n`, tempo humano total manual e assistido, tempo de revisão/correção, taxa de acerto e QA cega; reportar média/mediana e divergências. Só considerar ganho líquido se revisão e retrabalho estiverem incluídos. Não extrapolar amostra pequena.

## Falhas, correções e retestes

- **Parecer poderia alegar custo/ROI ou prazo sem base:** instruções e validações de texto foram reforçadas em `ai_agent.py`; nova saída foi inspecionada em capturas e não ordenou implementação imediata.
- **Parecer poderia sugerir que números foram auditados externamente:** texto final foi restringido a indicar que os indicadores vieram da aplicação; rodapé observado.
- **Pendente:** executar T2, T3 e T4 e registrar data, captura/log, comportamento obtido, correção e reteste. Não classificar esses cenários como aprovados sem execução.

## Limitações da evidência

Capturas demonstram execução em Streamlit Community Cloud e geração de texto por Gemini, mas não demonstram durabilidade do SQLite entre reinicializações, segurança de acesso, desempenho sob carga ou confiabilidade estatística. O armazenamento local do Streamlit Community Cloud pode ser efêmero. Nenhum sistema real foi alterado.
