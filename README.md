# Eleições Legislativas — Simulador CNE

Projeto final da cadeira **PIV** (ISTEC, LEI).

## Autores

- Pedro Mouro
- Daniel Batalha

## Descrição

Sistema de simulação das Eleições Legislativas em Portugal para um órgão
de comunicação social. Compõe-se de três componentes:

1. **Produtor** — simula votações por freguesia e envia os resultados à CNE
2. **Servidor CNE** — recebe, valida e arquiva os resultados; calcula a abstenção
3. **Servidor Público** — disponibiliza consultas e exportações dos resultados

## Tecnologias

- Python 3.14
- pytest 9.0.3 (testes)
- pytest-cov 7.1.0 (cobertura de testes)
- pylint 4.0.5 (análise estática)

## Estrutura do projeto
eleicoes-istec/
├── data/                       # CSVs de freguesias, partidos, eleitores
├── docs/                       # Documentação técnica
├── src/
│   └── eleicoes/
│       └── dominio/            # Classes do domínio (Partido, Freguesia, ...)
├── tests/
│   └── dominio/                # Testes unitários do domínio
├── .vscode/                    # Configurações partilhadas do VS Code
├── pyproject.toml              # Configuração de pytest, pylint, coverage
└── requirements.txt            # Dependências do projeto
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

## Como correr

### Testes

```bash
pytest
```

### Testes com cobertura

```bash
pytest --cov=src/eleicoes
```

### Análise estática (pylint)

```bash
pylint src/eleicoes
```

## Estado de desenvolvimento

### Concluído

- [x] Estrutura inicial do projeto
- [x] Configuração de pytest, pylint, coverage
- [x] Classe `Partido` (com testes; 100% cobertura; pylint 10/10)
- [x] Classe `Freguesia` (com testes; 100% cobertura; pylint 10/10)
- [x] Classes `Concelho` (com testes; 100% cobertura; pylint 10/10)
### Em desenvolvimento

- [ ] `Distrito`
- [ ] Carregador de dados (CSV das freguesias e partidos)
- [ ] Produtor de votos
- [ ] Servidor CNE (FastAPI)
- [ ] Servidor Público (FastAPI)
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
