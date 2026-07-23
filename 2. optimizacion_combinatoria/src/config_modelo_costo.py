"""
Configuracion central del modelo de costo para optimizacion combinatoria.

Se adopta un modelo alineado con el enunciado:

    costo_total = peajes(euros) + gasolina(euros) + tiempo_horas * tarifa_vendedor

Notas:
- El SMIC es nacional en Francia, asi que no se usa un valor distinto para Paris.
- El dataset ya trae la columna ``gasolina(euros)``, por lo que ese componente
  se reutiliza directamente como costo de combustible por tramo.
- Se deja documentado un vehiculo de referencia para justificar el supuesto del
  recorrido en carro del vendedor.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class VehicleSpec:
    name: str
    fuel_type: str
    segment: str
    note: str


VEHICLE = VehicleSpec(
    name="Renault Clio",
    fuel_type="gasolina",
    segment="compacto",
    note=(
        "Vehiculo de referencia para justificar el recorrido. "
        "El componente de combustible se toma desde la columna gasolina(euros) del dataset."
    ),
)

SMIC_HOURLY_EUR_2026 = 12.02


def seller_cost_from_minutes(time_min: float, hourly_rate_eur: float = SMIC_HOURLY_EUR_2026) -> float:
    return (time_min / 60.0) * hourly_rate_eur


def edge_total_cost(
    toll_eur: float,
    fuel_eur: float,
    time_min: float,
    hourly_rate_eur: float = SMIC_HOURLY_EUR_2026,
) -> float:
    return toll_eur + fuel_eur + seller_cost_from_minutes(time_min, hourly_rate_eur)


def cost_formula_label(hourly_rate_eur: float = SMIC_HOURLY_EUR_2026) -> str:
    return (
        "peajes(euros) + gasolina(euros) + "
        f"(tiempo(min)/60) * {hourly_rate_eur:.2f}"
    )


def model_metadata(hourly_rate_eur: float = SMIC_HOURLY_EUR_2026) -> dict:
    return {
        "vehiculo_referencia": asdict(VEHICLE),
        "tarifa_vendedor_eur_h": hourly_rate_eur,
        "salario_referencia": "SMIC Francia 2026",
        "formula_peso": cost_formula_label(hourly_rate_eur),
    }
