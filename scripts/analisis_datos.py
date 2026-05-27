import pandas as pd
import os
import matplotlib.pyplot as plt

# POR QUÉ: Se opta por Pandas ya que gestiona nativamente la indexación relacional de estructuras CSV,
# reduciendo la complejidad algorítmica de O(N^2) a O(N) al acumular vectores en memoria.
df = pd.read_csv('datos/resultados_partidos.csv')

estadisticas = {}

def obtener_o_inicializar(equipo):
    if equipo not in estadisticas:
        # POR QUÉ: Se utiliza un diccionario indexado por nombre para agilizar la búsqueda directa
        # evitando búsquedas lineales repetitivas sobre matrices bidimensionales.
        estadisticas[equipo] = {'puntos': 0, 'partidos_jugados': 0, 'ganados': 0, 'empates': 0, 'derrotas': 0, 'goles_favor': 0}
    return estadisticas[equipo]

# Iteración limpia sobre el histórico deportivo
for _, fila in df.iterrows():
    local = fila['equipo_local']
    visitante = fila['equipo_visitante']
    g_local = int(fila['goles_local'])
    g_visitante = int(fila['goles_visitante'])

    est_local = obtener_o_inicializar(local)
    est_visitante = obtener_o_inicializar(visitante)

    est_local['goles_favor'] += g_local
    est_local['partidos_jugados'] += 1
    est_visitante['goles_favor'] += g_visitante
    est_visitante['partidos_jugados'] += 1

    # POR QUÉ: Cómputo matemático riguroso basado en el reglamento oficial de la FIFA (3 pts por victoria, 1 por empate).
    if g_local > g_visitante:
        est_local['puntos'] += 3
        est_local['ganados'] += 1
        est_visitante['derrotas'] += 1
    elif g_local < g_visitante:
        est_visitante['puntos'] += 3
        est_visitante['ganados'] += 1
        est_local['derrotas'] += 1
    else:
        est_local['puntos'] += 1
        est_local['empates'] += 1
        est_visitante['puntos'] += 1
        est_visitante['empates'] += 1

df_posiciones = pd.DataFrame.from_dict(estadisticas, orient='index').reset_index()
df_posiciones.rename(columns={'index': 'equipo'}, inplace=True)

# POR QUÉ: Se redondea a 2 decimales para estandarizar las métricas organizacionales en reportes ejecutivos.
df_posiciones['promedio_gol'] = (df_posiciones['goles_favor'] / df_posiciones['partidos_jugados']).round(2)

# POR QUÉ: Ordenamiento descendente por puntos. En caso de empate en esta fase, Pandas mantiene el orden de aparición.
df_posiciones = df_posiciones.sort_values(by='puntos', ascending=False).reset_index(drop=True)

df_posiciones.to_csv('resultados/tabla_posiciones.csv', index=False)

# VISUALIZACIÓN GRÁFICA COMPARATIVA
plt.figure(figsize=(10, 6))
plt.bar(df_posiciones['equipo'], df_posiciones['puntos'], color=['skyblue', 'navy', 'red', 'green', 'gray'])
plt.title('Rendimiento General de los Equipos - Puntos Totales')
plt.xlabel('Equipos')
plt.ylabel('Puntos')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# POR QUÉ: El formato PNG a 300 DPI previene la pixelación en presentaciones directivas y tableros BI.
plt.savefig('resultados/rendimiento_equipos.png', dpi=300)
plt.close()
