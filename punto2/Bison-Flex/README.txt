SASHA Language — Bison y Flex

Descripción General

SASHA es un lenguaje de dominio específico (DSL) diseñado para representar operaciones CRUD (Create, Read, Update, Delete) sobre bases de datos NoSQL. Este proyecto presenta la implementación formal de su gramática utilizando herramientas clásicas de construcción de compiladores: Bison para el análisis sintáctico y Flex para el análisis léxico.

El objetivo principal es validar la estructura del lenguaje mediante un parser funcional, evidenciando el proceso de reconocimiento de instrucciones y su correcta conformación según las reglas definidas.

Objetivos del Proyecto

* Diseñar una gramática formal para un lenguaje CRUD
* Implementar el analizador léxico con Flex
* Implementar el analizador sintáctico con Bison
* Validar la sintaxis del lenguaje SASHA
* Demostrar el funcionamiento del parser mediante pruebas

Características del Lenguaje

* Sintaxis estructurada y clara
* Soporte para operaciones CRUD completas
* Manejo de estructuras tipo clave-valor
* Evaluación de condiciones mediante operadores relacionales
* Independencia de esquemas, característica de NoSQL
* Diseño modular orientado a compiladores

---

Estructura del Lenguaje

El lenguaje SASHA define las siguientes operaciones principales:

| Operación | Descripción                         |
| --------- | ----------------------------------- |
| INSERT    | Inserta documentos en una colección |
| FIND      | Consulta documentos                 |
| UPDATE    | Modifica documentos existentes      |
| DELETE    | Elimina documentos                  |

---

Sintaxis

INSERT

INSERT <coleccion> {campo: valor, campo: valor}

Ejemplo:

INSERT usuarios {nombre: "Juan", edad: 20}

---

FIND

FIND <coleccion>
FIND <coleccion> WHERE <campo> <operador> <valor>

Ejemplo:

FIND usuarios
FIND usuarios WHERE edad > 18

---

UPDATE

UPDATE <coleccion> SET <campo> = <valor> WHERE <condicion>

Ejemplo:

UPDATE usuarios SET edad = 30 WHERE nombre = "Juan"

---

DELETE

DELETE <coleccion> WHERE <condicion>

Ejemplo:

DELETE usuarios WHERE edad < 25

---

Arquitectura del Sistema

El sistema se compone de dos módulos principales:

1. Análisis Léxico (Flex)

Encargado de reconocer los tokens del lenguaje, tales como:

* Palabras reservadas: INSERT, FIND, UPDATE, DELETE, WHERE, SET
* Identificadores
* Números
* Cadenas de texto

Archivo principal:

sasha_lexer.l

2. Análisis Sintáctico (Bison)

Encargado de validar la estructura del lenguaje mediante reglas gramaticales.

Archivo principal:

sasha_parser.y

Requisitos

* Sistema operativo Linux o entorno compatible
* Bison
* Flex
* Compilador GCC

Instalación

Instalar dependencias:

sudo apt update
sudo apt install bison flex gcc

Compilación

1. Generar el parser:

bison -d sasha_parser.y

2. Generar el lexer:

flex sasha_lexer.l

3. Compilar:

gcc sasha_parser.tab.c lex.yy.c -o sasha

Ejecución

Ejecutar el programa:

./sasha

Ejemplo de Uso

Entrada:

INSERT usuarios {nombre: "Juan", edad: 20}

Para finalizar la entrada, presionar:

CTRL + D

Salida esperada:

SASHA Parser iniciado...
Entrada válida en lenguaje SASHA

Validación

El sistema valida la estructura sintáctica de las instrucciones ingresadas. Si la entrada cumple con la gramática definida, se considera válida. En caso contrario, se reporta un error sintáctico.

Consideraciones

* Los comandos deben escribirse en mayúsculas
* Las estructuras de datos deben usar llaves {}
* Las cadenas deben ir entre comillas dobles
* El parser no ejecuta operaciones, solo valida la sintaxis

Posibles Extensiones

* Generación de árbol sintáctico
* Implementación de análisis semántico
* Integración con un intérprete en Python
* Soporte para operadores lógicos
* Persistencia en bases de datos reales

Conclusión

La implementación del lenguaje SASHA mediante Bison y Flex permite comprender el funcionamiento interno de los analizadores léxicos y sintácticos. Este enfoque proporciona un control detallado sobre el proceso de parsing, siendo fundamental en el desarrollo de compiladores.

El proyecto demuestra la aplicación práctica de gramáticas formales y herramientas clásicas, consolidando los fundamentos teóricos de los lenguajes de programación.
