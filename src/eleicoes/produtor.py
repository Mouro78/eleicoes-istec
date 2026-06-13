"""
Produtor de votos para o simulador de Eleições Legislativas Portuguesas.

Lê data/freguesias.csv, gera votos aleatórios por freguesia e envia
os resultados ao Servidor CNE via HTTP POST.

Uso:
    python src/eleicoes/produtor.py
"""

import csv
import random
import os
import json
import urllib.request
import urllib.error

from eleicoes.dominio.partido import Partido
from eleicoes.dominio.freguesia import Freguesia
from eleicoes.dominio.concelho import Concelho
from eleicoes.dominio.distrito import Distrito

# Seed fixa para resultados reprodutíveis
SEED = 42

# Ficheiro de dados
FICHEIRO_CSV = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "freguesias.csv"
)

# URL do servidor CNE
URL_SERVIDOR = "http://localhost:8000/resultados"

# Partidos concorrentes nas legislativas 2024
PARTIDOS = [
    Partido("AD",  "Aliança Democrática"),
    Partido("PS",  "Partido Socialista"),
    Partido("CH",  "Chega"),
    Partido("IL",  "Iniciativa Liberal"),
    Partido("BE",  "Bloco de Esquerda"),
    Partido("CDU", "Coligação Democrática Unitária"),
    Partido("L",   "Livre"),
    Partido("PAN", "Pessoas-Animais-Natureza"),
    Partido("ADN", "Alternativa Democrática Nacional"),
    Partido("RIR", "Reagir Incluir Reciclar"),
]


def distribuir_votos_partidos(votos_validos, partidos, rng):
    """Distribui votos válidos proporcionalmente pelos partidos."""
    pesos = [rng.random() for _ in partidos]
    total_pesos = sum(pesos)

    votos_partido = {}
    votos_distribuidos = 0
    for i, partido in enumerate(partidos[:-1]):
        votos = int(votos_validos * pesos[i] / total_pesos)
        votos_partido[partido.obter_sigla()] = votos
        votos_distribuidos += votos

    ultimo = partidos[-1].obter_sigla()
    votos_partido[ultimo] = votos_validos - votos_distribuidos
    return votos_partido


def gerar_votos_freguesia(eleitores, partidos, rng):
    """Gera votos aleatórios para uma freguesia."""
    taxa_participacao = rng.uniform(0.40, 0.75)
    total_votantes = int(eleitores * taxa_participacao)
    brancos = int(total_votantes * rng.uniform(0.01, 0.05))
    nulos = int(total_votantes * rng.uniform(0.01, 0.05))
    votos_validos = total_votantes - brancos - nulos
    votos_partido = distribuir_votos_partidos(votos_validos, partidos, rng)
    return votos_partido, brancos, nulos


def carregar_csv(ficheiro):
    """Lê o CSV e devolve lista de dicts com os dados de cada freguesia."""
    with open(ficheiro, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def enviar_resultado(dados):
    """Envia os resultados de uma freguesia ao Servidor CNE via POST."""
    corpo = json.dumps(dados).encode("utf-8")
    pedido = urllib.request.Request(URL_SERVIDOR, data=corpo, method="POST")
    pedido.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(pedido) as resposta:
            return resposta.status == 200
    except urllib.error.HTTPError as e:
        print(f"  Erro HTTP {e.code} na freguesia {dados['nome_freguesia']}")
        return False
    except urllib.error.URLError as e:
        print(f"  Erro de ligação: {e.reason}")
        return False


def construir_hierarquia(linhas, partidos, rng):
    """Constrói a hierarquia e envia cada freguesia ao Servidor CNE via POST."""
    distritos = {}
    concelhos = {}
    enviados = 0
    erros = 0

    for linha in linhas:
        cod_distrito = linha["codigo_distrito"]
        cod_concelho = linha["codigo_concelho"]
        cod_freguesia = linha["codigo_freguesia"]
        eleitores = int(linha["eleitores"])

        if cod_distrito not in distritos:
            distritos[cod_distrito] = Distrito(cod_distrito, linha["distrito"])

        if cod_concelho not in concelhos:
            concelho = Concelho(cod_concelho, linha["concelho"])
            concelhos[cod_concelho] = concelho
            distritos[cod_distrito].adicionar_concelho(concelho)

        freguesia = Freguesia(cod_freguesia, linha["freguesia"], eleitores)
        votos_partido, brancos, nulos = gerar_votos_freguesia(eleitores, partidos, rng)
        freguesia.registar_resultado(votos_partido, brancos, nulos)
        concelhos[cod_concelho].adicionar_freguesia(freguesia)

        dados = {
            "codigo_freguesia":    cod_freguesia,
            "nome_freguesia":      linha["freguesia"],
            "distrito":            linha["distrito"],
            "concelho":            linha["concelho"],
            "eleitores_inscritos": eleitores,
            "votos_partido":       votos_partido,
            "votos_brancos":       brancos,
            "votos_nulos":         nulos,
        }

        if enviar_resultado(dados):
            enviados += 1
        else:
            erros += 1

    print(f"\nEnviados: {enviados} | Erros: {erros}")
    return distritos


def simular_eleicao(ficheiro_csv=None, partidos=None, seed=SEED):
    """Simula uma eleição legislativa completa."""
    if ficheiro_csv is None:
        ficheiro_csv = FICHEIRO_CSV
    if partidos is None:
        partidos = PARTIDOS

    rng = random.Random(seed)
    linhas = carregar_csv(ficheiro_csv)
    return construir_hierarquia(linhas, partidos, rng)


def main():
    """Ponto de entrada — simula e envia resultados ao Servidor CNE."""
    print("A simular eleição legislativa e a enviar ao Servidor CNE...\n")
    simular_eleicao()


if __name__ == "__main__":
    main()