Calculadora Booleana en YACC

Descripción

Este proyecto implementa una **calculadora de escritorio para expresiones booleanas** utilizando herramientas clásicas de compiladores:

* **LEX (FLEX):** análisis léxico
* **YACC:** análisis sintáctico

El sistema permite evaluar expresiones lógicas ingresadas por el usuario, respetando la precedencia y asociatividad de los operadores.

Características

* Evaluación de expresiones booleanas
* Soporte para operadores:

  * `&&` (AND)
  * `||` (OR)
  * `!` (NOT)
* Uso de paréntesis `()`
* Valores booleanos: `true`, `false`
* Medición de rendimiento (tiempo de ejecución)
* Conteo de tokens procesados

Archivos Entregados

Este proyecto incluye únicamente:

* `calculadora.y` → definición del parser (YACC)
* `calculadora.l` → definición del lexer (LEX)
* `README.md` → documentación del proyecto

Requisitos

Antes de ejecutar, asegúrese de tener instalado:

* `flex` (o `lex`)
* `bison` o `yacc`
* `gcc`

En sistemas Linux:

```bash
sudo apt install flex bison gcc
```

Compilación y Ejecución

Dado que solo se entregan los archivos fuente (`.l` y `.y`), es necesario generar los archivos intermedios.

🔹 Paso 1: Generar el parser

```bash
yacc -d calculadora.y
```

Esto genera:

* `y.tab.c`
* `y.tab.h`

🔹 Paso 2: Generar el analizador léxico

```bash
lex calculadora.l
```

Esto genera:

* `lex.yy.c`

🔹 Paso 3: Compilar el programa

```bash
gcc y.tab.c lex.yy.c -o calculadora -lfl
```

🔹 Paso 4: Ejecutar

```bash
./calculadora
```

Ejemplo de Uso

Entrada:

```
true && false || true
```

Salida esperada:

```
Resultado: true

========== Rendimiento ==========
Tokens procesados: 9
Tiempo de ejecucion: 0.0000XX segundos
================================
```

Fundamentos Teóricos

El parser generado por YACC es de tipo **LALR(1)**, lo que implica:

* Análisis **bottom-up**
* Uso de tablas de parsing eficientes
* Capacidad para manejar gramáticas más complejas que LL(1)

Gramática Implementada

```
E → E OR E
E → E AND E
E → NOT E
E → ( E )
E → TRUE
E → FALSE
```

Precedencia definida como:

* `NOT` → mayor precedencia
* `AND` → intermedia
* `OR` → menor precedencia

Análisis de Rendimiento

El programa mide el rendimiento utilizando la función `clock()` del lenguaje C.

🔹 Métricas evaluadas

* **Tiempo de ejecución:** duración total del análisis
* **Tokens procesados:** cantidad de unidades léxicas reconocidas

🔹 Complejidad

El analizador presenta una complejidad:

[
O(n)
]

Donde ( n ) es el número de tokens de entrada.

🔹 Interpretación

* Para entradas pequeñas, el tiempo es prácticamente despreciable
* A mayor tamaño de la expresión, el tiempo crece de forma lineal
* Esto valida el comportamiento esperado de un parser LALR(1)

🔹 Factores que influyen

* Longitud de la expresión
* Cantidad de operadores
* Uso de paréntesis
* Rendimiento del sistema

Ventajas

* Alta eficiencia (O(n))
* Manejo automático de precedencia
* Escalable a lenguajes más complejos
* Implementación formal basada en compiladores

Limitaciones

* Dependencia de herramientas externas (LEX/YACC)
* Posibles conflictos si la gramática es ambigua
* Requiere correcta definición de reglas

Conclusión

La implementación de esta calculadora booleana demuestra la eficiencia de los analizadores sintácticos generados con YACC. Su comportamiento lineal y su capacidad de evaluación semántica en tiempo real la convierten en una solución sólida dentro del contexto de construcción de compiladores.


