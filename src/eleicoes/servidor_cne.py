import http.server
import socketserver
import json
import os

PORTA = 8000
FICHEIRO_RESULTADOS =os.path.join(os.path.dirname(__file__), "..","..", "data","resultados.json")

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

def calcular_totais(resultados): # função que recebe os resultados do ficheiro json
    totais = {} # inicia um dicionário vazio
    totais["brancos"] = 0 # inicia o campo brancos a zero
    totais["nulos"] = 0 # inicia o campo nulos a zero
    for codigo ,freguesia in resultados.items(): #percorre todas as freguesias dentro de resultados.json
        for partido, votos in freguesia["votos_partido"].items(): #percorre o atributo "Votos por partido"
            if partido in totais: # verifica se partido já existe no dicionário Totais
                totais[partido] += votos #se der true ele adiciona os votos referentes ao partido no dicionário Totais senão cria o registo no mesmo dicionário
            else:
                totais[partido] = votos
        totais["brancos"] += freguesia["votos_brancos"] #soma os votos recebidos pelo parametro "votos_brancos" que vem do ficheiro json e adiciona ao
        totais["nulos"] += freguesia["votos_nulos"] # soma os votos recebidos pelo parametro "votos_nulos" que vem do ficheiro json e adiciona ao atributo nulos do dicionário Totais
    return totais #retorna o dicionário  totais

def calcular_partidos(resultados): # função que recebe os resultados do ficheiro json
    totais = {} #inicia um dicionário vazio
    for codigo ,freguesia in resultados.items(): #percorre todas as freguesias dentro de resultados.json
        for partido, votos in freguesia["votos_partido"].items(): #percorre o atributo "Votos por partido"
            if partido in totais: # verifica se partido já existe no dicionário Totais
                totais[partido] += votos #se der true ele adiciona os votos referentes ao partido no dicionário Totais senão cria o registo no mesmo dicionário
            else:
                totais[partido] = votos
    return totais #retorna o dicionário  totais

class ServidorCNE(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Ler os dados
        comprimento = int(self.headers["Content-Length"])
        corpo = self.rfile.read(comprimento)
        dados = json.loads(corpo)

        # 2. Carregar o que já existe
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

        # 6. Guardar
        resultados[codigo] = dados
        guardar_resultados(resultados)

        # 7. Responder sucesso
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"mensagem": "Freguesia registada com sucesso"}).encode("utf-8"))



    def do_GET(self):
        # 1. Carregar os resultados guardados no JSON
        resultados = carregar_resultados()

        # 2. Se ainda não houver dados, devolver uma mensagem amigável
        if not resultados:
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            resposta = {"mensagem": "Ainda não foram recebidos dados de votação."}
            self.wfile.write(json.dumps(resposta, ensure_ascii=False).encode("utf-8"))
            return

        # 3. Se existirem dados, calcular os totais nacionais
        totais_votos = calcular_totais(resultados)

        # 4. Responder com sucesso (200 OK) e enviar os totais em JSON
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(totais_votos, ensure_ascii=False, indent=2).encode("utf-8"))


def arrancar_servidor():
    with socketserver.TCPServer(("", PORTA), ServidorCNE) as httpd:
        print(f"Servidor CNE a correr na porta {PORTA}")
        httpd.serve_forever()


if __name__ == "__main__":
    arrancar_servidor()
