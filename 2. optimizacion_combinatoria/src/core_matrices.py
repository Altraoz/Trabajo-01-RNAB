from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

from src.config_modelo_costo import cost_formula_label, model_metadata
from src.core_paths import PHASE3_DIR, WEIGHTED_EDGES_CSV_PATH


def load_graph(path: Path = WEIGHTED_EDGES_CSV_PATH) -> tuple[dict[int, str], dict[int, list[dict]]]:
    idx_to_name: dict[int, str] = {}
    graph: dict[int, list[dict]] = {}

    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            start_idx = int(row["indice_inicio"])
            end_idx = int(row["indice_destino"])
            start_city = row["ciudad_inicio"]
            end_city = row["ciudad_destino"]

            edge = {
                "weight": float(row["peso"]),
                "distance": float(row["distancia"]),
                "time_min": float(row["tiempo(min)"]),
                "toll_eur": float(row["peajes(euros)"]),
                "fuel_eur": float(row["gasolina(euros)"]),
            }

            idx_to_name[start_idx] = start_city
            idx_to_name[end_idx] = end_city
            graph.setdefault(start_idx, []).append({"target": end_idx, **edge})
            graph.setdefault(end_idx, []).append({"target": start_idx, **edge})

    return idx_to_name, graph


def run_dijkstra(
    graph: dict[int, list[dict]], source: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    n = len(graph)
    costs = np.full(n, np.inf, dtype=np.float64)
    distances = np.full(n, np.inf, dtype=np.float64)
    times = np.full(n, np.inf, dtype=np.float64)
    tolls = np.full(n, np.inf, dtype=np.float64)
    fuels = np.full(n, np.inf, dtype=np.float64)
    previous = np.full(n, -1, dtype=np.int64)

    costs[source] = 0.0
    distances[source] = 0.0
    times[source] = 0.0
    tolls[source] = 0.0
    fuels[source] = 0.0

    heap: list[tuple[float, int]] = [(0.0, source)]
    import heapq

    while heap:
        current_cost, node = heapq.heappop(heap)
        if current_cost > costs[node]:
            continue

        for edge in graph[node]:
            neighbor = edge["target"]
            new_cost = current_cost + edge["weight"]
            if new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                distances[neighbor] = distances[node] + edge["distance"]
                times[neighbor] = times[node] + edge["time_min"]
                tolls[neighbor] = tolls[node] + edge["toll_eur"]
                fuels[neighbor] = fuels[node] + edge["fuel_eur"]
                previous[neighbor] = node
                heapq.heappush(heap, (new_cost, neighbor))

    return costs, distances, times, tolls, fuels, previous


def build_next_hop(previous: np.ndarray, source: int) -> np.ndarray:
    n = len(previous)
    next_hop = np.full(n, -1, dtype=np.int64)
    next_hop[source] = source

    for target in range(n):
        if target == source or previous[target] == -1:
            continue

        node = target
        while previous[node] != source:
            node = previous[node]
            if node == -1:
                break

        if node != -1:
            next_hop[target] = node

    return next_hop


def save_matrix_csv(
    path: Path,
    matrix: np.ndarray,
    city_names: dict[int, str] | list[str],
    integer: bool = False,
) -> None:
    ordered_names = (
        [city_names[i] for i in range(len(city_names))]
        if isinstance(city_names, dict)
        else city_names
    )
    path.parent.mkdir(exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Ciudad"] + ordered_names)
        for i, city in enumerate(ordered_names):
            row = matrix[i]
            values = row.astype(int).tolist() if integer else row.tolist()
            writer.writerow([city] + values)


def build_complete_matrices(
    input_csv: Path = WEIGHTED_EDGES_CSV_PATH,
    output_dir: Path = PHASE3_DIR,
) -> dict:
    idx_to_name, graph = load_graph(input_csv)
    n = len(idx_to_name)

    cost_matrix = np.full((n, n), np.inf, dtype=np.float64)
    distance_matrix = np.full((n, n), np.inf, dtype=np.float64)
    time_matrix = np.full((n, n), np.inf, dtype=np.float64)
    toll_matrix = np.full((n, n), np.inf, dtype=np.float64)
    fuel_matrix = np.full((n, n), np.inf, dtype=np.float64)
    next_hop_matrix = np.full((n, n), -1, dtype=np.int64)

    for source in range(n):
        costs, distances, times, tolls, fuels, previous = run_dijkstra(graph, source)
        cost_matrix[source, :] = costs
        distance_matrix[source, :] = distances
        time_matrix[source, :] = times
        toll_matrix[source, :] = tolls
        fuel_matrix[source, :] = fuels
        next_hop_matrix[source, :] = build_next_hop(previous, source)

    tsp_cost_matrix = cost_matrix.copy()
    np.fill_diagonal(tsp_cost_matrix, 0.0)
    np.fill_diagonal(next_hop_matrix, -1)

    off_diagonal_mask = ~np.eye(n, dtype=bool)
    if np.isinf(cost_matrix[off_diagonal_mask]).any():
        raise ValueError("La matriz completa tiene infinitos fuera de la diagonal.")

    output_dir.mkdir(exist_ok=True)
    np.save(output_dir / "matriz_costo_total_96x96.npy", tsp_cost_matrix)
    np.save(output_dir / "matriz_siguiente_salto_96x96.npy", next_hop_matrix)
    summary = {
        "ciudades": len(idx_to_name),
        "shape": list(tsp_cost_matrix.shape),
        "costo_minimo_finito": float(tsp_cost_matrix[off_diagonal_mask].min()),
        "costo_maximo_finito": float(tsp_cost_matrix[off_diagonal_mask].max()),
        "costo_promedio_finito": float(tsp_cost_matrix[off_diagonal_mask].mean()),
        "diagonal_cero": bool(np.allclose(np.diag(tsp_cost_matrix), 0.0)),
        "formula_peso": cost_formula_label(),
    }
    summary.update(model_metadata())

    return {
        "city_names": idx_to_name,
        "cost_matrix": tsp_cost_matrix,
        "distance_matrix": distance_matrix,
        "time_matrix": time_matrix,
        "toll_matrix": toll_matrix,
        "fuel_matrix": fuel_matrix,
        "next_hop_matrix": next_hop_matrix,
        "summary": summary,
    }
