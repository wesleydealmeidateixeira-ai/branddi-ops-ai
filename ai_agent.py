import os
import json
import re

from dotenv import load_dotenv
from google import genai
from google.genai import types


# CONFIGURAÇÃO DO AGENTE
load_dotenv()
chave_api = os.getenv("GEMINI_API_KEY")

if not chave_api:
    try:
        import streamlit as st
        chave_api = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        pass
if not chave_api:
    raise ValueError("GEMINI_API_KEY não encontrada. Configure .env ou Streamlit Secrets.")

cliente = genai.Client(
    api_key=chave_api,
    http_options=types.HttpOptions(timeout=120000),
)
MODELO = "gemini-3.5-flash-lite"
FRASE_VALIDACAO = (
    "Os indicadores apresentados foram fornecidos pela "
    "aplicação e utilizados como base para esta análise."
)


def validar_resposta_ia(texto):
    """Sinaliza afirmações financeiras e prazos que exigem revisão humana."""
    alertas = []
    padroes_financeiros = [
        r"\bmaior ROI\b", r"\bmenor custo\b", r"\bmais barata\b",
        r"\beconomia garantida\b", r"\bretorno financeiro garantido\b",
    ]
    if any(re.search(p, texto, re.IGNORECASE) for p in padroes_financeiros):
        alertas.append("A resposta contém uma afirmação financeira que precisa de comprovação.")

    padroes_prazos = [
        r"\bem até \d+ (dias?|semanas?|meses?)\b",
        r"\bpiloto de \d+ (dias?|semanas?|meses?)\b",
        r"\bimplementação em \d+ (dias?|semanas?|meses?)\b",
        r"\bimplementad[ao] em \d+ (dias?|semanas?|meses?)\b",
        r"\bimplementar em \d+ (dias?|semanas?|meses?)\b",
    ]
    if any(re.search(p, texto, re.IGNORECASE) for p in padroes_prazos):
        alertas.append("A resposta contém um prazo que precisa ser conferido com os dados fornecidos.")
    return alertas


def padronizar_validacao_final(texto):
    """Evita declaração final duplicada; não realiza auditoria dos dados."""
    padrao_secao = r"(?im)^\s{0,3}(?:#{1,6}\s*)?(?:\*\*)?validação final(?:\*\*)?\s*:?\s*$"
    resultado = re.search(padrao_secao, texto)
    if resultado:
        texto = texto[:resultado.start()].rstrip()
    texto = texto.replace(FRASE_VALIDACAO, "").rstrip()
    texto = re.sub(r"(?:\n\s*---\s*)+$", "", texto).rstrip()
    return texto + "\n\n---\n\n**Validação final:** " + FRASE_VALIDACAO


def consultar_agente(pergunta):
    """Consulta o Gemini e aplica as validações textuais existentes."""
    resposta = cliente.models.generate_content(
        model=MODELO,
        contents=pergunta,
        config=types.GenerateContentConfig(
            max_output_tokens=1200,
            temperature=0.2,
        ),
    )
    texto = resposta.text
    if not texto or not texto.strip():
        raise ValueError("O Gemini não retornou uma resposta textual.")

    alertas = validar_resposta_ia(texto)
    texto = padronizar_validacao_final(texto)
    if alertas:
        texto += "\n\n---\n\n### ⚠️ Alertas de validação automática\n"
        for alerta in alertas:
            texto += f"- {alerta}\n"
        texto += (
            "\n**Atenção:** este diagnóstico contém afirmações que precisam "
            "de validação antes de qualquer decisão gerencial."
        )
    return texto


def analisar_operacao(dados_operacionais):
    """Interpreta indicadores fornecidos pela aplicação sem recalculá-los."""
    dados_json = json.dumps(dados_operacionais, ensure_ascii=False, separators=(",", ":"))
    prompt = f"""Você é o Branddi Ops AI, consultor de operações SaaS, suporte N1/N2 e gestão de filas.
Responda em português do Brasil, com objetividade, usando SOMENTE os dados abaixo.

REGRAS:
- Não invente nem altere indicadores, custos, economias, resultados ou prazos.
- Diferencie fatos, hipóteses, projeções e recomendações. Não alegue auditoria ou consulta a fontes externas.
- Não considere tickets transferidos/reclassificados como resolvidos sem encerramento comprovado.
- Com demanda e capacidade constantes, a evolução do backlog é linear.
- Diferencie automação de demanda nova e do backlog.
- Alternativas de recuperação são independentes; combinações são opcionais, não obrigatórias.
- Não compare custos sem dados financeiros; não confunda prazo de recuperação com implantação.
- Não garanta resultados ou determine contratação, automação ou mudanças sem aprovação humana.
- Os dados vêm da aplicação; não inclua seção de validação final, pois será acrescentada pelo sistema.

DADOS: {dados_json}

Produza EXATAMENTE seis seções curtas, com títulos:
1. DIAGNÓSTICO EXECUTIVO — situação e números relevantes.
2. PRINCIPAIS RISCOS — capacidade, fila, produtividade e SLA.
3. RECOMENDAÇÕES PRIORIZADAS — até 3 ações com dependências.
4. PLANO DE RECUPERAÇÃO — alternativas independentes e premissas da meta.
5. INDICADORES DE ACOMPANHAMENTO — até 5 indicadores.
6. DECISÃO GERENCIAL — comparar viabilidade técnica, financeira, riscos e capacidade de execução antes de aprovar.
Se não houver dados para alguma conclusão, declare a limitação. Seja conciso."""
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
            "casos_automatizar_semana": 75,
        },
    }
    print("Iniciando análise operacional com IA...")
    print(analisar_operacao(dados_teste))
