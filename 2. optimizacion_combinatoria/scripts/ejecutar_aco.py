"""
Paso 7: ejecutar ACO final sobre la matriz completa preparada.

Esta version evita depender del notebook o de una libreria externa clonada.
Corre ACO directamente sobre la matriz 96x96 generada en el paso 5 y guarda:

- mejor tour TSP encontrado
- costo del tour
- historial de convergencia
- metadatos de configuracion
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
from src.core_paths import INPUT_COST_MATRIX_PATH, PHASE7_DIR, WEIGHTED_EDGES_CSV_PATH
from src.core_tsp_aco import ACOConfig, run_aco


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ejecuta ACO final sobre la matriz preparada.")
    parser.add_argument("--ants", type=int, default=40)
    parser.add_argument("--iterations", type=int, default=250)
    parser.add_argument("--alpha", type=float, default=1.0)
    parser.add_argument("--beta", type=float, default=3.0)
    parser.add_argument("--evaporation-rate", type=float, default=0.35)
    parser.add_argument("--intensification", type=float, default=2.0)
    parser.add_argument("--elite-weight", type=float, default=2.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--start-node", type=int, default=0)
    return parser.parse_args()


def build_config(args: argparse.Namespace) -> ACOConfig:
    return ACOConfig(
        ants=args.ants,
        iterations=args.iterations,
        alpha=args.alpha,
        beta=args.beta,
        evaporation_rate=args.evaporation_rate,
        intensification=args.intensification,
        elite_weight=args.elite_weight,
        seed=args.seed,
        start_node=args.start_node,
    )

def main() -> None:
    args = parse_args()
    config = build_config(args)
    cost_matrix = np.load(INPUT_COST_MATRIX_PATH)
    city_name_map = load_city_index_to_name(WEIGHTED_EDGES_CSV_PATH)
    city_names = [city_name_map[index] for index in range(cost_matrix.shape[0])]

    if config.start_node < 0 or config.start_node >= cost_matrix.shape[0]:
        raise ValueError("El nodo inicial esta fuera de rango.")

    best_tour, best_cost, history = run_aco(cost_matrix, config)
    unique_tour = best_tour[:-1]

    result = {
        "configuracion_aco": asdict(config),
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
        "iteraciones": config.iterations,
        "hormigas": config.ants,
        "seed": config.seed,
        "n_ciudades": len(unique_tour),
        "tour_cerrado": len(best_tour),
    }
    summary.update(model_metadata())

    save_json(PHASE7_DIR / "resultado_aco_final.json", result)
    save_json(PHASE7_DIR / "resumen_aco_final.json", summary)

    print("Paso 7 completado.")
    print(f"Mejor costo del tour: {best_cost:.4f}")
    print(f"Ciudades visitadas: {len(unique_tour)}")
    print(f"Salida: {PHASE7_DIR}")


if __name__ == "__main__":
    main()
