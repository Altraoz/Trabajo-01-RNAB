"""
Paso 2: optimizador local entre un nodo A y un nodo B.

Resuelve el problema de encontrar la mejor ruta entre dos ciudades usando el
grafo ponderado construido en el paso 1.

Entrada:
- ciudad origen (indice o nombre)
- ciudad destino (indice o nombre)

Salida:
- costo minimo
- ruta de indices
- ruta de nombres
"""

from __future__ import annotations

import argparse
import csv
import heapq
import json
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config_modelo_costo import cost_formula_label
from src.core_paths import OUTPUTS_DIR, WEIGHTED_EDGES_CSV_PATH


INPUT_CSV = WEIGHTED_EDGES_CSV_PATH
OUTPUT_DIR = OUTPUTS_DIR / "rutas_locales"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Encuentra la mejor ruta entre dos ciudades del grafo."
    )
    parser.add_argument("--origen", required=True, help="Indice o nombre de la ciudad origen.")
    parser.add_argument("--destino", required=True, help="Indice o nombre de la ciudad destino.")
    return parser.parse_args()


def load_graph(path: Path) -> tuple[dict[int, str], dict[str, int], dict[int, list[dict]]]:
    idx_to_name: dict[int, str] = {}
    name_to_idx: dict[str, int] = {}
    graph: dict[int, list[dict]] = {}

    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            start_idx = int(row["indice_inicio"])
            end_idx = int(row["indice_destino"])
            start_city = row["ciudad_inicio"]
            end_city = row["ciudad_destino"]
            weight = float(row["peso"])
            distance = float(row["distancia"])
            time_min = float(row["tiempo(min)"])
            toll_eur = float(row["peajes(euros)"])
            fuel_eur = float(row["gasolina(euros)"])
            seller_cost_eur = float(row["costo_vendedor(euros)"])

            idx_to_name[start_idx] = start_city
            idx_to_name[end_idx] = end_city
            name_to_idx[start_city.casefold()] = start_idx
            name_to_idx[end_city.casefold()] = end_idx

            graph.setdefault(start_idx, []).append(
                {
                    "target": end_idx,
                    "weight": weight,
                    "distance": distance,
                    "time_min": time_min,
                    "toll_eur": toll_eur,
                    "fuel_eur": fuel_eur,
                    "seller_cost_eur": seller_cost_eur,
                }
            )
            graph.setdefault(end_idx, []).append(
                {
                    "target": start_idx,
                    "weight": weight,
                    "distance": distance,
                    "time_min": time_min,
                    "toll_eur": toll_eur,
                    "fuel_eur": fuel_eur,
                    "seller_cost_eur": seller_cost_eur,
                }
            )

    return idx_to_name, name_to_idx, graph


def resolve_city(value: str, idx_to_name: dict[int, str], name_to_idx: dict[str, int]) -> int:
    if value.isdigit():
        index = int(value)
        if index not in idx_to_name:
            raise ValueError(f"No existe una ciudad con indice {index}.")
        return index

    key = value.casefold()
    if key not in name_to_idx:
        raise ValueError(f"No existe una ciudad con nombre '{value}'.")
    return name_to_idx[key]


def shortest_path(
    graph: dict[int, list[dict]], source: int, target: int
) -> tuple[float, list[int], dict[str, float]]:
    distances: dict[int, float] = {node: float("inf") for node in graph}
    previous: dict[int, int | None] = {node: None for node in graph}
    distance_km: dict[int, float] = {node: float("inf") for node in graph}
    time_min: dict[int, float] = {node: float("inf") for node in graph}
    toll_eur: dict[int, float] = {node: float("inf") for node in graph}
    fuel_eur: dict[int, float] = {node: float("inf") for node in graph}
    seller_cost_eur: dict[int, float] = {node: float("inf") for node in graph}

    distances[source] = 0.0
    distance_km[source] = 0.0
    time_min[source] = 0.0
    toll_eur[source] = 0.0
    fuel_eur[source] = 0.0
    seller_cost_eur[source] = 0.0

    heap: list[tuple[float, int]] = [(0.0, source)]

    while heap:
        current_cost, node = heapq.heappop(heap)
        if current_cost > distances[node]:
            continue
        if node == target:
            break

        for edge in graph[node]:
            neighbor = edge["target"]
            new_cost = current_cost + edge["weight"]
            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                previous[neighbor] = node
                distance_km[neighbor] = distance_km[node] + edge["distance"]
                time_min[neighbor] = time_min[node] + edge["time_min"]
                toll_eur[neighbor] = toll_eur[node] + edge["toll_eur"]
                fuel_eur[neighbor] = fuel_eur[node] + edge["fuel_eur"]
                seller_cost_eur[neighbor] = seller_cost_eur[node] + edge["seller_cost_eur"]
                heapq.heappush(heap, (new_cost, neighbor))

    if distances[target] == float("inf"):
        raise ValueError("No existe ruta entre el origen y el destino.")

    path: list[int] = []
    current: int | None = target
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()

    metrics = {
        "costo_minimo": distances[target],
        "distancia_total": distance_km[target],
        "tiempo_total_min": time_min[target],
        "peajes_totales_eur": toll_eur[target],
        "gasolina_total_eur": fuel_eur[target],
        "costo_vendedor_total_eur": seller_cost_eur[target],
    }
    return distances[target], path, metrics


def save_result(path: Path, payload: dict) -> None:
    path.parent.mkdir(exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def main() -> None:
    args = parse_args()
    idx_to_name, name_to_idx, graph = load_graph(INPUT_CSV)

    source = resolve_city(args.origen, idx_to_name, name_to_idx)
    target = resolve_city(args.destino, idx_to_name, name_to_idx)

    best_cost, path_indices, metrics = shortest_path(graph, source, target)
    path_names = [idx_to_name[index] for index in path_indices]

    result = {
        "origen_indice": source,
        "origen_nombre": idx_to_name[source],
        "destino_indice": target,
        "destino_nombre": idx_to_name[target],
        "costo_minimo": round(best_cost, 6),
        "ruta_indices": path_indices,
        "ruta_nombres": path_names,
        "metricas_acumuladas": {
            key: round(value, 6) for key, value in metrics.items()
        },
        "formula_peso": cost_formula_label(),
    }

    output_name = f"ruta_{source}_a_{target}.json"
    save_result(OUTPUT_DIR / output_name, result)

    print("Paso 2 completado.")
    print(f"Origen: {idx_to_name[source]} ({source})")
    print(f"Destino: {idx_to_name[target]} ({target})")
    print(f"Costo minimo: {best_cost:.4f}")
    print(f"Ruta de indices: {path_indices}")
    print(f"Ruta de nombres: {' -> '.join(path_names)}")
    print(f"Resultado guardado en: {OUTPUT_DIR / output_name}")


if __name__ == "__main__":
    main()
