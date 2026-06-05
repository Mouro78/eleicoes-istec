# pylint: disable=import-error
import pytest
from eleicoes.dominio.freguesia import Freguesia
from eleicoes.dominio.concelho import Concelho
from eleicoes.dominio.distrito import Distrito


def criar_concelho(codigo, nome, votos, eleitores=1000, brancos=10, nulos=5):
    """Cria um Concelho real com uma Freguesia com resultados registados."""
    f = Freguesia(codigo + "01", nome + " (freg.)", eleitores)
    f.registar_resultado(votos, brancos, nulos)
    c = Concelho(codigo, nome)
    c.adicionar_freguesia(f)
    return c


# ---------- Construção e getters ----------

def test_cria_distrito_com_dados_basicos():
    """Verifica que o construtor guarda código e nome."""
    d = Distrito("11", "Lisboa")
    assert d.obter_codigo() == "11"
    assert d.obter_nome() == "Lisboa"

def test_distrito_novo_nao_tem_concelhos():
    """Verifica que um distrito recém-criado começa sem concelhos."""
    d = Distrito("11", "Lisboa")
    assert len(d._concelhos) == 0


# ---------- Adicionar concelho ----------

def test_adicionar_concelho_valido():
    """Verifica que um concelho é adicionado correctamente."""
    d = Distrito("11", "Lisboa")
    c = criar_concelho("1106", "Lisboa", {"PS": 50})
    d.adicionar_concelho(c)
    assert "1106" in d._concelhos

def test_adicionar_concelho_duplicado_levanta_erro():
    """Verifica que não é possível adicionar um concelho com código repetido."""
    d = Distrito("11", "Lisboa")
    c = criar_concelho("1106", "Lisboa", {"PS": 50})
    d.adicionar_concelho(c)
    with pytest.raises(ValueError):
        d.adicionar_concelho(c)

def test_adicionar_multiplos_concelhos():
    """Verifica que é possível adicionar vários concelhos distintos."""
    d = Distrito("11", "Lisboa")
    d.adicionar_concelho(criar_concelho("1106", "Lisboa", {"PS": 50}))
    d.adicionar_concelho(criar_concelho("1107", "Loures", {"PS": 30}))
    assert len(d._concelhos) == 2


# ---------- Agregações ----------

@pytest.fixture
def distrito_com_dois_concelhos():
    d = Distrito("11", "Lisboa")
    d.adicionar_concelho(
        criar_concelho("1106", "Lisboa", {"PS": 50, "PSD": 30},
                       eleitores=200, brancos=5, nulos=3)
    )
    d.adicionar_concelho(
        criar_concelho("1107", "Loures", {"PS": 40, "Bloco": 20},
                       eleitores=300, brancos=8, nulos=4)
    )
    return d

def test_obter_eleitores_inscritos(distrito_com_dois_concelhos):
    """Verifica que o total de eleitores soma todos os concelhos."""
    assert distrito_com_dois_concelhos.obter_eleitores_inscritos() == 500

def test_obter_total_votantes(distrito_com_dois_concelhos):
    """Verifica que o total de votantes soma todos os concelhos."""
    # Lisboa: 50+30+5+3=88, Loures: 40+20+8+4=72 → 160
    assert distrito_com_dois_concelhos.obter_total_votantes() == 160

def test_obter_votos_brancos(distrito_com_dois_concelhos):
    """Verifica que os votos brancos somam todos os concelhos."""
    assert distrito_com_dois_concelhos.obter_votos_brancos() == 13

def test_obter_votos_nulos(distrito_com_dois_concelhos):
    """Verifica que os votos nulos somam todos os concelhos."""
    assert distrito_com_dois_concelhos.obter_votos_nulos() == 7

def test_calcular_abstencao(distrito_com_dois_concelhos):
    """Verifica o cálculo correcto da taxa de abstenção."""
    # 1 - (160/500) = 0.68
    assert distrito_com_dois_concelhos.calcular_abstencao() == pytest.approx(0.68)

