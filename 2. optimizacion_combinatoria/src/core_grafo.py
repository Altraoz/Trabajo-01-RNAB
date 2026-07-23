from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np


def load_city_names_from_matrix_csv(path: Path) -> list[str]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        return header[1:]


def load_city_index_to_name(path: Path) -> dict[int, str]:
    idx_to_name: dict[int, str] = {}
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            idx_to_name[int(row["indice_inicio"])] = row["ciudad_inicio"]
            idx_to_name[int(row["indice_destino"])] = row["ciudad_destino"]
    return idx_to_name


def parse_tour_indices(raw_tour: str, valid_indices: set[int]) -> list[int]:
    try:
        tour = [int(value.strip()) for value in raw_tour.split(",") if value.strip()]
    except ValueError as exc:
        raise ValueError(
            "El tour debe contener solo indices enteros separados por comas."
        ) from exc

    if len(tour) < 2:
        raise ValueError("El tour debe tener al menos dos ciudades.")

    invalid = [index for index in tour if index not in valid_indices]
    if invalid:
        raise ValueError(f"Indices de ciudad invalidos en el tour: {invalid}")

    return tour


def reconstruct_path(next_hop: np.ndarray, source: int, target: int) -> list[int]:
    if source == target:
        return [source]
    if int(next_hop[source, target]) == -1:
        raise ValueError(f"No existe ruta reconstruible entre {source} y {target}.")

    path = [source]
    current = source
    safety = next_hop.shape[0] + 1

    while current != target and safety > 0:
        current = int(next_hop[current, target])
        if current == -1:
            raise ValueError(f"La ruta entre {source} y {target} se interrumpio.")
        path.append(current)
        safety -= 1

    if current != target:
        raise ValueError(f"No fue posible completar la ruta entre {source} y {target}.")
    return path


def expand_tour(
    tsp_tour: list[int],
    next_hop: np.ndarray,
    cost_matrix: np.ndarray,
) -> tuple[list[dict], list[int], float]:
    expanded_segments: list[dict] = []
    expanded_route: list[int] = [tsp_tour[0]]
    total_cost = 0.0

    for source, target in zip(tsp_tour[:-1], tsp_tour[1:]):
        segment_path = reconstruct_path(next_hop, source, target)
        segment_cost = float(cost_matrix[source, target])
        total_cost += segment_cost
        expanded_segments.append(
            {
                "origen_indice": source,
                "destino_indice": target,
                "ruta_indices": segment_path,
                "costo_tramo": round(segment_cost, 6),
            }
        )
        if len(segment_path) > 1:
            expanded_route.extend(segment_path[1:])

    return expanded_segments, expanded_route, total_cost


def save_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)
