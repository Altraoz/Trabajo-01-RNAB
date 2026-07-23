# Comparativo ACO vs GA sobre el TSP de 96 capitales de Francia

## Contexto comun

Ambos algoritmos se ejecutaron sobre la misma matriz completa `96x96` construida
con el modelo de costo alineado al enunciado:

`costo_total = peajes(euros) + gasolina(euros) + (tiempo(min)/60) * 12.02`

Supuestos usados:

- Vehiculo de referencia: `Renault Clio`
- Tarifa del vendedor: `12.02 EUR/h`
- Salario de referencia: `SMIC Francia 2026`
- Nodo de inicio y cierre del tour: `Bourg-en-Bresse (indice 0)`

## Configuracion usada

### ACO

- Hormigas: `40`
- Iteraciones: `250`
- `alpha = 1.0`
- `beta = 3.0`
- Evaporacion: `0.35`
- Intensificacion: `2.0`
- Elite weight: `2.0`
- Semilla: `42`

### GA

- Tamano de poblacion: `180`
- Generaciones: `350`
- Tasa de mutacion: `0.12`
- Tasa de cruce: `0.9`
- Elite count: `12`
- Tournament size: `5`
- Semilla: `42`
- Inicializacion con semilla ACO: `si`

## Resultado principal

| Metodo | Mejor costo del tour | Ciudades visitadas | Longitud del tour cerrado |
|---|---:|---:|---:|
| ACO | `4471.569332` | `96` | `97` |
| GA | `4303.602999` | `96` | `97` |

## Diferencia entre metodos

- Mejora absoluta de GA frente a ACO: `167.966333`
- Mejora relativa de GA frente a ACO: `3.76%`

Calculo:

`(4471.569332 - 4303.602999) / 4471.569332 * 100 = 3.76%`

## Lectura del resultado

En estas corridas finales, el algoritmo genetico obtuvo una mejor solucion que
el algoritmo de colonia de hormigas.

Esto significa que, bajo la misma definicion de costo y usando la misma matriz
de entrada:

- `GA` encontro un tour mas barato
- `ACO` tambien encontro un tour valido y consistente, pero con mayor costo

## Comportamiento de convergencia

### ACO

- Arranco con un mejor costo inicial de `6855.457334`
- Bajo progresivamente hasta `4471.569332`
- La mejora fuerte ocurrio en las primeras iteraciones
- Luego entro en una zona de estabilizacion relativamente rapida

### GA

- Arranco usando como mejor referencia inicial el tour sembrado desde ACO
- Mejoro desde `4471.569332` hasta `4303.602999`
- La mejora se dio por escalones, no de manera continua
- La poblacion fue refinando una solucion que ya era buena y logro superarla

## Interpretacion tecnica

Una lectura razonable de estas corridas es la siguiente:

- `ACO` fue util para construir rapidamente una solucion buena y factible
- `GA` fue especialmente fuerte refinando el orden de visita hasta encontrar un
  tour mejor
- En este problema, la combinacion de ambos enfoques es valiosa:
  - primero `ACO` como explorador de una buena ruta
  - luego `GA` como refinador

## Archivos de soporte

- Resultado ACO: [resultado_aco_final.json](C:\Carlos\Uni\Algortimos\trabajos\trabajo_1\trabajo_carlos\2. optimizacion_combinatoria\fase_7_aco_final\resultado_aco_final.json)
- Resumen ACO: [resumen_aco_final.json](C:\Carlos\Uni\Algortimos\trabajos\trabajo_1\trabajo_carlos\2. optimizacion_combinatoria\fase_7_aco_final\resumen_aco_final.json)
- Resultado GA: [resultado_ga_final.json](C:\Carlos\Uni\Algortimos\trabajos\trabajo_1\trabajo_carlos\2. optimizacion_combinatoria\fase_8_ga_final\resultado_ga_final.json)
- Resumen GA: [resumen_ga_final.json](C:\Carlos\Uni\Algortimos\trabajos\trabajo_1\trabajo_carlos\2. optimizacion_combinatoria\fase_8_ga_final\resumen_ga_final.json)
- Visualizacion ACO: [visualizacion_aco_final.svg](C:\Carlos\Uni\Algortimos\trabajos\trabajo_1\trabajo_carlos\2. optimizacion_combinatoria\fase_7_aco_final\visualizacion_aco_final.svg)
- Convergencia ACO: [convergencia_aco_final.svg](C:\Carlos\Uni\Algortimos\trabajos\trabajo_1\trabajo_carlos\2. optimizacion_combinatoria\fase_7_aco_final\convergencia_aco_final.svg)

## Conclusion

Con las corridas finales disponibles hasta el `22 de julio de 2026`, el mejor
resultado computacional de la parte de optimizacion combinatoria lo entrega el
algoritmo genetico.

Si la comparacion final del trabajo se basa en el menor costo hallado sobre la
misma matriz de costos, entonces:

`GA > ACO` en esta ejecucion concreta.
