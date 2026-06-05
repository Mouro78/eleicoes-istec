"""
Script para gerar dados/freguesias.csv a partir do JSON público de
distritos/concelhos/freguesias de Portugal.

Fonte: https://gist.github.com/tomahock/a6c07dd255d04499d8336237e35a4827
Eleitores inscritos: gerados aleatoriamente com seed fixa (reprodutível).

Uso:
    python dados/gerar_csv.py
"""

import csv
import json
import random
import urllib.request
import os

URL_JSON = (
    "https://gist.githubusercontent.com/tomahock/"
    "a6c07dd255d04499d8336237e35a4827/raw/"
    "861a6345dedc4292188bb71e39d0062318197fdf/"
    "distritos-concelhos-freguesias-Portugal.json"
)

FICHEIRO_SAIDA = os.path.join(os.path.dirname(__file__), "freguesias.csv")

# Intervalos realistas de eleitores por freguesia
ELEITORES_MIN = 200
ELEITORES_MAX = 50000

# Seed fixa para resultados reprodutíveis
SEED = 42


def descarregar_json(url):
    """Descarrega e devolve o JSON da URL fornecida."""
    with urllib.request.urlopen(url) as resposta:
        return json.loads(resposta.read().decode("utf-8"))


def construir_csv(dados, ficheiro_saida):
    """Constrói o CSV com a hierarquia completa e eleitores gerados."""
    random.seed(SEED)

    distrito_atual = None
    concelho_atual = None
    linhas = []

    for entrada in dados:
        nivel = entrada["level"]
        codigo = entrada["code"]
        nome = entrada["name"]

        if nivel == 1:
            distrito_atual = {"codigo": str(codigo), "nome": nome}

        elif nivel == 2:
            concelho_atual = {"codigo": str(codigo), "nome": nome}

        elif nivel == 3 and distrito_atual and concelho_atual:
            eleitores = random.randint(ELEITORES_MIN, ELEITORES_MAX)
            linhas.append({
                "codigo_distrito": distrito_atual["codigo"],
                "distrito": distrito_atual["nome"],
                "codigo_concelho": concelho_atual["codigo"],
                "concelho": concelho_atual["nome"],
                "codigo_freguesia": str(codigo),
                "freguesia": nome,
                "eleitores": eleitores,
            })

    cabecalho = [
        "codigo_distrito", "distrito",
        "codigo_concelho", "concelho",
        "codigo_freguesia", "freguesia",
        "eleitores",
    ]

    with open(ficheiro_saida, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=cabecalho)
        escritor.writeheader()
        escritor.writerows(linhas)

    return len(linhas)


def main():
    """Ponto de entrada do script."""
    print("A descarregar dados de Portugal...")
    dados = descarregar_json(URL_JSON)

    print("A gerar CSV...")
    total = construir_csv(dados, FICHEIRO_SAIDA)

    print(f"Concluído: {total} freguesias escritas em '{FICHEIRO_SAIDA}'")


if __name__ == "__main__":
    main()
