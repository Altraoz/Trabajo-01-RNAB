from pathlib import Path
import sys


def find_project_dir(start: Path | None = None) -> Path:
    current = (start or Path(__file__).resolve()).resolve()
    for candidate in [current, *current.parents]:
        if candidate.name == "1. optimizacion_numerica" and (candidate / "functions").exists():
            return candidate
    raise FileNotFoundError("No se pudo ubicar la carpeta 1. optimizacion_numerica.")


FUNCTIONS_DIR = find_project_dir() / "functions"
if str(FUNCTIONS_DIR) not in sys.path:
    sys.path.insert(0, str(FUNCTIONS_DIR))

from funciones_heuristicas import (
    evolutionary_crossover,
    evolutionary_initial_population,
    evolutionary_mutation,
    evolutionary_next_generation,
    evolutionary_population_eval,
    run_differential_evolution,
    run_evolutionary_algorithm,
    run_particle_swarm_optimization,
)

__all__ = [
    "evolutionary_crossover",
    "evolutionary_initial_population",
    "evolutionary_mutation",
    "evolutionary_next_generation",
    "evolutionary_population_eval",
    "run_differential_evolution",
    "run_evolutionary_algorithm",
    "run_particle_swarm_optimization",
]
