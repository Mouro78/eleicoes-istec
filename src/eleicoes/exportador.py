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

## Caminho para o ficheiro JSON com os resultados recebidos do Produtor

FICHEIRO_RESULTADOS = os.path.join( #a pasta onde este ficheiro está" (src/eleicoes/)
    os.path.dirname(__file__), "..", "..", "data", "resultados.json"
)

# Caminho para o ficheiro Excel gerado com os resultados eleitorais
FICHEIRO_EXCEL = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "resultados.xlsx"
)

# Caminho para o ficheiro de imagem com o gráfico de barras por partido
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
    """Agrupa os votos por distrito de forma segura."""
    distritos = {}
    for freguesia in resultados.values():
        nome_distrito = freguesia.get("distrito", "Distrito " + freguesia["codigo_freguesia"][:2])

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
    """Exporta os resultados para ficheiro Excel com 3 folhas (Exigido em Aula)."""
    totais = calcular_totais(resultados)

    # --- Folha 1: Totais Nacionais ---
    df_totais = pd.DataFrame(
        list(totais.items()),
        columns=["Partido/Registo", "Votos"]
    )
    df_totais = df_totais.sort_values("Votos", ascending=False).reset_index(drop=True)

    # --- Folha 2: Partidos com percentagem real (excluindo brancos/nulos do bolo partidário) ---
    partidos_puros = {k: v for k, v in totais.items() if k not in ("brancos", "nulos")}
    total_votos_partidos = sum(partidos_puros.values())

    df_partidos = pd.DataFrame(list(partidos_puros.items()), columns=["Partido", "Votos"])
    df_partidos = df_partidos.sort_values("Votos", ascending=False).reset_index(drop=True)
    df_partidos["Percentagem (%)"] = (
        df_partidos["Votos"] / total_votos_partidos * 100
    ).round(2)

    # --- Folha 3: Distritos ---
    distritos = calcular_distritos(resultados)
    df_distritos = pd.DataFrame(distritos).T
    df_distritos.index.name = "Distrito"
    df_distritos = df_distritos.fillna(0).astype(int)
    df_distritos = df_distritos.reset_index()

    # Guardar as 3 folhas no mesmo ficheiro Excel usando openpyxl
    with pd.ExcelWriter(FICHEIRO_EXCEL, engine="openpyxl") as writer:
        df_totais.to_excel(writer, sheet_name="Totais", index=False)
        df_partidos.to_excel(writer, sheet_name="Partidos", index=False)
        df_distritos.to_excel(writer, sheet_name="Distritos", index=False)

    print(f"Excel gerado com sucesso: {FICHEIRO_EXCEL}")


def exportar_grafico(resultados):
    """Gera gráfico de barras com votos por partido (Matplotlib)."""
    totais = calcular_totais(resultados)

    # Separar partidos de brancos/nulos
    partidos = {k: v for k, v in totais.items() if k not in ("brancos", "nulos")}
    partidos_ordenados = sorted(partidos.items(), key=lambda x: x[1], reverse=True)

    siglas = [p[0] for p in partidos_ordenados]
    votos = [p[1] for p in partidos_ordenados]
    total = sum(votos)
    percentagens = [v / total * 100 for v in votos]

    # Criar gráfico (Uso de subplots ensinado na Sessão 14/15)
    fig, ax = plt.subplots(figsize=(12, 6))
    barras = ax.bar(siglas, votos, color="steelblue", edgecolor="black")

    # Percentagem em cima de cada barra
    for barra, pct in zip(barras, percentagens):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height() + max(votos) * 0.01,
            f"{pct:.1f}%",
            ha="center", va="bottom", fontsize=9, fontweight="bold"
        )

    ax.set_title("Eleições Legislativas — Votos por Partido", fontsize=14, fontweight="bold")
    ax.set_xlabel("Partido", fontsize=11)
    ax.set_ylabel("Votos", fontsize=11)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(FICHEIRO_GRAFICO, dpi=150)
    plt.close()

    print(f"Gráfico gerado com sucesso: {FICHEIRO_GRAFICO}")


def main():
    """Ponto de entrada — gera Excel e gráfico a partir do resultados.json."""
    print("A exportar resultados...\n")
    try:
        resultados = carregar_resultados()
        exportar_excel(resultados)
        exportar_grafico(resultados)
        print("\nExportação concluída com absoluto sucesso!")
    except FileNotFoundError as e:
        print(f"[ERRO] {e}")


if __name__ == "__main__":
    main()
