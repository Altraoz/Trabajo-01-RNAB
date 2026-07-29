from __future__ import annotations

import csv
import html
import json
import math
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


def _project_single(lat: float, lon: float, width: int, height: int, padding: int) -> tuple[float, float]:
    lats = CITY_COORDS[:, 0]
    lons = CITY_COORDS[:, 1]
    min_lon, max_lon = float(lons.min()), float(lons.max())
    min_lat, max_lat = float(lats.min()), float(lats.max())
    x = padding + (lon - min_lon) / (max_lon - min_lon) * (width - 2 * padding)
    y = height - padding - (lat - min_lat) / (max_lat - min_lat) * (height - 2 * padding)
    return float(x), float(y)


def _cross(origin: tuple[float, float], a: tuple[float, float], b: tuple[float, float]) -> float:
    return (a[0] - origin[0]) * (b[1] - origin[1]) - (a[1] - origin[1]) * (b[0] - origin[0])


def _convex_hull(points: np.ndarray) -> np.ndarray:
    unique_points = np.unique(points.astype(float), axis=0)
    if len(unique_points) <= 1:
        return unique_points

    sorted_points = unique_points[np.lexsort((unique_points[:, 1], unique_points[:, 0]))]
    lower: list[tuple[float, float]] = []
    upper: list[tuple[float, float]] = []

    for point in sorted_points:
        current = (float(point[0]), float(point[1]))
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], current) <= 0:
            lower.pop()
        lower.append(current)

    for point in reversed(sorted_points):
        current = (float(point[0]), float(point[1]))
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], current) <= 0:
            upper.pop()
        upper.append(current)

    return np.array(lower[:-1] + upper[:-1], dtype=float)


def _points_to_svg(points: np.ndarray) -> str:
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def _build_corsica_blob(points: np.ndarray, padding: float = 16.0) -> np.ndarray:
    min_x, min_y = points.min(axis=0)
    max_x, max_y = points.max(axis=0)
    return np.array(
        [
            [min_x - padding, min_y - padding],
            [max_x + padding, min_y - padding / 2],
            [max_x + padding * 0.8, max_y + padding],
            [min_x - padding * 0.7, max_y + padding / 1.5],
        ],
        dtype=float,
    )


