# Pipeline de Dados – Autorizações Ambientais (Fauna)

Pipeline de dados para coleta, normalização e disponibilização de autorizações para estudos de fauna no âmbito do licenciamento ambiental estadual do Paraná.

O projeto centraliza informações públicas que atualmente se encontram dispersas em portais institucionais, transformando dados não estruturados em um dataset relacional consultável via API.

Este repositório representa a camada de ingestão e serving de dados de um sistema futuro voltado à transparência e análise ambiental.

---

## Arquitetura do Pipeline

O fluxo segue um modelo clássico de engenharia de dados:

1. Ingestão  
   Scraper baseado em Selenium realiza a coleta automatizada no portal oficial.

2. Transformação  
   Os dados coletados são tratados, normalizados e estruturados.

3. Persistência  
   Armazenamento em banco relacional (no momento está sendo utilizado um SQLite local por padrão, no deploy ocorerrá a migração para PostgreSQL).

4. Serving  
   API FastAPI expõe os dados com filtros dinâmicos, ordenação e paginação.

---

## Estrutura do Projeto

```
api/        → Aplicação FastAPI (rotas, modelos, schemas e configuração do banco)
scraper/    → Scraper Selenium e lógica de ingestão
alembic/    → Migrations do banco de dados
pyproject.toml → Configuração e dependências
```

---

## Tecnologias Utilizadas

- Python 3.13+
- FastAPI
- SQLAlchemy
- Alembic
- Selenium
- SQLite (default) / PostgreSQL
- Uvicorn
- uv (gerenciamento de dependências)

---

## Requisitos

- Python 3.13+
- Google Chrome ou Chromium
- ChromeDriver compatível
- uv instalado

---

## Instalação (usando uv)

Este projeto utiliza `uv` como gerenciador de dependências e ambientes virtuais.

### 1. Instalar o uv (caso necessário)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

ou

```bash
pip install uv
```

---

### 2. Criar ambiente virtual

```bash
uv venv
source .venv/bin/activate
```

---

### 3. Instalar dependências

```bash
uv sync
```

---

## Configuração

Variáveis de ambiente:

- `DATABASE_URL`: URL de conexão com o banco.
- `API_KEY = "sua API_KEY"

---

## Execução da API

```bash
uv run uvicorn api.main:app --reload
```

---

## Endpoints

GET /health  
Verificação de integridade da aplicação.

GET /autorizacao  
Lista todas as autorizações registradas.

POST /autorizacao/query  
Consulta dinâmica com filtros, ordenação e paginação.

Exemplo de payload:

```json
{
  "fields": ["id", "protocolo", "atividade"],
  "filters": {
    "municipio": "Curitiba"
  },
  "order_by": "id",
  "order_dir": "asc",
  "limit": 50,
  "offset": 0
}
```

Documentação interativa disponível no Endpoint /docs

---

## Execução do Scraper

```bash
uv run python scraper/sia_scraper.py
```

O scraper:

- Navega automaticamente no portal oficial
- Coleta registros de autorizações
- Persiste os dados no banco configurado
- Registra logs detalhados em scraper/logs/scraper.log

---

## Banco de Dados e Migrations

As migrations são gerenciadas via Alembic.

---

