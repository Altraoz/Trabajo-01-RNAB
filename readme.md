# Trabajo 1 - RNA y Algoritmos Bioinspirados

Repositorio del Trabajo 1 del curso RNA y Algoritmos Bioinspirados. El proyecto integra dos bloques principales:

- optimizacion numerica sobre funciones de prueba
- optimizacion combinatoria aplicada al problema del agente viajero

Ademas, incluye un sitio en Quarto con la presentacion final de resultados.

## Sitio publicado

La version publicada del proyecto puede consultarse aqui:

[https://altraoz.github.io/Trabajo-01-RNAB/](https://altraoz.github.io/Trabajo-01-RNAB/)

## Estructura del proyecto

```text
Trabajo-01-RNAB/
|-- 1. optimizacion_numerica/
|   |-- gradiente/
|   |-- heuristicos/
|   |-- 12_comparacion_final_metodos.ipynb
|   |-- animacion_de_rastrigin_2d.ipynb
|   `-- reporte_estructura.md
|-- 2. optimizacion_combinatoria/
|   |-- data/
|   |-- docs/
|   |-- entrega_final/
|   |-- notebooks/
|   |-- outputs/
|   |-- scripts/
|   `-- src/
|-- blog/
|   |-- assets/
|   |-- docs/
|   |-- notebooks/
|   |-- presentacion/
|   |-- scripts/
|   |-- _quarto.yml
|   |-- index.qmd
|   |-- numerica.qmd
|   |-- comparacion_final_numerica.qmd
|   `-- combinatoria.qmd
|-- docs/
|   `-- sitio renderizado para GitHub Pages
`-- .github/
    `-- workflows/
        `-- publish-quarto.yml
```

## Descripcion por carpetas

### `1. optimizacion_numerica/`

Reune el desarrollo del bloque de optimizacion numerica.

- `gradiente/`: implementacion de funciones objetivo y gradientes, notebooks de generacion y analisis, y salidas reproducibles en `datos/`.
- `heuristicos/`: implementacion central de EA, PSO y DE, junto con notebooks y resultados experimentales.
- `12_comparacion_final_metodos.ipynb`: consolida la comparacion entre metodos.
- `animacion_de_rastrigin_2d.ipynb`: genera material visual del comportamiento de los algoritmos.

### `2. optimizacion_combinatoria/`

Contiene el pipeline del bloque de optimizacion combinatoria.

- `src/`: modulos principales para preprocesamiento, matrices, grafo, ACO, GA, resultados y visualizacion.
- `scripts/`: ejecuciones auxiliares para correr experimentos y generar artefactos finales.
- `notebooks/`: flujo documentado del proceso, desde la construccion del grafo hasta los resultados finales.
- `entrega_final/`: archivos finales recomendados para reporte y presentacion.
- `outputs/` y `data/`: resultados, rutas, figuras y datos intermedios.
- `docs/`: documentos de apoyo y comparativos.

### `blog/`

Contiene las fuentes del sitio en Quarto.

- `index.qmd`, `numerica.qmd`, `combinatoria.qmd` y `comparacion_final_numerica.qmd`: paginas principales del proyecto.
- `notebooks/` y `presentacion/`: cuadernos integrados al sitio.
- `assets/`: imagenes, gifs, videos y otros recursos usados en la publicacion.
- `_quarto.yml`: configuracion del sitio y del proceso de render.

### `docs/`

Guarda la version renderizada del sitio. Esta carpeta se conserva en el repositorio porque funciona como salida lista para publicar en GitHub Pages.

## Ruta recomendada para recorrer el repositorio

1. Revisar el sitio publicado para ver la entrega consolidada.
2. Explorar `blog/` si se quiere entender como se organiza la presentacion final.
3. Entrar a `1. optimizacion_numerica/` y `2. optimizacion_combinatoria/` para revisar codigo, notebooks y resultados.
4. Consultar `2. optimizacion_combinatoria/entrega_final/` si se necesitan artefactos listos para reporte.

## Nota

El repositorio incluye tanto codigo fuente como resultados generados y material de publicacion. Por eso varias carpetas contienen notebooks, figuras, tablas y archivos ya renderizados.
