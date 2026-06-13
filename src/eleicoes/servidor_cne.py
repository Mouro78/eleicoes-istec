"""
Servidor CNE - recebe resultados eleitorais (POST) e responde a consultas (GET).

Uso:
    python src/eleicoes/servidor_cne.py
"""

import http.server
import socketserver
import json
import os

# Porta onde o servidor fica à escuta
PORTA = 8000

# Caminho para o ficheiro JSON onde os resultados são arquivados
FICHEIRO_RESULTADOS = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "resultados.json"
)


def carregar_resultados():
    """Lê o ficheiro JSON de resultados. Devolve dicionário vazio se não existir."""
    if not os.path.exists(FICHEIRO_RESULTADOS):
        return {}
    with open(FICHEIRO_RESULTADOS, encoding="utf-8") as f:
        return json.load(f)


def guardar_resultados(resultados):
    """Guarda o dicionário de resultados no ficheiro JSON."""
    with open(FICHEIRO_RESULTADOS, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)


def calcular_totais(resultados):
    """Soma todos os votos de todas as freguesias (totais nacionais)."""
    totais = {}
    totais["brancos"] = 0  # inicia o campo brancos a zero
    totais["nulos"] = 0    # inicia o campo nulos a zero
    for codigo, freguesia in resultados.items():  # percorre todas as freguesias
        for partido, votos in freguesia["votos_partido"].items():  # percorre votos por partido
            if partido in totais:  # se partido já existe, soma
                totais[partido] += votos
            else:                  # senão, cria entrada
                totais[partido] = votos
        totais["brancos"] += freguesia["votos_brancos"]  # soma brancos da freguesia
        totais["nulos"] += freguesia["votos_nulos"]      # soma nulos da freguesia
    return totais


def calcular_partidos(resultados):
    """Devolve apenas os votos por partido (sem brancos e nulos)."""
    partidos = {}
    for codigo, freguesia in resultados.items():  # percorre todas as freguesias
        for partido, votos in freguesia["votos_partido"].items():
            if partido in partidos:
                partidos[partido] += votos
            else:
                partidos[partido] = votos
    return partidos


def calcular_distritos(resultados):
    """Agrupa os votos por distrito."""
    distritos = {}
    for codigo, freguesia in resultados.items():  # percorre todas as freguesias
        nome_distrito = freguesia["distrito"]     # obtém nome do distrito

        # Criar entrada do distrito se ainda não existe
        if nome_distrito not in distritos:
            distritos[nome_distrito] = {"brancos": 0, "nulos": 0}

        # Somar votos dos partidos
        for partido, votos in freguesia["votos_partido"].items():
            if partido in distritos[nome_distrito]:
                distritos[nome_distrito][partido] += votos
            else:
                distritos[nome_distrito][partido] = votos

        # Somar brancos e nulos
        distritos[nome_distrito]["brancos"] += freguesia["votos_brancos"]
        distritos[nome_distrito]["nulos"] += freguesia["votos_nulos"]

    return distritos


class ServidorCNE(http.server.BaseHTTPRequestHandler):

    def do_POST(self):
        # 1. Ler os dados — Content-Length diz quantos bytes ler
        comprimento = int(self.headers["Content-Length"])
        corpo = self.rfile.read(comprimento)  # lê exactamente esse número de bytes
        dados = json.loads(corpo)             # converte JSON em dicionário Python

        # 2. Carregar o que já existe no ficheiro JSON
        resultados = carregar_resultados()

        # 3. Validar - freguesia já existe?
        codigo = dados["codigo_freguesia"]
        if codigo in resultados:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"erro": "Freguesia já registada"}).encode("utf-8"))
            return

        # 4. Validar - votos negativos?
        for partido, votos in dados["votos_partido"].items():
            if votos < 0:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"erro": "Votos negativos"}).encode("utf-8"))
                return

        # 5. Validar - total excede inscritos?
        total = sum(dados["votos_partido"].values()) + dados["votos_brancos"] + dados["votos_nulos"]
        if total > dados["eleitores_inscritos"]:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"erro": "Total de votos excede eleitores inscritos"}).encode("utf-8"))
            return

        # 6. Guardar no ficheiro JSON
        resultados[codigo] = dados
        guardar_resultados(resultados)

        # 7. Responder com sucesso
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"mensagem": "Freguesia registada com sucesso"}).encode("utf-8"))

    def do_GET(self):
        # Carregar resultados do ficheiro JSON
        resultados = carregar_resultados()

        # Verificar qual rota foi pedida e calcular resposta
        if self.path == "/totais":
            resposta = calcular_totais(resultados)
        elif self.path == "/partidos":
            resposta = calcular_partidos(resultados)
        elif self.path == "/distritos":
            resposta = calcular_distritos(resultados)
        else:
            # Rota não existe — responder com 404
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"erro": "Rota não encontrada"}).encode("utf-8"))
            return

        # Responder com sucesso
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(resposta, ensure_ascii=False).encode("utf-8"))

    def log_message(self, format, *args):
        """Silencia os logs automáticos do servidor."""
        pass


def arrancar_servidor():
    """Arranca o servidor CNE na porta definida."""
    with socketserver.TCPServer(("", PORTA), ServidorCNE) as httpd:
        print(f"Servidor CNE a correr na porta {PORTA}")
        print(f"  POST /resultados   -> recebe votos do Produtor")
        print(f"  GET  /totais       -> totais nacionais")
        print(f"  GET  /partidos     -> votos por partido")
        print(f"  GET  /distritos    -> votos por distrito")
        httpd.serve_forever()


if __name__ == "__main__":
    arrancar_servidor()