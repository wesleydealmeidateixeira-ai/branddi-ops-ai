import logging

import streamlit as st
from capacity import calcular_capacidade
from recommendations import gerar_recomendacoes
from recovery import calcular_recuperacao
from database import registrar_decisao, consultar_decisoes
from ai_agent import analisar_operacao
st.set_page_config(
    page_title="Branddi Ops AI",
    page_icon="📊",
    layout="wide"
)

st.title("Branddi Ops AI")
st.subheader("Inteligência Operacional e Automação com IA")

st.success("Sistema iniciado com sucesso!")

st.write("Bem-vindo ao painel de gestão operacional da Branddi.")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Casos N1 / Semana", "800")

with col2:
    st.metric("Casos N2 / Semana", "420")

with col3:
    st.metric("Disponibilidade Produtiva", "65%")

st.divider()

st.info("Ambiente de demonstração. Dados iniciais do case.")


st.header("Simulador de Capacidade Operacional")

st.write("Configure os parametros para simular a capacidade da equipe.")

analistas = st.number_input(
    "Quantidade de analistas",
    min_value=1,
    value=5,
    step=1
)

horas_dia = st.number_input(
    "Horas trabalhadas por dia",
    min_value=1,
    max_value=24,
    value=8
)

dias_semana = st.number_input(
    "Dias trabalhados por semana",
    min_value=1,
    max_value=7,
    value=5
)

disponibilidade = st.slider(
    "Disponibilidade produtiva (%)",
    min_value=0,
    max_value=100,
    value=65
)

tempo_medio = st.number_input(
    "Tempo medio por caso (minutos)",
    min_value=1,
    value=30
)

demanda = st.number_input(
    "Demanda semanal de casos",
    min_value=0,
    value=420
)

resultado = calcular_capacidade(
    analistas=analistas,
    horas_dia=horas_dia,
    dias_semana=dias_semana,
    disponibilidade=disponibilidade / 100,
    tempo_medio_minutos=tempo_medio,
    demanda_semanal=demanda
)


st.subheader("Resultado da Simulação")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.metric(
        "Capacidade Semanal",
        f"{resultado['capacidade_semanal']:.2f} casos"
    )

with col_b:
    st.metric(
        "Utilização da Capacidade",
        f"{resultado['utilizacao_percentual']:.2f}%"
    )

with col_c:
    st.metric(
        "Saldo de Capacidade",
        f"{resultado['saldo_capacidade']:.2f} casos"
    )

if resultado["saldo_capacidade"] < 0:
    st.error("Alerta: demanda acima da capacidade operacional!")
else:
    st.success("Capacidade operacional suficiente para a demanda.")

st.divider()
st.header("Diagnóstico Operacional — N1 e N2")

st.caption(
    "Comparação entre a operação atual e o cenário futuro "
    "com crescimento de 20% na demanda."
)

cenarios_operacionais = {
    "N1 Atual": (12, 1.8, 9, 800, 140),
    "N1 Futuro": (7, 1.8, 5, 960, 140),
    "N2 Atual": (9, 3, 12, 420, 180),
    "N2 Futuro": (7, 3, 9, 504, 180)
}
resultados_cenarios = {}
for nome, dados in cenarios_operacionais.items():
    analistas, acoes, tempo, demanda, fila = dados

    resultado_cenario = calcular_capacidade(
        analistas=analistas,
        horas_dia=8,
        dias_semana=5,
        disponibilidade=0.65,
        acoes_por_caso=acoes,
        tempo_medio_minutos=tempo,
        demanda_semanal=demanda,
               fila_inicial=fila
    )

    resultados_cenarios[nome] = resultado_cenario

    st.subheader(nome)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Capacidade Semanal",
            f"{resultado_cenario['capacidade_semanal']:.2f}"
        )

    with c2:
        st.metric(
            "Utilização",
            f"{resultado_cenario['utilizacao_percentual']:.2f}%"
        )

    with c3:
        st.metric(
            "Fila Projetada",
            f"{resultado_cenario['fila_final']:.2f}"
        )

    if resultado_cenario["saldo_capacidade"] < 0:
        st.error("Capacidade insuficiente para a demanda.")
    else:
        st.success("Capacidade suficiente para a demanda.")

    st.divider()

