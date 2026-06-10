# pylint: disable=import-error
import unittest

from eleicoes.dominio.partido import Partido


class TestConstrucaoEValidacoes(unittest.TestCase):
    """Testes de construção e validação do Partido."""

    def test_cria_partido_com_sigla_e_nome(self):
        """Verifica que o construtor guarda sigla e nome."""
        partido = Partido("PS", "Partido Socialista")
        self.assertEqual(partido.obter_sigla(), "PS")
        self.assertEqual(partido.obter_nome(), "Partido Socialista")

    def test_sigla_vazia_levanta_erro(self):
        """Verifica que uma sigla vazia é recusada."""
        with self.assertRaises(ValueError):
            Partido("", "Partido Socialista")

    def test_sigla_so_com_espacos_levanta_erro(self):
        """Verifica que uma sigla só com espaços é recusada."""
        with self.assertRaises(ValueError):
            Partido("   ", "Partido Socialista")

    def test_nome_vazio_levanta_erro(self):
        """Verifica que um nome vazio é recusado."""
        with self.assertRaises(ValueError):
            Partido("PS", "")

    def test_nome_so_com_espacos_levanta_erro(self):
        """Verifica que um nome só com espaços é recusado."""
        with self.assertRaises(ValueError):
            Partido("PS", "    ")


class TestNormalizacao(unittest.TestCase):
    """Testes de normalização da sigla e do nome."""

    def test_sigla_minusculas_e_convertida_para_maiusculas(self):
        """Verifica que a sigla é convertida para maiúsculas."""
        partido = Partido("ps", "Partido Socialista")
        self.assertEqual(partido.obter_sigla(), "PS")

    def test_espacos_a_volta_do_nome_sao_removidos(self):
        """Verifica que os espaços à volta do nome são removidos."""
        partido = Partido("PS ", " Partido Socialista ")
        self.assertEqual(partido.obter_nome(), "Partido Socialista")

    def test_nome_mantem_capitalizacao(self):
        """Verifica que o nome mantém a capitalização original."""
        partido = Partido("PS", "Partido Socialista")
        self.assertEqual(partido.obter_nome(), "Partido Socialista")

    def test_espacos_a_volta_da_sigla_sao_removidos(self):
        """Verifica que os espaços à volta da sigla são removidos."""
        partido = Partido(" PS ", "Partido Socialista")
        self.assertEqual(partido.obter_sigla(), "PS")


class TestIgualdade(unittest.TestCase):
    """Testes do método __eq__."""

    def test_dois_partidos_iguais(self):
        """Verifica que partidos com a mesma sigla são iguais."""
        p1 = Partido("PS", "Partido Socialista")
        p2 = Partido("PS", "Partido Socialista")
        self.assertEqual(p1, p2)

    def test_dois_partidos_com_siglas_diferentes_nao_sao_iguais(self):
        """Verifica que partidos com siglas diferentes não são iguais."""
        p1 = Partido("PS", "Partido Socialista")
        p2 = Partido("PSD", "Partido Social Democrata")
        self.assertNotEqual(p1, p2)

    def test_normalizacao_afeta_igualdade(self):
        """Verifica que a normalização da sigla afeta a igualdade."""
        p1 = Partido("PS", "Partido Socialista")
        p2 = Partido("ps", "Partido Socialista")
        self.assertEqual(p1, p2)

    def test_sigla_igual_nome_diferente(self):
        """Verifica que a identidade depende só da sigla, não do nome."""
        p1 = Partido("PS", "Partido Socialista")
        p2 = Partido("PS", "Pedro Sousa")
        self.assertEqual(p1, p2)

    def test_partido_nao_e_igual_a_outro_tipo(self):
        """Verifica que um partido não é igual a objetos de outro tipo."""
        partido = Partido("PS", "Partido Socialista")
        self.assertNotEqual(partido, "PS")
        self.assertNotEqual(partido, 42)


class TestHash(unittest.TestCase):
    """Testes do método __hash__."""

    def test_partidos_iguais_tem_mesmo_hash(self):
        """Verifica que partidos iguais têm o mesmo hash."""
        p1 = Partido("PS", "Partido Socialista")
        p2 = Partido("PS", "Partido Socialista")
        self.assertEqual(hash(p1), hash(p2))


class TestRepresentacoes(unittest.TestCase):
    """Testes dos métodos __str__ e __repr__."""

    def test_str_devolve_sigla_e_nome(self):
        """Verifica a representação amigável (str) do partido."""
        partido = Partido("PS", "Partido Socialista")
        self.assertEqual(str(partido), "PS - Partido Socialista")

    def test_repr_formato_tecnico(self):
        """Verifica a representação técnica (repr) do partido."""
        partido = Partido("PS", "Partido Socialista")
        self.assertEqual(repr(partido), "Partido(sigla='PS', nome='Partido Socialista')")


if __name__ == "__main__":
    unittest.main()
