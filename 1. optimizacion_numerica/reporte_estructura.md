# Reporte Tecnico - Parte 1: Optimizacion numerica

## 1. Introduccion

En esta parte del trabajo se estudia el problema de optimizacion numerica sobre un conjunto de funciones de prueba ampliamente usadas en la literatura. El objetivo es comparar el comportamiento de un metodo de descenso por gradiente frente a distintos metodos heuristicos, considerando tanto la calidad de la solucion encontrada como el numero de evaluaciones de la funcion objetivo.

Tambien se busca analizar el efecto de la dimension del problema, trabajando en 2 y 3 dimensiones, y estudiar la estabilidad de los algoritmos mediante multiples ejecuciones con condiciones iniciales aleatorias.

## 2. Objetivos

### 2.1 Objetivo general

Comparar el desempeno de metodos de optimizacion basados en gradiente y metodos heuristicos sobre funciones de prueba en 2D y 3D.

### 2.2 Objetivos especificos

- Implementar las funciones objetivo indicadas en el enunciado.
- Implementar descenso por gradiente para la minimizacion de las funciones.
- Implementar metodos heuristicos de optimizacion.
- Ejecutar experimentos repetidos para analizar estabilidad y calidad de solucion.
- Representar graficamente la evolucion de los algoritmos en un caso de estudio.
- Discutir ventajas y limitaciones de cada enfoque.

## 3. Funciones objetivo

En esta seccion se presentan las funciones objetivo utilizadas en el estudio.

Importante:
- Aqui van las **formulas matematicas**.
- Aqui **no hace falta pegar todo el codigo**.
- Si quieres, puedes mencionar en una frase que la implementacion esta en `funciones.py`.

### 3.1 Funcion de Rosenbrock

Formula:
$$f(x, y) = (a - x)^2 + b(y - x^2)^2$$

En este trabajo se usa la forma clasica de la funcion de Rosenbrock, con $a = 1$ y $b = 100$, por lo que la expresion empleada es:

$$f(x, y) = (1 - x)^2 + 100(y - x^2)^2$$

### 3.2 Funcion de Rastrigin

Formula:
$$f(x) = 10N + \sum_{i=1}^{N} \left(x_i^2 - 10 \cos(2 \pi x_i)\right)$$

### 3.3 Funcion de Schwefel

Formula:
$$f(x) = 418.9829N - \sum_{i=1}^{N} x_i \sin\left(\sqrt{|x_i|}\right)$$

### 3.4 Funcion de Griewank

Formula:
$$f(x) = 1 + \frac{1}{4000} \sum_{i=1}^{N} x_i^2 - \prod_{i=1}^{N} \cos\left(\frac{x_i}{\sqrt{i}}\right)$$

### 3.5 Funcion Goldstein-Price

Formula:
$$f(x, y) = \left[1 + (x + y + 1)^2(19 - 14x + 3x^2 - 14y + 6xy + 3y^2)\right] \left[30 + (2x - 3y)^2(18 - 32x + 12x^2 + 48y - 36xy + 27y^2)\right]$$

### 3.6 Funcion de las seis jorobas de camello

Formula:
$$f(x, y) = (4 - 2.1x^2 + \frac{x^4}{3})x^2 + xy + (-4 + 4y^2)y^2$$

Consideraciones generales para las funciones objetivo:

Dimension trabajada:
- 2D
- 3D, cuando aplique

Implementacion:
- Archivo: `funciones.py`

## 4. Gradientes y descenso por gradiente

En esta seccion se explica el metodo de descenso por gradiente utilizado para minimizar las funciones objetivo.

Aqui deberias mostrar:
- la idea del metodo
- la regla de actualizacion
- los gradientes de las funciones donde aplique

### 4.1 Regla de actualizacion

Formula:

$$
x^{(t+1)} = x^{(t)} - \eta \, \nabla f\!\left(x^{(t)}\right)
$$

donde:
- $\eta$ es la tasa de aprendizaje
- $\nabla f(x)$ es el gradiente de la funcion objetivo

### 4.2 Gradientes de las funciones

Aqui puedes hacer una de estas dos cosas:

- Opcion A: mostrar la formula del gradiente para cada funcion.
- Opcion B: mostrar solo las funciones mas importantes en el cuerpo del reporte y dejar las derivaciones completas en anexo o notebook.

Ejemplo de como organizarlo:

#### Gradiente de Rosenbrock

Formula:
$$\nabla f(x, y) = \left( \frac{\partial f}{\partial x}, \frac{\partial f}{\partial y} \right)$$

$$\frac{\partial f}{\partial x} = -2(1 - x) - 400x(y - x^2)$$

$$\frac{\partial f}{\partial y} = 200(y - x^2)$$

Implementacion:
- Archivo: `funciones_gradientes.py`

#### Gradiente de Schwefel

Formula:
$$\nabla f(x) = \left( \frac{\partial f}{\partial x_1}, \frac{\partial f}{\partial x_2}, \dots, \frac{\partial f}{\partial x_N} \right)$$

