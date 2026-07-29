from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from src.core_grafo import expand_tour, load_city_index_to_name, load_json, save_json
from src.core_paths import (
    ACO_OUTPUT_DIR,
    GA_OUTPUT_DIR,
    NEXT_HOP_MATRIX_PATH,
    TOTAL_COST_MATRIX_PATH,
    VIS_OUTPUT_DIR,
    WEB_OUTPUT_DIR,
    WEIGHTED_EDGES_CSV_PATH,
)
from src.core_visualizacion import (
    CITY_COORDS,
    create_history_svg,
    create_route_map_html,
    create_route_map_svg,
    create_route_svg,
    save_html,
    save_svg,
)


WIDTH = 900
HEIGHT = 1100
PADDING = 60
BACKGROUND = "#f7f4ea"
CITY_COLOR = "#274690"
ROUTE_COLOR = "#d1495b"
START_COLOR = "#2a9d8f"
END_COLOR = "#e76f51"
TEXT_COLOR = "#222222"
SUBTEXT_COLOR = "#555555"


def load_method_results(
    aco_result_path: Path = ACO_OUTPUT_DIR / "resultado_aco_final.json",
    ga_result_path: Path = GA_OUTPUT_DIR / "resultado_ga_final.json",
) -> tuple[dict, dict]:
    return load_json(aco_result_path), load_json(ga_result_path)


def pick_best_result(aco: dict, ga: dict) -> tuple[str, dict]:
    if ga["mejor_costo_tour"] <= aco["mejor_costo_tour"]:
        return "GA", ga
    return "ACO", aco


def build_comparison(aco: dict, ga: dict) -> dict:
    aco_cost = float(aco["mejor_costo_tour"])
    ga_cost = float(ga["mejor_costo_tour"])
    best_method = "GA" if ga_cost <= aco_cost else "ACO"
    best_cost = min(aco_cost, ga_cost)
    worst_cost = max(aco_cost, ga_cost)
    absolute_gap = worst_cost - best_cost
    relative_gap_pct = (absolute_gap / worst_cost * 100.0) if worst_cost > 0 else 0.0
    return {
        "mejor_metodo": best_method,
        "costo_aco": round(aco_cost, 6),
        "costo_ga": round(ga_cost, 6),
        "mejor_costo": round(best_cost, 6),
        "diferencia_absoluta": round(abs(ga_cost - aco_cost), 6),
        "diferencia_relativa_pct": round(relative_gap_pct, 4),
    }


def expand_best_tour(
    result: dict,
    next_hop_path: Path = NEXT_HOP_MATRIX_PATH,
    cost_matrix_path: Path = TOTAL_COST_MATRIX_PATH,
    cities_csv_path: Path = WEIGHTED_EDGES_CSV_PATH,
) -> dict:
    idx_to_name = load_city_index_to_name(cities_csv_path)
    next_hop = np.load(next_hop_path)
    cost_matrix = np.load(cost_matrix_path)
    tsp_tour = result["mejor_tour_indices"]
    expanded_segments, expanded_route, total_cost = expand_tour(tsp_tour, next_hop, cost_matrix)
    return {
        "tour_tsp_indices": tsp_tour,
        "tour_tsp_nombres": [idx_to_name[index] for index in tsp_tour],
        "tramos_expandidos": [
            {
                **segment,
                "ruta_nombres": [idx_to_name[index] for index in segment["ruta_indices"]],
            }
            for segment in expanded_segments
        ],
        "recorrido_real_indices": expanded_route,
        "recorrido_real_nombres": [idx_to_name[index] for index in expanded_route],
        "costo_total_tour": round(total_cost, 6),
        "n_saltos_tsp": len(tsp_tour) - 1,
        "n_saltos_reales": len(expanded_route) - 1,
    }


def export_visual_artifacts(
    result: dict,
    method_name: str,
    expanded_tour: dict | None = None,
    output_dir: Path = VIS_OUTPUT_DIR,
) -> dict:
    route_indices = result["mejor_tour_indices"]
    route_for_map = expanded_tour["recorrido_real_indices"] if expanded_tour is not None else route_indices
    idx_to_name = load_city_index_to_name(WEIGHTED_EDGES_CSV_PATH)
    route_projection_svg = create_route_svg(
        route_indices,
        result["mejor_tour_nombres"],
        title=f"Mejor solucion {method_name}",
    )
    route_map_svg = create_route_map_svg(
        route_for_map,
        idx_to_name,
        title=f"Mejor ruta final {method_name} sobre Francia",
    )
    route_map_html = create_route_map_html(
        route_for_map,
        idx_to_name,
        title=f"Mejor ruta final {method_name} sobre Francia",
        method_name=method_name,
        total_cost=float(result["mejor_costo_tour"]),
    )
    history_svg = create_history_svg(result["historial_mejor_costo"], title=f"Convergencia {method_name}")
    route_svg_path = save_svg(route_map_svg, output_dir / "visualizacion_mejor_solucion.svg")
    route_projection_svg_path = save_svg(route_projection_svg, output_dir / "visualizacion_mejor_solucion_proyeccion.svg")
    route_map_html_path = save_html(route_map_html, output_dir / "visualizacion_mejor_solucion_mapa.html")
    history_svg_path = save_svg(history_svg, output_dir / f"convergencia_{method_name.lower()}.svg")
    return {
        "route_svg_path": route_svg_path,
        "route_projection_svg_path": route_projection_svg_path,
        "route_map_html_path": route_map_html_path,
        "history_svg_path": history_svg_path,
    }