def test_calcular_abstencao_sem_eleitores():
    """Verifica que a abstenção é 0.0 quando não há eleitores inscritos."""
    d = Distrito("99", "Vazio")
    assert d.calcular_abstencao() == 0.0


# ---------- Votos por partido ----------

def test_votos_por_partido_sem_concelhos():
    """Verifica que sem concelhos o dicionário de votos está vazio."""
    d = Distrito("11", "Lisboa")
    assert d.obter_votos_por_partido() == {}

def test_votos_por_partido_agrega_corretamente():
    """Verifica que os votos de vários concelhos são somados por partido."""
    d = Distrito("11", "Lisboa")
    d.adicionar_concelho(criar_concelho("1106", "Lisboa", {"PS": 60, "PSD": 30}))
    d.adicionar_concelho(criar_concelho("1107", "Loures", {"PS": 40, "Bloco": 20}))
    resultado = d.obter_votos_por_partido()
    assert resultado["PS"] == 100
    assert resultado["PSD"] == 30
    assert resultado["Bloco"] == 20

def test_votos_por_partido_devolve_copia():
    """Verifica que modificar o resultado não afecta os dados internos."""
    d = Distrito("11", "Lisboa")
    d.adicionar_concelho(criar_concelho("1106", "Lisboa", {"PS": 50}))
    resultado = d.obter_votos_por_partido()
    resultado["PS"] = 999
    assert d.obter_votos_por_partido()["PS"] == 50


# ---------- Vencedor ----------

def test_vencedor_e_partido_mais_votado():
    """Verifica que o vencedor é o partido com mais votos no distrito."""
    d = Distrito("11", "Lisboa")
    d.adicionar_concelho(criar_concelho("1106", "Lisboa", {"PS": 100, "PSD": 60}))
    assert d.obter_vencedor() == "PS"

def test_vencedor_calculado_por_agregacao():
    """Verifica que o vencedor resulta da soma de todos os concelhos."""
    d = Distrito("11", "Lisboa")
    d.adicionar_concelho(criar_concelho("1106", "Lisboa", {"PS": 40, "PSD": 60}))
    d.adicionar_concelho(criar_concelho("1107", "Loures", {"PS": 70, "PSD": 10}))
    # PS: 110, PSD: 70 → PS vence no total apesar de perder em Lisboa
    assert d.obter_vencedor() == "PS"

def test_distrito_sem_votos_nao_tem_vencedor():
    """Verifica que um distrito sem votos levanta ValueError."""
    d = Distrito("11", "Lisboa")
    with pytest.raises(ValueError):
        d.obter_vencedor()


# ---------- Dunder methods ----------

def test_distritos_com_mesmo_codigo_sao_iguais():
    """Verifica que distritos com o mesmo código são iguais."""
    assert Distrito("11", "Lisboa") == Distrito("11", "Lisboa")

def test_distritos_com_codigos_diferentes_nao_sao_iguais():
    """Verifica que distritos com códigos diferentes não são iguais."""
    assert Distrito("11", "Lisboa") != Distrito("13", "Porto")

def test_distrito_nao_e_igual_a_outro_tipo():
    """Verifica que um distrito não é igual a objectos de outro tipo."""
    d = Distrito("11", "Lisboa")
    assert d != "11"
    assert d != 42

def test_distritos_iguais_tem_mesmo_hash():
    """Verifica que distritos iguais têm o mesmo hash."""
    d1 = Distrito("11", "Lisboa")
    d2 = Distrito("11", "Lisboa")
    assert hash(d1) == hash(d2)

def test_str_mostra_nome_e_codigo():
    """Verifica a representação amigável (str) do distrito."""
    d = Distrito("11", "Lisboa")
    assert str(d) == "Lisboa (11)"

def test_repr_formato_tecnico():
    """Verifica a representação técnica (repr) do distrito."""
    d = Distrito("11", "Lisboa")
    assert repr(d) == "Distrito(codigo='11', nome='Lisboa')"
