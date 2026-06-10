# Eleições Legislativas — Simulador CNE

Projeto final da cadeira **PIV** (ISTEC, LEI).

## Autores

- Pedro Mouro

## Descrição

Sistema de simulação das Eleições Legislativas em Portugal para um órgão
de comunicação social. Compõe-se de três componentes:

1. **Produtor** — simula votações por freguesia e envia os resultados à CNE
2. **Servidor CNE** — recebe, valida e arquiva os resultados; calcula a abstenção
3. **Servidor Público** — disponibiliza consultas e exportações dos resultados

## Tecnologias

- Python 3.14
- http.server (biblioteca padrão — servidores)
- unittest (biblioteca padrão — testes)
- coverage 7.14.0 (cobertura de testes)
- pylint 4.0.5 (análise estática)

## Estrutura do projeto

```
eleicoes-istec/
├── data/                       # CSV de freguesias e JSON de resultados
│   ├── freguesias.csv          # 3092 freguesias de Portugal (gerado)
│   ├── gerar_csv.py            # Script para (re)gerar o CSV
│   └── resultados.json         # Resultados arquivados pelo servidor CNE
├── docs/                       # Documentação técnica
├── src/
│   └── eleicoes/
│       ├── dominio/            # Classes do domínio
│       │   ├── partido.py
│       │   ├── freguesia.py
│       │   ├── concelho.py
│       │   └── distrito.py
│       ├── produtor.py         # Simulador de votações
│       └── servidor_cne.py     # Servidor CNE (http.server)
├── tests/
│   └── dominio/                # Testes unitários do domínio
├── pyproject.toml              # Configuração de pylint e coverage
└── requirements.txt            # Dependências do projeto
```

## Como começar

### 1. Clonar o repositório

```bash
git clone https://github.com/Mouro78/eleicoes-istec.git
cd eleicoes-istec
```

### 2. Criar e ativar o ambiente virtual

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Gerar o CSV de freguesias

```bash
python data/gerar_csv.py
```

## Como correr

### Produtor de votos

```powershell
$env:PYTHONPATH="src"; python src/eleicoes/produtor.py
```

### Servidor CNE

```powershell
python src/eleicoes/servidor_cne.py
```

O servidor fica disponível em: `http://127.0.0.1:8000`

### Testes

```bash
python -m unittest discover -v
```

### Testes com cobertura

```bash
coverage run -m unittest discover
coverage report
```

### Análise estática (pylint)

```bash
pylint src/eleicoes
```

## Estado de desenvolvimento

### Concluído

- [x] Estrutura inicial do projeto
- [x] Configuração de unittest, pylint, coverage
- [x] Classe `Partido` (com testes; pylint 10/10)
- [x] Classe `Freguesia` (com testes; pylint 10/10)
- [x] Classe `Concelho` (com testes; pylint 10/10)
- [x] Classe `Distrito` (com testes; pylint 10/10)
- [x] Gerador de CSV com 3092 freguesias de Portugal
- [x] Produtor de votos — simula eleição completa (pylint 10/10)
- [x] Servidor CNE — recebe, valida e arquiva resultados (pylint 10/10)

### Em desenvolvimento

- [ ] Servidor Público (http.server)
- [ ] Exportadores (JSON, XLSX, gráfico)

### Bónus considerados

- [ ] Mapas georreferenciados
- [ ] Comparação com eleição anterior
- [ ] Cálculo de deputados eleitos (método de Hondt)

## Workflow Git

O projeto usa **branches por feature**. Cada nova classe ou módulo é
desenvolvido num branch próprio (`feature/...`) e integrado no `main`
via Pull Request.

## Licença

Projeto académico — uso restrito à avaliação da cadeira PIV (ISTEC).
