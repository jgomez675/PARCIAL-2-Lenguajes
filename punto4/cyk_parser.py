"""
=============================================================================
 CYK PARSER — Calculadora Aritmética
 Algoritmo Cocke-Younger-Kasami  (O(n³ · |G|))
=============================================================================
 Gramática en Forma Normal de Chomsky (CNF):
 
   E  → E T1 | T
   T1 → OP_AD E          (operación aditiva: + | -)
   T  → T T2 | F
   T2 → OP_MU T          (operación multiplicativa: * | /)
   F  → LP E3            (paréntesis)
   E3 → E RP
   F  → NUM | FLOAT

 Terminales (tokens): NUM, FLOAT, OP_AD, OP_MU, LP, RP

=============================================================================
"""

import re
import time
from typing import Any

# ---------------------------------------------------------------------------
# 1. TOKENIZADOR
# ---------------------------------------------------------------------------

class Token:
    """Representa un token léxico con su tipo y valor."""
    __slots__ = ("type", "value", "pos")

    def __init__(self, type_: str, value: str, pos: int = -1):
        self.type  = type_
        self.value = value
        self.pos   = pos

    def __repr__(self):
        return f"Token({self.type!r}, {self.value!r})"


_TOKEN_PATTERNS = [
    ("FLOAT",  r"\d+\.\d+"),
    ("NUM",    r"\d+"),
    ("OP_AD",  r"[+\-]"),
    ("OP_MU",  r"[*/]"),
    ("LP",     r"\("),
    ("RP",     r"\)"),
    ("WS",     r"\s+"),
]

_MASTER_RE = re.compile(
    "|".join(f"(?P<{name}>{pat})" for name, pat in _TOKEN_PATTERNS)
)


def tokenize(expression: str) -> list[Token]:
    """Convierte una expresión de texto en una lista de tokens."""
    tokens: list[Token] = []
    for m in _MASTER_RE.finditer(expression):
        kind = m.lastgroup
        if kind == "WS":
            continue
        tokens.append(Token(kind, m.group(), m.start()))
    return tokens


# ---------------------------------------------------------------------------
# 2. GRAMÁTICA CNF
# ---------------------------------------------------------------------------
# Representamos la gramática como:
#   UNIT_RULES  : A → a  (reglas de terminal)
#   BINARY_RULES: A → B C (reglas binarias)
#
# Tabla CNF construida manualmente para la gramática de calculadora:
#
#   expr  → expr  add_op  |  term
#   expr  → term           (necesitamos tabla de unarios también)
#   add_op→ ADD_T  expr
#   term  → term  mul_op  |  factor
#   mul_op→ MUL_T  term
#   factor→ LP  rp_part
#   rp_part→ expr  RP
#   factor→ NUM | FLOAT
#
# Para CYK puro necesitamos la CNF estricta (solo A→BC o A→a).

# UNIT_RULES: {terminal_type: [lista de no-terminales que lo derivan]}
UNIT_RULES: dict[str, list[str]] = {
    "NUM":   ["factor", "term", "expr"],   # factor→NUM, y luego expr→term→factor
    "FLOAT": ["factor", "term", "expr"],
    "OP_AD": ["op_ad"],
    "OP_MU": ["op_mu"],
    "LP":    ["lp"],
    "RP":    ["rp"],
}

# BINARY_RULES: lista de (A, B, C) tal que A → B C
BINARY_RULES: list[tuple[str, str, str]] = [
    # expr   → expr   add_chunk   (expr + expr)
    ("expr",     "expr",    "add_chunk"),
    # add_chunk → op_ad  expr        (el lado derecho de una suma)
    ("add_chunk","op_ad",   "expr"),
    # term   → term   mul_chunk
    ("term",     "term",    "mul_chunk"),
    # mul_chunk → op_mu  term
    ("mul_chunk","op_mu",   "term"),
    # parenthesized → lp  rp_part
    ("factor",   "lp",      "rp_part"),
    # rp_part → expr  rp
    ("rp_part",  "expr",    "rp"),
    # term → factor  (propagación factor→term)
    # expr → term    (propagación term→expr)
    # Las propagaciones unitarias las manejamos en UNIT_RULES expandidas
]

# Propagaciones unitarias explícitas en CNF (A → B donde B es no-terminal)
# CYK clásico no admite reglas unitarias, las "cerramos" en el llenado de celda:
UNIT_NT: dict[str, list[str]] = {
    "factor": ["term", "expr"],
    "term":   ["expr"],
}


# ---------------------------------------------------------------------------
# 3. ALGORITMO CYK
# ---------------------------------------------------------------------------

