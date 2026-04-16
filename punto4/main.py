"""
=============================================================================
 MAIN — Comparación de Rendimiento: Parser CYK vs Parser Predictivo LL(1)
 Lenguajes de Programación — Parcial 2, 2026-1
=============================================================================
 Genera:
   1. Salida de consola con tabla de resultados formateada
   2. Gráficas comparativas (PNG)  →  benchmark_results.png
   3. Informe de análisis por consola

 Autor  : Estudiante — LP 2026-1
 Parsers: CYK (O(n³·|G|))  vs  LL(1) (O(n))
=============================================================================
"""

import sys
import math
import time
import statistics
from typing import Any

import matplotlib
matplotlib.use("Agg")          # backend sin GUI
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

from cyk_parser import tokenize, benchmark_cyk, CYKParser
from ll_parser  import benchmark_ll, PredictiveParser


# ---------------------------------------------------------------------------
# SUITE DE EXPRESIONES DE PRUEBA
# ---------------------------------------------------------------------------

TEST_SUITE: list[tuple[str, str]] = [
    # (etiqueta, expresión)
    ("Num. simple",              "42"),
    ("Suma básica",              "1 + 2"),
    ("Suma-resta mixta",         "10 + 5 - 3"),
    ("Mult. simple",             "3 * 4"),
    ("Expresión mixta",          "2 + 3 * 4"),
    ("Con paréntesis",           "(2 + 3) * 4"),
    ("Expresión mediana",        "1 + 2 * 3 - 4 / 2"),
    ("Anidamiento mod.",         "(1 + 2) * (3 - 4)"),
    ("Decimales",                "3.14 * 2.0"),
    ("Compleja nivel 1",         "10 + 20 * 30 - 40 / 5"),
    ("Compleja nivel 2",         "(10 + 20) * (30 - 40) / 5 + 2"),
    ("Anidamiento profundo",     "((((1 + 2) * 3) - 4) * 5) + 6"),
    ("Larga sin paréntesis",     "1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10"),
    ("Larga con mult.",          "2 * 3 + 4 * 5 + 6 * 7 + 8 * 9"),
    ("Multi-nivel anidado",      "((2 + 3) * (4 - 1)) / ((6 + 1) * (2 + 3))"),
    ("Flotantes complejos",      "1.5 * 2.5 + 3.5 / 0.5 - 1.0"),
    ("Muy larga plana",          "1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1"),
    ("Muy larga con mult.",      "2*3+4*5+6*7+8*9+10*11+12*13+14*15+16*17"),
    ("Anidamiento extremo",      "((((((1+2)*3)-4)*5)+6)*7)"),
    ("Máxima complejidad",       "((1+2)*(3-4)+(5*6))/(((7+8)*9)-10*(2+3))"),
]

REPS = 2000   # repeticiones por benchmark


# ---------------------------------------------------------------------------
# UTILIDADES DE SALIDA
# ---------------------------------------------------------------------------

BOX_WIDTH = 80
LINE = "═" * BOX_WIDTH

def header(title: str):
    pad = (BOX_WIDTH - len(title) - 4) // 2
    print(f"\n╔{LINE}╗")
    print(f"║  {' ' * pad}{title}{' ' * (BOX_WIDTH - pad - len(title) - 2)}  ║")
    print(f"╚{LINE}╝\n")

def section(title: str):
    print(f"\n{'─'*BOX_WIDTH}")
    print(f"  {title}")
    print(f"{'─'*BOX_WIDTH}")

def col(s: str, w: int, align: str = "<") -> str:
    return f"{s:{align}{w}}"


# ---------------------------------------------------------------------------
# FUNCIONES DE REPORTE
# ---------------------------------------------------------------------------

def print_correctness_check():
    """Verifica que ambos parsers producen los mismos resultados."""
    section("VERIFICACIÓN DE CORRECTITUD")
    print(f"\n  {'Expresión':<35} {'LL(1)':<14} {'CYK':<14} {'Match':<6}")
    print(f"  {'─'*35} {'─'*14} {'─'*14} {'─'*6}")

    all_match = True
    for label, expr in TEST_SUITE:
        tokens = tokenize(expr)

        ll_parser  = PredictiveParser()
        cyk_parser = CYKParser()

        _, ll_result  = ll_parser.parse_and_evaluate(tokens)
        cyk_result    = cyk_parser.evaluate(tokens)

        def fmt(v):
            if v is None: return "ERROR"
            return f"{v:.4f}"

        match = (
            ll_result is not None and cyk_result is not None and
            abs(ll_result - cyk_result) < 1e-9
        )
        if not match:
            all_match = False

        mark = "✓" if match else "✗"
        print(f"  {label:<35} {fmt(ll_result):<14} {fmt(cyk_result):<14} {mark}")

    print()
    if all_match:
        print("  ✅  TODOS los resultados coinciden. Ambos parsers son correctos.\n")
    else:
        print("  ❌  DISCREPANCIAS detectadas. Revisar la implementación.\n")


