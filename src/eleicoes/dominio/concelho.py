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
