from __future__ import annotations

from pathlib import Path

import pandas as pd


def add_run_count_from_filename(df: pd.DataFrame, file_paths: list[Path]) -> pd.DataFrame:
    """Annotate each run with the sample size encoded in its source filename."""
    file_map: dict[tuple[str, int], list[int]] = {}

    for path in file_paths:
        stem_parts = path.stem.split("_")
        if len(stem_parts) < 4:
            continue

        function_name = "_".join(stem_parts[:-3])
        method_text = stem_parts[-3]
        dimension_text = stem_parts[-2]
        run_count_text = stem_parts[-1]
        if method_text != "gradient" or not dimension_text.endswith("d") or not run_count_text.startswith("n"):
            continue

        dimension = int(dimension_text[:-1])
        run_count = int(run_count_text[1:])
        file_map.setdefault((function_name, dimension), []).append(run_count)

    enriched_frames: list[pd.DataFrame] = []
    matched_index_parts: list[pd.Index] = []
    for (function_name, dimension), counts in file_map.items():
        subset = df[(df["funcion"] == function_name) & (df["dimension"] == dimension)].copy()
        if subset.empty:
            continue

        matched_index_parts.append(subset.index)
        counts = sorted(counts)
        start = 0
        for count in counts:
            end = min(start + count, len(subset))
            block = subset.iloc[start:end].copy()
            block["n_corridas_archivo"] = count
            enriched_frames.append(block)
            start = end

    if not enriched_frames:
        enriched = df.copy()
        enriched["n_corridas_archivo"] = pd.NA
        return enriched

    matched_index = matched_index_parts[0]
    for extra_index in matched_index_parts[1:]:
        matched_index = matched_index.union(extra_index)

    unmatched = df.loc[~df.index.isin(matched_index)].copy()
    if not unmatched.empty:
        unmatched["n_corridas_archivo"] = pd.NA
        enriched_frames.append(unmatched)

    return pd.concat(enriched_frames, ignore_index=True)


def prepare_function_runs(
    runs_df: pd.DataFrame,
    file_paths: list[Path],
    function_name: str,
    dimension: int,
) -> pd.DataFrame:
    """Return the runs for one function and dimension, annotated with sample size."""
    runs_enriched = add_run_count_from_filename(runs_df.copy(), file_paths)
    filtered = runs_enriched[
        (runs_enriched["funcion"] == function_name) & (runs_enriched["dimension"] == dimension)
    ].copy()
    return filtered.reset_index(drop=True)


def save_figure(fig, output_path: Path, dpi: int = 200) -> Path:
    """Save a matplotlib figure and return the destination path."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
    return output_path


def build_summary_table(
    summary_df: pd.DataFrame,
    function_name: str,
    dimension: int,
    dimension_label: str | None = None,
    function_label: str | None = None,
    round_digits: int = 6,
) -> pd.DataFrame:
    """Build a compact report table from the aggregated summary data."""
    dimension_text = dimension_label or f"{dimension}D"
    display_name = function_label or function_name.replace("_", " ").title()

    filtered = summary_df[
        (summary_df["funcion"] == function_name) & (summary_df["dimension"] == dimension)
    ].copy()
    filtered = filtered.sort_values("n_corridas").reset_index(drop=True)

    table = pd.DataFrame(
        {
            "Funcion": [display_name] * len(filtered),
            "Dimension": [dimension_text] * len(filtered),
            "Corridas": filtered["n_corridas"].astype(int),
            "Mejor valor": filtered["mejor_valor_final"].astype(float),
            "Peor valor": filtered["peor_valor_final"].astype(float),
            "Promedio": filtered["promedio_valor_final"].astype(float),
            "Desviacion estandar": filtered["desviacion_valor_final"].astype(float),
            "Promedio de evaluaciones": filtered["promedio_evaluaciones"].astype(float),
        }
    )

    numeric_columns = [
        "Mejor valor",
        "Peor valor",
        "Promedio",
        "Desviacion estandar",
        "Promedio de evaluaciones",
    ]
    for column in numeric_columns:
        table[column] = table[column].map(lambda value: round(value, round_digits))

    return table
