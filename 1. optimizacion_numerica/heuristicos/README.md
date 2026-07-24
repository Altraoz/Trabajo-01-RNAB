# Heuristicos

Este bloque sigue la misma idea de organizacion usada en `gradiente/`:

- `funciones_heuristicas.py`: nucleo unico con la implementacion de EA, PSO y DE.
- `__init__.py`: punto de entrada del paquete para importar los algoritmos desde notebooks y scripts.
- `generador_de_datos.ipynb`: notebook destinado a ejecutar corridas y guardar resultados.
- `analisis_resultados.ipynb`: notebook destinado a leer resultados ya generados y producir tablas/figuras.
- `11_animacion_pso.ipynb`: animacion heuristica para el caso representativo del enunciado.
- `08_algoritmo_evolutivo.ipynb`, `09_pso.ipynb`, `10_evolucion_diferencial.ipynb`: notebooks de apoyo y validacion rapida de cada metodo.
- `datos/`: carpeta reservada para salidas reproducibles de corridas, metricas y figuras.

## Criterio de uso

La logica experimental no debe duplicarse dentro de los notebooks. Toda ejecucion debe apoyarse en las funciones de `funciones_heuristicas.py`, importadas preferiblemente desde el paquete:

```python
from heuristicos import (
    run_differential_evolution,
    run_evolutionary_algorithm,
    run_particle_swarm_optimization,
)
```

Con esto, `funciones_heuristicas.py` queda como fuente unica de verdad para la parte heuristica, y los notebooks pasan a ser capas de ejecucion, analisis o visualizacion.
