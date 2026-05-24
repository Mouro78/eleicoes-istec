import pytest
from eleicoes.dominio.partido import Partido


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

