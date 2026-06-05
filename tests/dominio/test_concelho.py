import pytest
from eleicoes.dominio.freguesia import Freguesia
from eleicoes.dominio.concelho import Concelho


def criar_freguesia(codigo, nome, votos, eleitores=1000, brancos=10, nulos=5):
    """Cria uma Freguesia real com resultados registados."""
    f = Freguesia(codigo, nome, eleitores)
    f.registar_resultado(votos, brancos, nulos)
    return f


# ---------- Construção e getters ----------

def test_cria_concelho_com_dados_basicos():
    """Verifica que o construtor guarda código e nome."""
    c = Concelho("1106", "Lisboa")
    assert c.obter_codigo() == "1106"
    assert c.obter_nome() == "Lisboa"

def test_concelho_novo_nao_tem_freguesias():
    """Verifica que um concelho recém-criado começa sem freguesias."""
    c = Concelho("1106", "Lisboa")
    assert len(c._freguesias) == 0


# ---------- Adicionar freguesia ----------

def test_adicionar_freguesia_valida():
    """Verifica que uma freguesia é adicionada correctamente."""
    c = Concelho("1106", "Lisboa")
    f = criar_freguesia("110601", "Ajuda", {"PS": 50})
    c.adicionar_freguesia(f)
    assert "110601" in c._freguesias

def test_adicionar_freguesia_duplicada_levanta_erro():
    """Verifica que não é possível adicionar uma freguesia com código repetido."""
    c = Concelho("1106", "Lisboa")
    f = criar_freguesia("110601", "Ajuda", {"PS": 50})
    c.adicionar_freguesia(f)
    with pytest.raises(ValueError):
        c.adicionar_freguesia(f)

def test_adicionar_multiplas_freguesias():
    """Verifica que é possível adicionar várias freguesias distintas."""
    c = Concelho("1106", "Lisboa")
    c.adicionar_freguesia(criar_freguesia("110601", "Ajuda", {"PS": 50}))
    c.adicionar_freguesia(criar_freguesia("110602", "Belém", {"PS": 30}))
    assert len(c._freguesias) == 2


# ---------- Agregações ----------

@pytest.fixture
def concelho_com_duas_freguesias():
    c = Concelho("1306", "Porto")
    c.adicionar_freguesia(
        criar_freguesia("130601", "Bonfim", {"PS": 50, "PSD": 30},
                        eleitores=200, brancos=5, nulos=3)
    )
    c.adicionar_freguesia(
        criar_freguesia("130602", "Campanhã", {"PS": 40, "Bloco": 20},
                        eleitores=300, brancos=8, nulos=4)
    )
    return c

def test_obter_eleitores_inscritos(concelho_com_duas_freguesias):
    """Verifica que o total de eleitores soma todas as freguesias."""
    assert concelho_com_duas_freguesias.obter_eleitores_inscritos() == 500

def test_obter_total_votantes(concelho_com_duas_freguesias):
    """Verifica que o total de votantes soma todas as freguesias."""
    # Bonfim: 50+30+5+3=88, Campanhã: 40+20+8+4=72 → 160
    assert concelho_com_duas_freguesias.obter_total_votantes() == 160

def test_obter_votos_brancos(concelho_com_duas_freguesias):
    """Verifica que os votos brancos somam todas as freguesias."""
    assert concelho_com_duas_freguesias.obter_votos_brancos() == 13

def test_obter_votos_nulos(concelho_com_duas_freguesias):
    """Verifica que os votos nulos somam todas as freguesias."""
    assert concelho_com_duas_freguesias.obter_votos_nulos() == 7

def test_calcular_abstencao(concelho_com_duas_freguesias):
    """Verifica o cálculo correcto da taxa de abstenção."""
    # 1 - (160/500) = 0.68
    assert concelho_com_duas_freguesias.calcular_abstencao() == pytest.approx(0.68)

