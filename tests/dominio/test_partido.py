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
# ----------- Grupo 1 --- Testes de __eq__ (igualdade) -----------------

def test_dois_partidos_iguais():
    p1 = Partido("PS", "Partido Socialista")
    p2 = Partido("PS", "Partido Socialista")
    assert p1 == p2

def test_dois_partidos_com_siglas_differentes_nao_sao_iguais():
    p1 = Partido("PS", "Partido Socialista")
    p2 = Partido("PSD", "Partido Social Democrata")
    assert p1 != p2

def test_normalizacao_afeta_igualdade():
    p1 = Partido("PS","Partido Socialista")
    p2 = Partido("ps","Partido Socialista")
    assert p1 == p2

def test_sigla_igual_nome_diferente():
    p1 = Partido("PS","Partido Socialista")
    p2 = Partido("PS","Pedro Sousa")
    assert p1 == p2

def test_partido_nao_e_igual_a_outro_tipo():
    partido = Partido("PS", "Partido Socialista")
    assert partido != "PS"
    assert partido != 42
    assert partido != None
#----------------------- Grupo 2 — Teste de __hash__ ----------------------
def test_partidos_iguais_tem_mesmo_hash():
    p1 = Partido("PS", "Partido Socialista")
    p2 = Partido("PS", "Partido Socialista")
    assert hash(p1) == hash(p2)


#----------------------  Grupo 3 — Testes de __str__ e __repr__-------------

def test_str_devolve_sigla_e_nome():
    partido = Partido("PS", "Partido Socialista")
    assert str(partido) == "PS - Partido Socialista"

def test_repr_formato_tecnico():
    partido = Partido("PS", "Partido Socialista")
    assert repr(partido) == "Partido(sigla='PS', nome='Partido Socialista')"
