# `web_scrapping.js`

Este archivo automatiza en el navegador la consulta de rutas entre ciudades y exporta los resultados a un CSV.

## Qué hace

- Usa la lista `ciudades` como referencia de nombres.
- Lee pares de índices desde `csvTexto`.
- Busca los inputs de origen y destino en la página.
- Escribe cada ciudad y selecciona la sugerencia correspondiente.
- Espera a que la página calcule la ruta.
- Extrae desde el texto visible la distancia, el tiempo de conducción y el peaje estimado.
- Genera y descarga `resultados_vinci_indices.csv`.

## Funciones principales

- `obtenerInputs()`: encuentra los campos de origen y destino.
- `escribirYSeleccionar()`: escribe la ciudad y simula teclas para seleccionar una opción.
- `leerParesDesdeTextoCSV()`: convierte el texto de pares en una lista de rutas.
- `extraerDatosRuta()`: lee la página y extrae los datos de la ruta.
- `convertirResultadosACSVConIndices()`: arma el contenido del CSV final.
- `ejecutarRutasDesdeVariableCSV()`: ejecuta todo el flujo para todas las rutas.

## Salida

El CSV final contiene las columnas:

- `origen_indice`
- `destino_indice`
- `origen`
- `destino`
- `de_voyage`
- `de_conduite`
- `estimation_peage`
- `estado`
