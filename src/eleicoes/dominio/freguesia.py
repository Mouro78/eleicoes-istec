class Freguesia:
    """Classe que vai receber os dados das freguesias"""

    def __init__(self, codigo, nome, eleitores_inscritos):
       #Guardar os dados recebidos
        self._codigo = codigo
        self._nome = nome
        self._eleitores_inscritos = eleitores_inscritos
        self._resultados_registados = False

        #Inicialização dos votos (Freguesia vazia)
        self._votos_partido = {}
        self._votos_brancos = 0
        self._votos_nulos = 0

    def obter_codigo(self):
        """Serve para devolver o código da freguesia"""
        return self._codigo

    def obter_nome(self):
        """devolve o nome da freqguesia"""
        return self._nome

    def obter_eleitores_inscritos(self):
        """devolve os eleitores incritos"""
        return self._eleitores_inscritos

    def registar_resultado(self, votos_partido, votos_brancos, votos_nulos):
        """Regista os resultados da votação (só pode ser feito uma vez)."""
        if self._resultados_registados:
            raise RuntimeError("Esta freguesia já tem resultados registados")
        if votos_brancos < 0 or votos_nulos < 0:
            raise ValueError("Votos brancos/nulos não podem ser negativos")
        for votos in votos_partido.values():
            if votos < 0:
                raise ValueError("Votos de um partido não podem ser negativos")

        total = sum(votos_partido.values()) + votos_brancos + votos_nulos
        if total > self._eleitores_inscritos:
            raise ValueError("Total de votos excede eleitores inscritos")

        self._votos_partido = votos_partido
        self._votos_brancos = votos_brancos
        self._votos_nulos = votos_nulos

        self._resultados_registados = True

    def obter_total_votantes(self):
        """Devolve o total de votos(partidos + brancos + nulos)"""
        return sum(self._votos_partido.values()) +self._votos_brancos + self._votos_nulos

    def calcular_abstencao(self):
        """Devolve a taxa de abstenção (entre 0.0 e 1.0)"""
        if self.obter_eleitores_inscritos() == 0:
            return 0.0
        return 1 - (self.obter_total_votantes() / self.obter_eleitores_inscritos())

    def obter_vencedor(self):
        """Devolve o partido mais votado, ou none se não houver votos"""
        if not self._votos_partido:
            return None
        return max(self._votos_partido, key=self._votos_partido.get)

    def obter_votos_brancos(self):
        """Devolve o numero de votos em branco"""
        return self._votos_brancos

    def obter_votos_nulos(self):
        """devolve o número de votos nulos"""
        return self._votos_nulos

    def obter_votos_por_partido(self):
        """Devolve uma cópia do dicionário de votos por partido."""
        return dict(self._votos_partido)

    def __eq__(self, other):
        if not isinstance(other, Freguesia):
            return NotImplemented
        return self._codigo == other._codigo

    def __hash__(self):
        return hash(self._codigo)

    def __str__(self):
        return f"{self._nome} ({self._codigo})"

    def __repr__(self):
        return f"Freguesia(codigo={self._codigo!r}, nome={self._nome!r})"