class CYKParser:
    """
    Parser CYK (Cocke-Younger-Kasami).
    
    Complejidad temporal: O(n³ · |P|)
    Complejidad espacial: O(n² · |V|)
    
    Donde n = longitud de la cadena, |P| = nº de producciones, |V| = |V_NT|.
    """

    def __init__(self):
        self.operations_count = 0   # Contador de operaciones elementales
        self.table: list[list[set]] = []

    def _close_units(self, cell: set[str]) -> None:
        """Aplica la clausura de reglas unitarias NT→NT sobre una celda."""
        changed = True
        while changed:
            changed = False
            additions = set()
            for sym in list(cell):
                for parent in UNIT_NT.get(sym, []):
                    if parent not in cell:
                        additions.add(parent)
                        changed = True
            cell |= additions

    def parse(self, tokens: list[Token]) -> tuple[bool, list[list[set]]]:
        """
        Ejecuta CYK sobre la lista de tokens.
        
        Retorna:
            (aceptado: bool, tabla: list[list[set]])
        """
        n = len(tokens)
        self.operations_count = 0

        if n == 0:
            return False, []

        # Tabla triangular: table[i][j] = conjunto de NT que derivan tokens[i..j]
        table: list[list[set]] = [[set() for _ in range(n)] for _ in range(n)]

        # --- Paso 1: llenar diagonal (longitud 1) con terminales ---
        for i, tok in enumerate(tokens):
            self.operations_count += 1
            for nt in UNIT_RULES.get(tok.type, []):
                table[i][i].add(nt)
            self._close_units(table[i][i])

        # --- Paso 2: llenar substrings de longitud 2..n ---
        for length in range(2, n + 1):          # longitud del span
            for i in range(n - length + 1):     # inicio del span
                j = i + length - 1              # fin del span

                for k in range(i, j):           # punto de división
                    left_cell  = table[i][k]
                    right_cell = table[k+1][j]

                    for (A, B, C) in BINARY_RULES:
                        self.operations_count += 1
                        if B in left_cell and C in right_cell:
                            table[i][j].add(A)

                self._close_units(table[i][j])

        self.table = table
        accepted = "expr" in table[0][n - 1]
        return accepted, table

    def evaluate(self, tokens: list[Token]) -> float | None:
        """
        Evalúa la expresión numéricamente usando descenso recursivo
        sobre la tabla CYK ya construida.
        """
        accepted, _ = self.parse(tokens)
        if not accepted:
            return None
        # Una vez validada la cadena, evaluamos con descenso recursivo directo
        self._pos = 0
        self._tokens = tokens
        try:
            result = self._eval_expr()
            return result
        except Exception:
            return None

    # — evaluación por descenso recursivo (usa el mismo tokenizado) —

    def _peek(self) -> Token | None:
        if self._pos < len(self._tokens):
            return self._tokens[self._pos]
        return None

    def _consume(self) -> Token:
        tok = self._tokens[self._pos]
        self._pos += 1
        return tok

    def _eval_expr(self) -> float:
        left = self._eval_term()
        while (t := self._peek()) and t.type == "OP_AD":
            self._consume()
            right = self._eval_term()
            if t.value == "+":
                left += right
            else:
                left -= right
        return left

    def _eval_term(self) -> float:
        left = self._eval_factor()
        while (t := self._peek()) and t.type == "OP_MU":
            self._consume()
            right = self._eval_factor()
            if t.value == "*":
                left *= right
            else:
                left /= right
        return left

    def _eval_factor(self) -> float:
        t = self._peek()
        if t is None:
            raise SyntaxError("Token inesperado")
        if t.type in ("NUM", "FLOAT"):
            self._consume()
            return float(t.value)
        if t.type == "LP":
            self._consume()
            val = self._eval_expr()
            rp = self._peek()
            if rp is None or rp.type != "RP":
                raise SyntaxError("Se esperaba ')'")
            self._consume()
            return val
        raise SyntaxError(f"Token inesperado: {t}")


# ---------------------------------------------------------------------------
# 4. MÉTRICAS DE RENDIMIENTO
# ---------------------------------------------------------------------------

def benchmark_cyk(expression: str, repetitions: int = 1000
                  ) -> dict[str, Any]:
    """
    Mide el rendimiento del parser CYK sobre una expresión.
    
    Retorna un dict con tiempos, conteos de operaciones y resultado.
    """
    parser = CYKParser()
    tokens = tokenize(expression)

    # Calentamiento (evitar JIT/cache fría de Python)
    for _ in range(5):
        parser.parse(tokens)

    times: list[float] = []
    ops: list[int] = []

    for _ in range(repetitions):
        t0 = time.perf_counter()
        accepted, table = parser.parse(tokens)
        t1 = time.perf_counter()
        times.append(t1 - t0)
        ops.append(parser.operations_count)

    result = parser.evaluate(tokens)

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
        "complexity_class": f"O(n³) ≈ O({len(tokens)}³) = O({len(tokens)**3})",
    }