def create_route_map_svg(
    route_indices: list[int],
    city_names: dict[int, str],
    title: str = "Mejor ruta sobre Francia",
    width: int = 980,
    height: int = 1180,
    padding: int = 70,
) -> str:
    projected_all = _project_points(CITY_COORDS, width, height, padding)
    projected_route = _project_points(CITY_COORDS[np.array(route_indices)], width, height, padding)
    corsica_mask = CITY_COORDS[:, 1] > 8.0
    mainland_hull = _convex_hull(projected_all[~corsica_mask])
    corsica_blob = _build_corsica_blob(projected_all[corsica_mask])
    route_polyline = _points_to_svg(projected_route)
    mainland_polygon = _points_to_svg(mainland_hull)
    corsica_polygon = _points_to_svg(corsica_blob)
    last_city_index = route_indices[-2] if len(route_indices) >= 2 and route_indices[-1] == route_indices[0] else route_indices[-1]
    start_name = html.escape(city_names[route_indices[0]])
    end_name = html.escape(city_names[last_city_index])
    subtitle = "Ruta expandida sobre un mapa estilizado de Francia a partir de coordenadas geograficas reales"

    min_lat, max_lat = float(CITY_COORDS[:, 0].min()), float(CITY_COORDS[:, 0].max())
    min_lon, max_lon = float(CITY_COORDS[:, 1].min()), float(CITY_COORDS[:, 1].max())
    grid_latitudes = range(math.ceil(min_lat), math.floor(max_lat) + 1)
    grid_longitudes = range(math.ceil(min_lon / 2) * 2, math.floor(max_lon / 2) * 2 + 1, 2)
    grid_lines: list[str] = []

    for lat in grid_latitudes:
        x1, y = _project_single(float(lat), float(CITY_COORDS[:, 1].min()), width, height, padding)
        x2, _ = _project_single(float(lat), float(CITY_COORDS[:, 1].max()), width, height, padding)
        grid_lines.append(
            f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" '
            'stroke="#d8dee9" stroke-width="1" stroke-dasharray="4 6"/>'
        )
        grid_lines.append(
            f'<text x="{padding - 12:.1f}" y="{y + 4:.1f}" text-anchor="end" font-size="11" fill="#758196">{lat}N</text>'
        )

    for lon in grid_longitudes:
        x, y1 = _project_single(float(CITY_COORDS[:, 0].min()), float(lon), width, height, padding)
        _, y2 = _project_single(float(CITY_COORDS[:, 0].max()), float(lon), width, height, padding)
        grid_lines.append(
            f'<line x1="{x:.1f}" y1="{y1:.1f}" x2="{x:.1f}" y2="{y2:.1f}" '
            'stroke="#d8dee9" stroke-width="1" stroke-dasharray="4 6"/>'
        )
        grid_lines.append(
            f'<text x="{x:.1f}" y="{height - padding + 20:.1f}" text-anchor="middle" font-size="11" fill="#758196">{lon}</text>'
        )

    all_cities_svg = [
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.1" fill="#315a8a" fill-opacity="0.75" />'
        for x, y in projected_all
    ]
    route_markers_svg: list[str] = []
    sample_positions = np.linspace(0, len(projected_route) - 2, min(12, len(projected_route) - 1), dtype=int)
    for sample_number, position in enumerate(sample_positions, start=1):
        x, y = projected_route[position]
        route_markers_svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.3" fill="#d1495b" fill-opacity="0.95" />')
        route_markers_svg.append(
            f'<text x="{x + 8:.1f}" y="{y - 8:.1f}" font-size="11.5" fill="#3b3b3b">{sample_number}</text>'
        )

    start_x, start_y = projected_route[0]
    end_x, end_y = projected_route[-2] if len(projected_route) >= 2 and route_indices[-1] == route_indices[0] else projected_route[-1]

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#f6f8fb"/>
  <rect x="24" y="92" width="{width - 48}" height="{height - 186}" rx="24" fill="#edf4fb"/>
  <polygon points="{mainland_polygon}" fill="#e7f0d8" stroke="#9eb68a" stroke-width="2.4"/>
  <polygon points="{corsica_polygon}" fill="#e7f0d8" stroke="#9eb68a" stroke-width="2.0"/>
  {''.join(grid_lines)}
  <text x="{width/2:.1f}" y="38" text-anchor="middle" font-size="28" font-family="Arial, sans-serif" fill="#1f2933">{html.escape(title)}</text>
  <text x="{width/2:.1f}" y="64" text-anchor="middle" font-size="13" font-family="Arial, sans-serif" fill="#52606d">{html.escape(subtitle)}</text>
  {''.join(all_cities_svg)}
  <polyline points="{route_polyline}" fill="none" stroke="#d1495b" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round" stroke-opacity="0.92"/>
  {''.join(route_markers_svg)}
  <circle cx="{start_x:.1f}" cy="{start_y:.1f}" r="9" fill="#2a9d8f" stroke="#ffffff" stroke-width="2.5"/>
  <circle cx="{end_x:.1f}" cy="{end_y:.1f}" r="9" fill="#f4a261" stroke="#ffffff" stroke-width="2.5"/>
  <rect x="34" y="{height - 164}" width="{width - 68}" height="122" rx="18" fill="#fffdf9" stroke="#d7dde5"/>
  <line x1="58" y1="{height - 126}" x2="128" y2="{height - 126}" stroke="#d1495b" stroke-width="4"/>
  <circle cx="74" cy="{height - 96}" r="7" fill="#2a9d8f"/>
  <circle cx="74" cy="{height - 68}" r="7" fill="#f4a261"/>
  <text x="142" y="{height - 121}" font-size="13" fill="#243b53">Recorrido expandido reconstruido sobre el grafo real</text>
  <text x="88" y="{height - 92}" font-size="13" fill="#243b53">Inicio y cierre: {start_name}</text>
  <text x="88" y="{height - 64}" font-size="13" fill="#243b53">Ultima ciudad antes del cierre: {end_name}</text>
  <text x="{width - 54:.1f}" y="{height - 92}" text-anchor="end" font-size="12.5" fill="#52606d">Capitales mostradas: {len(projected_all)}</text>
  <text x="{width - 54:.1f}" y="{height - 64}" text-anchor="end" font-size="12.5" fill="#52606d">Saltos del recorrido trazado: {max(len(route_indices) - 1, 0)}</text>
