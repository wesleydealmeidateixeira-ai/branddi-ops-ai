
def calcular_capacidade(
    analistas,
    horas_dia,
    dias_semana,
    disponibilidade,
    tempo_medio_minutos,
    demanda_semanal,
    acoes_por_caso=1,
    fila_inicial=0
):
    if analistas < 0 or horas_dia <= 0 or dias_semana <= 0:
        raise ValueError("Quantidade de analistas ou jornada inválida.")

    if not 0 <= disponibilidade <= 1:
        raise ValueError("Disponibilidade deve estar entre 0 e 1.")

    if tempo_medio_minutos <= 0 or acoes_por_caso <= 0:
        raise ValueError("Tempo e ações por caso devem ser positivos.")

    if demanda_semanal < 0 or fila_inicial < 0:
        raise ValueError("Demanda e fila não podem ser negativas.")

    minutos_disponiveis = (
        analistas * horas_dia * dias_semana * 60 * disponibilidade
    )

    minutos_por_caso = acoes_por_caso * tempo_medio_minutos

    capacidade = minutos_disponiveis / minutos_por_caso

    utilizacao = (
        demanda_semanal / capacidade * 100
        if capacidade > 0 else 0
    )

    saldo = capacidade - demanda_semanal

    fila_final = max(0, fila_inicial - saldo)

    return {
        "capacidade_semanal": round(capacidade, 2),
        "demanda_semanal": demanda_semanal,
        "utilizacao_percentual": round(utilizacao, 2),
        "saldo_capacidade": round(saldo, 2),
        "fila_inicial": fila_inicial,
        "fila_final": round(fila_final, 2),
        "minutos_por_caso": round(minutos_por_caso, 2)
    }
