# USO DE IA — Branddi Ops AI

## Ferramentas, data e papel

Desenvolvimento iterativo em novembro de 2026 com assistência do **ChatGPT (GPT-6)** para arquitetura, revisão de cálculos, documentação, depuração e construção de regras. O protótipo publicado utiliza a API **Google Gemini** por meio da biblioteca `google-genai`; a versão de modelo configurada no código durante o desenvolvimento foi `gemini-3.1-flash-lite` (verificar `ai_agent.py` para versão efetivamente implantada). O Gemini gera **parecer executivo textual**, não é a fonte dos cálculos matemáticos nem executa decisões.

## Etapas e prompts representativos (resumos, não transcrições integrais)

1. **Arquitetura:** “Construir uma aplicação visual em Streamlit para simular capacidade N1/N2, crescimento de demanda, backlog, alternativas de recuperação e aprovação humana.” Resultado aceito: separação entre interface, cálculos, recomendações, IA e persistência.
2. **Consistência:** “Não somar entradas N1 e N2 como clientes únicos; usar 65% de disponibilidade, ações humanas por caso e tempos específicos; separar cenários atual/futuro.” Resultado: cálculo determinístico verificável e memória de cálculo no `PROJETO.md`.
3. **Governança do parecer:** “O modelo deve usar apenas os indicadores enviados pela aplicação, distinguir hipótese de evidência, não inventar ROI, custos, prazos nem afirmar auditoria externa.” Resultado: instruções restritivas e validação de resposta em `ai_agent.py`.
4. **Decisão humana:** “Apresentar alternativas independentes, exigir avaliação de viabilidade e aprovação humana, sem ordenar implementação imediata.” Resultado: revisão das recomendações e formulário de decisão.

## Iteração inicial versus revisada

| Aspecto | Versão inicial/risco identificado | Revisão aplicada | Verificação disponível |
|---|---|---|---|
| Linguagem financeira | Possibilidade de inferir menor custo/ROI sem valores | Restrições de prompt e checagem de expressões financeiras | Revisão de código e inspeção visual do parecer |
| Prazos | Recomendação de início imediato sem viabilidade | Exigir análise de execução, custo e riscos antes da aprovação | Parecer publicado passou a solicitar comparação e validação gerencial |
| Origem dos dados | Parecer poderia insinuar validação de fonte externa | Rodapé informa que indicadores foram fornecidos pela aplicação | Captura do diagnóstico online |
| Alternativas | Risco de somar contratação, produtividade e automação como ganhos simultâneos | Tratar alternativas como independentes, salvo estudo específico de combinação | Comparação entre simulador e texto gerado |
| Cálculo | LLM poderia produzir números próprios | Motor Python determinístico; IA apenas interpreta dados estruturados | Conferência das fórmulas e números do case |

## Trechos representativos de saída observada

- Diagnóstico: “demanda semanal é de 420 chamados, enquanto a capacidade instalada é de 390, gerando um déficit semanal de 30 chamados”.
- Governança: “Não há dados financeiros ou de complexidade técnica que permitam classificar uma alternativa como superior a outra neste momento.”
- Validação: “Os indicadores apresentados foram fornecidos pela aplicação e utilizados como base para esta análise.”

Os trechos são curtos e ilustrativos; respostas do LLM variam. As capturas da demonstração foram inspecionadas visualmente, mas não substituem teste automatizado de regressão.

## O que foi aceito, corrigido ou rejeitado

**Aceito:** interpretação gerencial assistida por LLM, recomendações condicionais, revisão humana. **Corrigido:** confusão entre hipótese e ganho comprovado; formulações categóricas de prazo e custo; alegações de validação externa. **Rejeitado:** reduzir N2 a sete analistas sem capacidade demonstrada; usar IA como fonte de contas; publicar credenciais.

## Limites, custos e segurança

API externa depende de credencial válida, rede, cotas e política comercial vigente do provedor; pode haver cobrança conforme uso/plano. A chave deve ficar em variável de ambiente/Secrets, nunca no GitHub. Apenas dados fictícios do case. O protótipo não é ferramenta de decisão autônoma nem está integrado a sistemas reais.
