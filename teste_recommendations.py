
from recommendations import gerar_recomendacoes

resultado = gerar_recomendacoes(
    capacidade_semanal=390,
    demanda_semanal=420,
    quantidade_analistas=5,
    tempo_medio_minutos=30
)

print("=== RECOMENDACOES N2 ===")

for indicador, valor in resultado.items():
    print(f"{indicador}: {valor}")
