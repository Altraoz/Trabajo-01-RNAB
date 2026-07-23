from __future__ import annotations

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUTS_DIR = BASE_DIR / "outputs"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
ACO_OUTPUT_DIR = OUTPUTS_DIR / "aco"
GA_OUTPUT_DIR = OUTPUTS_DIR / "ga"
VIS_OUTPUT_DIR = OUTPUTS_DIR / "visualizaciones"
WEB_OUTPUT_DIR = OUTPUTS_DIR / "web"


def _prefer_existing(preferred: Path, legacy: Path) -> Path:
    if preferred.exists():
        return preferred
    return legacy


PHASE1_DIR = PROCESSED_DATA_DIR
PHASE3_DIR = PROCESSED_DATA_DIR
PHASE5_DIR = PROCESSED_DATA_DIR
PHASE6_DIR = VIS_OUTPUT_DIR
PHASE7_DIR = ACO_OUTPUT_DIR
PHASE8_DIR = GA_OUTPUT_DIR
PHASE9_DIR = VIS_OUTPUT_DIR

WEIGHTED_EDGES_CSV_PATH = _prefer_existing(
    PROCESSED_DATA_DIR / "aristas_ponderadas.csv",
    BASE_DIR / "fase_1_grafo" / "aristas_ponderadas.csv",
)
RAW_CONNECTIONS_DATASET_PATH = _prefer_existing(
    RAW_DATA_DIR / "dataset_cities_france.csv",
    BASE_DIR / "dataset_cities_france.csv",
)
RAW_CONNECTIONS_CSV_PATH = _prefer_existing(
    RAW_DATA_DIR / "conexiones.csv",
    BASE_DIR / "conexiones.csv",
)
INPUT_COST_MATRIX_PATH = _prefer_existing(
    PROCESSED_DATA_DIR / "matriz_costo_total_96x96.npy",
    PHASE3_DIR / "matriz_costo_total_96x96.npy",
)
INPUT_COST_CSV_PATH = _prefer_existing(
    PROCESSED_DATA_DIR / "matriz_costo_total_96x96.csv",
    PHASE3_DIR / "matriz_costo_total_96x96.csv",
)
NEXT_HOP_MATRIX_PATH = _prefer_existing(
    PROCESSED_DATA_DIR / "matriz_siguiente_salto_96x96.npy",
    PHASE3_DIR / "matriz_siguiente_salto_96x96.npy",
)
TOTAL_COST_MATRIX_PATH = _prefer_existing(
    PROCESSED_DATA_DIR / "matriz_costo_total_96x96.npy",
    PHASE3_DIR / "matriz_costo_total_96x96.npy",
)
