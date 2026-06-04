# pylint: disable=import-error
import pytest
from eleicoes.dominio.partido import Partido


# ---------- Construção e validações ----------

def test_cria_partido_com_sigla_e_nome():
    """Verifica que o construtor guarda sigla e nome."""
    partido = Partido("PS", "Partido Socialista")
    assert partido.obter_sigla() == "PS"
    assert partido.obter_nome() == "Partido Socialista"


def test_sigla_vazia_levanta_erro():
    """Verifica que uma sigla vazia é recusada."""
    with pytest.raises(ValueError):
        Partido("", "Partido Socialista")


def test_sigla_so_com_espacos_levanta_erro():
    """Verifica que uma sigla só com espaços é recusada."""
    with pytest.raises(ValueError):
        Partido("   ", "Partido Socialista")


def test_nome_vazio_levanta_erro():
    """Verifica que um nome vazio é recusado."""
    with pytest.raises(ValueError):
        Partido("PS", "")


def test_nome_so_com_espacos_levanta_erro():
    """Verifica que um nome só com espaços é recusado."""
    with pytest.raises(ValueError):
        Partido("PS", "    ")


# ---------- Normalização ----------

def test_sigla_minusculas_e_convertida_para_maiusculas():
    """Verifica que a sigla é convertida para maiúsculas."""
    partido = Partido("ps", "Partido Socialista")
    assert partido.obter_sigla() == "PS"


def test_espacos_a_volta_do_nome_sao_removidos():
    """Verifica que os espaços à volta do nome são removidos."""
    partido = Partido("PS ", " Partido Socialista ")
    assert partido.obter_nome() == "Partido Socialista"


def test_nome_mantem_capitalizacao():
    """Verifica que o nome mantém a capitalização original."""
    partido = Partido("PS", "Partido Socialista")
    assert partido.obter_nome() == "Partido Socialista"


def test_espacos_a_volta_da_sigla_sao_removidos():
    """Verifica que os espaços à volta da sigla são removidos."""
    partido = Partido(" PS ", "Partido Socialista")
    assert partido.obter_sigla() == "PS"


# ---------- Igualdade (__eq__) ----------

def test_dois_partidos_iguais():
    """Verifica que partidos com a mesma sigla são iguais."""
    p1 = Partido("PS", "Partido Socialista")
    p2 = Partido("PS", "Partido Socialista")
    assert p1 == p2


def test_dois_partidos_com_siglas_differentes_nao_sao_iguais():
    """Verifica que partidos com siglas diferentes não são iguais."""
    p1 = Partido("PS", "Partido Socialista")
    p2 = Partido("PSD", "Partido Social Democrata")
    assert p1 != p2


def test_normalizacao_afeta_igualdade():
    """Verifica que a normalização da sigla afeta a igualdade."""
    p1 = Partido("PS", "Partido Socialista")
    p2 = Partido("ps", "Partido Socialista")
    assert p1 == p2


def test_sigla_igual_nome_diferente():
    """Verifica que a identidade depende só da sigla, não do nome."""
    p1 = Partido("PS", "Partido Socialista")
    p2 = Partido("PS", "Pedro Sousa")
    assert p1 == p2


def test_partido_nao_e_igual_a_outro_tipo():
    """Verifica que um partido não é igual a objetos de outro tipo."""
    partido = Partido("PS", "Partido Socialista")
    assert partido != "PS"
    assert partido != 42


# ---------- Hash (__hash__) ----------

def test_partidos_iguais_tem_mesmo_hash():
    """Verifica que partidos iguais têm o mesmo hash."""
    p1 = Partido("PS", "Partido Socialista")
    p2 = Partido("PS", "Partido Socialista")
    assert hash(p1) == hash(p2)


# ---------- Representações (__str__ e __repr__) ----------

def test_str_devolve_sigla_e_nome():
    """Verifica a representação amigável (str) do partido."""
    partido = Partido("PS", "Partido Socialista")
    assert str(partido) == "PS - Partido Socialista"


def test_repr_formato_tecnico():
    """Verifica a representação técnica (repr) do partido."""
    partido = Partido("PS", "Partido Socialista")
    assert repr(partido) == "Partido(sigla='PS', nome='Partido Socialista')"