st.header("Recomendações Operacionais — N2")

st.write(
    "Alternativas para eliminar o déficit semanal "
    "de capacidade do N2."
)

resultado_n2_atual = resultados_cenarios["N2 Atual"]

analistas_n2, acoes_n2, tempo_n2, demanda_n2, fila_n2 = (
    cenarios_operacionais["N2 Atual"]
)

recomendacoes_n2 = gerar_recomendacoes(
    capacidade_semanal=resultado_n2_atual["capacidade_semanal"],
    demanda_semanal=resultado_n2_atual["demanda_semanal"],
    quantidade_analistas=analistas_n2,
    tempo_medio_minutos=tempo_n2 * acoes_n2
)

if recomendacoes_n2["deficit_semanal"] > 0:
    st.warning(
        "O N2 apresenta déficit de "
        f"{recomendacoes_n2['deficit_semanal']:.0f} "
        "casos por semana."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Analistas adicionais",
            recomendacoes_n2["analistas_adicionais"]
        )

    with col2:
        st.metric(
            "Redução do tempo médio",
            f"{recomendacoes_n2['reducao_tempo_percentual']:.2f}%"
        )

    with col3:
        st.metric(
            "Casos para automatizar/semana",
            recomendacoes_n2["casos_para_automatizar"]
        )

    st.info(
        "Alternativas independentes para equilibrar a "
        "demanda semanal. A fila acumulada exige "
        "um plano adicional de redução."
    )
else:
    st.success(
        "O N2 possui capacidade suficiente "
        "para atender à demanda semanal."
    )

st.divider()

st.header("Plano de Recuperação Operacional — N2")

st.write(
    "Simule os recursos necessários para eliminar "
    "a fila acumulada do N2 dentro do prazo desejado."
)

prazo_recuperacao = st.slider(
    "Prazo para eliminar a fila (semanas)",
    min_value=1,
    max_value=12,
    value=4,
    step=1
)

resultado_recuperacao = calcular_recuperacao(
    capacidade_semanal=resultado_n2_atual["capacidade_semanal"],
    demanda_semanal=resultado_n2_atual["demanda_semanal"],
    fila_inicial=resultado_n2_atual["fila_inicial"],
    quantidade_analistas=analistas_n2,
    tempo_medio_minutos=tempo_n2 * acoes_n2,
    prazo_semanas=prazo_recuperacao
)

st.subheader("Diagnóstico da Recuperação")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Fila Acumulada",
        f"{resultado_recuperacao['fila_inicial']:.0f} casos"
    )

with c2:
    st.metric(
        "Capacidade Necessária",
        f"{resultado_recuperacao['capacidade_necessaria']:.0f} casos/semana"
    )

with c3:
    st.metric(
        "Prazo de Recuperação",
        f"{prazo_recuperacao} semanas"
    )

st.subheader("Alternativas de Recuperação")

c4, c5, c6 = st.columns(3)

with c4:
    st.metric(
        "Analistas Adicionais",
        resultado_recuperacao["analistas_adicionais"]
    )

with c5:
    st.metric(
        "Redução do Tempo Médio",
        f"{resultado_recuperacao['reducao_tempo_percentual']:.2f}%"
    )

with c6:
    st.metric(
        "Casos para Automatizar/Semana",
        resultado_recuperacao["casos_automatizar_semana"]
    )

st.info(
    "As alternativas são independentes e representam "
    "a capacidade adicional necessária para absorver "
    "a demanda semanal e reduzir a fila acumulada "
    "dentro do prazo selecionado."
)



st.divider()

st.header("Diagnóstico Executivo com Inteligência Artificial")

st.write(
    "O Branddi Ops AI utiliza o Gemini para interpretar "
    "os indicadores operacionais e propor ações gerenciais. "
    "Os cálculos são realizados pelo simulador e "
    "as decisões permanecem sob responsabilidade humana."
)

