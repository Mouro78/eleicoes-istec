# pylint: disable=import-error
import pytest
from eleicoes.dominio.freguesia import Freguesia


# ---------- Construção e getters ----------

def test_cria_freguesia_com_dados_basicos():
    """Verifica que o construtor guarda código, nome e eleitores."""
    f = Freguesia("110611", "Marvila", 38542)
    assert f.obter_codigo() == "110611"
    assert f.obter_nome() == "Marvila"
    assert f.obter_eleitores_inscritos() == 38542


def test_freguesia_nova_nao_tem_votos():
    """Verifica que uma freguesia recém-criada começa sem votos."""
    f = Freguesia("110611", "Marvila", 38542)
    assert f.obter_total_votantes() == 0
    assert f.obter_votos_brancos() == 0
    assert f.obter_votos_nulos() == 0
    assert f.obter_votos_por_partido() == {}


# ---------- Registar resultado (válido) ----------

def test_registar_resultado_guarda_votos():
    """Verifica que os votos registados ficam corretamente guardados."""
    f = Freguesia("110611", "Marvila", 38542)
    f.registar_resultado({"PS": 8312, "PSD": 6201}, 412, 189)
    assert f.obter_votos_por_partido() == {"PS": 8312, "PSD": 6201}
    assert f.obter_votos_brancos() == 412
    assert f.obter_votos_nulos() == 189


def test_total_votantes_soma_tudo():
    """Verifica que o total soma votos de partidos, brancos e nulos."""
    f = Freguesia("110611", "Marvila", 38542)
    f.registar_resultado({"PS": 8312, "PSD": 6201}, 412, 189)
    assert f.obter_total_votantes() == 15114


# ---------- Validações ----------

def test_votos_de_partido_negativos_levanta_erro():
    """Verifica que votos negativos num partido são recusados."""
    f = Freguesia("110611", "Marvila", 38542)
    with pytest.raises(ValueError):
        f.registar_resultado({"PS": -50}, 0, 0)


def test_votos_brancos_negativos_levanta_erro():
    """Verifica que votos brancos negativos são recusados."""
    f = Freguesia("110611", "Marvila", 38542)
    with pytest.raises(ValueError):
        f.registar_resultado({"PS": 100}, -10, 0)


def test_votos_nulos_negativos_levanta_erro():
    """Verifica que votos nulos negativos são recusados."""
    f = Freguesia("110611", "Marvila", 38542)
    with pytest.raises(ValueError):
        f.registar_resultado({"PS": 100}, 0, -5)


def test_total_excede_inscritos_levanta_erro():
    """Verifica que o total de votos não pode exceder os inscritos."""
    f = Freguesia("110611", "Marvila", 100)
    with pytest.raises(ValueError):
        f.registar_resultado({"PS": 80, "PSD": 50}, 0, 0)


def test_nao_pode_registar_duas_vezes():
    """Verifica que não é possível registar resultados duas vezes."""
    f = Freguesia("110611", "Marvila", 38542)
    f.registar_resultado({"PS": 100}, 0, 0)
    with pytest.raises(RuntimeError):
        f.registar_resultado({"PSD": 50}, 0, 0)


# ---------- Cálculos ----------

def test_calcular_abstencao():
    """Verifica o cálculo correto da taxa de abstenção."""
    f = Freguesia("110611", "Marvila", 1000)
    f.registar_resultado({"PS": 400, "PSD": 200}, 0, 0)
    assert f.calcular_abstencao() == 0.4


def test_vencedor_e_partido_mais_votado():
    """Verifica que o vencedor é o partido com mais votos."""
    f = Freguesia("110611", "Marvila", 38542)
    f.registar_resultado({"PS": 8312, "PSD": 6201, "CH": 3104}, 0, 0)
    assert f.obter_vencedor() == "PS"


# ---------- Casos especiais ----------

def test_freguesia_sem_eleitores_abstencao_zero():
    """Verifica que abstenção é 0.0 quando não há eleitores inscritos."""
    f = Freguesia("000000", "Fantasma", 0)
    assert f.calcular_abstencao() == 0.0


def test_freguesia_sem_votos_nao_tem_vencedor():
    """Verifica que uma freguesia sem votos não tem vencedor."""
    f = Freguesia("110611", "Marvila", 38542)
    assert f.obter_vencedor() is None


# ---------- Dunder methods ----------

def test_freguesias_com_mesmo_codigo_sao_iguais():
    """Verifica que freguesias com o mesmo código são iguais."""
    f1 = Freguesia("110611", "Marvila", 38542)
    f2 = Freguesia("110611", "Marvila", 38542)
    assert f1 == f2


def test_freguesias_com_codigos_diferentes_nao_sao_iguais():
    """Verifica que freguesias com códigos diferentes não são iguais."""
    f1 = Freguesia("110611", "Marvila", 38542)
    f2 = Freguesia("110612", "Beato", 20000)
    assert f1 != f2


def test_freguesia_nao_e_igual_a_outro_tipo():
    """Verifica que uma freguesia não é igual a objetos de outro tipo."""
    f = Freguesia("110611", "Marvila", 38542)
    assert f != "110611"
    assert f != 42


def test_freguesias_iguais_tem_mesmo_hash():
    """Verifica que freguesias iguais têm o mesmo hash."""
    f1 = Freguesia("110611", "Marvila", 38542)
    f2 = Freguesia("110611", "Marvila", 38542)
    assert hash(f1) == hash(f2)


def test_str_mostra_nome_e_codigo():
    """Verifica a representação amigável (str) da freguesia."""
    f = Freguesia("110611", "Marvila", 38542)
    assert str(f) == "Marvila (110611)"


def test_repr_formato_tecnico():
    """Verifica a representação técnica (repr) da freguesia."""
    f = Freguesia("110611", "Marvila", 38542)
    assert repr(f) == "Freguesia(codigo='110611', nome='Marvila')"
