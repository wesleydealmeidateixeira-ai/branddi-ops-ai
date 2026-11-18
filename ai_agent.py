
import os
import json
import re

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ============================================================
# CONFIGURAÇÃO DO AGENTE
# ============================================================

load_dotenv()

chave_api = os.getenv("GEMINI_API_KEY")

if not chave_api:
    raise ValueError(
        "GEMINI_API_KEY não encontrada no arquivo .env"
    )

cliente = genai.Client(
    api_key=chave_api,
    http_options=types.HttpOptions(timeout=30000)
)

MODELO = "gemini-3.1-flash-lite"

FRASE_VALIDACAO = (
    "Os indicadores apresentados foram fornecidos pela "
    "aplicação e utilizados como base para esta análise."
)


# ============================================================
# VALIDAÇÃO DE AFIRMAÇÕES DA IA
# ============================================================

def validar_resposta_ia(texto):
    """
    Identifica afirmações financeiras e prazos que
    exigem validação adicional.

    Não altera os cálculos do simulador.
    Não substitui a revisão humana.
    """

    alertas = []

    padroes_financeiros = [
        r"\bmaior ROI\b",
        r"\bmenor custo\b",
        r"\bmais barata\b",
        r"\beconomia garantida\b",
        r"\bretorno financeiro garantido\b",
    ]

    for padrao in padroes_financeiros:
        if re.search(padrao, texto, re.IGNORECASE):
            alertas.append(
                "A resposta contém uma afirmação financeira "
                "que precisa de comprovação."
            )
            break

    padroes_prazos = [
        r"\bem até \d+ (dias?|semanas?|meses?)\b",
        r"\bpiloto de \d+ (dias?|semanas?|meses?)\b",
        r"\bimplementação em \d+ (dias?|semanas?|meses?)\b",
        r"\bimplementad[ao] em \d+ (dias?|semanas?|meses?)\b",
        r"\bimplementar em \d+ (dias?|semanas?|meses?)\b",
    ]

    for padrao in padroes_prazos:
        if re.search(padrao, texto, re.IGNORECASE):
            alertas.append(
                "A resposta contém um prazo que precisa "
                "ser conferido com os dados fornecidos."
            )
            break

    return alertas


# ============================================================
# PADRONIZAÇÃO DA VALIDAÇÃO FINAL
# ============================================================

def padronizar_validacao_final(texto):
    """
    Remove uma eventual seção final de validação
    gerada pela IA e acrescenta uma declaração única.

    Esta função não audita os dados operacionais.
    """

    # Identifica uma seção final intitulada
    # "Validação final", com ou sem Markdown.
    padrao_secao = (
        r"(?im)^[ \t]*(?:#{1,6}[ \t]*)?"
        r"(?:\*\*)?validação final(?:\*\*)?[ \t]*:?.*$"
    )

    resultado = re.search(padrao_secao, texto)

    if resultado:
        texto = texto[:resultado.start()].rstrip()

    # Remove a frase padronizada caso o Gemini
    # já a tenha incluído na resposta.
    texto = texto.replace(FRASE_VALIDACAO, "").rstrip()

    # Remove separadores finais isolados.
    texto = re.sub(
        r"(?:\n[ \t]*---[ \t]*)+$",
        "",
        texto
    ).rstrip()

    # Acrescenta uma única declaração final.
    return (
        texto
        + "\n\n---\n\n"
        + "**Validação final:** "
        + FRASE_VALIDACAO
    )


# ============================================================
# CONSULTA AO GEMINI
# ============================================================

