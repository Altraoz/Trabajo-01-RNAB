# Nota sobre este archivo

Este archivo se conserva solo como apunte de trabajo preliminar.

No debe usarse como referencia final para la entrega ni para el reporte tecnico, porque ya no refleja el estado real del proyecto.

El documento vigente para organizar la redaccion de la parte 1 es:

- `reporte_estructura.md`

Sobre las dimensiones trabajadas:

- `Rosenbrock`, `Rastrigin`, `Schwefel` y `Griewank` se evaluan en 2D y 3D porque en este proyecto se usan sus formas generalizadas.
- `Goldstein-Price` y `Six-Hump Camel` se reportan solo en 2D porque en el proyecto se implementaron en su forma clasica bidimensional, tanto en la funcion objetivo como en su gradiente.

Esta decision no corresponde a una omision experimental sino a una restriccion metodologica coherente con las definiciones implementadas en:

- `funciones_objetivo.py`
- `funciones_gradientes.py`

Si se necesita una justificacion formal para el reporte, debe tomarse de `reporte_estructura.md`.
