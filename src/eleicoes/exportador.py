"""
Exportador de resultados eleitorais para XLS e gráfico.

Lê o ficheiro data/resultados.json e gera:
- data/resultados.xlsx  (3 folhas: Totais, Partidos, Distritos)
- data/grafico.png      (gráfico de barras dos votos por partido)

Uso:
    python src/eleicoes/exportador.py
"""

import json
import os
import pandas as pd
import matplotlib.pyplot as plt

FICHEIRO_RESULTADOS = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "resultados.json"
)

FICHEIRO_EXCEL = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "resultados.xlsx"
)

FICHEIRO_GRAFICO = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "grafico.png"
)


def carregar_resultados():
    """Lê o ficheiro JSON de resultados."""
    if not os.path.exists(FICHEIRO_RESULTADOS):
        raise FileNotFoundError(f"Ficheiro não encontrado: {FICHEIRO_RESULTADOS}")
    with open(FICHEIRO_RESULTADOS, encoding="utf-8") as f:
        return json.load(f)


def calcular_totais(resultados):
    """Soma todos os votos de todas as freguesias (totais nacionais)."""
    totais = {"brancos": 0, "nulos": 0}
    for freguesia in resultados.values():
        for partido, votos in freguesia["votos_partido"].items():
            totais[partido] = totais.get(partido, 0) + votos
        totais["brancos"] += freguesia["votos_brancos"]
        totais["nulos"] += freguesia["votos_nulos"]
    return totais


def calcular_distritos(resultados):
    """Agrupa os votos por distrito."""
    distritos = {}
    for freguesia in resultados.values():
        nome_distrito = freguesia["distrito"]
        if nome_distrito not in distritos:
            distritos[nome_distrito] = {"brancos": 0, "nulos": 0}
        for partido, votos in freguesia["votos_partido"].items():
            distritos[nome_distrito][partido] = (
                distritos[nome_distrito].get(partido, 0) + votos
            )
        distritos[nome_distrito]["brancos"] += freguesia["votos_brancos"]
        distritos[nome_distrito]["nulos"] += freguesia["votos_nulos"]
    return distritos


def exportar_excel(resultados):
    """Exporta os resultados para ficheiro Excel com 3 folhas."""

    totais = calcular_totais(resultados)
    total_votos = sum(totais.values())

    # --- Folha 1: Totais Nacionais ---
    df_totais = pd.DataFrame(
        list(totais.items()),
        columns=["Partido", "Votos"]
    )
    df_totais = df_totais.sort_values("Votos", ascending=False).reset_index(drop=True)

    # --- Folha 2: Partidos com percentagem ---
    df_partidos = df_totais.copy()
    df_partidos["Percentagem (%)"] = (
        df_partidos["Votos"] / total_votos * 100
    ).round(2)

    # --- Folha 3: Distritos ---
    distritos = calcular_distritos(resultados)
    df_distritos = pd.DataFrame(distritos).T
    df_distritos.index.name = "Distrito"
    df_distritos = df_distritos.fillna(0).astype(int)
    df_distritos = df_distritos.reset_index()

    # Guardar as 3 folhas no mesmo ficheiro Excel
    with pd.ExcelWriter(FICHEIRO_EXCEL, engine="openpyxl") as writer:
        df_totais.to_excel(writer, sheet_name="Totais", index=False)
        df_partidos.to_excel(writer, sheet_name="Partidos", index=False)
        df_distritos.to_excel(writer, sheet_name="Distritos", index=False)

    print(f"Excel gerado: {FICHEIRO_EXCEL}")


def exportar_grafico(resultados):
    """Gera gráfico de barras com votos por partido."""

    totais = calcular_totais(resultados)

    # Separar partidos de brancos/nulos
    partidos = {k: v for k, v in totais.items() if k not in ("brancos", "nulos")}
    partidos_ordenados = sorted(partidos.items(), key=lambda x: x[1], reverse=True)

    siglas = [p[0] for p in partidos_ordenados]
    votos = [p[1] for p in partidos_ordenados]
    total = sum(votos)
    percentagens = [v / total * 100 for v in votos]

    # Criar gráfico
    fig, ax = plt.subplots(figsize=(12, 6))
    barras = ax.bar(siglas, votos, color="steelblue")

    # Percentagem em cima de cada barra
    for barra, pct in zip(barras, percentagens):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height() + max(votos) * 0.01,
            f"{pct:.1f}%",
            ha="center", va="bottom", fontsize=9
        )

    ax.set_title("Eleições Legislativas — Votos por Partido", fontsize=14)
    ax.set_xlabel("Partido")
    ax.set_ylabel("Votos")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))

    plt.tight_layout()
    plt.savefig(FICHEIRO_GRAFICO, dpi=150)
    plt.close()

    print(f"Gráfico gerado: {FICHEIRO_GRAFICO}")


def main():
    """Ponto de entrada — gera Excel e gráfico a partir do resultados.json."""
    print("A exportar resultados...\n")
    resultados = carregar_resultados()
    exportar_excel(resultados)
    exportar_grafico(resultados)
    print("\nExportação concluída!")


if __name__ == "__main__":
    main()
