from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
GRADIENT_DIR = ROOT_DIR / "gradiente"

if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))
if str(GRADIENT_DIR) not in sys.path:
    sys.path.append(str(GRADIENT_DIR))

from funciones_heuristicas import (  # type: ignore  # noqa: E402
    run_differential_evolution,
    run_evolutionary_algorithm,
    run_particle_swarm_optimization,
)
from funciones_objetivo import (  # type: ignore  # noqa: E402
    goldstein_price,
    griewank,
    rastrigin,
    rosenbrock,
    schwefel,
    six_hump_camel,
)


FUNCTIONS = [
    {
        "name": "Rosenbrock",
        "function": rosenbrock,
        "bounds": (-2.048, 2.048),
        "dimensions": [2, 3],
    },
    {
        "name": "Rastrigin",
        "function": rastrigin,
        "bounds": (-5.12, 5.12),
        "dimensions": [2, 3],
    },
    {
        "name": "Schwefel",
        "function": schwefel,
        "bounds": (-500.0, 500.0),
        "dimensions": [2, 3],
    },
    {
        "name": "Griewank",
        "function": griewank,
        "bounds": (-600.0, 600.0),
        "dimensions": [2, 3],
    },
    {
        "name": "Goldstein-Price",
        "function": goldstein_price,
        "bounds": (-2.0, 2.0),
        "dimensions": [2],
    },
    {
        "name": "Six-Hump Camel",
        "function": six_hump_camel,
        "bounds": (-3.0, 3.0),
        "dimensions": [2],
    },
]


def run_method(method_name: str, objective_function, bounds: tuple[float, float], dimension: int, seed: int) -> dict:
    lower, upper = bounds

    if method_name == "algoritmo_evolutivo":
        return run_evolutionary_algorithm(
            objective_function=objective_function,
            population_size=40,
            dimension=dimension,
            lower_bounds=lower,
            upper_bounds=upper,
            elitism_fraction=0.2,
            mutation_fraction=0.1,
            max_iterations=100,
            seed=seed,
        )

    if method_name == "pso":
        return run_particle_swarm_optimization(
            objective_function=objective_function,
            swarm_size=40,
            dimension=dimension,
            lower_bounds=lower,
            upper_bounds=upper,
            inertia_weight=0.7,
            cognitive_weight=1.5,
            social_weight=1.5,
            max_iterations=100,
            seed=seed,
        )

    if method_name == "evolucion_diferencial":
        return run_differential_evolution(
            objective_function=objective_function,
            population_size=40,
            dimension=dimension,
            lower_bounds=lower,
            upper_bounds=upper,
            mutation_factor=0.8,
            crossover_rate=0.7,
            max_iterations=100,
            seed=seed,
        )

    raise ValueError(f"Metodo no soportado: {method_name}")


def main() -> None:
    methods = ["algoritmo_evolutivo", "pso", "evolucion_diferencial"]
    seeds = [42, 123, 999]
    rows: list[dict] = []

    for function_config in FUNCTIONS:
        for dimension in function_config["dimensions"]:
            for method in methods:
                print(f"Procesando {function_config['name']} | {dimension}D | {method}")
                for run_number, seed in enumerate(seeds, start=1):
                    result = run_method(
                        method_name=method,
                        objective_function=function_config["function"],
                        bounds=function_config["bounds"],
                        dimension=dimension,
                        seed=seed,
                    )

                    rows.append(
                        {
                            "funcion": function_config["name"],
                            "dimension": dimension,
                            "metodo": method,
                            "corrida": run_number,
                            "seed": seed,
                            "mejor_valor": result["best_value"],
                            "mejor_solucion": result["best_solution"].tolist(),
                            "evaluaciones": result["evaluations"],
                            "iteraciones": result["iterations"],
                        }
                    )

    results = pd.DataFrame(rows)

    output_dir = CURRENT_DIR / "datos"
    output_dir.mkdir(exist_ok=True)

    results_path = output_dir / "resultados_punto_2_heuristicos.csv"
    summary_path = output_dir / "resumen_punto_2_heuristicos.csv"

    results.to_csv(results_path, index=False)

    summary = (
        results.groupby(["funcion", "dimension", "metodo"], as_index=False)
        .agg(
            mejor_valor_promedio=("mejor_valor", "mean"),
            mejor_valor_minimo=("mejor_valor", "min"),
            evaluaciones_promedio=("evaluaciones", "mean"),
        )
        .sort_values(["funcion", "dimension", "mejor_valor_minimo"])
    )
    summary.to_csv(summary_path, index=False)

    print()
    print("Archivos generados:")
    print(results_path)
    print(summary_path)
    print()
    print(summary.to_string(index=False))
    print()
    print("Goldstein-Price y Six-Hump Camel se ejecutan solo en 2D porque estas funciones estan definidas para dos variables.")


if __name__ == "__main__":
    main()
