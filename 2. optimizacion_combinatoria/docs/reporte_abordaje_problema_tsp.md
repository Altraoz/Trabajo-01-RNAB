# Reporte de abordaje del problema TSP sobre grafo conexo

## 1. Planteamiento del problema

En la parte de optimizacion combinatoria del trabajo se buscaba resolver un
problema tipo TSP sobre las 96 capitales departamentales de la Francia
continental.

El enunciado exigia:

- usar `colonias de hormigas`
- usar `algoritmos geneticos`
- definir un modelo de costo basado en:
  - valor de la hora del vendedor
  - peajes
  - combustible
- representar visualmente la mejor solucion obtenida

El objetivo final no era solamente encontrar un orden de visita, sino hacerlo
con una funcion de costo interpretable y consistente con la logica del
problema.

## 2. Problema identificado

El primer enfoque consistio en construir una matriz de costos usando unicamente
las conexiones directas disponibles en el dataset original.

Eso producia una matriz parcial:

- si existia conexion directa entre dos ciudades, se asignaba un costo
- si no existia conexion directa, quedaba un infinito

El inconveniente de este enfoque es que tanto ACO como GA trabajan mejor sobre
una instancia completa del TSP, donde siempre exista un costo definido para ir
de cualquier ciudad a cualquier otra.

En el caso particular del ACO, la matriz parcial provocaba errores de
transicion como `probabilities contain NaN`, porque algunas hormigas quedaban
sin movimientos validos hacia nodos no visitados.

## 3. Diagnostico conceptual

El problema no estaba en la idea de trabajar con conexiones reales, sino en la
forma de representar esa informacion para el TSP.

La red construida no era un TSP clasico, sino un grafo parcial de conexiones
directas. Sin embargo, ese grafo era conexo, lo cual significa que desde
cualquier ciudad se puede llegar a cualquier otra pasando, si es necesario, por
ciudades intermedias.

Por tanto, la solucion correcta fue transformar ese grafo en una matriz
completa de costos minimos entre todos los pares de ciudades.

## 4. Idea de solucion

La solucion adoptada fue dividir el problema en dos niveles:

1. **Nivel de red real**
   Se conserva el grafo original de conexiones directas entre ciudades.

2. **Nivel TSP**
   Se calcula el costo minimo entre cada par de ciudades y con esos valores se
   construye una matriz completa `96x96`, apta para ACO y GA.

De esta manera:

- se respeta la estructura real de conexiones recolectada en el trabajo
- se adapta el problema al formato requerido por el TSP
- se elimina el problema de infinitos fuera de la diagonal

## 5. Modelo final de costo

Una vez resuelta la parte estructural del grafo, se alineo la funcion de costo
con el enunciado.

Se adopto el siguiente modelo:

`costo_total = peajes(euros) + gasolina(euros) + (tiempo(min)/60) * 12.02`

Donde:

- `gasolina(euros)` proviene directamente del dataset
- `12.02 EUR/h` corresponde al `SMIC Francia 2026`
- el tiempo se convierte a horas para calcular el costo del vendedor

Supuestos adoptados:

- vehiculo de referencia: `Renault Clio`
- tipo de combustible: `gasolina`
- tarifa del vendedor: `12.02 EUR/h`

Este modelo cumple con la estructura pedida en el enunciado y deja explicita
la forma en que se computa cada tramo.

## 6. Metodologia implementada

El abordaje final puede resumirse en dos pasos de preparacion y luego las etapas de optimizacion y visualizacion.

### Fase 1. Valorar conexiones directas

Se leyo `dataset_cities_france.csv` y se asigno un peso numerico a cada arista
directa del grafo usando el modelo final de costo.

Resultado:

- grafo ponderado de 96 ciudades
- 242 conexiones directas valoradas

Archivo principal:

- [preprocesamiento.py](C:\Carlos\Uni\Algortimos\trabajos\trabajo_1\trabajo_carlos\2. optimizacion_combinatoria\scripts\preprocesamiento.py)

### Etapa 2. Construir optimizador local A -> B

Se implemento un algoritmo de caminos minimos para resolver la mejor ruta entre
dos ciudades cualesquiera del grafo.

Archivo principal:

- [util_ruta_minima.py](C:\Carlos\Uni\Algortimos\trabajos\trabajo_1\trabajo_carlos\2. optimizacion_combinatoria\scripts\util_ruta_minima.py)

### Etapa 3. Generalizar a todos los pares

Se ejecuto el optimizador desde cada ciudad hacia todas las demas para
construir directamente la matriz completa `96x96` usada por el TSP.

Como artefactos principales se conservaron:

- `matriz_costo_total_96x96.npy`
- `matriz_siguiente_salto_96x96.npy`

Archivo principal:

- [matrices_completas.py](C:\Carlos\Uni\Algortimos\trabajos\trabajo_1\trabajo_carlos\2. optimizacion_combinatoria\scripts\matrices_completas.py)

### Etapa 4. Reconstruccion de rutas reales

Se guardo una estructura de `siguiente salto` para poder reconstruir la ruta
real minima entre cualquier par de ciudades.

Archivo principal:

- [util_reconstruir_ruta.py](C:\Carlos\Uni\Algortimos\trabajos\trabajo_1\trabajo_carlos\2. optimizacion_combinatoria\scripts\util_reconstruir_ruta.py)

La misma construccion de la matriz completa la deja lista para TSP, porque se
garantiza una instancia cuadrada, con diagonal en cero y costos finitos fuera
de la diagonal.

### Etapa 6. Expandir un tour a recorrido real

Se implemento un procedimiento para tomar un tour TSP y expandir cada salto a
su trayecto minimo dentro del grafo real.

