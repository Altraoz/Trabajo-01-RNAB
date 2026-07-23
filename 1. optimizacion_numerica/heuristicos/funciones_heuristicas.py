import numpy as np
from numpy.typing import NDArray
from typing import Callable

Array = NDArray[np.float64]


def _ensure_bounds(bounds: float | list[float] | tuple[float, ...] | Array | None, d: int, default: float) -> Array:
    """Normaliza limites escalares o vectoriales a un arreglo de tamano d."""
    if bounds is None:
        return np.full(d, default, dtype=float)

    if np.isscalar(bounds):
        return np.full(d, float(bounds), dtype=float)

    arr = np.asarray(bounds, dtype=float)
    if arr.shape != (d,):
        raise ValueError(f"Los limites deben tener tamano {d}.")
    return arr


def evolutionary_initial_population(
    population_size: int = 30,
    dimension: int = 5,
    lower_bounds: float | list[float] | tuple[float, ...] | Array | None = None,
    upper_bounds: float | list[float] | tuple[float, ...] | Array | None = None,
) -> Array:
    """Genera una poblacion inicial uniforme dentro de los limites dados."""
    lb = _ensure_bounds(lower_bounds, dimension, -1.0)
    ub = _ensure_bounds(upper_bounds, dimension, 1.0)

    if np.any(lb >= ub):
        raise ValueError("Cada limite inferior debe ser menor que su limite superior.")

    population = np.random.rand(population_size, dimension)
    return population * (ub - lb) + lb


def evolutionary_mutation(
    population: Array,
    mutant_indices: Array | None = None,
    mutation_coordinates: Array | None = None,
    lower_bounds: float | list[float] | tuple[float, ...] | Array | None = None,
    upper_bounds: float | list[float] | tuple[float, ...] | Array | None = None,
) -> Array:
    """Genera individuos mutantes reemplazando una coordenada por un valor aleatorio."""
    population = np.asarray(population, dtype=float).copy()
    n_rows, n_cols = population.shape

    if mutant_indices is None:
        mutant_indices = np.arange(n_rows)
    else:
        mutant_indices = np.asarray(mutant_indices, dtype=int)

    if mutation_coordinates is None:
        mutation_coordinates = np.random.randint(low=0, high=n_cols, size=n_rows)
    else:
        mutation_coordinates = np.asarray(mutation_coordinates, dtype=int)

    lb = _ensure_bounds(lower_bounds, n_cols, float(population.min()))
    ub = _ensure_bounds(upper_bounds, n_cols, float(population.max()))

    for idx in mutant_indices:
        coord = mutation_coordinates[idx]
        population[idx, coord] = np.random.rand() * (ub[coord] - lb[coord]) + lb[coord]

    return population[mutant_indices, :]


def evolutionary_crossover(crossover_population: Array) -> Array:
    """Realiza cruzamiento de un punto entre pares de individuos."""
    crossover_population = np.asarray(crossover_population, dtype=float).copy()
    n_rows, n_cols = crossover_population.shape

    children = np.zeros_like(crossover_population)
    n_pairs = n_rows // 2

    for i in range(n_pairs):
        crossover_coordinate = np.random.randint(low=0, high=n_cols)
        children[i, :] = np.concatenate(
            (
                crossover_population[i, :crossover_coordinate],
                crossover_population[i + n_pairs, crossover_coordinate:],
            )
        )
        children[i + n_pairs, :] = np.concatenate(
            (
                crossover_population[i + n_pairs, :crossover_coordinate],
                crossover_population[i, crossover_coordinate:],
            )
        )

    if n_rows % 2 == 1:
        children[-1, :] = crossover_population[-1, :]

    return children


def evolutionary_population_eval(population: Array, objective_function: Callable[[Array], float]) -> tuple[Array, Array]:
    """Evalua y ordena la poblacion de menor a mayor valor objetivo."""
    population = np.asarray(population, dtype=float).copy()
    fitness_values = np.array([float(objective_function(individual)) for individual in population], dtype=float)
    ranking = np.argsort(fitness_values)
    return population[ranking], fitness_values[ranking]


