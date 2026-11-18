
import math


def calcular_recuperacao(
    capacidade_semanal,
    demanda_semanal,
    fila_inicial,
    quantidade_analistas,
    tempo_medio_minutos,
    prazo_semanas
):
    """
    Calcula alternativas independentes para eliminar
    a fila acumulada dentro de um prazo determinado.
    """

    if capacidade_semanal <= 0:
        raise ValueError("A capacidade deve ser maior que zero.")

    if demanda_semanal < 0 or fila_inicial < 0:
        raise ValueError("Demanda e fila não podem ser negativas.")

    if quantidade_analistas <= 0 or tempo_medio_minutos <= 0:
        raise ValueError("Analistas e tempo médio devem ser positivos.")

    if prazo_semanas <= 0:
        raise ValueError("O prazo deve ser maior que zero.")

    saldo_atual = capacidade_semanal - demanda_semanal

    semanas_sem_intervencao = (
        math.ceil(fila_inicial / saldo_atual)
        if saldo_atual > 0
        else None
    )

    capacidade_necessaria = (
        demanda_semanal + fila_inicial / prazo_semanas
    )

    capacidade_por_analista = (
        capacidade_semanal / quantidade_analistas
    )

    analistas_adicionais = math.ceil(
        max(
            0,
            (capacidade_necessaria - capacidade_semanal)
            / capacidade_por_analista
        )
    )

    tempo_medio_necessario = (
        tempo_medio_minutos
        * capacidade_semanal
        / capacidade_necessaria
    )

    reducao_tempo_percentual = max(
        0,
        (1 - tempo_medio_necessario / tempo_medio_minutos) * 100
    )

    casos_automatizar_semana = math.ceil(
        max(0, capacidade_necessaria - capacidade_semanal)
    )

    return {
        "prazo_semanas": prazo_semanas,
        "fila_inicial": fila_inicial,
        "saldo_atual": round(saldo_atual, 2),
        "semanas_sem_intervencao": semanas_sem_intervencao,
        "capacidade_necessaria": round(capacidade_necessaria, 2),
        "analistas_adicionais": analistas_adicionais,
        "tempo_medio_necessario": round(tempo_medio_necessario, 2),
        "reducao_tempo_percentual": round(reducao_tempo_percentual, 2),
        "casos_automatizar_semana": casos_automatizar_semana
    }