$$\frac{\partial f}{\partial x_i} = -\sin\left(\sqrt{|x_i|}\right) - \frac{\sqrt{|x_i|}}{2}\cos\left(\sqrt{|x_i|}\right), \quad i = 1, 2, \dots, N$$

Implementacion:
- Archivo: `funciones_gradientes.py`

#### Gradiente de Rastrigin

Formula:
$$\nabla f(x) = \left( \frac{\partial f}{\partial x_1}, \frac{\partial f}{\partial x_2}, \dots, \frac{\partial f}{\partial x_N} \right)$$

$$\frac{\partial f}{\partial x_i} = 2x_i + 20\pi \sin(2\pi x_i), \quad i = 1, 2, \dots, N$$

Implementacion:
- Archivo: `funciones_gradientes.py`

#### Gradiente de Griewank

Formula:
$$\frac{\partial f}{\partial x_i} = \frac{x_i}{2000} + \frac{\sin\left(\frac{x_i}{\sqrt{i}}\right)}{\sqrt{i}} \prod_{\substack{j=1 \\ j \ne i}}^{N} \cos\left(\frac{x_j}{\sqrt{j}}\right), \quad i = 1, 2, \dots, N$$

Implementacion:
- Archivo: `funciones_gradientes.py`

#### Gradiente de Goldstein-Price

Formula:
$$A(x,y) = 1 + (x + y + 1)^2(19 - 14x + 3x^2 - 14y + 6xy + 3y^2)$$

$$B(x,y) = 30 + (2x - 3y)^2(18 - 32x + 12x^2 + 48y - 36xy + 27y^2)$$

$$\frac{\partial f}{\partial x} = \frac{\partial A}{\partial x}B + A\frac{\partial B}{\partial x}$$

$$\frac{\partial f}{\partial y} = \frac{\partial A}{\partial y}B + A\frac{\partial B}{\partial y}$$

Implementacion:
- Archivo: `funciones_gradientes.py`

#### Gradiente de la funcion de las seis jorobas de camello

Formula:
$$\nabla f(x, y) = \left( \frac{\partial f}{\partial x}, \frac{\partial f}{\partial y} \right)$$

$$\frac{\partial f}{\partial x} = 8x - 8.4x^3 + 2x^5 + y$$

$$\frac{\partial f}{\partial y} = x - 8y + 16y^3$$

Implementacion:
- Archivo: `funciones_gradientes.py`

### 4.3 Implementacion computacional

Aqui puedes poner una explicacion corta del codigo.

Ejemplo:

```text
El algoritmo de descenso por gradiente fue implementado de forma generica para recibir como entrada una funcion objetivo, su gradiente, una posicion inicial aleatoria, una tasa de aprendizaje y un numero maximo de iteraciones.
```

Si quieres mostrar codigo, aqui solo iria un fragmento corto, por ejemplo la firma de la funcion:

```python
def run_gradient_descent(initial_position, function, gradient_function, rate, max_iterations, tolerance=None):
    ...
```

No pongas todo el archivo completo en el reporte.

## 5. Metodos heuristicos

En esta seccion explicas los metodos heuristicos implementados.

### 5.1 Algoritmos evolutivos

Descripcion:
- [Aqui explicas poblacion inicial, mutacion, cruzamiento y seleccion.]

Si quieres mostrar codigo, solo un fragmento corto:

```python
def mi_algoritmo_evolutivo(...):
    ...
```

### 5.2 Optimizacion por particulas

Descripcion:
- [Aqui explicas la idea general de PSO.]

Codigo:
- [Solo si realmente aporta.]

### 5.3 Evolucion diferencial

Descripcion:
- [Aqui explicas la idea general de evolucion diferencial.]

Codigo:
- [Solo si realmente aporta.]

## 6. Metodologia experimental

En esta seccion explicas exactamente como corriste los experimentos.

### 6.1 Configuracion general

- Funciones evaluadas: Rosenbrock, Rastrigin, Schwefel, Griewank, Goldstein-Price y seis jorobas de camello.
- Dimensiones: 2D y 3D, cuando aplique.
- Condicion inicial: aleatoria.
- Numero de repeticiones: 100, 500 y 1000.
- Metricas registradas:
  - valor final de la funcion objetivo
  - solucion final
  - numero de evaluaciones de la funcion objetivo

### 6.2 Parametros de los algoritmos

Aqui pones una tabla como esta:

| Metodo | Parametro | Valor |
|---|---|---|
| Descenso por gradiente | Tasa de aprendizaje | [valor] |
| Descenso por gradiente | Maximo de iteraciones | [valor] |
| Algoritmo evolutivo | Tamano de poblacion | [valor] |
| PSO | Numero de particulas | [valor] |
| Evolucion diferencial | Factor de mutacion | [valor] |

## 7. Resultados

Esta es una de las secciones mas importantes.