def evolutionary_next_generation(
    ranked_population: Array,
    elitism_fraction: float = 0.2,
    mutation_fraction: float = 0.1,
    lower_bounds: float | list[float] | tuple[float, ...] | Array | None = None,
    upper_bounds: float | list[float] | tuple[float, ...] | Array | None = None,
) -> Array:
    """Construye la siguiente generacion a partir de elite, cruce y mutacion."""
    ranked_population = np.asarray(ranked_population, dtype=float).copy()
    n_rows, n_cols = ranked_population.shape

    n_mutation = int(np.floor(n_rows * mutation_fraction))
    n_crossover = int(2 * np.floor(n_rows * (1 - elitism_fraction - mutation_fraction) / 2))
    n_elite = n_rows - n_mutation - n_crossover

    if n_elite < 0:
        raise ValueError("Las fracciones de elitismo y mutacion producen un tamano de elite negativo.")

    elite_population = ranked_population[:n_elite, :]

    if n_crossover > 0:
        crossover_indices = np.random.choice(n_rows, size=n_crossover, replace=False)
        crossover_population = evolutionary_crossover(ranked_population[crossover_indices, :])
    else:
        crossover_population = np.empty((0, n_cols), dtype=float)

    if n_mutation > 0:
        mutant_indices = np.random.randint(low=0, high=n_rows, size=n_mutation)
        mutation_coordinates = np.random.randint(low=0, high=n_cols, size=n_rows)
        mutant_population = evolutionary_mutation(
            ranked_population,
            mutant_indices=mutant_indices,
            mutation_coordinates=mutation_coordinates,
            lower_bounds=lower_bounds,
            upper_bounds=upper_bounds,
        )
    else:
        mutant_population = np.empty((0, n_cols), dtype=float)

    return np.concatenate((elite_population, crossover_population, mutant_population), axis=0)


def run_evolutionary_algorithm(
    objective_function: Callable[[Array], float],
    population_size: int = 30,
    dimension: int = 3,
    lower_bounds: float | list[float] | tuple[float, ...] | Array | None = None,
    upper_bounds: float | list[float] | tuple[float, ...] | Array | None = None,
    elitism_fraction: float = 0.2,
    mutation_fraction: float = 0.1,
    max_iterations: int = 50,
    seed: int | None = None,
) -> dict:
    """Ejecuta un algoritmo evolutivo generico para minimizacion."""
    if seed is not None:
        np.random.seed(seed)

    population = evolutionary_initial_population(
        population_size=population_size,
        dimension=dimension,
        lower_bounds=lower_bounds,
        upper_bounds=upper_bounds,
    )

    populations = [population.copy()]
    best_values = []
    best_solutions = []

    for _ in range(max_iterations):
        ranked_population, ranked_fitness = evolutionary_population_eval(population, objective_function)
        best_values.append(float(ranked_fitness[0]))
        best_solutions.append(ranked_population[0].copy())
        population = evolutionary_next_generation(
            ranked_population=ranked_population,
            elitism_fraction=elitism_fraction,
            mutation_fraction=mutation_fraction,
            lower_bounds=lower_bounds,
            upper_bounds=upper_bounds,
        )
        populations.append(population.copy())

    best_solution = np.array(best_solutions[-1], dtype=float)
    best_value = float(best_values[-1])

    return {
        "initial_population": populations[0],
        "final_population": populations[-1],
        "best_solution": best_solution,
        "best_value": best_value,
        "best_values_history": np.array(best_values, dtype=float),
        "best_solutions_history": np.array(best_solutions, dtype=float),
        "populations_history": populations,
        "iterations": max_iterations,
        "evaluations": population_size * max_iterations,
    }


