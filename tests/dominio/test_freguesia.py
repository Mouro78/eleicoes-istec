# pylint: disable=import-error
import unittest

from eleicoes.dominio.freguesia import Freguesia


class TestConstrucaoEGetters(unittest.TestCase):
    """Testes de construção e getters da Freguesia."""

    def test_cria_freguesia_com_dados_basicos(self):
        """Verifica que o construtor guarda código, nome e eleitores."""
        f = Freguesia("110611", "Marvila", 38542)
        self.assertEqual(f.obter_codigo(), "110611")
        self.assertEqual(f.obter_nome(), "Marvila")
        self.assertEqual(f.obter_eleitores_inscritos(), 38542)

    def test_freguesia_nova_nao_tem_votos(self):
        """Verifica que uma freguesia recém-criada começa sem votos."""
        f = Freguesia("110611", "Marvila", 38542)
        self.assertEqual(f.obter_total_votantes(), 0)
        self.assertEqual(f.obter_votos_brancos(), 0)
        self.assertEqual(f.obter_votos_nulos(), 0)
        self.assertEqual(f.obter_votos_por_partido(), {})


class TestRegistarResultado(unittest.TestCase):
    """Testes do registo de resultados válidos."""

    def test_registar_resultado_guarda_votos(self):
        """Verifica que os votos registados ficam corretamente guardados."""
        f = Freguesia("110611", "Marvila", 38542)
        f.registar_resultado({"PS": 8312, "PSD": 6201}, 412, 189)
        self.assertEqual(f.obter_votos_por_partido(), {"PS": 8312, "PSD": 6201})
        self.assertEqual(f.obter_votos_brancos(), 412)
        self.assertEqual(f.obter_votos_nulos(), 189)

    def test_total_votantes_soma_tudo(self):
        """Verifica que o total soma votos de partidos, brancos e nulos."""
        f = Freguesia("110611", "Marvila", 38542)
        f.registar_resultado({"PS": 8312, "PSD": 6201}, 412, 189)
        self.assertEqual(f.obter_total_votantes(), 15114)


class TestValidacoes(unittest.TestCase):
    """Testes das validações do registo de resultados."""

    def test_votos_de_partido_negativos_levanta_erro(self):
        """Verifica que votos negativos num partido são recusados."""
        f = Freguesia("110611", "Marvila", 38542)
        with self.assertRaises(ValueError):
            f.registar_resultado({"PS": -50}, 0, 0)

    def test_votos_brancos_negativos_levanta_erro(self):
        """Verifica que votos brancos negativos são recusados."""
        f = Freguesia("110611", "Marvila", 38542)
        with self.assertRaises(ValueError):
            f.registar_resultado({"PS": 100}, -10, 0)

    def test_votos_nulos_negativos_levanta_erro(self):
        """Verifica que votos nulos negativos são recusados."""
        f = Freguesia("110611", "Marvila", 38542)
        with self.assertRaises(ValueError):
            f.registar_resultado({"PS": 100}, 0, -5)

    def test_total_excede_inscritos_levanta_erro(self):
        """Verifica que o total de votos não pode exceder os inscritos."""
        f = Freguesia("110611", "Marvila", 100)
        with self.assertRaises(ValueError):
            f.registar_resultado({"PS": 80, "PSD": 50}, 0, 0)

    def test_nao_pode_registar_duas_vezes(self):
        """Verifica que não é possível registar resultados duas vezes."""
        f = Freguesia("110611", "Marvila", 38542)
        f.registar_resultado({"PS": 100}, 0, 0)
        with self.assertRaises(RuntimeError):
            f.registar_resultado({"PSD": 50}, 0, 0)


class TestCalculos(unittest.TestCase):
    """Testes dos cálculos da freguesia."""

    def test_calcular_abstencao(self):
        """Verifica o cálculo correto da taxa de abstenção."""
        f = Freguesia("110611", "Marvila", 1000)
        f.registar_resultado({"PS": 400, "PSD": 200}, 0, 0)
        self.assertEqual(f.calcular_abstencao(), 0.4)

    def test_vencedor_e_partido_mais_votado(self):
        """Verifica que o vencedor é o partido com mais votos."""
        f = Freguesia("110611", "Marvila", 38542)
        f.registar_resultado({"PS": 8312, "PSD": 6201, "CH": 3104}, 0, 0)
        self.assertEqual(f.obter_vencedor(), "PS")


class TestCasosEspeciais(unittest.TestCase):
    """Testes de casos-limite."""

    def test_freguesia_sem_eleitores_abstencao_zero(self):
        """Verifica que abstenção é 0.0 quando não há eleitores inscritos."""
        f = Freguesia("000000", "Fantasma", 0)
        self.assertEqual(f.calcular_abstencao(), 0.0)

    def test_freguesia_sem_votos_nao_tem_vencedor(self):
        """Verifica que uma freguesia sem votos não tem vencedor."""
        f = Freguesia("110611", "Marvila", 38542)
        self.assertIsNone(f.obter_vencedor())


class TestDunderMethods(unittest.TestCase):
    """Testes dos métodos especiais (__eq__, __hash__, __str__, __repr__)."""

    def test_freguesias_com_mesmo_codigo_sao_iguais(self):
        """Verifica que freguesias com o mesmo código são iguais."""
        f1 = Freguesia("110611", "Marvila", 38542)
        f2 = Freguesia("110611", "Marvila", 38542)
        self.assertEqual(f1, f2)

    def test_freguesias_com_codigos_diferentes_nao_sao_iguais(self):
        """Verifica que freguesias com códigos diferentes não são iguais."""
        f1 = Freguesia("110611", "Marvila", 38542)
        f2 = Freguesia("110612", "Beato", 20000)
        self.assertNotEqual(f1, f2)

    def test_freguesia_nao_e_igual_a_outro_tipo(self):
        """Verifica que uma freguesia não é igual a objetos de outro tipo."""
        f = Freguesia("110611", "Marvila", 38542)
        self.assertNotEqual(f, "110611")
        self.assertNotEqual(f, 42)

    def test_freguesias_iguais_tem_mesmo_hash(self):
        """Verifica que freguesias iguais têm o mesmo hash."""
        f1 = Freguesia("110611", "Marvila", 38542)
        f2 = Freguesia("110611", "Marvila", 38542)
        self.assertEqual(hash(f1), hash(f2))

    def test_str_mostra_nome_e_codigo(self):
        """Verifica a representação amigável (str) da freguesia."""
        f = Freguesia("110611", "Marvila", 38542)
        self.assertEqual(str(f), "Marvila (110611)")

    def test_repr_formato_tecnico(self):
        """Verifica a representação técnica (repr) da freguesia."""
        f = Freguesia("110611", "Marvila", 38542)
        self.assertEqual(repr(f), "Freguesia(codigo='110611', nome='Marvila')")


if __name__ == "__main__":
    unittest.main()
