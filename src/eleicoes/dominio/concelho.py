class Concelho:
    """Classe que representa um concelho de Portugal, que agrega freguesias"""

    def __init__(self, codigo, nome):
        self._codigo = codigo
        self._nome = nome
        self._freguesias = {}

    def obter_codigo(self):
        """Devolve o codigo do Concelho"""
        return self._codigo

    def obter_nome(self):
        """Devolve o nome do Concelho"""
        return self._nome

    def adicionar_freguesia(self, freguesia):
        """Adiciona uma freguesia ao concelho."""
        codigo = freguesia.obter_codigo()
        if codigo in self._freguesias:
            raise ValueError(f"Freguesia {codigo} já existe no concelho {self._nome}")
        self._freguesias[codigo] = freguesia

    def obter_eleitores_inscritos(self):
        """Devolve o total de eleitores inscritos no concelho."""
        return sum(f.obter_eleitores_inscritos() for f in self._freguesias.values())

    def obter_total_votantes(self):
        """Devolve o total de votantes do concelho (soma de todas as freguesias)."""
        return sum(f.obter_total_votantes() for f in self._freguesias.values())

    def obter_votos_brancos(self):
        """Devolve o total de votos brancos do concelho (soma de todas as freguesias)."""
        return sum(f.obter_votos_brancos() for f in self._freguesias.values())

    def obter_votos_nulos(self):
        """Devolve o total de votos nulos do concelho (soma de todas as freguesias)."""
        return sum(f.obter_votos_nulos() for f in self._freguesias.values())

    def calcular_abstencao(self):
        """Devolve abstenção do Concelho"""
        if self.obter_eleitores_inscritos() == 0:
            return 0.0
        return 1 -(self.obter_total_votantes() / self.obter_eleitores_inscritos())
