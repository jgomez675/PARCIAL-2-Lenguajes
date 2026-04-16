SASHA Language — ANTLR4

Descripción General

**SASHA** es un lenguaje de dominio específico (DSL) diseñado para modelar operaciones **CRUD (Create, Read, Update, Delete)** sobre bases de datos NoSQL.

Su propósito es demostrar la construcción formal de un lenguaje de programación, desde el diseño de su gramática hasta su implementación mediante herramientas de análisis sintáctico como **ANTLR4**.

El lenguaje utiliza una sintaxis clara, inspirada en estructuras tipo JSON, permitiendo representar datos de manera flexible y sin esquemas rígidos, característica fundamental de los sistemas NoSQL.

Objetivos del Proyecto

* Diseñar una gramática formal para un lenguaje CRUD
* Implementar dicha gramática utilizando **ANTLR4**
* Validar la sintaxis del lenguaje mediante análisis léxico y sintáctico
* Visualizar árboles sintácticos (parse trees)
* Demostrar el funcionamiento del lenguaje en diferentes entornos

Características del Lenguaje

* Sintaxis simple y expresiva
* Soporte completo para operaciones CRUD
* Estructuras de datos tipo clave-valor
* Evaluación de condiciones con operadores relacionales
* Independencia de esquemas (NoSQL)
* Fácil extensibilidad

Estructura del Lenguaje

Operaciones soportadas

| Operación | Descripción                         |
| --------- | ----------------------------------- |
| `INSERT`  | Inserta documentos en una colección |
| `FIND`    | Consulta documentos                 |
| `UPDATE`  | Modifica documentos existentes      |
| `DELETE`  | Elimina documentos                  |

---

Sintaxis

INSERT

```txt
INSERT <coleccion> {campo: valor, campo: valor}
```

Ejemplo:

```txt
INSERT usuarios {nombre: "Juan", edad: 20}
```

FIND

```txt
FIND <coleccion>
FIND <coleccion> WHERE <campo> <operador> <valor>
```

Ejemplo:

```txt
FIND usuarios
FIND usuarios WHERE edad > 18
```

---

UPDATE

```txt
UPDATE <coleccion> SET <campo> = <valor> WHERE <condicion>
```

Ejemplo:

```txt
UPDATE usuarios SET edad = 30 WHERE nombre = "Juan"
```

---

DELETE

```txt
DELETE <coleccion> WHERE <condicion>
```

Ejemplo:

```txt
DELETE usuarios WHERE edad < 25
```

Definición de la Gramática

El lenguaje SASHA está definido mediante una gramática en ANTLR4:

* Símbolo inicial: `program`
* Producciones recursivas para múltiples instrucciones
* Separación clara entre:

  * Expresiones
  * Condiciones
  * Objetos tipo JSON

Archivo principal:

```bash
Sasha.g4
```

Requisitos

* Java JDK 8 o superior
* ANTLR4 (archivo `.jar`)
* Python 3 (opcional para integración futura)

Instalación y Ejecución

1. Descargar ANTLR4

```bash
wget https://www.antlr.org/download/antlr-4.13.1-complete.jar
```

2. Generar el parser

```bash
java -jar antlr-4.13.1-complete.jar Sasha.g4
```

3. Compilar

```bash
javac -cp ".:antlr-4.13.1-complete.jar" *.java
```

4. Ejecutar el analizador

Árbol gráfico (GUI):

```bash
java -cp ".:antlr-4.13.1-complete.jar" org.antlr.v4.gui.TestRig Sasha program -gui
```

Árbol en consola:

bash
java -cp ".:antlr-4.13.1-complete.jar" org.antlr.v4.gui.TestRig Sasha program -tree
```

Tokens (análisis léxico):

```bash
java -cp ".:antlr-4.13.1-complete.jar" org.antlr.v4.gui.TestRig Sasha program -tokens
```

Ejemplo de Uso

Entrada:

```txt
INSERT usuarios {nombre: "Juan", edad: 20}
FIND usuarios WHERE edad > 18
```

Salida esperada:

* Árbol sintáctico estructurado
* Tokens identificados correctamente
* Validación de sintaxis sin errores

Árbol Sintáctico

ANTLR genera automáticamente un **árbol sintáctico (parse tree)** que representa la estructura jerárquica del programa.

Este árbol permite:

* Verificar la correcta interpretación del lenguaje
* Analizar la estructura de las instrucciones
* Servir como base para la construcción de un AST o intérprete

Arquitectura

El proyecto se basa en tres niveles conceptuales:

1. **Análisis Léxico**

   * Identificación de tokens (ID, STRING, NUMBER)

2. **Análisis Sintáctico**

   * Validación estructural mediante reglas gramaticales

3. **Representación del Lenguaje**

   * Árbol sintáctico generado automáticamente

Consideraciones

* El lenguaje es sensible a la sintaxis definida
* Se deben usar llaves `{}` para objetos
* Los strings deben ir entre comillas dobles
* Los comandos deben escribirse en mayúsculas

Posibles Extensiones

* Integración con un intérprete en Python
* Generación de AST (Abstract Syntax Tree)
* Validación semántica
* Soporte para operadores lógicos (AND, OR)
* Persistencia en bases de datos reales

Conclusión

El lenguaje SASHA demuestra la aplicación práctica de conceptos fundamentales de lenguajes de programación, como:

* Diseño de gramáticas formales
* Construcción de analizadores léxicos y sintácticos
* Representación estructural mediante árboles

La implementación en ANTLR4 facilita el desarrollo de herramientas robustas y extensibles, posicionando este proyecto como una base sólida para futuras aplicaciones en compiladores e intérpretes.
