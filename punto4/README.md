Comparación de Parsers: CYK vs LL(1)
Parcial 2 – Lenguajes de Programación
Análisis de Rendimiento y Complejidad

Descripción General

Este proyecto implementa y compara dos analizadores sintácticos para
expresiones aritméticas:

Parser LL(1) (Descenso Recursivo Predictivo)
Parser CYK (Cocke-Younger-Kasami)

El sistema:

1. Valida expresiones aritméticas
2. Evalúa su resultado
3. Ejecuta benchmarks de rendimiento
4. Genera análisis estadístico
5. Guarda gráficas comparativas en archivo PNG

 Nota:
El sistema está configurado para ejecutarse en Linux sin entorno gráfico,
por lo tanto las gráficas **no se muestran en pantalla**, únicamente se guardan en archivo.

Fundamento Teórico

Parser LL(1)

Tipo:
Top-Down Predictivo

Gramática utilizada:

E   → T E'  
E'  → + T E' | - T E' | ε  
T   → F T'  
T'  → * F T' | / F T' | ε  
F   → ( E ) | num | float  

Complejidad:

- Tiempo: O(n)
- Espacio: O(d)

Donde:
- n = número de tokens
- d = profundidad del árbol

Características:

- Consume tokens una sola vez
- No requiere backtracking
- Evalúa mientras analiza
- Muy eficiente

Parser CYK

Tipo:
Bottom-Up con Programación Dinámica

Requiere:
Gramática en Forma Normal de Chomsky (CNF)

Funcionamiento:

- Construye tabla triangular n × n
- Evalúa todas las particiones posibles
- Determina pertenencia al lenguaje

Complejidad:

- Tiempo: O(n³ · |G|)
- Espacio: O(n² · |V|)

Donde:
- n = número de tokens
- |G| = número de reglas
- |V| = número de no terminales

Análisis Comparativo

| Característica | LL(1) | CYK |
|---------------|-------|-----|
| Estrategia | Top-Down | Bottom-Up |
| Complejidad | O(n) | O(n³) |
| Velocidad práctica | Muy alta | Baja |
| Generalidad | Limitada | Alta |

Resultados Observados

Los benchmarks demuestran que:

- LL(1) mantiene crecimiento lineal.
- CYK crece cúbicamente.
- La diferencia se amplifica con expresiones largas.
- El ratio CYK / LL(1) aumenta conforme crece n.

Conclusión:

Para esta calculadora, LL(1) es significativamente más eficiente.

Requisitos

- Python 3.12+
- Linux
- Entorno virtual recomendado

Instalación de Dependencias

Crear entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

Instalar librerías:

```bash
pip install matplotlib numpy
```

Ejecución

Desde la carpeta del proyecto:

```bash
python main.py
```

El sistema:

1. Ejecuta pruebas
2. Calcula estadísticas
3. Guarda las gráficas comparativas

Guardado de Gráficas

Actualmente el sistema guarda automáticamente la imagen en:

```
benchmark_results.png
```

Si se desea cambiar la ruta, modificar en `main.py`:

```python
plot_path = "benchmark_results.png"
```

Por ejemplo:

```python
plot_path = "/home/julian/resultados/analisis.png"
```

Si la carpeta no existe, debe crearse previamente:

```bash
mkdir -p /home/julian/resultados
```

Estructura del Proyecto

.
├── main.py  
├── cyk_parser.py  
├── ll_parser.py  
└── README.md  

Qué Incluyen las Gráficas

- Tiempo promedio por expresión
- Tiempo vs número de tokens
- Ratio CYK / LL(1)
- Operaciones elementales ejecutadas

Conclusión Académica

Este proyecto demuestra empíricamente que:

- La complejidad teórica se refleja en mediciones reales.
- O(n) es considerablemente más eficiente que O(n³).
- La generalidad algorítmica implica mayor costo computacional.
- En compiladores reales se priorizan parsers tipo LL o LR.
