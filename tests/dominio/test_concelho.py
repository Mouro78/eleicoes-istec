# pylint: disable=import-error,protected-access
import unittest

from eleicoes.dominio.freguesia import Freguesia
from eleicoes.dominio.concelho import Concelho


def criar_freguesia(codigo, nome, votos, eleitores=1000, brancos=10, nulos=5):
    """Cria uma Freguesia real com resultados registados."""
    f = Freguesia(codigo, nome, eleitores)
    f.registar_resultado(votos, brancos, nulos)
    return f


class TestConstrucaoEGetters(unittest.TestCase):
    """Testes de construção e getters do Concelho."""

    def test_cria_concelho_com_dados_basicos(self):
        """Verifica que o construtor guarda código e nome."""
        c = Concelho("1106", "Lisboa")
        self.assertEqual(c.obter_codigo(), "1106")
        self.assertEqual(c.obter_nome(), "Lisboa")

    def test_concelho_novo_nao_tem_freguesias(self):
        """Verifica que um concelho recém-criado começa sem freguesias."""
        c = Concelho("1106", "Lisboa")
        self.assertEqual(len(c._freguesias), 0)


class TestAdicionarFreguesia(unittest.TestCase):
    """Testes da adição de freguesias ao concelho."""

    def test_adicionar_freguesia_valida(self):
        """Verifica que uma freguesia é adicionada corretamente."""
        c = Concelho("1106", "Lisboa")
        f = criar_freguesia("110601", "Ajuda", {"PS": 50})
        c.adicionar_freguesia(f)
        self.assertIn("110601", c._freguesias)

    def test_adicionar_freguesia_duplicada_levanta_erro(self):
        """Verifica que não é possível adicionar uma freguesia com código repetido."""
        c = Concelho("1106", "Lisboa")
        f = criar_freguesia("110601", "Ajuda", {"PS": 50})
        c.adicionar_freguesia(f)
        with self.assertRaises(ValueError):
            c.adicionar_freguesia(f)

    def test_adicionar_multiplas_freguesias(self):
        """Verifica que é possível adicionar várias freguesias distintas."""
        c = Concelho("1106", "Lisboa")
        c.adicionar_freguesia(criar_freguesia("110601", "Ajuda", {"PS": 50}))
        c.adicionar_freguesia(criar_freguesia("110602", "Belém", {"PS": 30}))
        self.assertEqual(len(c._freguesias), 2)


class TestAgregacoes(unittest.TestCase):
    """Testes das agregações de valores das freguesias."""

    def setUp(self):
        """Prepara um concelho com duas freguesias para os testes."""
        self.concelho = Concelho("1306", "Porto")
        self.concelho.adicionar_freguesia(
            criar_freguesia("130601", "Bonfim", {"PS": 50, "PSD": 30},
                            eleitores=200, brancos=5, nulos=3)
        )
        self.concelho.adicionar_freguesia(
            criar_freguesia("130602", "Campanhã", {"PS": 40, "Bloco": 20},
                            eleitores=300, brancos=8, nulos=4)
        )

    def test_obter_eleitores_inscritos(self):
        """Verifica que o total de eleitores soma todas as freguesias."""
        self.assertEqual(self.concelho.obter_eleitores_inscritos(), 500)

    def test_obter_total_votantes(self):
        """Verifica que o total de votantes soma todas as freguesias."""
        # Bonfim: 50+30+5+3=88, Campanhã: 40+20+8+4=72 → 160
        self.assertEqual(self.concelho.obter_total_votantes(), 160)

    def test_obter_votos_brancos(self):
        """Verifica que os votos brancos somam todas as freguesias."""
        self.assertEqual(self.concelho.obter_votos_brancos(), 13)

    def test_obter_votos_nulos(self):
        """Verifica que os votos nulos somam todas as freguesias."""
        self.assertEqual(self.concelho.obter_votos_nulos(), 7)

    def test_calcular_abstencao(self):
        """Verifica o cálculo correto da taxa de abstenção."""
        # 1 - (160/500) = 0.68
        self.assertAlmostEqual(self.concelho.calcular_abstencao(), 0.68)

    def test_calcular_abstencao_sem_eleitores(self):
        """Verifica que a abstenção é 0.0 quando não há eleitores inscritos."""
        c = Concelho("9999", "Vazio")
        self.assertEqual(c.calcular_abstencao(), 0.0)


