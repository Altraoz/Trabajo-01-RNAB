from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class GAConfig:
    population_size: int = 180
    generations: int = 350
    mutation_rate: float = 0.12
    crossover_rate: float = 0.9
    elite_count: int = 12
    tournament_size: int = 5
    seed: int = 42
    start_node: int = 0
    inject_aco_seed: bool = True


def tour_cost(route: np.ndarray, cost_matrix: np.ndarray, start_node: int) -> float:
    total = float(cost_matrix[start_node, route[0]])
    total += float(sum(cost_matrix[a, b] for a, b in zip(route[:-1], route[1:])))
    total += float(cost_matrix[route[-1], start_node])
    return total


def canonical_closed_tour(route: np.ndarray, start_node: int) -> list[int]:
    return [start_node] + route.tolist() + [start_node]


def load_aco_seed(result_path: Path, start_node: int) -> np.ndarray | None:
    if not result_path.exists():
        return None
    with result_path.open("r", encoding="utf-8") as handle:
        result = json.load(handle)
    tour = result["mejor_tour_indices_sin_cierre"]
    if not tour or tour[0] != start_node:
        return None
    return np.array(tour[1:], dtype=np.int64)


def make_initial_population(
    n: int,
    rng: np.random.Generator,
    config: GAConfig,
    aco_result_path: Path | None = None,
) -> list[np.ndarray]:
    nodes = np.array([idx for idx in range(n) if idx != config.start_node], dtype=np.int64)
    population: list[np.ndarray] = []

    if config.inject_aco_seed and aco_result_path is not None:
        seeded = load_aco_seed(aco_result_path, config.start_node)
        if seeded is not None and len(seeded) == len(nodes):
            population.append(seeded.copy())

    while len(population) < config.population_size:
        candidate = nodes.copy()
        rng.shuffle(candidate)
        population.append(candidate)
    return population


def ordered_crossover(parent_a: np.ndarray, parent_b: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    n = len(parent_a)
    left, right = sorted(rng.choice(n, size=2, replace=False))
    child = np.full(n, -1, dtype=np.int64)
    child[left:right + 1] = parent_a[left:right + 1]
    fill_values = [gene for gene in parent_b if gene not in child]
    fill_positions = [idx for idx, gene in enumerate(child) if gene == -1]
    for idx, gene in zip(fill_positions, fill_values):
        child[idx] = gene
    return child


def mutate_swap(route: np.ndarray, rng: np.random.Generator, mutation_rate: float) -> np.ndarray:
    mutated = route.copy()
    if rng.random() < mutation_rate:
        i, j = sorted(rng.choice(len(mutated), size=2, replace=False))
        mutated[i], mutated[j] = mutated[j], mutated[i]
    return mutated


def tournament_select(
    population: list[np.ndarray],
    fitness: np.ndarray,
    rng: np.random.Generator,
    tournament_size: int,
) -> np.ndarray:
    indices = rng.choice(len(population), size=tournament_size, replace=False)
    best_idx = indices[np.argmin(fitness[indices])]
    return population[int(best_idx)]


def run_ga(
    cost_matrix: np.ndarray,
    config: GAConfig,
    aco_result_path: Path | None = None,
) -> tuple[list[int], float, list[float]]:
    rng = np.random.default_rng(config.seed)
    n = cost_matrix.shape[0]
    population = make_initial_population(n, rng, config, aco_result_path)

    best_route: np.ndarray | None = None
    best_cost = float("inf")
    history: list[float] = []

    for _ in range(config.generations):
        fitness = np.array(
            [tour_cost(route, cost_matrix, config.start_node) for route in population],
            dtype=np.float64,
        )
        order = np.argsort(fitness)
        population = [population[i] for i in order]
        fitness = fitness[order]

        if fitness[0] < best_cost:
            best_cost = float(fitness[0])
            best_route = population[0].copy()
        history.append(best_cost)

        next_population = [population[i].copy() for i in range(min(config.elite_count, len(population)))]
        while len(next_population) < config.population_size:
            parent_a = tournament_select(population, fitness, rng, config.tournament_size)
            parent_b = tournament_select(population, fitness, rng, config.tournament_size)
            if rng.random() < config.crossover_rate:
                child = ordered_crossover(parent_a, parent_b, rng)
            else:
                child = parent_a.copy()
            child = mutate_swap(child, rng, config.mutation_rate)
            next_population.append(child)
        population = next_population

    if best_route is None:
        raise ValueError("GA no encontro ningun tour valido.")
    return canonical_closed_tour(best_route, config.start_node), best_cost, history