dados_para_ia = {
    "operacao": "Suporte N2",
    "capacidade_semanal": resultado_n2_atual["capacidade_semanal"],
    "demanda_semanal": resultado_n2_atual["demanda_semanal"],
    "deficit_semanal": max(
        0,
        -resultado_n2_atual["saldo_capacidade"]
    ),
    "fila_acumulada": resultado_recuperacao["fila_inicial"],
    "prazo_recuperacao_semanas": prazo_recuperacao,
    "capacidade_necessaria": resultado_recuperacao[
        "capacidade_necessaria"
    ],
    "alternativas_recuperacao": {
        "analistas_adicionais": resultado_recuperacao[
            "analistas_adicionais"
        ],
        "reducao_tempo_percentual": resultado_recuperacao[
            "reducao_tempo_percentual"
        ],
        "casos_automatizar_semana": resultado_recuperacao[
            "casos_automatizar_semana"
        ]
    }
}

if st.button(
    "Gerar diagnóstico com IA",
    type="primary"
):
    with st.spinner(
        "O Gemini está analisando os indicadores operacionais..."
    ):
        try:
            diagnostico_ia = analisar_operacao(dados_para_ia)

            if diagnostico_ia:
                st.session_state["diagnostico_ia"] = diagnostico_ia
                st.session_state["dados_diagnostico_ia"] = (
                    dados_para_ia.copy()
                )
            else:
                st.warning(
                    "O Gemini não retornou um diagnóstico."
                )

        except Exception as erro:
            logging.error(
                "Falha na consulta ao Gemini (%s)",
                type(erro).__name__,
                exc_info=True
            )
            st.error(
                "Não foi possível consultar o Gemini. "
                "Verifique a conexão ou tente novamente. "
                "Os cálculos operacionais continuam disponíveis."
            )

if "diagnostico_ia" in st.session_state:
    if (
        st.session_state.get("dados_diagnostico_ia")
        == dados_para_ia
    ):
        st.markdown(st.session_state["diagnostico_ia"])
        st.caption(
            "Parecer gerado por IA. "
            "Recomendações sujeitas à validação e aprovação humana."
        )
    else:
        st.info(
            "Os parâmetros da simulação foram alterados. "
            "Gere um novo diagnóstico para atualizar a análise."
        )

st.divider()


st.header("Revisão Humana — Decisão Gerencial")

st.write(
    "Analise as recomendações operacionais e registre "
    "a decisão antes de qualquer implementação."
)

with st.form("formulario_decisao_gerencial", clear_on_submit=True):
    decisao_gerencial = st.radio(
        "Qual é a decisão sobre o plano de recuperação do N2?",
        [
            "Aprovar recomendação",
            "Solicitar ajustes",
            "Rejeitar recomendação"
        ],
        index=None
    )

    justificativa = st.text_area(
        "Justificativa da decisão",
        placeholder="Descreva os motivos e critérios da decisão..."
    )

    responsavel = st.text_input(
        "Responsável pela decisão",
        placeholder="Ex.: Gerente Operacional"
    )

    confirmar = st.form_submit_button("Registrar decisão")

if confirmar:
    if not decisao_gerencial:
        st.error("Selecione uma decisão.")
    elif not justificativa.strip():
        st.error("Informe a justificativa.")
    elif not responsavel.strip():
        st.error("Informe o responsável.")
    else:
        try:
            id_registro = registrar_decisao(
                decisao=decisao_gerencial,
                justificativa=justificativa.strip(),
                responsavel=responsavel.strip(),
                capacidade_semanal=resultado_n2_atual[
                    "capacidade_semanal"
                ],
                demanda_semanal=resultado_n2_atual[
                    "demanda_semanal"
                ],
                fila_inicial=fila_n2,
                prazo_semanas=prazo_recuperacao
            )

            st.success(
                f"Decisão registrada com sucesso! "
                f"Registro nº {id_registro}."
            )

        except Exception as erro:
            st.error(f"Erro ao registrar decisão: {erro}")

st.divider()

st.header("Histórico de Decisões Gerenciais")

try:
    historico = consultar_decisoes()

    if historico:
        st.metric("Total de decisões registradas", len(historico))

        st.dataframe(
            historico,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Nenhuma decisão registrada até o momento.")

except Exception as erro:
    st.error(f"Erro ao consultar histórico: {erro}")
