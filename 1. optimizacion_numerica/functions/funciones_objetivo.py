import numpy as np
from numpy.typing import NDArray

Array = NDArray[np.float64]


def rosenbrock(x: Array) -> float:
    """Calcula la funcion generalizada de Rosenbrock en un punto x."""
    n = len(x)
    return sum(
        100 * (x[i] - x[i - 1] ** 2) ** 2 + (1 - x[i - 1]) ** 2
        for i in range(1, n)
    )

def schwefel(x: Array) -> float:
    """Calcula la funcion de Schwefel en un punto x."""
    d = len(x)
    return 418.9829 * d - np.sum(x * np.sin(np.sqrt(np.abs(x))))


def rastrigin(x: Array) -> float:
    """Calcula la funcion generalizada de Rastrigin en un punto x."""
    n = len(x)
    total = 10 * n

    for value in x:
        value = float(value)
        total += value ** 2 - 10 * np.cos(2 * np.pi * value)

    return total


def griewank(x: Array) -> float:
    """Calcula la funcion generalizada de Griewank en un punto x."""
    sum_term = 0.0
    product_term = 1.0

    for i, value in enumerate(x, start=1):
        value = float(value)
        sum_term += (value ** 2) / 4000
        product_term *= np.cos(value / np.sqrt(i))

    return sum_term - product_term + 1


def goldstein_price(x: Array) -> float:
    """Calcula la funcion de Goldstein-Price en 2 dimensiones."""
    if len(x) != 2:
        raise ValueError("goldstein_price solo esta definida aqui para 2 dimensiones.")

    x1 = float(x[0])
    x2 = float(x[1])

    first_term = 1 + np.power(x1 + x2 + 1, 2) * (
        19 - 14 * x1 + 3 * (x1 ** 2) - 14 * x2 + 6 * x1 * x2 + 3 * (x2 ** 2)
    )
    second_term = 30 + np.power(2 * x1 - 3 * x2, 2) * (
        18 - 32 * x1 + 12 * (x1 ** 2) + 48 * x2 - 36 * x1 * x2 + 27 * (x2 ** 2)
    )

    return first_term * second_term


def six_hump_camel(x: Array) -> float:
    """Calcula la funcion de las seis jorobas de camello en 2 dimensiones."""
    if len(x) != 2:
        raise ValueError("six_hump_camel solo esta definida aqui para 2 dimensiones.")

    x1 = float(x[0])
    x2 = float(x[1])

    return (
        (4 - 2.1 * (x1 ** 2) + (x1 ** 4) / 3) * (x1 ** 2)
        + x1 * x2
        + (-4 + 4 * (x2 ** 2)) * (x2 ** 2)
    )
