$ErrorActionPreference = "Stop"

$blogDir = Split-Path -Parent $PSScriptRoot
$projectDir = Split-Path -Parent $blogDir
$targetRoot = Join-Path $blogDir "notebooks"
$assetsRoot = Join-Path $blogDir "assets\combinatoria"

$files = @(
  @{
    Source = Join-Path $projectDir "1. optimizacion_numerica\gradiente\analisis_resultados.ipynb"
    Target = Join-Path $targetRoot "numerica\gradiente\analisis_resultados.ipynb"
  },
  @{
    Source = Join-Path $projectDir "1. optimizacion_numerica\heuristicos\analisis_resultados.ipynb"
    Target = Join-Path $targetRoot "numerica\heuristicos\analisis_resultados.ipynb"
  },
  @{
    Source = Join-Path $projectDir "2. optimizacion_combinatoria\notebooks\00_construccion_grafo_inicial.ipynb"
    Target = Join-Path $targetRoot "combinatoria\00_construccion_grafo_inicial.ipynb"
  },
  @{
    Source = Join-Path $projectDir "2. optimizacion_combinatoria\notebooks\01_preprocesamiento.ipynb"
    Target = Join-Path $targetRoot "combinatoria\01_preprocesamiento.ipynb"
  },
  @{
    Source = Join-Path $projectDir "2. optimizacion_combinatoria\notebooks\02_optimizacion.ipynb"
    Target = Join-Path $targetRoot "combinatoria\02_optimizacion.ipynb"
  },
  @{
    Source = Join-Path $projectDir "2. optimizacion_combinatoria\notebooks\03_resultados_finales.ipynb"
    Target = Join-Path $targetRoot "combinatoria\03_resultados_finales.ipynb"
  }
)

foreach ($file in $files) {
  if (-not (Test-Path -LiteralPath $file.Source)) {
    Write-Warning "No se encontro el notebook: $($file.Source)"
    continue
  }

  $targetDir = Split-Path -Parent $file.Target
  if (-not (Test-Path -LiteralPath $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
  }

  Copy-Item -LiteralPath $file.Source -Destination $file.Target -Force
}

$assetFiles = @(
  @(
    Join-Path $projectDir "2. optimizacion_combinatoria\outputs\visualizaciones\mejor_solucion_combinatoria.gif"
  ),
  @(
    Join-Path $projectDir "2. optimizacion_combinatoria\outputs\visualizaciones\convergencia_ga.svg"
  ),
  @(
    Join-Path $projectDir "2. optimizacion_combinatoria\outputs\visualizaciones\visualizacion_mejor_solucion.svg"
  )
)

if (-not (Test-Path -LiteralPath $assetsRoot)) {
  New-Item -ItemType Directory -Path $assetsRoot -Force | Out-Null
}

foreach ($assetGroup in $assetFiles) {
  $source = $assetGroup[0]

  if (-not (Test-Path -LiteralPath $source)) {
    Write-Warning "No se encontro el recurso visual: $source"
    continue
  }

  $target = Join-Path $assetsRoot (Split-Path -Leaf $source)
  Copy-Item -LiteralPath $source -Destination $target -Force
}
