
import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

import re


def validar_resposta_ia(texto):
    """
    Identifica afirmações que exigem validação adicional.
    Não modifica os cálculos do simulador.
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


def consultar_agente(pergunta):
    resposta = cliente.models.generate_content(
        model=MODELO,
        contents=pergunta
    )

    texto = resposta.text

    if not texto:
        raise ValueError(
            "O Gemini não retornou uma resposta textual."
        )

    alertas = validar_resposta_ia(texto)

    if alertas:
        texto += "\n\n---\n"
        texto += "### ⚠️ Alertas de validação automática\n"

        for alerta in alertas:
            texto += f"- {alerta}\n"

        texto += (
            "\n**Atenção:** este diagnóstico contém "
            "afirmações que precisam de validação "
            "antes de qualquer decisão gerencial."
        )

    return texto

    


def analisar_operacao(dados_operacionais):
    """
    Analisa os indicadores calculados pelo sistema.
    A IA não substitui os cálculos matemáticos.
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
11. As alternativas de recuperação apresentadas pelo simulador
são independentes. Cada uma representa uma possibilidade
de atingir a capacidade necessária isoladamente, desde que
suas premissas sejam atendidas.
12. Não afirme que é obrigatório combinar contratação,
automação e produtividade para alcançar a meta.
13. Caso recomende combinar alternativas, apresente a
combinação como estratégia opcional e justifique seus benefícios.
14. Não afirme que automação é mais barata que contratação
sem dados comprovados de custos e investimentos.
15. Não invente prazos de implantação, retorno financeiro,
economia ou ganhos de produtividade.
16. Diferencie capacidade teórica de resultados efetivamente
alcançados na operação.
17. Apresente as recomendações como propostas sujeitas
a validação técnica, financeira e gerencial.
18. Não considere tickets transferidos ou reclassificados
como resolvidos sem evidência de encerramento efetivo.


DADOS OPERACIONAIS:
{dados_json}

ESTRUTURA DA RESPOSTA:

1. DIAGNÓSTICO EXECUTIVO
Explique a situação operacional com os números
fornecidos.

2. PRINCIPAIS RISCOS
Identifique riscos de capacidade, fila,
produtividade e atendimento.

3. RECOMENDAÇÕES PRIORIZADAS
Apresente até cinco ações, explicando
o impacto esperado e as dependências.

4. PLANO DE RECUPERAÇÃO
Analise as alternativas calculadas e o prazo
necessário para recuperação da fila.

5. INDICADORES DE ACOMPANHAMENTO
Recomende indicadores para monitorar a execução.

6. DECISÃO GERENCIAL
Indique qual decisão deve ser avaliada
pela liderança, com justificativa.

IMPORTANTE:
Sua análise é consultiva.
A aprovação e a execução são humanas.

VALIDAÇÃO FINAL OBRIGATÓRIA:
Antes de concluir, confira se todos os números citados
correspondem exatamente aos dados operacionais recebidos.

As alternativas de recuperação são independentes.
Não recomende a combinação como obrigatória quando uma
alternativa isolada já atende à capacidade necessária.

Se sugerir uma combinação, explique que ela é opcional
e depende de validação de viabilidade.

Não afirme redução de custos, economia ou retorno
financeiro sem dados financeiros fornecidos.

Não confunda metas projetadas com resultados alcançados. 


REGRAS DE CONSISTÊNCIA OPERACIONAL:

1. Diferencie automação de novos chamados e automação
   de chamados acumulados. Explique como cada alternativa
   contribui para reduzir a fila.

2. Não afirme que contratações são obrigatórias sem
   comprovação da inviabilidade das demais alternativas.

3. Não invente prazos de implantação, custos, economias
   ou condições de contratação.

4. Trate as alternativas de recuperação como independentes.
   Combinações podem ser sugeridas como opções adicionais,
   desde que sua viabilidade seja validada.

5. Diferencie resultados matematicamente projetados
   de resultados operacionais efetivamente alcançados.

6. Não proponha prazos específicos para pilotos,
   implementação, contratação ou validação
   quando esses prazos não forem fornecidos.

   O prazo de recuperação da fila não deve ser
   confundido com o prazo de implantação de uma solução.

   Quando o prazo de implantação for desconhecido,
   recomende sua estimativa e validação pela liderança.
7. Não associe automaticamente o prazo de recuperação
   da fila à duração de contratos temporários, pilotos
   ou projetos de implantação.

8. Não afirme que uma alternativa possui menor custo
   sem dados financeiros comparáveis. Apresente custos
   como fatores que precisam ser avaliados.

9. Com demanda e capacidade constantes, o crescimento
   da fila é linear. Não utilize termos como crescimento
   exponencial sem evidências que sustentem essa projeção.

"""

    return consultar_agente(prompt)


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
