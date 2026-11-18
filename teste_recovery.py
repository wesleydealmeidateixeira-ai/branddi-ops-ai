
from recovery import calcular_recuperacao

resultado = calcular_recuperacao(
    capacidade_semanal=390,
    demanda_semanal=420,
    fila_inicial=180,
    quantidade_analistas=9,
    tempo_medio_minutos=36,
    prazo_semanas=4
)

print("=== PLANO DE RECUPERACAO N2 ===")

for indicador, valor in resultado.items():
    print(f"{indicador}: {valor}")
