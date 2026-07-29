import numpy as np
from numpy.typing import NDArray
from typing import Callable

Array = NDArray[np.float64]

LIMITS = (-5.0, 5.0)


def get_initial_position(size: int, limits: tuple[float, float] = LIMITS) -> Array:
    """Genera una posicion inicial aleatoria dentro de los limites dados."""
    return np.random.uniform(*limits, size)

def rosenbrock_gradient(x: Array) -> Array:
    """Calcula el gradiente de Rosenbrock para un vector de tamano arbitrario."""
    gradient = np.zeros_like(x, dtype=float)

    for i in range(len(x)):
        if i == 0:
            gradient[i] = -400 * x[i] * (x[i + 1] - x[i] ** 2) - 2 * (1 - x[i])
        elif i == len(x) - 1:
            gradient[i] = 200 * (x[i] - x[i - 1] ** 2)
        else:
            gradient[i] = (
                200 * (x[i] - x[i - 1] ** 2)
                - 400 * x[i] * (x[i + 1] - x[i] ** 2)
                - 2 * (1 - x[i])
            )

    return gradient


def schwefel_gradient(x: Array) -> Array:
    """Calcula el gradiente de Schwefel para un vector de tamano arbitrario."""
    abs_x = np.abs(x)
    sqrt_abs_x = np.sqrt(abs_x)
    gradient = -np.sin(sqrt_abs_x) - 0.5 * sqrt_abs_x * np.cos(sqrt_abs_x)

    # En x = 0 la derivada se toma por continuidad para evitar divisiones/NaN.
    gradient = np.where(abs_x == 0, 0.0, gradient)
    return gradient.astype(float)


def rastrigin_gradient(x: Array) -> Array:
    """Calcula el gradiente de Rastrigin para un vector de tamano arbitrario."""
    x = np.asarray(x, dtype=float)
    return 2.0 * x + 20.0 * np.pi * np.sin(2.0 * np.pi * x)


def griewank_gradient(x: Array) -> Array:
    """Calcula el gradiente de Griewank para un vector de tamano arbitrario."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    gradient = np.zeros_like(x, dtype=float)

    cos_terms = np.array([np.cos(x[i] / np.sqrt(i + 1)) for i in range(n)], dtype=float)

    for i in range(n):
        product_without_i = 1.0
        for j in range(n):
            if j != i:
                product_without_i *= cos_terms[j]

        gradient[i] = (
            x[i] / 2000.0
            + (np.sin(x[i] / np.sqrt(i + 1)) / np.sqrt(i + 1)) * product_without_i
        )

    return gradient


def goldstein_price_gradient(x: Array) -> Array:
    """Calcula el gradiente de Goldstein-Price en 2 dimensiones."""
    if len(x) != 2:
        raise ValueError("goldstein_price_gradient solo esta definida aqui para 2 dimensiones.")

    x1 = float(x[0])
    x2 = float(x[1])

    q = x1 + x2 + 1.0
    p = 19.0 - 14.0 * x1 + 3.0 * x1**2 - 14.0 * x2 + 6.0 * x1 * x2 + 3.0 * x2**2
    a = 1.0 + q**2 * p

    r = 2.0 * x1 - 3.0 * x2
    s = 18.0 - 32.0 * x1 + 12.0 * x1**2 + 48.0 * x2 - 36.0 * x1 * x2 + 27.0 * x2**2
    b = 30.0 + r**2 * s

    dp_dx1 = -14.0 + 6.0 * x1 + 6.0 * x2
    dp_dx2 = -14.0 + 6.0 * x1 + 6.0 * x2
    da_dx1 = 2.0 * q * p + q**2 * dp_dx1
    da_dx2 = 2.0 * q * p + q**2 * dp_dx2

    ds_dx1 = -32.0 + 24.0 * x1 - 36.0 * x2
    ds_dx2 = 48.0 - 36.0 * x1 + 54.0 * x2
    db_dx1 = 4.0 * r * s + r**2 * ds_dx1
    db_dx2 = -6.0 * r * s + r**2 * ds_dx2

    gradient_x1 = da_dx1 * b + a * db_dx1
    gradient_x2 = da_dx2 * b + a * db_dx2

    return np.array([gradient_x1, gradient_x2], dtype=float)


def six_hump_camel_gradient(x: Array) -> Array:
    """Calcula el gradiente de la funcion de las seis jorobas de camello en 2 dimensiones."""
    if len(x) != 2:
        raise ValueError("six_hump_camel_gradient solo esta definida aqui para 2 dimensiones.")

    x1 = float(x[0])
    x2 = float(x[1])

    gradient_x1 = 8.0 * x1 - 8.4 * x1**3 + 2.0 * x1**5 + x2
    gradient_x2 = x1 - 8.0 * x2 + 16.0 * x2**3

    return np.array([gradient_x1, gradient_x2], dtype=float)


def descend(
    position: Array,
    gradient_function: Callable[[Array], Array],
    rate: float,
) -> tuple[Array, Array, Array]:
    """Calcula un paso de descenso por gradiente."""
    gradient = gradient_function(position)
    change = -rate * gradient
    new_position = position + change
    return new_position, gradient, change


def run_gradient_descent(
    initial_position: Array,
    function: Callable[[Array], float],
    gradient_function: Callable[[Array], Array],
    rate: float,
    max_iterations: int,
    tolerance: float | None = None,
) -> dict:
    """Ejecuta descenso por gradiente y retorna el historial del proceso."""
    position = np.array(initial_position, dtype=float)
    history = [position.copy()]
    function_values = [float(function(position))]
    gradients = []
    changes = []

    for _ in range(max_iterations):
        new_position, gradient, change = descend(position, gradient_function, rate)

        gradients.append(gradient.copy())
        changes.append(change.copy())

        position = np.array(new_position, dtype=float)
        history.append(position.copy())
        function_values.append(float(function(position)))

        if tolerance is not None and np.linalg.norm(change) < tolerance:
            break

    return {
        "initial_position": np.array(initial_position, dtype=float),
        "final_position": position,
        "final_value": float(function(position)),
        "iterations": len(history) - 1,
        "history": np.array(history, dtype=float),
        "function_values": np.array(function_values, dtype=float),
        "gradients": gradients,
        "changes": changes,
    }
