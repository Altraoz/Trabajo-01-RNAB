from __future__ import annotations

import csv
from pathlib import Path

from src.config_modelo_costo import (
    SMIC_HOURLY_EUR_2026,
    cost_formula_label,
    edge_total_cost,
    model_metadata,
    seller_cost_from_minutes,
)
from src.core_paths import PHASE1_DIR, RAW_CONNECTIONS_DATASET_PATH


WEIGHTED_EDGES_FILENAME = "aristas_ponderadas.csv"


def load_rows(path: Path = RAW_CONNECTIONS_DATASET_PATH) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def build_weighted_edges(
    rows: list[dict], hourly_rate_eur: float = SMIC_HOURLY_EUR_2026
) -> tuple[list[dict], dict[int, str]]:
    weighted_edges: list[dict] = []
    cities: dict[int, str] = {}

    for row in rows:
        start_idx = int(row["indice_inicio"])
        end_idx = int(row["indice_destino"])
        start_city = row["ciudad_inicio"]
        end_city = row["ciudad_destino"]
        distance = float(row["distancia"])
        time_min = float(row["tiempo(min)"])
        toll_eur = float(row["peajes(euros)"])
        fuel_eur = float(row["gasolina(euros)"])
        seller_cost_eur = seller_cost_from_minutes(time_min, hourly_rate_eur)
        weight = edge_total_cost(toll_eur, fuel_eur, time_min, hourly_rate_eur)

        cities[start_idx] = start_city
        cities[end_idx] = end_city

        weighted_edges.append(
            {
                "indice_inicio": start_idx,
                "indice_destino": end_idx,
                "ciudad_inicio": start_city,
                "ciudad_destino": end_city,
                "peso": round(weight, 6),
                "distancia": distance,
                "tiempo(min)": time_min,
                "peajes(euros)": toll_eur,
                "gasolina(euros)": fuel_eur,
                "costo_vendedor(euros)": round(seller_cost_eur, 6),
            }
        )

    return weighted_edges, cities


def build_adjacency(edges: list[dict], cities: dict[int, str]) -> dict:
    adjacency = {
        str(index): {"ciudad": cities[index], "vecinos": []}
        for index in sorted(cities)
    }

    for edge in edges:
        forward = {
            "destino_indice": edge["indice_destino"],
            "destino_ciudad": edge["ciudad_destino"],
            "peso": edge["peso"],
            "distancia": edge["distancia"],
            "tiempo(min)": edge["tiempo(min)"],
            "peajes(euros)": edge["peajes(euros)"],
            "gasolina(euros)": edge["gasolina(euros)"],
            "costo_vendedor(euros)": edge["costo_vendedor(euros)"],
        }
        backward = {
            "destino_indice": edge["indice_inicio"],
            "destino_ciudad": edge["ciudad_inicio"],
            "peso": edge["peso"],
            "distancia": edge["distancia"],
            "tiempo(min)": edge["tiempo(min)"],
            "peajes(euros)": edge["peajes(euros)"],
            "gasolina(euros)": edge["gasolina(euros)"],
            "costo_vendedor(euros)": edge["costo_vendedor(euros)"],
        }
        adjacency[str(edge["indice_inicio"])]["vecinos"].append(forward)
        adjacency[str(edge["indice_destino"])]["vecinos"].append(backward)

    return adjacency


def build_summary(
    edges: list[dict],
    cities: dict[int, str],
    hourly_rate_eur: float = SMIC_HOURLY_EUR_2026,
) -> dict:
    weights = [edge["peso"] for edge in edges]
    summary = {
        "ciudades": len(cities),
        "conexiones_directas": len(edges),
        "peso_minimo": min(weights),
        "peso_maximo": max(weights),
        "peso_promedio": round(sum(weights) / len(weights), 6),
        "formula_peso": cost_formula_label(hourly_rate_eur),
    }
    summary.update(model_metadata(hourly_rate_eur))
    return summary


def save_csv(path: Path, edges: list[dict]) -> None:
    fieldnames = [
        "indice_inicio",
        "indice_destino",
        "ciudad_inicio",
        "ciudad_destino",
        "peso",
        "distancia",
        "tiempo(min)",
        "peajes(euros)",
        "gasolina(euros)",
        "costo_vendedor(euros)",
    ]
    path.parent.mkdir(exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(edges)


def run_preprocessing(
    input_csv: Path = RAW_CONNECTIONS_DATASET_PATH,
    output_dir: Path = PHASE1_DIR,
    hourly_rate_eur: float = SMIC_HOURLY_EUR_2026,
) -> dict:
    rows = load_rows(input_csv)
    edges, cities = build_weighted_edges(rows, hourly_rate_eur)
    adjacency = build_adjacency(edges, cities)
    summary = build_summary(edges, cities, hourly_rate_eur)

    weighted_edges_path = output_dir / WEIGHTED_EDGES_FILENAME
    save_csv(weighted_edges_path, edges)

    return {
        "rows": rows,
        "edges": edges,
        "cities": cities,
        "adjacency": adjacency,
        "summary": summary,
        "weighted_edges_path": weighted_edges_path,
    }
