from collections import Counter


class Distrito:
    """Classe que representa um Distrito de Portugal, que agrega Concelhos"""

    def __init__(self, codigo, nome):
        self._codigo = codigo
        self._nome = nome
        self._concelhos = {}

    def obter_codigo(self):
        """Devolve o codigo do Distrito"""
        return self._codigo

    def obter_nome(self):
        """Devolve o nome do Distrito"""
        return self._nome

    def adicionar_concelho(self, concelho):
        """Adiciona um Concelho a um Distrito"""
        codigo = concelho.obter_codigo()
        if codigo in self._concelhos:
            raise ValueError(f"Concelho {codigo} já existe no Distrito {self._nome}")
        self._concelhos[codigo]= concelho

    def obter_eleitores_inscritos(self):
        """Devolve o total de eleitores no Distrito"""
        return sum(f.obter_eleitores_inscritos() for f in self._concelhos.values())

    def obter_total_votantes(self):
        """Total de votantes no Distrito"""
        return sum(f.obter_total_votantes() for f in self._concelhos.values())

    def obter_votos_brancos(self):
        """Devolve o total de votos brancos por Distrito"""
        return sum(f.obter_votos_brancos() for f in self._concelhos.values())

    def obter_votos_nulos(self):
        """Devolve os votos nulos no Distrito"""
        return sum(f.obter_votos_nulos() for f in self._concelhos.values())

    def calcular_abstencao(self):
        """Devolve abstencão do Distrito"""
        if self.obter_eleitores_inscritos() == 0:
            return 0.0
        return 1 - (self.obter_total_votantes() / self.obter_eleitores_inscritos())

    def obter_votos_por_partido(self):
        """Devolve o Dicionário agregado de votos por partido no Distrito"""
        agregado = Counter()
        for concelho in self._concelhos.values():
            agregado.update(concelho.obter_votos_por_partido())
        return dict(agregado)

    def obter_vencedor(self):
        """Devolve o Partido com mais votos no Distrito"""
        votos = self.obter_votos_por_partido()
        if not votos:
            raise ValueError(f"Distrito '{self._nome}' não tem votos registados.")
        return Counter(votos).most_common(1)[0][0]

    def __eq__(self, other):
        if not isinstance(other, Distrito):
            return NotImplemented
        return self._codigo == other._codigo

    def __hash__(self):
        return hash(self._codigo)

    def __str__(self):
        return f"{self._nome} ({self._codigo})"

    def __repr__(self):
        return f"Distrito(codigo={self._codigo!r}, nome={self._nome!r})"