Lo mejor es organizarla **por funcion** para que no se mezcle todo.

### 7.1 Rosenbrock

#### 7.1.1 Resultados en 2D

Aqui puedes poner:
- una tabla resumen
- histogramas
- observaciones cortas

Imagenes que deberian ir:
- histograma de soluciones finales
- histograma del numero de evaluaciones

Ejemplo de marcador:

```text
[Insertar imagen: histograma de soluciones finales para Rosenbrock 2D]
```

```text
[Insertar imagen: histograma de evaluaciones para Rosenbrock 2D]
```

#### 7.1.2 Resultados en 3D

```text
[Insertar tablas e imagenes correspondientes]
```

### 7.2 Rastrigin

#### 7.2.1 Resultados en 2D

```text
[Insertar histogramas y analisis]
```

#### 7.2.2 Resultados en 3D

```text
[Insertar histogramas y analisis]
```

### 7.3 Schwefel

#### 7.3.1 Resultados en 2D

```text
[Insertar histogramas y analisis]
```

#### 7.3.2 Resultados en 3D

```text
[Insertar histogramas y analisis]
```

### 7.4 Griewank

#### 7.4.1 Resultados en 2D

```text
[Insertar histogramas y analisis]
```

#### 7.4.2 Resultados en 3D

```text
[Insertar histogramas y analisis]
```

### 7.5 Goldstein-Price

#### 7.5.1 Resultados en 2D

```text
[Insertar histogramas y analisis]
```

### 7.6 Funcion de las seis jorobas de camello

#### 7.6.1 Resultados en 2D

```text
[Insertar histogramas y analisis]
```

## 8. Animaciones del proceso de optimizacion

Aqui debes mostrar el caso elegido para la animacion.

Debes incluir:
- que funcion elegiste
- en que dimension
- por que ese caso es representativo

### 8.1 Animacion de descenso por gradiente

```text
[Insertar gif, frame o enlace al video]
```

Descripcion:
- [Aqui explicas brevemente que se observa.]

### 8.2 Animacion del metodo heuristico

```text
[Insertar gif, frame o enlace al video]
```

Descripcion:
- [Aqui explicas brevemente que se observa.]

## 9. Discusion

Aqui respondes directamente la pregunta del enunciado:

```text
Que aportaron los metodos de descenso por gradiente y que aportaron los metodos heuristicos.
```

La discusion deberia girar alrededor de:
- valor final de la funcion objetivo
- numero de evaluaciones
- sensibilidad a la condicion inicial
- capacidad para evitar minimos locales
- costo computacional

Puedes organizar esta parte asi:

### 9.1 Aportes del descenso por gradiente

- [Aqui escribes tus hallazgos.]

### 9.2 Aportes de los metodos heuristicos

- [Aqui escribes tus hallazgos.]

### 9.3 Comparacion general

Tabla sugerida:

| Criterio | Descenso por gradiente | Metodos heuristicos |
|---|---|---|
| Velocidad | [comentario] | [comentario] |
| Evaluaciones | [comentario] | [comentario] |
| Minimos locales | [comentario] | [comentario] |
| Robustez | [comentario] | [comentario] |

## 10. Conclusiones

- [Conclusion principal 1.]
- [Conclusion principal 2.]
- [Conclusion principal 3.]

## 11. Organizacion del codigo

Aqui puedes mostrar de forma breve como organizaste el proyecto:

```text
1. optimizacion_numerica/
├── funciones.py
├── funciones_gradientes.py
├── 01_funciones_y_gradientes.ipynb
├── 02_descenso_gradiente.ipynb
├── 03_metodos_heuristicos.ipynb
├── 04_animaciones.ipynb
└── 05_comparacion_final.ipynb
```

## 12. Repositorio

Aqui va el enlace al repositorio Git:

```text
[Pegar enlace al repositorio]
```

## 13. Uso de IA

El enunciado pide reportar los principales prompts utilizados y discutir su impacto.

Puedes organizarlo asi:

### 13.1 Prompts principales

- [Prompt 1]
- [Prompt 2]
- [Prompt 3]

### 13.2 Impacto en el resultado final

- [Aqui explicas como ayudo la IA y cuales fueron sus limitaciones.]

## 14. Bibliografia

Aqui debes poner las referencias en formato APA.

Ejemplo de marcador:

- [Referencia 1 en APA]
- [Referencia 2 en APA]
- [Referencia 3 en APA]

## Nota final sobre que mostrar y que no mostrar

En el reporte:
- Si van **formulas matematicas** para las funciones objetivo.
- Si van **formulas de gradiente** o al menos las mas importantes.
- Si van **imagenes**: histogramas, graficas, animaciones o capturas.
- Si van **tablas** de comparacion.
- Si puede ir **codigo**, pero solo fragmentos pequenos y utiles.

En el reporte no conviene:
- pegar notebooks enteros
- pegar archivos `.py` completos
- llenar paginas con bloques de codigo que no aportan a la explicacion