</svg>"""


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


def _build_route_map_payload(
    route_indices: list[int],
    city_names: dict[int, str],
) -> tuple[np.ndarray, list[dict], list[dict], dict]:
    route_coords = CITY_COORDS[np.array(route_indices)]
    all_cities = [
        {
            "index": index,
            "name": city_names[index],
            "lat": float(lat),
            "lon": float(lon),
        }
        for index, (lat, lon) in enumerate(CITY_COORDS)
    ]
    route_points = [
        {
            "order": order + 1,
            "index": int(index),
            "name": city_names[int(index)],
            "lat": float(lat),
            "lon": float(lon),
        }
        for order, (index, (lat, lon)) in enumerate(zip(route_indices, route_coords))
    ]
    last_city = route_points[-2] if len(route_points) >= 2 and route_points[-1]["index"] == route_points[0]["index"] else route_points[-1]
    return route_coords, all_cities, route_points, last_city


def _create_route_map_html_with_folium(
    route_indices: list[int],
    city_names: dict[int, str],
    title: str = "Mejor ruta sobre Francia",
    method_name: str | None = None,
    total_cost: float | None = None,
) -> str:
    import folium

    route_coords, all_cities, route_points, last_city = _build_route_map_payload(route_indices, city_names)
    route_locations = [[float(lat), float(lon)] for lat, lon in route_coords]
    summary_lines = [
        html.escape(title),
        f"Metodo ganador: {html.escape(method_name)}" if method_name else None,
        f"Costo total: {total_cost:.2f} EUR" if total_cost is not None else None,
        f"Saltos trazados: {max(len(route_indices) - 1, 0)}",
    ]
    summary_html = "<br/>".join(line for line in summary_lines if line is not None)

    mapa = folium.Map(
        location=[float(route_coords[:, 0].mean()), float(route_coords[:, 1].mean())],
        zoom_start=6,
        tiles=None,
        control_scale=True,
    )
    folium.TileLayer("OpenStreetMap", name="OpenStreetMap").add_to(mapa)
    folium.TileLayer("CartoDB positron", name="CartoDB Positron").add_to(mapa)

    for city in all_cities:
        folium.CircleMarker(
            location=[city["lat"], city["lon"]],
            radius=3,
            color="#315a8a",
            weight=1,
            fill=True,
            fill_color="#315a8a",
            fill_opacity=0.55,
            tooltip=f'{city["index"]} - {html.escape(city["name"])}',
        ).add_to(mapa)

    folium.PolyLine(
        locations=route_locations,
        weight=4,
        color="#d1495b",
        opacity=0.9,
        tooltip=f"Recorrido expandido del metodo {method_name}" if method_name else "Recorrido expandido",
    ).add_to(mapa)

    sample_count = min(12, max(len(route_points) - 1, 1))
    sample_limit = len(route_points) - 2 if len(route_points) >= 2 and route_points[-1]["index"] == route_points[0]["index"] else len(route_points) - 1
    sample_positions = np.linspace(0, max(sample_limit, 0), sample_count, dtype=int)
    for sample_number, position in enumerate(sample_positions, start=1):
        point = route_points[int(position)]
        folium.Marker(
            location=[point["lat"], point["lon"]],
            icon=folium.DivIcon(
                html=(
                    '<div style="font-family: Arial, sans-serif; font-size: 11px; '
                    'color: #243b53; font-weight: 700;">'
                    f"{sample_number}</div>"
                )
            ),
        ).add_to(mapa)

    folium.CircleMarker(
        location=[route_points[0]["lat"], route_points[0]["lon"]],
        radius=8,
        color="#ffffff",
        weight=2,
        fill=True,
        fill_color="#2a9d8f",
        fill_opacity=1,
        popup=f'Inicio y cierre: {html.escape(route_points[0]["name"])}',
    ).add_to(mapa)

    folium.CircleMarker(
        location=[last_city["lat"], last_city["lon"]],
        radius=8,
        color="#ffffff",
        weight=2,
        fill=True,
        fill_color="#f4a261",
        fill_opacity=1,
        popup=f'Ultima ciudad antes del cierre: {html.escape(last_city["name"])}',
    ).add_to(mapa)

    folium.LayerControl(collapsed=False).add_to(mapa)
    mapa.fit_bounds(route_locations)

    overlay_html = f"""
    <div style="
      position: fixed;
      top: 14px;
      left: 50px;
      z-index: 9999;
      background: rgba(255, 255, 255, 0.93);
      border: 1px solid #cbd5e1;
      border-radius: 12px;
      box-shadow: 0 10px 28px rgba(15, 23, 42, 0.14);
      padding: 10px 12px;
      font-family: Arial, sans-serif;
      color: #1f2933;
      line-height: 1.4;
      max-width: 360px;
    ">
      <div style="font-size: 20px; font-weight: 700; margin-bottom: 4px;">{html.escape(title)}</div>
      <div style="font-size: 13px; color: #52606d;">{summary_html}</div>
    </div>
    """
    mapa.get_root().html.add_child(folium.Element(overlay_html))
    return mapa.get_root().render()


def _create_route_map_html_fallback(
    route_indices: list[int],
    city_names: dict[int, str],
    title: str = "Mejor ruta sobre Francia",
    method_name: str | None = None,
    total_cost: float | None = None,
) -> str:
    _, all_cities, route_points, last_city = _build_route_map_payload(route_indices, city_names)
    info_lines = [
        title,
        f"Metodo ganador: {method_name}" if method_name else None,
        f"Costo total: {total_cost:.2f} EUR" if total_cost is not None else None,
        f"Saltos trazados: {max(len(route_indices) - 1, 0)}",
    ]
    info_lines = [line for line in info_lines if line is not None]
    info_html = "<br/>".join(html.escape(line) for line in info_lines)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css"/>
  <style>
    body {{
      margin: 0;
      font-family: Arial, sans-serif;
      background: #f6f8fb;
      color: #1f2933;
    }}
    .frame {{
      max-width: 1080px;
      margin: 0 auto;
      padding: 18px 18px 24px;
    }}
    h1 {{
      margin: 0 0 6px;
      font-size: 28px;
    }}
    p {{
      margin: 0 0 14px;
      color: #52606d;
      font-size: 14px;
    }}
    #map {{
      height: 760px;
      border-radius: 18px;
      box-shadow: 0 10px 32px rgba(15, 23, 42, 0.12);
      overflow: hidden;
    }}
    .info-card {{
      background: rgba(255, 255, 255, 0.95);
      border: 1px solid rgba(148, 163, 184, 0.55);
      border-radius: 12px;
      box-shadow: 0 10px 28px rgba(15, 23, 42, 0.12);
      padding: 10px 12px;
      line-height: 1.45;
    }}
  </style>
</head>
<body>
  <div class="frame">
    <h1>{html.escape(title)}</h1>
    <p>Vista interactiva de la ruta expandida sobre un mapa base. Esta version sirve para inspeccion visual y captura para el reporte.</p>
    <div id="map"></div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>
    const routePoints = {json.dumps(route_points, ensure_ascii=False)};
    const allCities = {json.dumps(all_cities, ensure_ascii=False)};
    const lastCity = {json.dumps(last_city, ensure_ascii=False)};
    const infoHtml = {json.dumps(info_html, ensure_ascii=False)};

    const map = L.map('map', {{
      zoomControl: true,
      scrollWheelZoom: true
    }});

    L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
      attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
      maxZoom: 18
    }}).addTo(map);

    allCities.forEach((city) => {{
      L.circleMarker([city.lat, city.lon], {{
        radius: 3,
        color: '#315a8a',
        weight: 1,
        fillColor: '#315a8a',
        fillOpacity: 0.55
      }}).bindTooltip(`${{city.index}} - ${{city.name}}`, {{sticky: true}}).addTo(map);
    }});

    const routeLine = L.polyline(
      routePoints.map((point) => [point.lat, point.lon]),
      {{
        color: '#d1495b',
        weight: 4,
        opacity: 0.9
      }}
    ).addTo(map);

    L.circleMarker([routePoints[0].lat, routePoints[0].lon], {{
      radius: 8,
      color: '#ffffff',
      weight: 2,
      fillColor: '#2a9d8f',
      fillOpacity: 1
    }}).bindPopup(`Inicio y cierre: ${{routePoints[0].name}}`).addTo(map);

    L.circleMarker([lastCity.lat, lastCity.lon], {{
      radius: 8,
      color: '#ffffff',
      weight: 2,
      fillColor: '#f4a261',
      fillOpacity: 1
    }}).bindPopup(`Ultima ciudad antes del cierre: ${{lastCity.name}}`).addTo(map);

    L.control.scale({{metric: true, imperial: false}}).addTo(map);

    const infoControl = L.control({{position: 'topright'}});
    infoControl.onAdd = function() {{
      const div = L.DomUtil.create('div', 'info-card');
      div.innerHTML = infoHtml;
      return div;
    }};
    infoControl.addTo(map);

    map.fitBounds(routeLine.getBounds(), {{padding: [28, 28]}});
  </script>
</body>
</html>"""


def create_route_map_html(
    route_indices: list[int],
    city_names: dict[int, str],
    title: str = "Mejor ruta sobre Francia",
    method_name: str | None = None,
    total_cost: float | None = None,
) -> str:
    try:
        return _create_route_map_html_with_folium(
            route_indices,
            city_names,
            title=title,
            method_name=method_name,
            total_cost=total_cost,
        )
    except ImportError:
        return _create_route_map_html_fallback(
            route_indices,
            city_names,
            title=title,
            method_name=method_name,
            total_cost=total_cost,
        )


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


def save_html(html_text: str, output_path: Path) -> Path:
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(html_text, encoding="utf-8")
    return output_path