def test_calcular_abstencao_sem_eleitores():
    """Verifica que a abstenção é 0.0 quando não há eleitores inscritos."""
    c = Concelho("9999", "Vazio")
    assert c.calcular_abstencao() == 0.0


# ---------- Votos por partido ----------

def test_votos_por_partido_sem_freguesias():
    """Verifica que sem freguesias o dicionário de votos está vazio."""
    c = Concelho("1106", "Lisboa")
    assert c.obter_votos_por_partido() == {}

def test_votos_por_partido_agrega_corretamente():
    """Verifica que os votos de várias freguesias são somados por partido."""
    c = Concelho("1106", "Lisboa")
    c.adicionar_freguesia(criar_freguesia("110601", "Ajuda", {"PS": 60, "PSD": 30}))
    c.adicionar_freguesia(criar_freguesia("110602", "Belém", {"PS": 40, "Bloco": 20}))
    resultado = c.obter_votos_por_partido()
    assert resultado["PS"] == 100
    assert resultado["PSD"] == 30
    assert resultado["Bloco"] == 20

def test_votos_por_partido_devolve_copia():
    """Verifica que modificar o resultado não afecta os dados internos."""
    c = Concelho("1106", "Lisboa")
    c.adicionar_freguesia(criar_freguesia("110601", "Ajuda", {"PS": 50}))
    resultado = c.obter_votos_por_partido()
    resultado["PS"] = 999
    assert c.obter_votos_por_partido()["PS"] == 50


# ---------- Vencedor ----------

def test_vencedor_e_partido_mais_votado():
    """Verifica que o vencedor é o partido com mais votos no concelho."""
    c = Concelho("1106", "Lisboa")
    c.adicionar_freguesia(criar_freguesia("110601", "Ajuda", {"PS": 100, "PSD": 60}))
    assert c.obter_vencedor() == "PS"

def test_vencedor_calculado_por_agregacao():
    """Verifica que o vencedor resulta da soma de todas as freguesias."""
    c = Concelho("1106", "Lisboa")
    c.adicionar_freguesia(criar_freguesia("110601", "Ajuda", {"PS": 40, "PSD": 60}))
    c.adicionar_freguesia(criar_freguesia("110602", "Belém", {"PS": 70, "PSD": 10}))
    # PS: 110, PSD: 70 → PS vence no total apesar de perder em Ajuda
    assert c.obter_vencedor() == "PS"

def test_concelho_sem_votos_nao_tem_vencedor():
    """Verifica que um concelho sem votos levanta ValueError."""
    c = Concelho("1106", "Lisboa")
    with pytest.raises(ValueError):
        c.obter_vencedor()


# ---------- Dunder methods ----------

def test_concelhos_com_mesmo_codigo_sao_iguais():
    """Verifica que concelhos com o mesmo código são iguais."""
    assert Concelho("1106", "Lisboa") == Concelho("1106", "Lisboa")

def test_concelhos_com_codigos_diferentes_nao_sao_iguais():
    """Verifica que concelhos com códigos diferentes não são iguais."""
    assert Concelho("1106", "Lisboa") != Concelho("1307", "Porto")

def test_concelho_nao_e_igual_a_outro_tipo():
    """Verifica que um concelho não é igual a objectos de outro tipo."""
    c = Concelho("1106", "Lisboa")
    assert c != "1106"
    assert c != 42

def test_concelhos_iguais_tem_mesmo_hash():
    """Verifica que concelhos iguais têm o mesmo hash."""
    c1 = Concelho("1106", "Lisboa")
    c2 = Concelho("1106", "Lisboa")
    assert hash(c1) == hash(c2)

def test_str_mostra_nome_e_codigo():
    """Verifica a representação amigável (str) do concelho."""
    c = Concelho("1106", "Lisboa")
    assert str(c) == "Lisboa (1106)"

def test_repr_formato_tecnico():
    """Verifica a representação técnica (repr) do concelho."""
    c = Concelho("1106", "Lisboa")
    assert repr(c) == "Concelho(codigo='1106', nome='Lisboa')"
