from __future__ import annotations

import csv
import html
import json
from pathlib import Path

import numpy as np


CITY_COORDS = np.array([
    [46.2052, 5.2255], [49.5639, 3.6244], [46.5667, 3.3333], [44.0920, 6.2356],
    [44.5596, 6.0790], [43.7102, 7.2620], [44.7353, 4.5997], [49.7621, 4.7261],
    [42.9653, 1.6073], [48.2973, 4.0744], [43.2130, 2.3491], [44.3500, 2.5750],
    [43.2965, 5.3698], [49.1829, -0.3707], [44.9260, 2.4397], [45.6484, 0.1562],
    [46.1603, -1.1511], [47.0810, 2.3988], [45.2678, 1.7707], [41.9192, 8.7386],
    [42.6973, 9.4509], [47.3220, 5.0415], [48.5142, -2.7658], [46.1694, 1.8714],
    [45.1840, 0.7211], [47.2378, 6.0241], [44.9334, 4.8924], [49.0270, 1.1514],
    [48.4439, 1.4890], [47.9960, -4.1025], [43.8367, 4.3601], [43.6047, 1.4442],
    [43.6467, 0.5851], [44.8378, -0.5792], [43.6119, 3.8772], [48.1173, -1.6778],
    [46.8114, 1.6868], [47.3941, 0.6848], [45.1885, 5.7245], [46.6753, 5.5557],
    [43.8911, -0.5007], [47.5861, 1.3359], [45.4397, 4.3872], [45.0439, 3.8857],
    [47.2184, -1.5536], [47.9029, 1.9093], [44.4479, 1.4412], [44.2049, 0.6212],
    [44.5180, 3.5010], [47.4784, -0.5632], [49.1157, -1.0907], [48.9567, 4.3631],
    [48.1117, 5.1396], [48.0707, -0.7734], [48.6921, 6.1844], [48.7728, 5.1611],
    [47.6582, -2.7608], [49.1193, 6.1757], [46.9896, 3.1590], [50.6292, 3.0573],
    [49.4300, 2.0800], [48.4329, 0.0913], [50.2910, 2.7775], [45.7772, 3.0870],
    [43.2951, -0.3708], [43.2329, 0.0781], [42.6887, 2.8948], [48.5734, 7.7521],
    [48.0794, 7.3585], [45.7640, 4.8357], [47.6236, 6.1552], [46.3069, 4.8317],
    [48.0061, 0.1996], [45.5646, 5.9178], [45.8992, 6.1294], [48.8566, 2.3522],
    [49.4431, 1.0993], [48.5390, 2.6608], [48.8049, 2.1204], [46.3237, -0.4648],
    [49.8941, 2.2958], [43.9298, 2.1480], [44.0221, 1.3520], [43.1242, 5.9280],
    [43.9493, 4.8055], [46.6705, -1.4260], [46.5802, 0.3404], [45.8336, 1.2611],
    [48.1744, 6.4500], [47.7982, 3.5738], [47.6397, 6.8638], [48.6238, 2.4290],
    [48.8924, 2.2153], [48.9086, 2.4397], [48.7904, 2.4556], [49.0365, 2.0761],
], dtype=float)


def load_city_names(path: Path) -> list[str]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        return next(reader)[1:]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _project_points(coords: np.ndarray, width: int, height: int, padding: int) -> np.ndarray:
    lats = coords[:, 0]
    lons = coords[:, 1]
    min_lon, max_lon = float(lons.min()), float(lons.max())
    min_lat, max_lat = float(lats.min()), float(lats.max())
    x = padding + (lons - min_lon) / (max_lon - min_lon) * (width - 2 * padding)
    y = height - padding - (lats - min_lat) / (max_lat - min_lat) * (height - 2 * padding)
    return np.column_stack([x, y])


def create_route_svg(
    route_indices: list[int],
    city_names: list[str],
    title: str = "Tour final sobre Francia",
    width: int = 900,
    height: int = 1100,
    padding: int = 60,
) -> str:
    projected_all = _project_points(CITY_COORDS, width, height, padding)
    projected_route = _project_points(CITY_COORDS[np.array(route_indices)], width, height, padding)
    polyline_points = " ".join(f"{x:.1f},{y:.1f}" for x, y in projected_route)
    circles = [
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="#1f3c88" fill-opacity="0.65" />'
        for x, y in projected_all
    ]
    route_nodes: list[str] = []
    sample_positions = np.linspace(0, len(route_indices) - 2, 12, dtype=int)
    for pos in sample_positions:
        x, y = projected_route[pos]
        route_nodes.append(f'<text x="{x + 7:.1f}" y="{y - 7:.1f}" font-size="12" fill="#333">{pos + 1}</text>')
        route_nodes.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="#d1495b" />')
    start_x, start_y = projected_route[0]
    end_x, end_y = projected_route[-2]
    start_name = html.escape(city_names[route_indices[0]])
    end_name = html.escape(city_names[route_indices[-2]])
    title_text = html.escape(title)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#f7f4ea"/>
  <text x="{width/2:.1f}" y="32" text-anchor="middle" font-size="26" font-family="Arial, sans-serif" fill="#222">{title_text}</text>
  <text x="{width/2:.1f}" y="56" text-anchor="middle" font-size="13" font-family="Arial, sans-serif" fill="#555">Longitud vs latitud de las 96 capitales departamentales</text>
  <polyline points="{polyline_points}" fill="none" stroke="#d1495b" stroke-width="3.5" stroke-opacity="0.85"/>
  {''.join(circles)}
  {''.join(route_nodes)}
  <circle cx="{start_x:.1f}" cy="{start_y:.1f}" r="8" fill="#2a9d8f"/>
  <circle cx="{end_x:.1f}" cy="{end_y:.1f}" r="8" fill="#e76f51"/>
  <text x="{start_x + 12:.1f}" y="{start_y + 4:.1f}" font-size="13" fill="#222">Inicio: {start_name}</text>
  <text x="{end_x + 12:.1f}" y="{end_y + 4:.1f}" font-size="13" fill="#222">Ultima ciudad: {end_name}</text>
</svg>"""


def create_history_svg(
    history: list[float],
    title: str = "Convergencia",
    width: int = 900,
    height: int = 260,
    padding: int = 40,
) -> str:
    values = np.array(history, dtype=float)
    min_v, max_v = float(values.min()), float(values.max())
    xs = np.linspace(padding, width - padding, len(values))
    ys = np.full_like(xs, height / 2) if max_v == min_v else height - padding - (values - min_v) / (max_v - min_v) * (height - 2 * padding)
    points = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fffdf8"/>
  <text x="{width/2:.1f}" y="26" text-anchor="middle" font-size="22" font-family="Arial, sans-serif" fill="#222">{html.escape(title)}</text>
  <line x1="{padding}" y1="{height-padding}" x2="{width-padding}" y2="{height-padding}" stroke="#999" />
  <line x1="{padding}" y1="{padding}" x2="{padding}" y2="{height-padding}" stroke="#999" />
  <polyline points="{points}" fill="none" stroke="#d1495b" stroke-width="3"/>
  <text x="{padding}" y="{padding - 8}" font-size="12" fill="#555">Mejor: {values.min():.2f}</text>
  <text x="{width - padding - 120}" y="{padding - 8}" font-size="12" fill="#555">Inicial: {values[0]:.2f}</text>
</svg>"""


def save_svg(svg_text: str, output_path: Path) -> Path:
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(svg_text, encoding="utf-8")
    return output_path
