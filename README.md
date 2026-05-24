# Eleições Legislativas — Simulador CNE

Projeto final da cadeira **PIV** (ISTEC, LEI).

## Autores
- Pedro Mouro
- Daniel Batalha

## Descrição
Sistema de simulação de Eleições Legislativas em Portugal para um órgão
de comunicação social. Compõe-se de três componentes:

1. **Produtor** — simula votações por freguesia e envia resultados à CNE
2. **Servidor CNE** — recebe, valida e arquiva os resultados; calcula abstenção
3. **Servidor Público** — disponibiliza consultas e exportações dos resultados

## Tecnologias
- Python 3.14
- pytest 9.0.3 (testes)
- pytest-cov 7.1.0 (cobertura de testes)
- pylint 4.0.5 (análise estática)

## Setup do ambiente

Criar e ativar o ambiente virtual:

    python -m venv .venv
    .venv\Scripts\activate

Instalar as dependências:

    pip install -r requirements.txt

## Estrutura do projeto

(A documentar à medida que o projeto evolui.)