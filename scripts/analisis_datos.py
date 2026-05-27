
import pandas as pd
import os

# Carga de datos deportivos desde la estructura del repositorio
df = pd.read_csv('datos/resultados.csv')

# Diccionario centralizador de métricas de rendimiento por equipo
estadisticas = {}

def obtener_o_inicializar(equipo):
    if equipo not in estadisticas:
        estadisticas[equipo] = {'puntos': 0, 'partidos_jugados': 0, 'ganados': 0, 'empates': 0, 'derrotas': 0, 'goles_favor': 0}
    return estadisticas[equipo]

# Iteración iterativa del vector de resultados (Lógica de Negocio)
for _, fila in df.iterrows():
    local = fila['equipo_local']
    visitante = fila['equipo_visitante']
    g_local = int(fila['goles_local'])
    g_visitante = int(fila['goles_visitante'])

    est_local = obtener_o_inicializar(local)
    est_visitante = obtener_o_inicializar(visitante)

    # Acumulación de goles y partidos
    est_local['goles_favor'] += g_local
    est_local['partidos_jugados'] += 1
    est_visitante['goles_favor'] += g_visitante
    est_visitante['partidos_jugados'] += 1

    # Evaluación de victorias, empates y derrotas para el cómputo de puntajes
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

# Transformación a DataFrame para manipulación matemática avanzada
df_posiciones = pd.DataFrame.from_dict(estadisticas, orient='index').reset_index()
df_posiciones.rename(columns={'index': 'equipo'}, inplace=True)

# Cálculo matemático del promedio de gol por partido global e individual
df_posiciones['promedio_gol'] = (df_posiciones['goles_favor'] / df_posiciones['partidos_jugados']).round(2)

# Ordenamiento descendente de alta eficiencia según puntos obtenidos
df_posiciones = df_posiciones.sort_values(by='puntos', ascending=False).reset_index(drop=True)

# Exportación del reporte ordenado final en formato CSV plano
df_posiciones.to_csv('resultados/tabla_posiciones.csv', index=False)
print("Análisis finalizado. Tabla de posiciones exportada.")

import matplotlib.pyplot as plt

# Abstracción visual mediante diagrama de barras cruzadas
plt.figure(figsize=(10, 6))
plt.bar(df_posiciones['equipo'], df_posiciones['puntos'], color=['skyblue', 'navy', 'red', 'green', 'gray'])
plt.title('Rendimiento General de los Equipos - Puntos Totales')
plt.xlabel('Equipos')
plt.ylabel('Puntos')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Guardar la salida gráfica en el directorio de resultados correspondientes
plt.savefig('resultados/rendimiento_equipos.png', dpi=300)
plt.close()
print("Abstracción gráfica exportada con éxito.")
