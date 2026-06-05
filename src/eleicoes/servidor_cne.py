import json
import os
from fastapi import FastAPI
from pydantic import BaseModel

class ResultadoFreguesia(BaseModel):
    """Modelo de dados para o resultado eleitoral de uma freguesia."""
    codigo_freguesia: str
    nome_freguesia: str
    eleitores_inscritos: int
    votos_partido: dict
    votos_brancos: int
    votos_nulos: int



app = FastAPI(title="Servidor CNE")

FICHEIRO_RESULTADOS = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "resultados.json"
)

def carregar_resultados():
    """Lê o ficheiro JSON de resultados. Devolve dict vazio se não existir."""
    if not os.path.exists(FICHEIRO_RESULTADOS):
        return {}
    with open(FICHEIRO_RESULTADOS, encoding="utf-8") as f:
        return json.load(f)

def guardar_resultados(resultados):
    """Guarda o dict de resultados no ficheiro JSON."""
    with open(FICHEIRO_RESULTADOS, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

@app.post("/resultados/freguesia")
def registar_resultado(resultado: ResultadoFreguesia):
    """Recebe, valida e arquiva o resultado de uma freguesia."""

    # Validar votos negativos
    if resultado.votos_brancos < 0 or resultado.votos_nulos < 0:
        return {"erro": "Votos brancos/nulos não podem ser negativos"}

    for partido, votos in resultado.votos_partido.items():
        if votos < 0:
            return {"erro": f"Votos negativos no partido {partido}"}

    # Validar total não excede eleitores
    total = (
        sum(resultado.votos_partido.values())
        + resultado.votos_brancos
        + resultado.votos_nulos
    )
    if total > resultado.eleitores_inscritos:
        return {"erro": "Total de votos excede eleitores inscritos"}

    # Calcular abstenção
    abstencao = 1 - (total / resultado.eleitores_inscritos)

    # Arquivar
    resultados = carregar_resultados()
    resultados[resultado.codigo_freguesia] = {
        "nome": resultado.nome_freguesia,
        "eleitores_inscritos": resultado.eleitores_inscritos,
        "votos_partido": resultado.votos_partido,
        "votos_brancos": resultado.votos_brancos,
        "votos_nulos": resultado.votos_nulos,
        "total_votantes": total,
        "abstencao": round(abstencao, 4),
    }
    guardar_resultados(resultados)

    return {
        "mensagem": f"Freguesia {resultado.nome_freguesia} registada com sucesso",
        "total_votantes": total,
        "abstencao": round(abstencao * 100, 2),
    }
