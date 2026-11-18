
from capacity import calcular_capacidade

cenarios = {
    "N1 - Atual": {
        "analistas": 12,
        "acoes_por_caso": 1.8,
        "tempo_medio_minutos": 9,
        "demanda_semanal": 800,
        "fila_inicial": 140
    },
    "N1 - Futuro +20%": {
        "analistas": 7,
        "acoes_por_caso": 1.8,
        "tempo_medio_minutos": 5,
        "demanda_semanal": 960,
        "fila_inicial": 140
    },
    "N2 - Atual": {
        "analistas": 9,
        "acoes_por_caso": 3,
        "tempo_medio_minutos": 12,
        "demanda_semanal": 420,
        "fila_inicial": 180
    },
    "N2 - Futuro +20%": {
        "analistas": 7,
        "acoes_por_caso": 3,
        "tempo_medio_minutos": 9,
        "demanda_semanal": 504,
        "fila_inicial": 180
    }
}

for nome, parametros in cenarios.items():
    resultado = calcular_capacidade(
        horas_dia=8,
        dias_semana=5,
        disponibilidade=0.65,
        **parametros
    )

    print(f"\n=== {nome} ===")
    print("Capacidade:", resultado["capacidade_semanal"])
    print("Demanda:", resultado["demanda_semanal"])
    print("Utilizacao (%):", resultado["utilizacao_percentual"])
    print("Saldo:", resultado["saldo_capacidade"])
    print("Fila inicial:", resultado["fila_inicial"])
    print("Fila final:", resultado["fila_final"])