class TestVotosPorPartido(unittest.TestCase):
    """Testes da agregação de votos por partido."""

    def test_votos_por_partido_sem_freguesias(self):
        """Verifica que sem freguesias o dicionário de votos está vazio."""
        c = Concelho("1106", "Lisboa")
        self.assertEqual(c.obter_votos_por_partido(), {})

    def test_votos_por_partido_agrega_corretamente(self):
        """Verifica que os votos de várias freguesias são somados por partido."""
        c = Concelho("1106", "Lisboa")
        c.adicionar_freguesia(criar_freguesia("110601", "Ajuda", {"PS": 60, "PSD": 30}))
        c.adicionar_freguesia(criar_freguesia("110602", "Belém", {"PS": 40, "Bloco": 20}))
        resultado = c.obter_votos_por_partido()
        self.assertEqual(resultado["PS"], 100)
        self.assertEqual(resultado["PSD"], 30)
        self.assertEqual(resultado["Bloco"], 20)

    def test_votos_por_partido_devolve_copia(self):
        """Verifica que modificar o resultado não afeta os dados internos."""
        c = Concelho("1106", "Lisboa")
        c.adicionar_freguesia(criar_freguesia("110601", "Ajuda", {"PS": 50}))
        resultado = c.obter_votos_por_partido()
        resultado["PS"] = 999
        self.assertEqual(c.obter_votos_por_partido()["PS"], 50)


class TestVencedor(unittest.TestCase):
    """Testes da determinação do vencedor."""

    def test_vencedor_e_partido_mais_votado(self):
        """Verifica que o vencedor é o partido com mais votos no concelho."""
        c = Concelho("1106", "Lisboa")
        c.adicionar_freguesia(criar_freguesia("110601", "Ajuda", {"PS": 100, "PSD": 60}))
        self.assertEqual(c.obter_vencedor(), "PS")

    def test_vencedor_calculado_por_agregacao(self):
        """Verifica que o vencedor resulta da soma de todas as freguesias."""
        c = Concelho("1106", "Lisboa")
        c.adicionar_freguesia(criar_freguesia("110601", "Ajuda", {"PS": 40, "PSD": 60}))
        c.adicionar_freguesia(criar_freguesia("110602", "Belém", {"PS": 70, "PSD": 10}))
        # PS: 110, PSD: 70 → PS vence no total apesar de perder em Ajuda
        self.assertEqual(c.obter_vencedor(), "PS")

    def test_concelho_sem_votos_nao_tem_vencedor(self):
        """Verifica que um concelho sem votos levanta ValueError."""
        c = Concelho("1106", "Lisboa")
        with self.assertRaises(ValueError):
            c.obter_vencedor()


class TestDunderMethods(unittest.TestCase):
    """Testes dos métodos especiais (__eq__, __hash__, __str__, __repr__)."""

    def test_concelhos_com_mesmo_codigo_sao_iguais(self):
        """Verifica que concelhos com o mesmo código são iguais."""
        self.assertEqual(Concelho("1106", "Lisboa"), Concelho("1106", "Lisboa"))

    def test_concelhos_com_codigos_diferentes_nao_sao_iguais(self):
        """Verifica que concelhos com códigos diferentes não são iguais."""
        self.assertNotEqual(Concelho("1106", "Lisboa"), Concelho("1307", "Porto"))

    def test_concelho_nao_e_igual_a_outro_tipo(self):
        """Verifica que um concelho não é igual a objetos de outro tipo."""
        c = Concelho("1106", "Lisboa")
        self.assertNotEqual(c, "1106")
        self.assertNotEqual(c, 42)

    def test_concelhos_iguais_tem_mesmo_hash(self):
        """Verifica que concelhos iguais têm o mesmo hash."""
        c1 = Concelho("1106", "Lisboa")
        c2 = Concelho("1106", "Lisboa")
        self.assertEqual(hash(c1), hash(c2))

    def test_str_mostra_nome_e_codigo(self):
        """Verifica a representação amigável (str) do concelho."""
        c = Concelho("1106", "Lisboa")
        self.assertEqual(str(c), "Lisboa (1106)")

    def test_repr_formato_tecnico(self):
        """Verifica a representação técnica (repr) do concelho."""
        c = Concelho("1106", "Lisboa")
        self.assertEqual(repr(c), "Concelho(codigo='1106', nome='Lisboa')")


if __name__ == "__main__":
    unittest.main()
