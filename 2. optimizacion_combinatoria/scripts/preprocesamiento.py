"""Paso 1: transformar el dataset original en aristas ponderadas."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.core_preprocesamiento import run_preprocessing


def main() -> None:
    result = run_preprocessing()
    summary = result["summary"]

    print("Paso 1 completado.")
    print(f"Ciudades: {summary['ciudades']}")
    print(f"Conexiones directas: {summary['conexiones_directas']}")
    print(f"Peso minimo: {summary['peso_minimo']:.4f}")
    print(f"Peso maximo: {summary['peso_maximo']:.4f}")
    print(f"Salida principal: {result['weighted_edges_path']}")


if __name__ == "__main__":
    main()
