class Freguesia:
    """Classe que vai receber os dados das freguesias"""

    def __init__(self, codigo, nome, eleitores_inscritos):
       #Guardar os dados recebidos
        self._codigo = codigo
        self._nome = nome
        self._eleitores_inscritos = eleitores_inscritos

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
        """Recebe os votos"""
        self._votos_partido = votos_partido
        self._votos_brancos = votos_brancos
        self._votos_nulos = votos_nulos

    def obter_total_votantes(self):
        """Devolve o total de votos(partidos + brancos + nulos)"""
        return sum(self._votos_partido.values()) +self._votos_brancos + self._votos_nulos
