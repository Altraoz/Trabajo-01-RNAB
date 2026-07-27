# Estructura general del proyecto

Este documento resume la organizacion del proyecto segun la estructura visible en el repositorio. Dentro se concentran los desarrollos de optimizacion numerica, optimizacion combinatoria y la construccion del blog final en Quarto.

## Blog desplegado

El blog final desplegado del proyecto puede consultarse aqui:

[https://altraoz.github.io/Trabajo-01-RNAB/](https://altraoz.github.io/Trabajo-01-RNAB/)

## Estructura principal

- `1. optimizacion_numerica/`
  Reune todo lo relacionado con la solucion del bloque de optimizacion numerica del enunciado.

  Incluye:
  - `gradiente/`: notebooks, funciones y datos para descenso por gradiente.
  - `heuristicos/`: implementaciones y resultados de algoritmo evolutivo, PSO y evolucion diferencial.
  - notebooks de integracion o comparacion final, como la comparacion entre metodos y animaciones.

- `2. optimizacion_combinatoria/`
  Reune el desarrollo asociado al bloque de optimizacion combinatoria del enunciado.

  Incluye:
  - `src/`: funciones principales del modelo y algoritmos.
  - `scripts/`: scripts auxiliares de ejecucion, postproceso y construccion de salidas.
  - `outputs/`: resultados generados, incluyendo archivos para visualizacion y datos web.

- `blog/`
  Contiene el sitio en Quarto usado para presentar la entrega final del proyecto.

  Incluye:
  - `numerica.qmd`: pagina de optimizacion numerica.
  - `combinatoria.qmd`: pagina de optimizacion combinatoria.
  - `comparacion_final_numerica.qmd`: apoyo para consolidar la comparacion final.
  - `notebooks/`: notebooks conectados con las secciones del blog.
  - `assets/`: imagenes, gifs y figuras usadas en la publicacion.
  - `_quarto.yml`: configuracion general del sitio.

- `presentacion/`
  Guarda notebooks o materiales preparados para la version de presentacion del proyecto.

## Logica general del flujo

La organizacion del proyecto sigue esta logica:

1. En `1. optimizacion_numerica/` y `2. optimizacion_combinatoria/` se desarrolla el codigo base, se ejecutan experimentos y se generan resultados para cada parte del enunciado.
2. Esos resultados se transforman en tablas, figuras, gifs o resumenes.
3. Luego, en `blog/`, se integran esos productos en las paginas `.qmd` para construir la version final publicada.

## Recomendacion de lectura

Si alguien quiere entender rapido el proyecto, el orden mas natural es:

1. Entrar al blog desplegado del proyecto.
2. Revisar dentro de `blog/` los archivos `numerica.qmd` y `combinatoria.qmd`.
3. Si se necesita mas detalle tecnico, bajar a las carpetas `1. optimizacion_numerica/` y `2. optimizacion_combinatoria/`.
