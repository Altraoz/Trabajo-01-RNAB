"""
Paso 9: generar GIF de la mejor solucion combinatoria final.

Usa la mejor solucion disponible entre ACO y GA y construye un GIF donde la ruta
se va trazando progresivamente sobre un mapa simplificado de las capitales.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from PIL import Image, ImageDraw, ImageFont
import numpy as np

from src.core_grafo import load_json, save_json
from src.core_paths import BASE_DIR, PHASE7_DIR, PHASE8_DIR, PHASE9_DIR
from src.core_visualizacion import CITY_COORDS


ACO_RESULT_PATH = PHASE7_DIR / "resultado_aco_final.json"
GA_RESULT_PATH = PHASE8_DIR / "resultado_ga_final.json"
OUTPUT_DIR = PHASE9_DIR


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

def pick_best_result() -> tuple[str, dict]:
    aco = load_json(ACO_RESULT_PATH)
    ga = load_json(GA_RESULT_PATH)
    if ga["mejor_costo_tour"] <= aco["mejor_costo_tour"]:
        return "GA", ga
    return "ACO", aco


def project_points(coords: np.ndarray) -> np.ndarray:
    lats = coords[:, 0]
    lons = coords[:, 1]
    min_lon, max_lon = float(lons.min()), float(lons.max())
    min_lat, max_lat = float(lats.min()), float(lats.max())
    x = PADDING + (lons - min_lon) / (max_lon - min_lon) * (WIDTH - 2 * PADDING)
    y = HEIGHT - PADDING - (lats - min_lat) / (max_lat - min_lat) * (HEIGHT - 2 * PADDING)
    return np.column_stack([x, y])


def load_font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.truetype("arial.ttf", size=size)
    except OSError:
        return ImageFont.load_default()


def build_base_frame(title: str, subtitle: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    title_font = load_font(28)
    subtitle_font = load_font(16)

    draw.text((WIDTH // 2, 24), title, fill=TEXT_COLOR, font=title_font, anchor="ma")
    draw.text((WIDTH // 2, 58), subtitle, fill=SUBTEXT_COLOR, font=subtitle_font, anchor="ma")
    return image, draw


def draw_cities(draw: ImageDraw.ImageDraw, projected_all: np.ndarray) -> None:
    for x, y in projected_all:
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=CITY_COLOR)


def draw_route(
    draw: ImageDraw.ImageDraw,
    projected_route: np.ndarray,
    step: int,
) -> None:
    visible = projected_route[: step + 1]
    points = [tuple(map(float, point)) for point in visible]
    if len(points) >= 2:
        draw.line(points, fill=ROUTE_COLOR, width=4, joint="curve")

    start_x, start_y = points[0]
    draw.ellipse((start_x - 8, start_y - 8, start_x + 8, start_y + 8), fill=START_COLOR)

    current_x, current_y = points[-1]
    draw.ellipse((current_x - 7, current_y - 7, current_x + 7, current_y + 7), fill=END_COLOR)


def add_annotations(
    draw: ImageDraw.ImageDraw,
    method_name: str,
    result: dict,
    total_steps: int,
    current_step: int,
) -> None:
    info_font = load_font(16)
    cost_text = f"Costo: {result['mejor_costo_tour']:.2f} EUR"
    method_text = f"Mejor metodo: {method_name}"
    progress_text = f"Tramo {current_step}/{total_steps - 1}"
    formula_text = result["formula_peso"]

    draw.rounded_rectangle((30, HEIGHT - 145, WIDTH - 30, HEIGHT - 25), radius=16, fill="#fffdf8", outline="#d6d0c4")
    draw.text((48, HEIGHT - 130), method_text, fill=TEXT_COLOR, font=info_font)
    draw.text((48, HEIGHT - 104), cost_text, fill=TEXT_COLOR, font=info_font)
    draw.text((48, HEIGHT - 78), progress_text, fill=TEXT_COLOR, font=info_font)
    draw.text((48, HEIGHT - 52), formula_text, fill=SUBTEXT_COLOR, font=info_font)


def generate_frames(method_name: str, result: dict) -> list[Image.Image]:
    route_indices = result["mejor_tour_indices"]
    route_coords = CITY_COORDS[np.array(route_indices)]
    projected_all = project_points(CITY_COORDS)
    projected_route = project_points(route_coords)
    total_steps = len(route_indices)

    title = "Mejor solucion combinatoria final"
    subtitle = "Recorrido progresivo sobre las 96 capitales de Francia"

    frames: list[Image.Image] = []
    for step in range(1, total_steps):
        image, draw = build_base_frame(title, subtitle)
        draw_cities(draw, projected_all)
        draw_route(draw, projected_route, step)
        add_annotations(draw, method_name, result, total_steps, step)
        frames.append(image)

    frames.extend([frames[-1].copy() for _ in range(8)])
    return frames


def main() -> None:
    method_name, result = pick_best_result()
    frames = generate_frames(method_name, result)

    OUTPUT_DIR.mkdir(exist_ok=True)
    gif_path = OUTPUT_DIR / "mejor_solucion_combinatoria.gif"
    summary_path = OUTPUT_DIR / "resumen_gif_final.json"

    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=140,
        loop=0,
        optimize=False,
    )

    summary = {
        "metodo_ganador": method_name,
        "mejor_costo_tour": result["mejor_costo_tour"],
        "frames": len(frames),
        "archivo_gif": str(gif_path),
        "formula_peso": result["formula_peso"],
    }
    save_json(summary_path, summary)

    print("Paso 9 completado.")
    print(f"Metodo visualizado: {method_name}")
    print(f"GIF generado en: {gif_path}")


if __name__ == "__main__":
    main()