def run_particle_swarm_optimization(
    objective_function: Callable[[Array], float],
    swarm_size: int = 30,
    dimension: int = 3,
    lower_bounds: float | list[float] | tuple[float, ...] | Array | None = None,
    upper_bounds: float | list[float] | tuple[float, ...] | Array | None = None,
    inertia_weight: float = 0.7,
    cognitive_weight: float = 1.5,
    social_weight: float = 1.5,
    max_iterations: int = 100,
    seed: int | None = None,
) -> dict:
    """Ejecuta PSO generico para minimizacion."""
    if seed is not None:
        np.random.seed(seed)

    lb = _ensure_bounds(lower_bounds, dimension, -1.0)
    ub = _ensure_bounds(upper_bounds, dimension, 1.0)

    if np.any(lb >= ub):
        raise ValueError("Cada limite inferior debe ser menor que su limite superior.")

    positions = evolutionary_initial_population(
        population_size=swarm_size,
        dimension=dimension,
        lower_bounds=lb,
        upper_bounds=ub,
    )

    velocity_scale = ub - lb
    velocities = np.random.uniform(-velocity_scale, velocity_scale, size=(swarm_size, dimension))

    personal_best_positions = positions.copy()
    personal_best_values = np.array([float(objective_function(p)) for p in positions], dtype=float)

    best_index = int(np.argmin(personal_best_values))
    global_best_position = personal_best_positions[best_index].copy()
    global_best_value = float(personal_best_values[best_index])

    positions_history = [positions.copy()]
    velocities_history = [velocities.copy()]
    best_values_history = [global_best_value]
    global_best_history = [global_best_position.copy()]

    for _ in range(max_iterations):
        r1 = np.random.rand(swarm_size, dimension)
        r2 = np.random.rand(swarm_size, dimension)

        velocities = (
            inertia_weight * velocities
            + cognitive_weight * r1 * (personal_best_positions - positions)
            + social_weight * r2 * (global_best_position - positions)
        )

        positions = positions + velocities
        positions = np.clip(positions, lb, ub)

        current_values = np.array([float(objective_function(p)) for p in positions], dtype=float)
        improved = current_values < personal_best_values
        personal_best_positions[improved] = positions[improved]
        personal_best_values[improved] = current_values[improved]

        best_index = int(np.argmin(personal_best_values))
        global_best_position = personal_best_positions[best_index].copy()
        global_best_value = float(personal_best_values[best_index])

        positions_history.append(positions.copy())
        velocities_history.append(velocities.copy())
        best_values_history.append(global_best_value)
        global_best_history.append(global_best_position.copy())

    return {
        "initial_positions": positions_history[0],
        "final_positions": positions_history[-1],
        "final_velocities": velocities_history[-1],
        "best_solution": global_best_position,
        "best_value": global_best_value,
        "best_values_history": np.array(best_values_history, dtype=float),
        "global_best_history": np.array(global_best_history, dtype=float),
        "positions_history": positions_history,
        "velocities_history": velocities_history,
        "iterations": max_iterations,
        "evaluations": swarm_size * (max_iterations + 1),
    }


def run_differential_evolution(
    objective_function: Callable[[Array], float],
    population_size: int = 30,
    dimension: int = 3,
    lower_bounds: float | list[float] | tuple[float, ...] | Array | None = None,
    upper_bounds: float | list[float] | tuple[float, ...] | Array | None = None,
    mutation_factor: float = 0.8,
    crossover_rate: float = 0.7,
    max_iterations: int = 100,
    seed: int | None = None,
) -> dict:
    """Ejecuta evolucion diferencial generica para minimizacion."""
    if seed is not None:
        np.random.seed(seed)

    lb = _ensure_bounds(lower_bounds, dimension, -1.0)
    ub = _ensure_bounds(upper_bounds, dimension, 1.0)

    if np.any(lb >= ub):
        raise ValueError("Cada limite inferior debe ser menor que su limite superior.")
    if population_size < 4:
        raise ValueError("La poblacion debe tener al menos 4 individuos para evolucion diferencial.")

    population = evolutionary_initial_population(
        population_size=population_size,
        dimension=dimension,
        lower_bounds=lb,
        upper_bounds=ub,
    )
    fitness = np.array([float(objective_function(individual)) for individual in population], dtype=float)

    best_index = int(np.argmin(fitness))
    best_solution = population[best_index].copy()
    best_value = float(fitness[best_index])

    populations_history = [population.copy()]
    best_values_history = [best_value]
    best_solutions_history = [best_solution.copy()]

    for _ in range(max_iterations):
        new_population = population.copy()
        new_fitness = fitness.copy()

        for i in range(population_size):
            candidates = np.delete(np.arange(population_size), i)
            a_idx, b_idx, c_idx = np.random.choice(candidates, size=3, replace=False)

            mutant = population[a_idx] + mutation_factor * (population[b_idx] - population[c_idx])
            mutant = np.clip(mutant, lb, ub)

            trial = population[i].copy()
            j_rand = np.random.randint(dimension)

            for j in range(dimension):
                if np.random.rand() < crossover_rate or j == j_rand:
                    trial[j] = mutant[j]

            trial_value = float(objective_function(trial))
            if trial_value < fitness[i]:
                new_population[i] = trial
                new_fitness[i] = trial_value

        population = new_population
        fitness = new_fitness

        best_index = int(np.argmin(fitness))
        best_solution = population[best_index].copy()
        best_value = float(fitness[best_index])

        populations_history.append(population.copy())
        best_values_history.append(best_value)
        best_solutions_history.append(best_solution.copy())

    return {
        "initial_population": populations_history[0],
        "final_population": populations_history[-1],
        "best_solution": best_solution,
        "best_value": best_value,
        "best_values_history": np.array(best_values_history, dtype=float),
        "best_solutions_history": np.array(best_solutions_history, dtype=float),
        "populations_history": populations_history,
        "iterations": max_iterations,
        "evaluations": population_size * (max_iterations + 1),
    }
