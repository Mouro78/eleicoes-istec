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
import requests  # <-- Nova importação para comunicar com o servidor

from eleicoes.dominio.partido import Partido
from eleicoes.dominio.freguesia import Freguesia
from eleicoes.dominio.concelho import Concelho
from eleicoes.dominio.distrito import Distrito

# Seed fixa para resultados reprodutíveis (mesma que o gerar_csv.py)
SEED = 42
URL_SERVIDOR = "http://127.0.0.1:8000"  # <-- Endereço do teu servidor CNE

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
    pesos = []
    for _ in partidos:
        pesos.append(rng.random())
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


def construir_hierarquia(linhas, partidos, rng):
    """Constrói a hierarquia e envia os dados de cada freguesia para o servidor CNE."""
    distritos = {}
    concelhos = {}

    print("A enviar dados das freguesias para o servidor...")

    for linha in linhas:
        cod_distrito = linha["codigo_distrito"]
        cod_concelho = linha["codigo_concelho"]
        cod_freguesia = linha["codigo_freguesia"]
        eleitores = int(linha["eleitores"])

        # Criar Distrito se ainda não existe
        if cod_distrito not in distritos:
            distritos[cod_distrito] = Distrito(cod_distrito, linha["distrito"])

        # Criar Concelho se ainda não existe
        if cod_concelho not in concelhos:
            concelho = Concelho(cod_concelho, linha["concelho"])
            concelhos[cod_concelho] = concelho
            distritos[cod_distrito].adicionar_concelho(concelho)

        # Criar Freguesia e registar votos
        freguesia = Freguesia(cod_freguesia, linha["freguesia"], eleitores)
        (votos_partido, brancos, nulos) = gerar_votos_freguesia(eleitores, partidos, rng)
        freguesia.registar_resultado(votos_partido, brancos, nulos)
        concelhos[cod_concelho].adicionar_freguesia(freguesia)

        # --- NOVA LÓGICA: Enviar dados via HTTP POST para o servidor ---
        dados_freguesia = {
            "codigo_freguesia": cod_freguesia,
            "nome_freguesia": linha["freguesia"],
            "distrito": linha["distrito"],
            "eleitores_inscritos": eleitores,
            "votos_partido": votos_partido,
            "votos_brancos": brancos,
            "votos_nulos": nulos
        }

        try:
            requests.post(URL_SERVIDOR, json=dados_freguesia)
        except requests.exceptions.ConnectionError:
            # Se o servidor não estiver ligado, avisa e para para não inundar o terminal
            print("\n[ERRO] Não foi possível ligar ao Servidor CNE! Certifica-te de que está ativo na porta 8000.")
            return distritos

    print("Envio concluído com sucesso!\n")
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
