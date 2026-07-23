"""Paso 2: construir la matriz TSP y la matriz de siguiente salto."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.core_matrices import build_complete_matrices


def main() -> None:
    result = build_complete_matrices()
    summary = result["summary"]

    print("Paso 2 completado.")
    print(f"Ciudades: {summary['ciudades']}")
    print(f"Matriz: {summary['shape'][0]}x{summary['shape'][1]}")
    print(f"Diagonal cero: {summary['diagonal_cero']}")
    print(f"Costo minimo finito: {summary['costo_minimo_finito']:.4f}")
    print(f"Costo maximo finito: {summary['costo_maximo_finito']:.4f}")
    print("Salidas principales: matriz_costo_total_96x96.npy y matriz_siguiente_salto_96x96.npy")


if __name__ == "__main__":
    main()