def _project_points(coords: np.ndarray) -> np.ndarray:
    lats = coords[:, 0]
    lons = coords[:, 1]
    min_lon, max_lon = float(lons.min()), float(lons.max())
    min_lat, max_lat = float(lats.min()), float(lats.max())
    x = PADDING + (lons - min_lon) / (max_lon - min_lon) * (WIDTH - 2 * PADDING)
    y = HEIGHT - PADDING - (lats - min_lat) / (max_lat - min_lat) * (HEIGHT - 2 * PADDING)
    return np.column_stack([x, y])


def _load_font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.truetype("arial.ttf", size=size)
    except OSError:
        return ImageFont.load_default()


def _build_base_frame(title: str, subtitle: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    draw.text((WIDTH // 2, 24), title, fill=TEXT_COLOR, font=_load_font(28), anchor="ma")
    draw.text((WIDTH // 2, 58), subtitle, fill=SUBTEXT_COLOR, font=_load_font(16), anchor="ma")
    return image, draw


def _draw_cities(draw: ImageDraw.ImageDraw, projected_all: np.ndarray) -> None:
    for x, y in projected_all:
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=CITY_COLOR)


def _draw_route(draw: ImageDraw.ImageDraw, projected_route: np.ndarray, step: int) -> None:
    visible = projected_route[: step + 1]
    points = [tuple(map(float, point)) for point in visible]
    if len(points) >= 2:
        draw.line(points, fill=ROUTE_COLOR, width=4, joint="curve")
    start_x, start_y = points[0]
    draw.ellipse((start_x - 8, start_y - 8, start_x + 8, start_y + 8), fill=START_COLOR)
    current_x, current_y = points[-1]
    draw.ellipse((current_x - 7, current_y - 7, current_x + 7, current_y + 7), fill=END_COLOR)


def _add_annotations(draw: ImageDraw.ImageDraw, method_name: str, result: dict, total_steps: int, current_step: int) -> None:
    info_font = _load_font(16)
    draw.rounded_rectangle((30, HEIGHT - 145, WIDTH - 30, HEIGHT - 25), radius=16, fill="#fffdf8", outline="#d6d0c4")
    draw.text((48, HEIGHT - 130), f"Mejor metodo: {method_name}", fill=TEXT_COLOR, font=info_font)
    draw.text((48, HEIGHT - 104), f"Costo: {result['mejor_costo_tour']:.2f} EUR", fill=TEXT_COLOR, font=info_font)
    draw.text((48, HEIGHT - 78), f"Tramo {current_step}/{total_steps - 1}", fill=TEXT_COLOR, font=info_font)
    draw.text((48, HEIGHT - 52), result["formula_peso"], fill=SUBTEXT_COLOR, font=info_font)


def generate_solution_gif(
    method_name: str,
    result: dict,
    output_dir: Path = VIS_OUTPUT_DIR,
) -> dict:
    route_indices = result["mejor_tour_indices"]
    route_coords = CITY_COORDS[np.array(route_indices)]
    projected_all = _project_points(CITY_COORDS)
    projected_route = _project_points(route_coords)
    total_steps = len(route_indices)
    frames: list[Image.Image] = []

    for step in range(1, total_steps):
        image, draw = _build_base_frame(
            "Mejor solucion combinatoria final",
            "Recorrido progresivo sobre las 96 capitales de Francia",
        )
        _draw_cities(draw, projected_all)
        _draw_route(draw, projected_route, step)
        _add_annotations(draw, method_name, result, total_steps, step)
        frames.append(image)

    frames.extend([frames[-1].copy() for _ in range(8)])
    output_dir.mkdir(exist_ok=True)
    gif_path = output_dir / "mejor_solucion_combinatoria.gif"
    summary_path = output_dir / "resumen_gif_final.json"
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=140, loop=0, optimize=False)
    summary = {
        "metodo_ganador": method_name,
        "mejor_costo_tour": result["mejor_costo_tour"],
        "frames": len(frames),
        "archivo_gif": str(gif_path),
        "formula_peso": result["formula_peso"],
    }
    save_json(summary_path, summary)
    return {"gif_path": gif_path, "gif_summary_path": summary_path, "gif_summary": summary}


def export_final_bundle(
    best_method: str,
    best_result: dict,
    expanded_tour: dict,
    comparison: dict,
    output_dir: Path = WEB_OUTPUT_DIR,
) -> dict:
    output_dir.mkdir(exist_ok=True)
    save_json(output_dir / "comparacion_metodos.json", comparison)
    save_json(output_dir / "mejor_resultado.json", best_result)
    save_json(output_dir / "mejor_ruta_expandida.json", expanded_tour)
    summary = {
        "metodo_ganador": best_method,
        "mejor_costo_tour": best_result["mejor_costo_tour"],
        "n_ciudades": len(best_result["mejor_tour_indices"]) - 1,
        "n_saltos_reales": expanded_tour["n_saltos_reales"],
        "formula_peso": best_result["formula_peso"],
    }
    save_json(output_dir / "resumen_web.json", summary)
    return {
        "comparison_path": output_dir / "comparacion_metodos.json",
        "best_result_path": output_dir / "mejor_resultado.json",
        "expanded_route_path": output_dir / "mejor_ruta_expandida.json",
        "web_summary_path": output_dir / "resumen_web.json",
        "web_summary": summary,
    }
