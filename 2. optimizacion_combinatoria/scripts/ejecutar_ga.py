"""
Paso 8: ejecutar algoritmo genetico final sobre la matriz completa preparada.

Esta implementacion resuelve el TSP sobre la misma matriz usada en ACO y guarda:

- mejor tour encontrado
- costo del tour
- historial de convergencia
- metadatos del modelo de costo
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import numpy as np

from src.config_modelo_costo import model_metadata
from src.core_grafo import load_city_index_to_name, save_json
from src.core_paths import INPUT_COST_MATRIX_PATH, PHASE7_DIR, PHASE8_DIR, WEIGHTED_EDGES_CSV_PATH
from src.core_tsp_ga import GAConfig, run_ga


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ejecuta GA final sobre la matriz preparada.")
    parser.add_argument("--population-size", type=int, default=180)
    parser.add_argument("--generations", type=int, default=350)
    parser.add_argument("--mutation-rate", type=float, default=0.12)
    parser.add_argument("--crossover-rate", type=float, default=0.9)
    parser.add_argument("--elite-count", type=int, default=12)
    parser.add_argument("--tournament-size", type=int, default=5)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--start-node", type=int, default=0)
    parser.add_argument("--no-aco-seed", action="store_true")
    return parser.parse_args()


def build_config(args: argparse.Namespace) -> GAConfig:
    return GAConfig(
        population_size=args.population_size,
        generations=args.generations,
        mutation_rate=args.mutation_rate,
        crossover_rate=args.crossover_rate,
        elite_count=args.elite_count,
        tournament_size=args.tournament_size,
        seed=args.seed,
        start_node=args.start_node,
        inject_aco_seed=not args.no_aco_seed,
    )

def main() -> None:
    args = parse_args()
    config = build_config(args)
    cost_matrix = np.load(INPUT_COST_MATRIX_PATH)
    city_name_map = load_city_index_to_name(WEIGHTED_EDGES_CSV_PATH)
    city_names = [city_name_map[index] for index in range(cost_matrix.shape[0])]

    if config.start_node < 0 or config.start_node >= cost_matrix.shape[0]:
        raise ValueError("El nodo inicial esta fuera de rango.")

    best_tour, best_cost, history = run_ga(cost_matrix, config, PHASE7_DIR / "resultado_aco_final.json")
    unique_tour = best_tour[:-1]

    result = {
        "configuracion_ga": asdict(config),
        "shape_matriz": list(cost_matrix.shape),
        "mejor_costo_tour": round(best_cost, 6),
        "mejor_tour_indices": best_tour,
        "mejor_tour_indices_sin_cierre": unique_tour,
        "mejor_tour_nombres": [city_names[index] for index in best_tour],
        "mejor_tour_nombres_sin_cierre": [city_names[index] for index in unique_tour],
        "historial_mejor_costo": [round(value, 6) for value in history],
    }
    result.update(model_metadata())

    summary = {
        "mejor_costo_tour": round(best_cost, 6),
        "generaciones": config.generations,
        "tam_poblacion": config.population_size,
        "seed": config.seed,
        "n_ciudades": len(unique_tour),
        "tour_cerrado": len(best_tour),
    }
    summary.update(model_metadata())

    save_json(PHASE8_DIR / "resultado_ga_final.json", result)
    save_json(PHASE8_DIR / "resumen_ga_final.json", summary)

    print("Paso 8 completado.")
    print(f"Mejor costo del tour: {best_cost:.4f}")
    print(f"Ciudades visitadas: {len(unique_tour)}")
    print(f"Salida: {PHASE8_DIR}")


if __name__ == "__main__":
    main()
