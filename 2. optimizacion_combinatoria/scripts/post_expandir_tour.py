"""
Paso 6: reconstruir el recorrido final real a partir de un tour TSP.

Entrada esperada:
- una secuencia de indices de ciudades del tour TSP

Salida:
- tour original
- recorrido real expandido sobre el grafo
- saltos expandidos por tramo
- costo total del tour
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import numpy as np

from src.core_grafo import expand_tour, load_city_index_to_name, parse_tour_indices, save_json
from src.core_paths import NEXT_HOP_MATRIX_PATH, PHASE6_DIR, TOTAL_COST_MATRIX_PATH, WEIGHTED_EDGES_CSV_PATH


NEXT_HOP_PATH = NEXT_HOP_MATRIX_PATH
COST_PATH = TOTAL_COST_MATRIX_PATH
CITIES_CSV_PATH = WEIGHTED_EDGES_CSV_PATH
OUTPUT_DIR = PHASE6_DIR


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Expande un tour TSP a rutas reales del grafo."
    )
    parser.add_argument(
        "--tour",
        required=True,
        help="Lista de indices separada por comas. Ejemplo: 0,71,89,77,75,95",
    )
    parser.add_argument(
        "--cerrar-ciclo",
        action="store_true",
        help="Agrega el regreso al nodo inicial si no esta incluido.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    idx_to_name = load_city_index_to_name(CITIES_CSV_PATH)
    next_hop = np.load(NEXT_HOP_PATH)
    cost_matrix = np.load(COST_PATH)

    tsp_tour = parse_tour_indices(args.tour, set(idx_to_name.keys()))
    if args.cerrar_ciclo and tsp_tour[0] != tsp_tour[-1]:
        tsp_tour = tsp_tour + [tsp_tour[0]]

    expanded_segments, expanded_route, total_cost = expand_tour(
        tsp_tour, next_hop, cost_matrix
    )

    result = {
        "tour_tsp_indices": tsp_tour,
        "tour_tsp_nombres": [idx_to_name[index] for index in tsp_tour],
        "tramos_expandidos": [
            {
                **segment,
                "ruta_nombres": [idx_to_name[index] for index in segment["ruta_indices"]],
            }
            for segment in expanded_segments
        ],
        "recorrido_real_indices": expanded_route,
        "recorrido_real_nombres": [idx_to_name[index] for index in expanded_route],
        "costo_total_tour": round(total_cost, 6),
        "n_saltos_tsp": len(tsp_tour) - 1,
        "n_saltos_reales": len(expanded_route) - 1,
    }

    output_name = "tour_expandido.json"
    save_json(OUTPUT_DIR / output_name, result)

    print("Paso 6 completado.")
    print(f"Saltos del tour TSP: {len(tsp_tour) - 1}")
    print(f"Saltos reales expandidos: {len(expanded_route) - 1}")
    print(f"Costo total del tour: {total_cost:.4f}")
    print(f"Salida: {OUTPUT_DIR / output_name}")


if __name__ == "__main__":
    main()
