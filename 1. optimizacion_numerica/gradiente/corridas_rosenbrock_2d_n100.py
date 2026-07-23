import csv
import json
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

from funciones_gradientes import get_initial_position, run_gradient_descent
from funciones_objetivo import rosenbrock

Array = NDArray[np.float64]

N_CORRIDAS = 100
DIMENSION = 2
LIMITS = (-2.048, 2.048)
RATE = 1e-4
MAX_ITERATIONS = 1000
TOLERANCE = 1e-6
SEED = 42


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


def contar_evaluaciones(resultado: dict) -> int:
    """Cuenta evaluaciones de la funcion objetivo hechas durante la corrida."""
    return len(resultado["function_values"]) + 1


def ejecutar_corridas() -> list[dict]:
    """Ejecuta las 100 corridas de Rosenbrock en 2D."""
    np.random.seed(SEED)
    resultados = []

    for corrida in range(1, N_CORRIDAS + 1):
        posicion_inicial = get_initial_position(DIMENSION, limits=LIMITS)
        resultado = run_gradient_descent(
            initial_position=posicion_inicial,
            function=rosenbrock,
            gradient_function=rosenbrock_gradient,
            rate=RATE,
            max_iterations=MAX_ITERATIONS,
            tolerance=TOLERANCE,
        )

        resultados.append(
            {
                "corrida": corrida,
                "posicion_inicial": resultado["initial_position"].tolist(),
                "posicion_final": resultado["final_position"].tolist(),
                "valor_final": float(resultado["final_value"]),
                "iteraciones": int(resultado["iterations"]),
                "evaluaciones": contar_evaluaciones(resultado),
            }
        )

    return resultados


def guardar_resultados(resultados: list[dict]) -> tuple[Path, Path]:
    """Guarda los resultados en JSON y CSV."""
    directorio_salida = Path(__file__).resolve().parent / "resultados_corridas"
    directorio_salida.mkdir(exist_ok=True)

    json_path = directorio_salida / "rosenbrock_2d_n100.json"
    csv_path = directorio_salida / "rosenbrock_2d_n100.csv"

    with json_path.open("w", encoding="utf-8") as json_file:
        json.dump(resultados, json_file, indent=2)

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "corrida",
                "posicion_inicial",
                "posicion_final",
                "valor_final",
                "iteraciones",
                "evaluaciones",
            ],
        )
        writer.writeheader()
        writer.writerows(resultados)

    return json_path, csv_path


def imprimir_resumen(resultados: list[dict]) -> None:
    """Muestra un resumen corto de las corridas."""
    valores_finales = np.array([fila["valor_final"] for fila in resultados], dtype=float)
    evaluaciones = np.array([fila["evaluaciones"] for fila in resultados], dtype=int)

    print("Resumen Rosenbrock 2D - n=100")
    print(f"Mejor valor final: {valores_finales.min():.8f}")
    print(f"Peor valor final: {valores_finales.max():.8f}")
    print(f"Promedio valor final: {valores_finales.mean():.8f}")
    print(f"Promedio evaluaciones: {evaluaciones.mean():.2f}")


if __name__ == "__main__":
    resultados = ejecutar_corridas()
    json_path, csv_path = guardar_resultados(resultados)
    imprimir_resumen(resultados)
    print(f"JSON guardado en: {json_path}")
    print(f"CSV guardado en: {csv_path}")
