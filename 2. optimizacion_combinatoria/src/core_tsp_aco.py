from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ACOConfig:
    ants: int = 40
    iterations: int = 250
    alpha: float = 1.0
    beta: float = 3.0
    evaporation_rate: float = 0.35
    intensification: float = 2.0
    elite_weight: float = 2.0
    seed: int = 42
    start_node: int = 0


def build_heuristic(cost_matrix: np.ndarray) -> np.ndarray:
    heuristic = np.zeros_like(cost_matrix, dtype=np.float64)
    positive_mask = cost_matrix > 0
    heuristic[positive_mask] = 1.0 / cost_matrix[positive_mask]
    return heuristic


def construct_ant_tour(
    cost_matrix: np.ndarray,
    pheromone: np.ndarray,
    heuristic: np.ndarray,
    rng: np.random.Generator,
    config: ACOConfig,
) -> tuple[list[int], float]:
    n = cost_matrix.shape[0]
    start = config.start_node
    unvisited = set(range(n))
    unvisited.remove(start)
    tour = [start]
    current = start
    total_cost = 0.0

    while unvisited:
        candidates = np.array(sorted(unvisited), dtype=np.int64)
        desirability = (
            np.power(pheromone[current, candidates], config.alpha)
            * np.power(heuristic[current, candidates], config.beta)
        )
        desirability = np.where(np.isfinite(desirability), desirability, 0.0)
        desirability_sum = desirability.sum()

        if desirability_sum <= 0.0:
            next_node = int(candidates[np.argmin(cost_matrix[current, candidates])])
        else:
            probabilities = desirability / desirability_sum
            next_node = int(rng.choice(candidates, p=probabilities))

        total_cost += float(cost_matrix[current, next_node])
        tour.append(next_node)
        unvisited.remove(next_node)
        current = next_node

    total_cost += float(cost_matrix[current, start])
    tour.append(start)
    return tour, total_cost


def reinforce_path(
    pheromone: np.ndarray,
    tour: list[int],
    score: float,
    intensification: float,
) -> None:
    deposit = intensification / max(score, 1e-12)
    for source, target in zip(tour[:-1], tour[1:]):
        pheromone[source, target] += deposit
        pheromone[target, source] += deposit


def run_aco(cost_matrix: np.ndarray, config: ACOConfig) -> tuple[list[int], float, list[float]]:
    rng = np.random.default_rng(config.seed)
    n = cost_matrix.shape[0]
    pheromone = np.ones((n, n), dtype=np.float64)
    np.fill_diagonal(pheromone, 0.0)
    heuristic = build_heuristic(cost_matrix)

    best_tour: list[int] | None = None
    best_cost = float("inf")
    history: list[float] = []

    for _ in range(config.iterations):
        iteration_best_tour: list[int] | None = None
        iteration_best_cost = float("inf")

        for _ant in range(config.ants):
            tour, cost = construct_ant_tour(cost_matrix, pheromone, heuristic, rng, config)
            if cost < iteration_best_cost:
                iteration_best_tour = tour
                iteration_best_cost = cost
            if cost < best_cost:
                best_tour = tour
                best_cost = cost

        pheromone *= (1.0 - config.evaporation_rate)
        pheromone = np.maximum(pheromone, 1e-12)

        if iteration_best_tour is not None:
            reinforce_path(pheromone, iteration_best_tour, iteration_best_cost, config.intensification)
        if best_tour is not None:
            reinforce_path(
                pheromone,
                best_tour,
                best_cost,
                config.intensification * config.elite_weight,
            )
        history.append(best_cost)

    if best_tour is None:
        raise ValueError("ACO no encontro ningun tour valido.")
    return best_tour, best_cost, history

