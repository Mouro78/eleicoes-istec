import http.server
import socketserver
import json
import os

PORTA_PUBLICA = 8001
FICHEIRO_RESULTADOS = os.path.join(os.path.dirname(__file__), "..", "..", "data", "resultados.json")

def carregar_resultados():
    """Lê o ficheiro JSON de resultados atualizado pela CNE."""
    if not os.path.exists(FICHEIRO_RESULTADOS):
        return {}
    with open(FICHEIRO_RESULTADOS, encoding="utf-8") as f:
        return json.load(f)

def calcular_totais_e_abstencao(resultados):
    """Calcula os totais de votos e a abstenção global."""
    totais = {"brancos": 0, "nulos": 0, "partidos": {}, "inscritos": 0, "votantes": 0}

    for freguesia in resultados.values():
        totais["inscritos"] += freguesia["eleitores_inscritos"]
        totais["brancos"] += freguesia["votos_brancos"]
        totais["nulos"] += freguesia["votos_nulos"]

        # Somar os votantes desta freguesia
        votos_freguesia = sum(freguesia["votos_partido"].values()) + freguesia["votos_brancos"] + freguesia["votos_nulos"]
        totais["votantes"] += votos_freguesia

        # Somar por partido
        for partido, votos in freguesia["votos_partido"].items():
            totais["partidos"][partido] = totais["partidos"].get(partido, 0) + votos

    return totais

class ServidorPublico(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        resultados = carregar_resultados()

        # 1. Configurar cabeçalhos para responder em HTML (text/html)pip install pandas matplotlib openpyxl
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        # Caso ainda não haja dados submetidos
        if not resultados:
            html_vazio = """
            <html>
                <head><title>Portal Público CNE</title></head>
                <body style='font-family: sans-serif; text-align: center; padding-top: 50px;'>
                    <h1>Portal de Resultados das Eleições Legislativas</h1>
                    <p style='color: gray;'>Aguardando a receção e validação de dados por parte da CNE...</p>
                </body>
            </html>
            """
            self.wfile.write(html_vazio.encode("utf-8"))
            return

        # 2. Obter métricas consolidadas
        dados = calcular_totais_e_abstencao(resultados)

        # Calcular percentagem de abstenção
        if dados["inscritos"] > 0:
            tx_abstencao = (1 - (dados["votantes"] / dados["inscritos"])) * 100
        else:
            tx_abstencao = 0

        # 3. Construir o HTML dinamicamente com os resultados
        html = f"""
        <html>
            <head>
                <title>Resultados Oficiais - Legislativas</title>
                <style>
                    body {{ font-family: sans-serif; margin: 40px; background-color: #f4f6f9; }}
                    h1, h2 {{ color: #2c3e50; }}
                    .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }}
                    table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                    th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                    th {{ background-color: #2c3e50; color: white; }}
                    tr:hover {{ background-color: #f5f5f5; }}
                </style>
            </head>
            <body>
                <h1>Portal Público de Resultados Eleitorais</h1>

                <div class="card">
                    <h2>Resumo Global (Totais Nacionais)</h2>
                    <p><b>Eleitores Inscritos:</b> {dados["inscritos"]:,}</p>
                    <p><b>Total de Votantes:</b> {dados["votantes"]:,}</p>
                    <p><b>Abstenção:</b> {tx_abstencao:.2f}%</p>
                </div>

                <div class="card">
                    <h2>Votação por Partido</h2>
                    <table>
                        <tr><th>Partido</th><th>Votos</th></tr>
        """

        # Adicionar os partidos ordenados por mais votados
        partidos_ordenados = sorted(dados["partidos"].items(), key=lambda x: x[1], reverse=True)
        for partido, votos in partidos_ordenados:
            html += f"<tr><td><b>{partido}</b></td><td>{votos:,}</td></tr>"

        # Adicionar brancos e nulos no fim da tabela
        html += f"""
                        <tr style='background-color: #eee;'><td>Votos em Branco</td><td>{dados["brancos"]:,}</td></tr>
                        <tr style='background-color: #eee;'><td>Votos Nulos</td><td>{dados["nulos"]:,}</td></tr>
                    </table>
                </div>
            </body>
        </html>
        """

        self.wfile.write(html.encode("utf-8"))

def arrancar_servidor_publico():
    with socketserver.TCPServer(("", PORTA_PUBLICA), ServidorPublico) as httpd:
        print(f"Servidor Público a correr em http://localhost:{PORTA_PUBLICA}")
        httpd.serve_forever()

if __name__ == "__main__":
    arrancar_servidor_publico()