def consultar_agente(pergunta):
    """
    Envia uma solicitação ao Gemini e processa
    a resposta antes de apresentá-la ao usuário.
    """

    resposta = cliente.models.generate_content(
        model=MODELO,
        contents=pergunta
    )

    texto = resposta.text

    if not texto or not texto.strip():
        raise ValueError(
            "O Gemini não retornou uma resposta textual."
        )

    # Identifica afirmações que exigem revisão.
    alertas = validar_resposta_ia(texto)

    # Padroniza a declaração de origem dos dados.
    texto = padronizar_validacao_final(texto)

    # Acrescenta alertas apenas quando necessário.
    if alertas:
        texto += "\n\n---\n\n"
        texto += "### ⚠️ Alertas de validação automática\n"

        for alerta in alertas:
            texto += f"- {alerta}\n"

        texto += (
            "\n**Atenção:** este diagnóstico contém "
            "afirmações que precisam de validação "
            "antes de qualquer decisão gerencial."
        )

    return texto


# ============================================================
# ANÁLISE OPERACIONAL
# ============================================================

def analisar_operacao(dados_operacionais):
    """
    Analisa os indicadores calculados pelo sistema.

    A IA interpreta os resultados, mas não substitui
    os cálculos matemáticos nem a decisão humana.
    """

    dados_json = json.dumps(
        dados_operacionais,
        ensure_ascii=False,
        indent=2
    )

    prompt = f"""
Você é o Branddi Ops AI, um agente de inteligência
operacional especializado em operações SaaS,
suporte N1/N2, capacidade, produtividade,
automação e gestão de filas.

MISSÃO:
Analisar indicadores operacionais e produzir
recomendações fundamentadas para a gerência.


REGRAS OBRIGATÓRIAS:

1. Utilize exclusivamente os dados operacionais fornecidos.

2. Não invente indicadores, números, custos ou resultados.

3. Não altere os cálculos recebidos do simulador.

4. Diferencie claramente fatos, hipóteses e recomendações.

5. Identifique riscos operacionais e dependências.

6. Priorize ações por impacto e viabilidade demonstráveis.

7. Não prometa resultados sem comprovação.

8. Não execute decisões automaticamente.

9. Toda implementação depende de aprovação humana.

10. Responda em português do Brasil.

11. As alternativas de recuperação apresentadas pelo
simulador são independentes. Cada uma representa uma
possibilidade de atingir a capacidade necessária
isoladamente, desde que suas premissas sejam atendidas.

12. Não afirme que é obrigatório combinar contratação,
automação e produtividade para alcançar a meta.

13. Caso recomende combinar alternativas, apresente a
combinação como estratégia opcional e justifique
seus benefícios.

14. Não afirme que automação é mais barata que
contratação sem dados comprovados de custos
e investimentos.

15. Não invente prazos de implantação, retorno
financeiro, economia ou ganhos de produtividade.

16. Diferencie capacidade teórica de resultados
efetivamente alcançados na operação.

17. Apresente as recomendações como propostas
sujeitas a validação técnica, financeira e gerencial.

18. Não considere tickets transferidos ou
reclassificados como resolvidos sem evidência
de encerramento efetivo.

19. Os dados operacionais foram fornecidos pela
aplicação Branddi Ops AI.

Não afirme que foram extraídos de um documento
original, PDF, relatório externo ou sistema
corporativo, pois essas fontes não foram
consultadas diretamente por este agente.

20. Não escreva uma seção de validação final
nem repita a declaração de origem dos dados.

A aplicação acrescentará automaticamente
a declaração padronizada ao diagnóstico.

21. Não afirme ter verificado a autenticidade,
a origem documental ou a qualidade dos dados
recebidos.

A conferência da origem dos dados depende
de validação humana.


DADOS OPERACIONAIS:

{dados_json}


ESTRUTURA DA RESPOSTA:


1. DIAGNÓSTICO EXECUTIVO

Explique a situação operacional com os
números fornecidos.


2. PRINCIPAIS RISCOS

Identifique riscos de capacidade, fila,
produtividade e atendimento.


3. RECOMENDAÇÕES PRIORIZADAS

Apresente até cinco ações, explicando
o impacto esperado e as dependências.


4. PLANO DE RECUPERAÇÃO

Analise as alternativas calculadas e
o prazo necessário para recuperação da fila.


5. INDICADORES DE ACOMPANHAMENTO

Recomende indicadores para monitorar
a execução.


6. DECISÃO GERENCIAL

Indique qual decisão deve ser avaliada
pela liderança, com justificativa.

A decisão recomendada deve ser a avaliação
comparativa das alternativas disponíveis,
considerando:

- Viabilidade técnica.
- Viabilidade financeira.
- Capacidade de execução.
- Riscos operacionais.
- Dependências de implementação.

Não determine início imediato de contratação,
automação ou mudanças operacionais sem
aprovação formal da liderança.

Não escolha uma alternativa como superior
quando não existirem dados suficientes
para sustentar essa comparação.

Quando os dados forem insuficientes,
recomende validar as alternativas antes
de selecionar e autorizar a execução.

O prazo de recuperação da fila representa
uma meta operacional projetada, não uma
garantia de que a solução será implementada
dentro desse período.


IMPORTANTE:

Sua análise é consultiva.

A aprovação e a execução são humanas.


VERIFICAÇÃO DE CONSISTÊNCIA ANTES DE RESPONDER:

Confira internamente se os números citados
correspondem aos dados operacionais recebidos.

Não declare que os dados foram auditados.

As alternativas de recuperação são independentes.

Não recomende a combinação como obrigatória quando
uma alternativa isolada já atende à capacidade
necessária.

Se sugerir uma combinação, explique que ela é
opcional e depende de validação de viabilidade.

Não afirme redução de custos, economia ou retorno
financeiro sem dados financeiros fornecidos.

Não confunda metas projetadas com resultados alcançados.


REGRAS DE CONSISTÊNCIA OPERACIONAL:

1. Diferencie automação de novos chamados e
automação de chamados acumulados.

Explique como cada alternativa contribui
para reduzir a fila.

2. Não afirme que contratações são obrigatórias
sem comprovação da inviabilidade das demais
alternativas.

3. Não invente prazos de implantação, custos,
economias ou condições de contratação.

4. Trate as alternativas de recuperação como
independentes.

Combinações podem ser sugeridas como opções
adicionais, desde que sua viabilidade seja validada.

5. Diferencie resultados matematicamente projetados
de resultados operacionais efetivamente alcançados.

6. Não proponha prazos específicos para pilotos,
implementação, contratação ou validação quando
esses prazos não forem fornecidos.

O prazo de recuperação da fila não deve ser
confundido com o prazo de implantação de uma solução.

Quando o prazo de implantação for desconhecido,
recomende sua estimativa e validação pela liderança.

7. Não associe automaticamente o prazo de recuperação
da fila à duração de contratos temporários,
pilotos ou projetos de implantação.

8. Não afirme que uma alternativa possui menor
custo sem dados financeiros comparáveis.

Apresente custos como fatores que precisam
ser avaliados.

9. Com demanda e capacidade constantes, o crescimento
da fila é linear.

Não utilize termos como crescimento exponencial
sem evidências que sustentem essa projeção.

10. Não afirme que a meta de recuperação da fila
depende de implementação imediata.

O prazo projetado de recuperação considera
que a capacidade adicional esteja efetivamente
disponível durante o período calculado.

Quando o prazo de implantação for desconhecido,
não afirme que a recuperação ocorrerá em uma
data específica.

A meta de recuperação não é uma promessa
de prazo de implantação ou entrega.

"""

    return consultar_agente(prompt)


# ============================================================
# TESTE LOCAL DO AGENTE
# ============================================================

if __name__ == "__main__":

    dados_teste = {
        "operacao": "Suporte N2",
        "capacidade_semanal": 390,
        "demanda_semanal": 420,
        "deficit_semanal": 30,
        "fila_acumulada": 180,
        "prazo_recuperacao_semanas": 4,
        "capacidade_necessaria": 465,
        "alternativas": {
            "analistas_adicionais": 2,
            "reducao_tempo_percentual": 16.13,
            "casos_automatizar_semana": 75
        }
    }

    print("Iniciando análise operacional com IA...")
    print(analisar_operacao(dados_teste))