Archivo principal:

- [post_expandir_tour.py](C:\Carlos\Uni\Algortimos\trabajos\trabajo_1\trabajo_carlos\2. optimizacion_combinatoria\scripts\post_expandir_tour.py)

### Etapa 7. Ejecutar ACO final

Se implemento una corrida final reproducible de colonia de hormigas sobre la
matriz completa.

Archivo principal:

- [ejecutar_aco.py](C:\Carlos\Uni\Algortimos\trabajos\trabajo_1\trabajo_carlos\2. optimizacion_combinatoria\scripts\ejecutar_aco.py)

Resultado principal:

- mejor costo ACO: `4471.569332`

### Etapa 8. Ejecutar GA final

Se implemento una corrida final reproducible de algoritmo genetico sobre la
misma matriz de costos.

Archivo principal:

- [ejecutar_ga.py](C:\Carlos\Uni\Algortimos\trabajos\trabajo_1\trabajo_carlos\2. optimizacion_combinatoria\scripts\ejecutar_ga.py)

Resultado principal:

- mejor costo GA: `4303.602999`

### Etapa 9. Generar la visualizacion final

Se construyo un GIF de la mejor solucion combinatoria final usando el metodo
ganador de las corridas.

Archivo principal:

- [post_generar_gif.py](C:\Carlos\Uni\Algortimos\trabajos\trabajo_1\trabajo_carlos\2. optimizacion_combinatoria\scripts\post_generar_gif.py)

Salida principal:

- [mejor_solucion_combinatoria.gif](C:\Carlos\Uni\Algortimos\trabajos\trabajo_1\trabajo_carlos\2. optimizacion_combinatoria\entrega_final\mejor_solucion_combinatoria.gif)

## 7. Resultados finales

Los resultados finales del experimento fueron:

| Metodo | Mejor costo del tour | Ciudades visitadas | Longitud del tour cerrado |
|---|---:|---:|---:|
| ACO | `4471.569332` | `96` | `97` |
| GA | `4303.602999` | `96` | `97` |

Diferencia entre ambos:

- mejora absoluta de `GA` frente a `ACO`: `167.966333`
- mejora relativa de `GA` frente a `ACO`: `3.76%`

Con base en estas corridas finales, el mejor resultado computacional fue el del
algoritmo genetico.

## 8. Discusion

La comparacion entre ACO y GA permite extraer varias conclusiones utiles.

Primero, ambos algoritmos fueron capaces de producir un tour valido sobre las
96 ciudades, lo cual confirma que la reformulacion del problema como matriz
completa `96x96` fue correcta. En otras palabras, la parte esencial del trabajo
no fue solo correr una metaheuristica, sino convertir una red parcial de
conexiones reales en una instancia de TSP bien definida.

Segundo, ACO fue especialmente util para encontrar con rapidez una solucion
factible y relativamente buena. En sus primeras iteraciones redujo de manera
notable el costo del tour y estabilizo una solucion competitiva. Esto sugiere
que la colonia de hormigas se comporto bien como metodo exploratorio sobre la
matriz de costos.

Tercero, el algoritmo genetico logro refinar aun mas la solucion. Al trabajar
con una poblacion de recorridos y operadores de cruce y mutacion, fue capaz de
reordenar la visita de las ciudades hasta producir un tour de menor costo. La
mejora de `3.76%` frente a ACO no es marginal en este contexto, porque se da
sobre una ruta ya optimizada por una metaheuristica fuerte.

Cuarto, estos resultados muestran que en este problema concreto:

- `ACO` fue bueno para explorar
- `GA` fue mejor para refinar

Por eso, una interpretacion razonable es que ambos metodos no deben verse como
competidores puros, sino como estrategias complementarias. De hecho, usar una
buena solucion inicial proveniente de ACO puede ayudar al GA a acelerar el
proceso de mejora.

Finalmente, la visualizacion del recorrido final tambien aporta una lectura
cualitativa del resultado. El GIF no solo muestra que existe un tour completo,
sino que hace visible la progresion espacial del recorrido ganador y facilita
comunicar el resultado de una forma comprensible para el lector del blog o del
reporte tecnico.

## 9. Cierre del flujo final

La parte de optimizacion combinatoria quedo cerrada con una salida final lista
para entrega en:

- [entrega_final](C:\Carlos\Uni\Algortimos\trabajos\trabajo_1\trabajo_carlos\2. optimizacion_combinatoria\entrega_final)

Dentro de esa carpeta se centralizaron:

- el resultado final ganador
- el recorrido real expandido
- el GIF final
- la comparacion ACO vs GA
- la visualizacion estatica de la mejor solucion

Esto permite que la entrega no dependa solamente del pipeline de fases, sino de
artefactos finales organizados y directamente reutilizables en el reporte o en
la entrada de blog.

## 10. Conclusion

El problema inicial no se reducia a ejecutar ACO o GA sobre una matriz
cualquiera, sino a modelar correctamente una red real de conexiones directas
como un TSP compatible con metaheuristicas.

La solucion consistio en:

1. valorar el grafo con una funcion de costo alineada al enunciado
2. construir una matriz completa de costos minimos
3. ejecutar tanto ACO como GA sobre esa matriz
4. comparar ambos resultados
5. conservar como solucion final el mejor tour encontrado

Con las corridas finales realizadas el `22 de julio de 2026`, el mejor
resultado de la parte de optimizacion combinatoria fue el del algoritmo
genetico, con un costo total de `4303.602999`.

Por tanto, la salida final recomendada para la entrega es:

- metodo ganador: `GA`
- costo final: `4303.602999`
- soporte visual: `mejor_solucion_combinatoria.gif`
- comparativo: `ACO vs GA`