def run_benchmarks() -> tuple[list[dict], list[dict]]:
    """Ejecuta los benchmarks y retorna (ll_results, cyk_results)."""
    ll_results:  list[dict] = []
    cyk_results: list[dict] = []

    print()
    total = len(TEST_SUITE)
    for i, (label, expr) in enumerate(TEST_SUITE, 1):
        pct = i / total * 100
        bar_len = 30
        filled = int(bar_len * i // total)
        bar = "█" * filled + "░" * (bar_len - filled)
        print(f"\r  Benchmarking [{bar}] {pct:5.1f}%  ({i}/{total})  {label:<35}", end="", flush=True)

        ll_res  = benchmark_ll(expr,  repetitions=REPS)
        cyk_res = benchmark_cyk(expr, repetitions=REPS)

        ll_res["label"]  = label
        cyk_res["label"] = label
        ll_res["expr"]   = expr
        cyk_res["expr"]  = expr

        ll_results.append(ll_res)
        cyk_results.append(cyk_res)

    print(f"\r  {'Benchmarks completados.' + ' '*50}")
    return ll_results, cyk_results


def print_results_table(ll_results: list[dict], cyk_results: list[dict]):
    """Imprime la tabla comparativa principal."""
    section("TABLA COMPARATIVA DE RENDIMIENTO")

    hdr = (
        f"\n  {'#':<4}"
        f"{'Expresión':<25}"
        f"{'Tokens':>7}"
        f"{'LL(1) μs':>11}"
        f"{'CYK μs':>11}"
        f"{'Ratio CYK/LL':>14}"
        f"{'LL ops':>9}"
        f"{'CYK ops':>9}"
    )
    print(hdr)
    print("  " + "─" * (len(hdr) - 3))

    ratios = []
    for i, (ll, cyk) in enumerate(zip(ll_results, cyk_results), 1):
        ratio = cyk["time_mean_us"] / ll["time_mean_us"] if ll["time_mean_us"] > 0 else float("inf")
        ratios.append(ratio)
        print(
            f"  {i:<4}"
            f"{ll['label']:<25}"
            f"{ll['n_tokens']:>7}"
            f"{ll['time_mean_us']:>11.3f}"
            f"{cyk['time_mean_us']:>11.3f}"
            f"{ratio:>14.2f}x"
            f"{ll['ops_mean']:>9.0f}"
            f"{cyk['ops_mean']:>9.0f}"
        )

    print()
    avg_ratio = sum(ratios) / len(ratios)
    max_ratio = max(ratios)
    min_ratio = min(ratios)
    print(f"  Ratio promedio CYK/LL(1): {avg_ratio:.2f}x")
    print(f"  Ratio máximo:             {max_ratio:.2f}x")
    print(f"  Ratio mínimo:             {min_ratio:.2f}x")
    print()


def print_complexity_analysis(ll_results: list[dict], cyk_results: list[dict]):
    """Análisis teórico vs empírico de la complejidad."""
    section("ANÁLISIS DE COMPLEJIDAD TEÓRICA VS EMPÍRICA")

    print("""
  ┌─────────────────────────────────────────────────────────────┐
  │  Parser LL(1) — Descenso Recursivo Predictivo               │
  │                                                             │
  │  Complejidad temporal: O(n)                                 │
  │  ─ Una sola pasada lineal sobre los tokens                  │
  │  ─ Cada token se consume exactamente una vez                │
  │  ─ Sin backtracking (gramática LL(1) libre de ambigüedad)   │
  │                                                             │
  │  Complejidad espacial: O(d)                                 │
  │  ─ d = profundidad máxima del árbol de derivación           │
  │  ─ Equivalente a la profundidad de anidamiento              │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  Parser CYK — Cocke-Younger-Kasami                          │
  │                                                             │
  │  Complejidad temporal: O(n³ · |G|)                         │
  │  ─ n = longitud de la cadena de tokens                      │
  │  ─ |G| = número de producciones en la gramática CNF         │
  │  ─ Rellena una tabla triangular de tamaño n×n               │
  │  ─ Puede manejar gramáticas ambiguas y GLC generales        │
  │                                                             │
  │  Complejidad espacial: O(n² · |V|)                         │
  │  ─ |V| = tamaño del vocabulario de no-terminales            │
  └─────────────────────────────────────────────────────────────┘
""")

    # Verificar ajuste O(n) vs O(n³) empíricamente
    ns  = [ll["n_tokens"] for ll in ll_results]
    ll_times  = [ll["time_mean_us"] for ll in ll_results]
    cyk_times = [cyk["time_mean_us"] for cyk in cyk_results]

    # Normalizar por el primer punto
    if ns[0] > 0 and ll_times[0] > 0 and cyk_times[0] > 0:
        print("  Crecimiento temporal normalizado (base = expresión #1):\n")
        print(f"  {'n':>5}  {'T_LL(norm)':>12}  {'T_CYK(norm)':>13}  {'n (teórico)':>13}  {'n³ (teórico)':>14}")
        print(f"  {'─'*5}  {'─'*12}  {'─'*13}  {'─'*13}  {'─'*14}")
        n0   = ns[0]
        tl0  = ll_times[0]
        tc0  = cyk_times[0]
        for n, tl, tc in zip(ns, ll_times, cyk_times):
            teorico_ll  = n / n0
            teorico_cyk = (n / n0) ** 3
            print(
                f"  {n:>5}"
                f"  {tl/tl0:>12.3f}"
                f"  {tc/tc0:>13.3f}"
                f"  {teorico_ll:>13.3f}"
                f"  {teorico_cyk:>14.3f}"
            )
    print()


def print_statistical_summary(ll_results: list[dict], cyk_results: list[dict]):
    """Resumen estadístico agregado."""
    section("RESUMEN ESTADÍSTICO GLOBAL")

    ll_times  = [r["time_mean_us"] for r in ll_results]
    cyk_times = [r["time_mean_us"] for r in cyk_results]
    ll_ops    = [r["ops_mean"]  for r in ll_results]
    cyk_ops   = [r["ops_mean"]  for r in cyk_results]

    def stats(data, label):
        m  = statistics.mean(data)
        md = statistics.median(data)
        s  = statistics.stdev(data) if len(data) > 1 else 0
        mn = min(data)
        mx = max(data)
        print(f"\n  {label}")
        print(f"    Media:    {m:.4f}")
        print(f"    Mediana:  {md:.4f}")
        print(f"    Std dev:  {s:.4f}")
        print(f"    Mínimo:   {mn:.4f}")
        print(f"    Máximo:   {mx:.4f}")

    print()
    stats(ll_times,  "Tiempos LL(1)  [μs]:")
    stats(cyk_times, "Tiempos CYK    [μs]:")
    stats(ll_ops,    "Operaciones LL(1):")
    stats(cyk_ops,   "Operaciones CYK:")

    # Speedup
    speedups = [c/l for c, l in zip(cyk_times, ll_times) if l > 0]
    if speedups:
        print(f"\n  Speedup LL(1) sobre CYK:")
        print(f"    Promedio: {statistics.mean(speedups):.2f}x más rápido")
        print(f"    Máximo:   {max(speedups):.2f}x más rápido")
        print(f"    Mínimo:   {min(speedups):.2f}x más rápido")

    print(f"""
  CONCLUSIÓN:
  ─ El parser LL(1) es consistentemente más rápido que CYK.
  ─ La ventaja se incrementa con expresiones más largas (O(n) vs O(n³)).
  ─ CYK ofrece mayor generalidad (acepta cualquier GLC en CNF).
  ─ LL(1) requiere una gramática sin ambigüedades y sin recursión izquierda.
  ─ Para una calculadora, LL(1) es la elección óptima en producción.
""")


# ---------------------------------------------------------------------------
# GENERACIÓN DE GRÁFICAS
# ---------------------------------------------------------------------------

def generate_plots(ll_results: list[dict], cyk_results: list[dict],
                   output_path: str):
    """Genera el panel de 4 gráficas comparativas."""

    labels      = [r["label"] for r in ll_results]
    ns          = [r["n_tokens"] for r in ll_results]
    ll_times    = [r["time_mean_us"] for r in ll_results]
    cyk_times   = [r["time_mean_us"] for r in cyk_results]
    ll_ops      = [r["ops_mean"]  for r in ll_results]
    cyk_ops     = [r["ops_mean"]  for r in cyk_results]
    ll_std      = [r["time_std_us"] for r in ll_results]
    cyk_std     = [r["time_std_us"] for r in cyk_results]
    ratios      = [c/l for c, l in zip(cyk_times, ll_times)]

    # Estilo oscuro profesional
    plt.style.use("dark_background")
    COLORS = {
        "ll":     "#00D4FF",   # cian brillante
        "cyk":    "#FF6B35",   # naranja
        "ratio":  "#FFD700",   # dorado
        "ops_ll": "#7CFC00",   # verde
        "ops_cyk":"#FF4081",   # rosa
        "grid":   "#333355",
    }

    fig = plt.figure(figsize=(18, 14), facecolor="#0D0D1A")
    fig.suptitle(
        "Análisis Comparativo de Rendimiento: Parser CYK vs Parser Predictivo LL(1)\n"
        "Lenguajes de Programación — Parcial 2, 2026-1",
        fontsize=16, fontweight="bold", color="white", y=0.98
    )

    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 0])
    ax4 = fig.add_subplot(gs[1, 1])

    def style_ax(ax, title, xlabel, ylabel):
        ax.set_facecolor("#0D0D2E")
        ax.set_title(title, fontsize=11, color="white", pad=10, fontweight="bold")
        ax.set_xlabel(xlabel, color="#AAAACC", fontsize=9)
        ax.set_ylabel(ylabel, color="#AAAACC", fontsize=9)
        ax.tick_params(colors="#AAAACC", labelsize=7)
        ax.spines[:].set_color("#334455")
        ax.grid(color=COLORS["grid"], linestyle="--", linewidth=0.5, alpha=0.7)

    x = np.arange(len(labels))
    bar_w = 0.38

    # ── Gráfica 1: Tiempos medios por expresión (barras) ──────────────────
    bars1 = ax1.bar(x - bar_w/2, ll_times,  bar_w, label="LL(1)",
                    color=COLORS["ll"],  alpha=0.85, zorder=3)
    bars2 = ax1.bar(x + bar_w/2, cyk_times, bar_w, label="CYK",
                    color=COLORS["cyk"], alpha=0.85, zorder=3)
    ax1.errorbar(x - bar_w/2, ll_times,  yerr=ll_std,  fmt="none",
                 ecolor="white", elinewidth=1, capsize=3, alpha=0.6)
    ax1.errorbar(x + bar_w/2, cyk_times, yerr=cyk_std, fmt="none",
                 ecolor="white", elinewidth=1, capsize=3, alpha=0.6)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=45, ha="right", fontsize=6.5)
    ax1.legend(fontsize=9, facecolor="#1A1A2E", labelcolor="white")
    style_ax(ax1, "① Tiempo Medio de Ejecución por Expresión",
             "Expresión de prueba", "Tiempo (μs)")

    # ── Gráfica 2: Tiempo vs Nº de Tokens (dispersión + ajuste) ──────────
    ax2.scatter(ns, ll_times,  color=COLORS["ll"],  s=60, zorder=4,
                label="LL(1)", alpha=0.9, edgecolors="white", linewidths=0.5)
    ax2.scatter(ns, cyk_times, color=COLORS["cyk"], s=60, zorder=4,
                label="CYK",   alpha=0.9, edgecolors="white", linewidths=0.5)

    # Ajuste polinomial para visualizar la tendencia
    if len(set(ns)) > 2:
        xs = np.array(sorted(set(ns)))
        # Ajuste lineal para LL(1)
        c1 = np.polyfit(ns, ll_times, 1)
        ys_ll = np.polyval(c1, xs)
        ax2.plot(xs, ys_ll,  "--", color=COLORS["ll"],  alpha=0.6, linewidth=1.5)
        # Ajuste cúbico para CYK
        try:
            c3 = np.polyfit(ns, cyk_times, 3)
            ys_cyk = np.polyval(c3, xs)
            ax2.plot(xs, ys_cyk, "--", color=COLORS["cyk"], alpha=0.6, linewidth=1.5)
        except Exception:
            pass

    ax2.legend(fontsize=9, facecolor="#1A1A2E", labelcolor="white")
    style_ax(ax2, "② Tiempo vs Longitud de Entrada (Tokens)",
             "Número de tokens", "Tiempo (μs)")

    # ── Gráfica 3: Ratio CYK/LL(1) ────────────────────────────────────────
    colors_bar = [COLORS["ratio"] if r < 5 else "#FF4444" for r in ratios]
    bars3 = ax3.bar(x, ratios, color=colors_bar, alpha=0.85, zorder=3,
                    edgecolor="#555577", linewidth=0.5)
    ax3.axhline(y=1.0, color="white", linestyle="--", linewidth=1, alpha=0.5,
                label="Ratio = 1 (igual)")
    ax3.axhline(y=statistics.mean(ratios), color="#FF8C00", linestyle=":",
                linewidth=1.5, alpha=0.8,
                label=f"Media = {statistics.mean(ratios):.2f}x")
    ax3.set_xticks(x)
    ax3.set_xticklabels(labels, rotation=45, ha="right", fontsize=6.5)
    ax3.legend(fontsize=8, facecolor="#1A1A2E", labelcolor="white")
    for bar, r in zip(bars3, ratios):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                 f"{r:.1f}x", ha="center", va="bottom", fontsize=6,
                 color="white", fontweight="bold")
    style_ax(ax3, "③ Factor de Ralentización CYK respecto a LL(1)",
             "Expresión de prueba", "Ratio (CYK tiempo / LL tiempo)")

    # ── Gráfica 4: Conteo de Operaciones ──────────────────────────────────
    ax4.plot(x, ll_ops,  "o-", color=COLORS["ops_ll"],  linewidth=2,
             markersize=6, label="LL(1) ops", zorder=4)
    ax4.plot(x, cyk_ops, "s-", color=COLORS["ops_cyk"], linewidth=2,
             markersize=6, label="CYK ops",   zorder=4)
    ax4.fill_between(x, ll_ops,  alpha=0.15, color=COLORS["ops_ll"])
    ax4.fill_between(x, cyk_ops, alpha=0.15, color=COLORS["ops_cyk"])
    ax4.set_xticks(x)
    ax4.set_xticklabels(labels, rotation=45, ha="right", fontsize=6.5)
    ax4.legend(fontsize=9, facecolor="#1A1A2E", labelcolor="white")
    style_ax(ax4, "④ Conteo de Operaciones Elementales",
             "Expresión de prueba", "Número de operaciones")

    # Anotación de complejidad
    fig.text(0.5, 0.01,
             "LL(1): O(n)  —  una pasada lineal     │     "
             "CYK: O(n³·|G|)  —  tabla dinámica triangular     │     "
             f"Repeticiones: {REPS} por benchmark",
             ha="center", fontsize=9, color="#AAAACC",
             style="italic")

    plt.savefig(output_path, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close()
    print(f"\n  Gráfica guardada en: {output_path}\n")


# ---------------------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------------

def main():
    header("COMPARACIÓN DE PARSERS: CYK vs LL(1) — CALCULADORA ARITMÉTICA")

    print(f"  Número de expresiones de prueba : {len(TEST_SUITE)}")
    print(f"  Repeticiones por benchmark      : {REPS}")
    print(f"  Parsers evaluados               : CYK (O(n³)) y LL(1) (O(n))")

    # 1. Verificación de correctitud
    print_correctness_check()

    # 2. Benchmarks
    section("EJECUTANDO BENCHMARKS")
    ll_results, cyk_results = run_benchmarks()

    # 3. Tabla comparativa
    print_results_table(ll_results, cyk_results)

    # 4. Análisis de complejidad
    print_complexity_analysis(ll_results, cyk_results)

    # 5. Resumen estadístico
    print_statistical_summary(ll_results, cyk_results)

    # 6. Gráficas
    section("GENERANDO GRÁFICAS")
    plot_path = "/home/julian/parcial2/punto4/benchmark_results.png"
    generate_plots(ll_results, cyk_results, plot_path)

    header("FIN DEL ANÁLISIS")
    print("  Archivos generados:")
    print(f"    - benchmark_results.png  (panel de 4 gráficas)")
    print()


if __name__ == "__main__":
    main()
