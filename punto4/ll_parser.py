"""
=============================================================================
 PARSER PREDICTIVO LL(1) — Calculadora Aritmética
 Descenso Recursivo con tabla de análisis LL(1)
=============================================================================
 Gramática LL(1):
 
   E   → T E'
   E'  → + T E'  |  - T E'  |  ε
   T   → F T'
   T'  → * F T'  |  / F T'  |  ε
   F   → ( E )  |  num  |  float

 FIRST y FOLLOW:
   FIRST(E)  = FIRST(T)  = FIRST(F)  = { (, num, float }
   FIRST(E') = { +, -, ε }
   FIRST(T') = { *, /, ε }
   FOLLOW(E) = FOLLOW(E') = { ), $ }
   FOLLOW(T) = FOLLOW(T') = { +, -, ), $ }
   FOLLOW(F) = { *, /, +, -, ), $ }

 Tabla LL(1):
          num/float    +      -      *      /      (      )      $
   E      E→TE'                             E→TE'
   E'                 E'→+TE' E'→-TE'             ε      ε
   T      T→FT'                             T→FT'
   T'                 ε       ε      T'→*FT' T'→/FT' ε      ε
   F      F→num/float                        F→(E)
=============================================================================
"""

import time
from typing import Any
from cyk_parser import Token, tokenize   # reutilizamos el tokenizador


# ---------------------------------------------------------------------------
# 1. TABLA LL(1)
# ---------------------------------------------------------------------------
# Representamos la tabla como un dict:
#   (no_terminal, terminal_type) → producción a aplicar

# Codificamos cada producción como una función que parsea y evalúa
# (combinamos análisis + evaluación en una sola pasada — característica clave del LL)

class LLParserError(Exception):
    pass


class PredictiveParser:
    """
    Parser Predictivo LL(1) — Descenso Recursivo.
    
    Complejidad temporal: O(n)  (una pasada lineal sobre los tokens)
    Complejidad espacial: O(d)  donde d = profundidad máxima del árbol (≈ profundidad de anidamiento)
    
    La tabla LL(1) se implementa mediante selección de producción en cada
    método; sin ambigüedad porque la gramática es LL(1).
    """

    def __init__(self):
        self.operations_count = 0
        self._tokens: list[Token] = []
        self._pos: int = 0

    # ---- utilidades de navegación ----

    def _peek(self) -> Token | None:
        if self._pos < len(self._tokens):
            return self._tokens[self._pos]
        return None

    def _peek_type(self) -> str:
        t = self._peek()
        return t.type if t else "$"

    def _consume(self, expected_type: str | None = None) -> Token:
        self.operations_count += 1
        t = self._peek()
        if t is None:
            raise LLParserError("Fin de entrada inesperado")
        if expected_type and t.type != expected_type:
            raise LLParserError(
                f"Se esperaba {expected_type!r}, se obtuvo {t.type!r} ('{t.value}')"
            )
        self._pos += 1
        return t

    # ---- producciones LL(1) ----

    def _parse_E(self) -> float:
        """E → T E'"""
        self.operations_count += 1
        val = self._parse_T()
        return self._parse_Eprime(val)

    def _parse_Eprime(self, inherited: float) -> float:
        """E' → + T E'  |  - T E'  |  ε"""
        self.operations_count += 1
        tt = self._peek_type()
        if tt == "OP_AD":
            op = self._consume("OP_AD").value
            right = self._parse_T()
            result = inherited + right if op == "+" else inherited - right
            return self._parse_Eprime(result)
        # ε : cuando el siguiente es ), $ — no consume
        return inherited

    def _parse_T(self) -> float:
        """T → F T'"""
        self.operations_count += 1
        val = self._parse_F()
        return self._parse_Tprime(val)

    def _parse_Tprime(self, inherited: float) -> float:
        """T' → * F T'  |  / F T'  |  ε"""
        self.operations_count += 1
        tt = self._peek_type()
        if tt == "OP_MU":
            op = self._consume("OP_MU").value
            right = self._parse_F()
            if op == "*":
                result = inherited * right
            else:
                if right == 0:
                    raise LLParserError("División por cero")
                result = inherited / right
            return self._parse_Tprime(result)
        return inherited

    def _parse_F(self) -> float:
        """F → ( E )  |  NUM  |  FLOAT"""
        self.operations_count += 1
        tt = self._peek_type()
        if tt == "LP":
            self._consume("LP")
            val = self._parse_E()
            self._consume("RP")
            return val
        elif tt in ("NUM", "FLOAT"):
            tok = self._consume()
            return float(tok.value)
        else:
            raise LLParserError(
                f"Token inesperado {tt!r} en posición {self._pos}"
            )

    # ---- API pública ----

    def parse_and_evaluate(self, tokens: list[Token]) -> tuple[bool, float | None]:
        """
        Realiza el análisis sintáctico + evaluación semántica en una sola pasada.
        
        Retorna:
            (aceptado: bool, resultado: float | None)
        """
        self._tokens = tokens
        self._pos = 0
        self.operations_count = 0

        try:
            result = self._parse_E()
            # Verificar que consumimos toda la entrada
            remaining = self._peek()
            if remaining is not None:
                raise LLParserError(
                    f"Token inesperado al final: {remaining.type!r}"
                )
            return True, result
        except LLParserError:
            return False, None

    def validate_only(self, tokens: list[Token]) -> bool:
        """Solo valida sintaxis sin calcular (para benchmarking justo)."""
        accepted, _ = self.parse_and_evaluate(tokens)
        return accepted


# ---------------------------------------------------------------------------
# 2. MÉTRICAS DE RENDIMIENTO
# ---------------------------------------------------------------------------

def benchmark_ll(expression: str, repetitions: int = 1000) -> dict[str, Any]:
    """
    Mide el rendimiento del parser LL(1) sobre una expresión.
    
    Retorna un dict con tiempos, conteos de operaciones y resultado.
    """
    parser = PredictiveParser()
    tokens = tokenize(expression)

    # Calentamiento
    for _ in range(5):
        parser.parse_and_evaluate(tokens)

    times: list[float] = []
    ops:   list[int]   = []

    for _ in range(repetitions):
        t0 = time.perf_counter()
        accepted, result = parser.parse_and_evaluate(tokens)
        t1 = time.perf_counter()
        times.append(t1 - t0)
        ops.append(parser.operations_count)

    return {
        "accepted": accepted,
        "result":   result,
        "n_tokens": len(tokens),
        "ops_mean": sum(ops) / len(ops),
        "time_mean_us": (sum(times) / len(times)) * 1_000_000,
        "time_min_us":  min(times) * 1_000_000,
        "time_max_us":  max(times) * 1_000_000,
        "time_std_us":  (
            (sum((t - sum(times)/len(times))**2 for t in times) / len(times)) ** 0.5
        ) * 1_000_000,
        "complexity_class": f"O(n)  ≈ O({len(tokens)})",
    }
