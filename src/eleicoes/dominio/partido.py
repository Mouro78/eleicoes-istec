class Partido:
    """Representa um partido político concorrente nas eleições.
        # getter (encapsulamento)construtor + validações + normalização
        # getter (encapsulamento)
        # getter (encapsulamento)
        # identidade lógica (por sigla)
        # uso em set / dict
        # representação amigável
        # representação técnica
    """

    def __init__(self, sigla, nome):      
      
        if not sigla or not sigla.strip():
            raise ValueError("Tem de conter a sigla!")
        if not nome or not nome.strip():
            raise ValueError("Tem de conter nome!")

        sigla = sigla.strip().upper()
        nome = nome.strip()
        
        self._sigla = sigla
        self._nome = nome

    
    
    def obter_sigla(self):
        return self._sigla
    
    def obter_nome(self):
        return self._nome
    
    def __eq__(self, other ):
        if not isinstance(other ,Partido):
            return NotImplemented
        return self._sigla == other._sigla
    
    def __hash__(self):
        return hash(self._sigla)
    
    def __str__(self):
        return "{} - {}".format(self._sigla, self._nome)
    
    def __repr__(self):
        return "Partido(sigla={!r}, nome={!r})".format(self._sigla, self._nome)
