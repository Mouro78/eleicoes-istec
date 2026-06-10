"""
Produtor de votos para o simulador de Eleições Legislativas Portuguesas.

Lê data/freguesias.csv, gera votos aleatórios por freguesia e constrói
a hierarquia completa Distrito -> Concelho -> Freguesia com resultados.

Uso:
    python src/produtor.py
"""

import csv
import random
import os

from eleicoes.dominio.partido import Partido
from eleicoes.dominio.freguesia import Freguesia
from eleicoes.dominio.concelho import Concelho
from eleicoes.dominio.distrito import Distrito

# Seed fixa para resultados reprodutíveis (mesma que o gerar_csv.py)
SEED = 42

# Ficheiro de dados
FICHEIRO_CSV = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "freguesias.csv"
)

# Partidos concorrentes nas legislativas 2024
PARTIDOS = [
    Partido("AD",    "Aliança Democrática"),
    Partido("PS",    "Partido Socialista"),
    Partido("CH",    "Chega"),
    Partido("IL",    "Iniciativa Liberal"),
    Partido("BE",    "Bloco de Esquerda"),
    Partido("CDU",   "Coligação Democrática Unitária"),
    Partido("L",     "Livre"),
    Partido("PAN",   "Pessoas-Animais-Natureza"),
    Partido("ADN",   "Alternativa Democrática Nacional"),
    Partido("RIR",   "Reagir Incluir Reciclar"),
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
    """
    Gera votos aleatórios para uma freguesia.

    Args:
        eleitores (int): Número de eleitores inscritos.
        partidos (list): Lista de instâncias de Partido.
        rng (random.Random): Gerador de números aleatórios.

    Returns:
        tuple: (votos_partido, brancos, nulos)
    """
    x=0.01 #mnbmnbmnbmnbmnbmnb
    taxa_participacao = rng.uniform(0.40, 0.75)
    total_votantes = int(eleitores * taxa_participacao)
    brancos = int(total_votantes * rng.uniform(0.01, 0.05))
    nulos = int(total_votantes * rng.uniform(0.01, 0.05))
    votos_validos = total_votantes - brancos - nulos
    votos_partido = distribuir_votos_partidos(votos_validos, partidos, rng)
    return votos_partido, brancos, nulos


def carregar_csv(ficheiro):
    """
    Lê o CSV e devolve lista de dicts com os dados de cada freguesia.

    Args:
        ficheiro (str): Caminho para o ficheiro CSV.

    Returns:
        list: Lista de dicts com as colunas do CSV.
    """
    with open(ficheiro, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def construir_hierarquia(linhas, partidos, rng):
    """
    Constrói a hierarquia de Distritos -> Concelhos -> Freguesias
    com votos simulados.

    Args:
        linhas (list): Linhas do CSV.
        partidos (list): Lista de instâncias de Partido.
        rng (random.Random): Gerador de números aleatórios.

    Returns:
        dict: {codigo_distrito: Distrito} com toda a hierarquia.
    """
    distritos = {}
    concelhos = {}

    for linha in linhas:
        cod_distrito = linha["codigo_distrito"]
        cod_concelho = linha["codigo_concelho"]
        cod_freguesia = linha["codigo_freguesia"]
        eleitores = int(linha["eleitores"])

        # Criar Distrito se ainda não existe
        if cod_distrito not in distritos:
            distritos[cod_distrito] = Distrito(
                cod_distrito, linha["distrito"]
            )

        # Criar Concelho se ainda não existe
        if cod_concelho not in concelhos:
            concelho = Concelho(cod_concelho, linha["concelho"])
            concelhos[cod_concelho] = concelho
            distritos[cod_distrito].adicionar_concelho(concelho)

        # Criar Freguesia e registar votos
        freguesia = Freguesia(cod_freguesia, linha["freguesia"], eleitores)
        (votos_partido, brancos, nulos) = gerar_votos_freguesia(
            eleitores, partidos, rng
        )
        freguesia.registar_resultado(votos_partido, brancos, nulos)

        concelhos[cod_concelho].adicionar_freguesia(freguesia)

    return distritos


def simular_eleicao(ficheiro_csv=None, partidos=None, seed=SEED):
    """
    Simula uma eleição legislativa completa.

    Args:
        ficheiro_csv (str): Caminho para o CSV (usa o padrão se None).
        partidos (list): Lista de Partido (usa os de 2024 se None).
        seed (int): Seed para reprodutibilidade.

    Returns:
        dict: {codigo_distrito: Distrito} com resultados completos.
    """
    if ficheiro_csv is None:
        ficheiro_csv = FICHEIRO_CSV
    if partidos is None:
        partidos = PARTIDOS

    rng = random.Random(seed)
    linhas = carregar_csv(ficheiro_csv)
    return construir_hierarquia(linhas, partidos, rng)


def main():
    """Ponto de entrada — simula e mostra resumo dos resultados."""
    print("A simular eleição legislativa...\n")

    distritos = simular_eleicao()

    print(f"{'DISTRITO':<25} {'VENCEDOR':<8} {'VOTANTES':>10} {'ABSTENCAO':>10}")
    print("-" * 60)

    for distrito in distritos.values():
        try:
            vencedor = distrito.obter_vencedor()
        except ValueError:
            vencedor = "N/A"

        votantes = distrito.obter_total_votantes()
        abstencao = distrito.calcular_abstencao() * 100

        print(
            f"{distrito.obter_nome():<25} "
            f"{vencedor:<8} "
            f"{votantes:>10,} "
            f"{abstencao:>9.1f}%"
        )

    print(f"\nTotal de distritos: {len(distritos)}")


if __name__ == "__main__":
    main()
