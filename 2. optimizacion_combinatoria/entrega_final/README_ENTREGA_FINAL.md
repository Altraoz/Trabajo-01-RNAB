# Entrega final de optimizacion combinatoria

Esta carpeta reune los artefactos finales listos para usar en la entrega de la
parte de optimizacion combinatoria del trabajo.

## Resultado final recomendado

- Metodo ganador: `GA`
- Costo final del mejor tour: `4303.602999`
- Numero de ciudades: `96`
- Formula de costo:
  `peajes(euros) + gasolina(euros) + (tiempo(min)/60) * 12.02`

## Archivos principales

- `resultado_final_ga.json`
  Resultado final del mejor algoritmo encontrado.

- `resumen_final_ga.json`
  Resumen corto del mejor resultado.

- `tour_expandido_final_ga.json`
  Recorrido real expandido sobre el grafo original.

- `mejor_solucion_combinatoria.gif`
  GIF final de la mejor solucion combinatoria.

- `comparativo_aco_vs_ga.md`
  Comparacion final entre colonia de hormigas y algoritmo genetico.

- `visualizacion_mejor_solucion.svg`
  Visualizacion estatica del recorrido final.

- `convergencia_aco_final.svg`
  Convergencia del ACO.

## Lectura recomendada para el reporte

1. Usar `comparativo_aco_vs_ga.md` como base del analisis comparativo.
2. Reportar que el mejor resultado final fue obtenido por `GA`.
3. Usar el `gif` como evidencia visual de la mejor solucion.
4. Usar `tour_expandido_final_ga.json` si necesitan describir el recorrido real.

## Nota

El archivo `tour_expandido_final_ga.json` corresponde al mejor tour del
algoritmo genetico, que fue el ganador final en las corridas del `22 de julio
de 2026`.
