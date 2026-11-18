
import math


def gerar_recomendacoes(
    capacidade_semanal,
    demanda_semanal,
    quantidade_analistas,
    tempo_medio_minutos
):
    """
    Calcula alternativas para eliminar o déficit semanal
    de capacidade operacional.
    """

    if capacidade_semanal <= 0:
        raise ValueError("A capacidade deve ser maior que zero.")

    if quantidade_analistas <= 0 or tempo_medio_minutos <= 0:
        raise ValueError("Analistas e tempo médio devem ser positivos.")

    if demanda_semanal < 0:
        raise ValueError("A demanda não pode ser negativa.")

    deficit = max(0, demanda_semanal - capacidade_semanal)

    capacidade_por_analista = (
        capacidade_semanal / quantidade_analistas
    )

    analistas_adicionais = math.ceil(
        max(0, demanda_semanal / capacidade_por_analista
            - quantidade_analistas)
    )

    tempo_medio_necessario = (
        tempo_medio_minutos * capacidade_semanal
        / demanda_semanal
        if demanda_semanal > 0
        else tempo_medio_minutos
    )

    reducao_tempo_percentual = max(
        0,
        (1 - tempo_medio_necessario / tempo_medio_minutos) * 100
    )

    percentual_automacao = (
        deficit / demanda_semanal * 100
        if demanda_semanal > 0
        else 0
    )

    return {
        "deficit_semanal": round(deficit, 2),
        "analistas_adicionais": analistas_adicionais,
        "tempo_medio_necessario": round(tempo_medio_necessario, 2),
        "reducao_tempo_percentual": round(reducao_tempo_percentual, 2),
        "casos_para_automatizar": math.ceil(deficit),
        "percentual_automacao": round(percentual_automacao, 2)
    }
