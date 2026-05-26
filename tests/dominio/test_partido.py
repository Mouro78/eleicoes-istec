import pytest
from eleicoes.dominio.partido import Partido

# ---------- Construção e validações  ----------

def test_cria_partido_com_sigla_e_nome():
    partido = Partido("PS", "Partido Socialista")
    assert partido.obter_sigla() == "PS"
    assert partido.obter_nome() == "Partido Socialista"

def test_sigla_vazia_levanta_erro():
    with pytest.raises(ValueError):
        Partido("", "Partido Socialista")

def test_sigla_so_com_espacos_levanta_erro():
    with pytest.raises(ValueError):
        Partido("   ", "Partido Socialista")

def test_nome_vazio_levanta_erro():
    with pytest.raises(ValueError):
        Partido("PS", "")

def test_nome_so_com_espacos_levanta_erro():
    with pytest.raises(ValueError):
        Partido("PS", "    ")
# ---------- Normalização (NOVOS) ----------

def test_sigla_minusculas_e_convertida_para_maiusculas():
    partido = Partido("ps", "Partido Socialista")
    assert partido.obter_sigla() == 'PS'

def test_espacos_a_volta_do_nome_sao_removidos():
    partido = Partido ("PS ", " Partido Socialista " )
    assert partido.obter_nome() == "Partido Socialista"

def test_nome_mantem_capitalizacao():
    partido = Partido ("PS", "Partido Socialista")
    assert partido.obter_nome() == "Partido Socialista"

def test_espacos_a_volta_da_sigla_sao_removidos():
    partido = Partido(" PS ", "Partido Socialista")
    assert partido.obter_sigla() == "PS"
