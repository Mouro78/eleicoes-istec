import unittest

from eleicoes.dominio.freguesia import Freguesia
from eleicoes.dominio.concelho import Concelho
from eleicoes.dominio.distrito import Distrito

def criar_freguesia(codigo, nome, votos, eleitores=1000, brancos=10, nulos=5):
    """Cria uma Freguesia real com resultados registados."""
    f = Freguesia(codigo, nome, eleitores)
    f.registar_resultado(votos, brancos, nulos)
    return f

def criar_concelho(codigo, nome):
    c = Concelho(codigo, nome)
    c.adicionar_freguesia(criar_freguesia("000001", "Freguesias Teste", {"PS": 50}))
    return c

class TestConstrucaoEGetters(unittest.TestCase):
    """Testes de construção e getters do Distrito."""

    def test_cria_distrito_com_dados_basicos(self):
        """Verifica que o construtor guarda código e nome."""
        d = Distrito("01", "Aveiro")
        self.assertEqual(d.obter_codigo(), "01")
        self.assertEqual(d.obter_nome(), "Aveiro")

    def test_distrito_novo_nao_tem_concelhos(self):
        """Verifica que um distrito recém-criado começa sem concelhos."""
        d = Distrito("1106", "Lisboa")
        self.assertEqual(len(d._concelhos), 0)
class TestAdicionarConcelho(unittest.TestCase):
    """Testes da adição de freguesias ao concelho."""

    def test_adicionar_concelho_valido(self):
        """Verifica que um concelho é adicionado corretamente."""
        d = Distrito("01", "Aveiro")
        c = criar_concelho("0101", "Aveiro")
        d.adicionar_concelho(c)
        self.assertIn("0101", d._concelhos)

    def test_adicionar_distrito_duplicada_levanta_erro(self):
        """Verifica que não é possível adicionar uma concelho com código repetido."""
        d = Distrito("1106", "Lisboa")
        c = criar_concelho("110601", "Ajuda")
        d.adicionar_concelho(c)
        with self.assertRaises(ValueError):
            d.adicionar_concelho(c)

    def test_adicionar_multiplos_concelhos(self):
        """Verifica que é possível adicionar vários concelhos distintos."""
        d = Distrito("1106", "Lisboa")
        d.adicionar_concelho(criar_concelho("110601", "Lisboa"))
        d.adicionar_concelho(criar_concelho("110602", "Coimbra"))
        self.assertEqual(len(d._concelhos), 2)
    
class TestAgregacoes(unittest.TestCase):
    """Testes das agregações de valores das freguesias."""

    def setUp(self):
        """Prepara um Distrito com dois concelhos para os testes."""
        self.distrito = Distrito("01", "Aveiro")
        self.distrito.adicionar_concelho(criar_concelho("0101", "Amadora"))
        self.distrito.adicionar_concelho(criar_concelho("0102", "Sintra"))

    def test_obter_eleitores_inscritos(self):
        """Verifica que o total de eleitores soma todas as Concelhos."""
        self.assertEqual(self.distrito.obter_eleitores_inscritos(), 2000)

    def test_obter_total_votantes(self):
        """Verifica que o total de votantes soma todas as Concelhos."""
        
        self.assertEqual(self.distrito.obter_total_votantes(), 130)

    def test_obter_votos_brancos(self):
        """Verifica que os votos brancos somam todas as Concelhos."""
        self.assertEqual(self.distrito.obter_votos_brancos(), 20)

    def test_obter_votos_nulos(self):
        """Verifica que os votos nulos somam todas as COncelhos."""
        self.assertEqual(self.distrito.obter_votos_nulos(), 10)

    def test_calcular_abstencao(self):
        """Verifica o cálculo correto da taxa de abstenção."""
        
        self.assertAlmostEqual(self.distrito.calcular_abstencao(), 0.935)

    def test_calcular_abstencao_sem_eleitores(self):
        """Verifica que a abstenção é 0.0 quando não há eleitores inscritos."""
        d = Distrito("9999", "Vazio")
        self.assertEqual(d.calcular_abstencao(), 0.0)
class TestVotosPorPartido(unittest.TestCase):
    """Testes da agregação de votos por partido."""

    def test_votos_por_partido_sem_concelhos(self):
        """Verifica que sem concelhos o dicionário de votos está vazio."""
        d = Distrito("01", "Aveiro")
        self.assertEqual(d.obter_votos_por_partido(), {})

    def test_votos_por_partido_agrega_corretamente(self):
        """Verifica que os votos de vários concelhos são somados por partido."""
        d = Distrito("01", "Aveiro")
        d.adicionar_concelho(criar_concelho("0101", "Aveiro"))
        d.adicionar_concelho(criar_concelho("0102", "Águeda"))
        resultado = d.obter_votos_por_partido()
        self.assertEqual(resultado["PS"], 100)

    def test_votos_por_partido_devolve_copia(self):
        """Verifica que modificar o resultado não afeta os dados internos."""
        d = Distrito("01", "Aveiro")
        d.adicionar_concelho(criar_concelho("0101", "Aveiro"))
        resultado = d.obter_votos_por_partido()
        resultado["PS"] = 999
        self.assertEqual(d.obter_votos_por_partido()["PS"], 50)


class TestVencedor(unittest.TestCase):
    """Testes da determinação do vencedor."""

    def test_vencedor_e_partido_mais_votado(self):
        """Verifica que o vencedor é o partido com mais votos no distrito."""
        d = Distrito("01", "Aveiro")
        d.adicionar_concelho(criar_concelho("0101", "Aveiro"))
        self.assertEqual(d.obter_vencedor(), "PS")

    def test_distrito_sem_votos_nao_tem_vencedor(self):
        """Verifica que um distrito sem votos levanta ValueError."""
        d = Distrito("01", "Aveiro")
        with self.assertRaises(ValueError):
            d.obter_vencedor()


class TestDunderMethods(unittest.TestCase):
    """Testes dos métodos especiais (__eq__, __hash__, __str__, __repr__)."""

    def test_distritos_com_mesmo_codigo_sao_iguais(self):
        """Verifica que distritos com o mesmo código são iguais."""
        self.assertEqual(Distrito("01", "Aveiro"), Distrito("01", "Aveiro"))

    def test_distritos_com_codigos_diferentes_nao_sao_iguais(self):
        """Verifica que distritos com códigos diferentes não são iguais."""
        self.assertNotEqual(Distrito("01", "Aveiro"), Distrito("02", "Beja"))

    def test_distrito_nao_e_igual_a_outro_tipo(self):
        """Verifica que um distrito não é igual a objetos de outro tipo."""
        d = Distrito("01", "Aveiro")
        self.assertNotEqual(d, "01")
        self.assertNotEqual(d, 42)

    def test_distritos_iguais_tem_mesmo_hash(self):
        """Verifica que distritos iguais têm o mesmo hash."""
        d1 = Distrito("01", "Aveiro")
        d2 = Distrito("01", "Aveiro")
        self.assertEqual(hash(d1), hash(d2))

    def test_str_mostra_nome_e_codigo(self):
        """Verifica a representação amigável (str) do distrito."""
        d = Distrito("01", "Aveiro")
        self.assertEqual(str(d), "Aveiro (01)")

    def test_repr_formato_tecnico(self):
        """Verifica a representação técnica (repr) do distrito."""
        d = Distrito("01", "Aveiro")
        self.assertEqual(repr(d), "Distrito(codigo='01', nome='Aveiro')")


if __name__ == "__main__":
    unittest.main()