"""
Paso 4: reconstruccion de rutas reales entre cualquier par de ciudades.

Usa la matriz de siguiente salto generada en el paso 3 para reconstruir la
ruta minima entre dos ciudades.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import numpy as np

from src.core_paths import NEXT_HOP_MATRIX_PATH, OUTPUTS_DIR, TOTAL_COST_MATRIX_PATH, WEIGHTED_EDGES_CSV_PATH


NEXT_HOP_PATH = NEXT_HOP_MATRIX_PATH
COST_PATH = TOTAL_COST_MATRIX_PATH
CITIES_CSV_PATH = WEIGHTED_EDGES_CSV_PATH
OUTPUT_DIR = OUTPUTS_DIR / "rutas_reconstruidas"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Reconstruye la ruta minima entre dos ciudades."
    )
    parser.add_argument("--origen", required=True, help="Indice o nombre de la ciudad origen.")
    parser.add_argument("--destino", required=True, help="Indice o nombre de la ciudad destino.")
    return parser.parse_args()


def load_city_maps(path: Path) -> tuple[dict[int, str], dict[str, int]]:
    idx_to_name: dict[int, str] = {}
    name_to_idx: dict[str, int] = {}

    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            start_idx = int(row["indice_inicio"])
            end_idx = int(row["indice_destino"])
            start_city = row["ciudad_inicio"]
            end_city = row["ciudad_destino"]

            idx_to_name[start_idx] = start_city
            idx_to_name[end_idx] = end_city
            name_to_idx[start_city.casefold()] = start_idx
            name_to_idx[end_city.casefold()] = end_idx

    return idx_to_name, name_to_idx


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


def reconstruct_path(next_hop: np.ndarray, source: int, target: int) -> list[int]:
    if source == target:
        return [source]
    if int(next_hop[source, target]) == -1:
        raise ValueError("No existe ruta reconstruible entre el origen y el destino.")

    path = [source]
    current = source
    safety = next_hop.shape[0] + 1

    while current != target and safety > 0:
        current = int(next_hop[current, target])
        if current == -1:
            raise ValueError("La ruta se interrumpio durante la reconstruccion.")
        path.append(current)
        safety -= 1

    if current != target:
        raise ValueError("No fue posible reconstruir la ruta completa.")

    return path


def save_result(path: Path, payload: dict) -> None:
    path.parent.mkdir(exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def main() -> None:
    args = parse_args()
    idx_to_name, name_to_idx = load_city_maps(CITIES_CSV_PATH)
    next_hop = np.load(NEXT_HOP_PATH)
    cost_matrix = np.load(COST_PATH)

    source = resolve_city(args.origen, idx_to_name, name_to_idx)
    target = resolve_city(args.destino, idx_to_name, name_to_idx)

    path_indices = reconstruct_path(next_hop, source, target)
    path_names = [idx_to_name[index] for index in path_indices]
    total_cost = float(cost_matrix[source, target])

    result = {
        "origen_indice": source,
        "origen_nombre": idx_to_name[source],
        "destino_indice": target,
        "destino_nombre": idx_to_name[target],
        "costo_total": round(total_cost, 6),
        "ruta_indices": path_indices,
        "ruta_nombres": path_names,
        "saltos": len(path_indices) - 1,
    }

    output_name = f"ruta_reconstruida_{source}_a_{target}.json"
    save_result(OUTPUT_DIR / output_name, result)

    print("Paso 4 completado.")
    print(f"Origen: {idx_to_name[source]} ({source})")
    print(f"Destino: {idx_to_name[target]} ({target})")
    print(f"Costo total: {total_cost:.4f}")
    print(f"Ruta de indices: {path_indices}")
    print(f"Ruta de nombres: {' -> '.join(path_names)}")
    print(f"Resultado guardado en: {OUTPUT_DIR / output_name}")


if __name__ == "__main__":
    main()
