# API AA Fauna

API FastAPI para consulta de autorizações de fauna + scraper Selenium que coleta os dados e grava no banco.

## Estrutura

- `api/` — aplicação FastAPI, modelos, schemas, rotas e configuração do banco.
- `scraper/` — scraper Selenium e acesso ao banco.
- `tabela.sql` — schema SQLite de referência.
- `pyproject.toml` — dependências e configuração do projeto.

## Requisitos

- Python 3.13+
- Google Chrome/Chromium + ChromeDriver compatível

## Instalação

Crie um ambiente virtual e instale as dependências:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Variáveis de ambiente

- `DATABASE_URL`: URL do banco para a API.  
  Se não definida, a API usa SQLite local em `scraper/db.sqlite`.

Observação: a API key está fixa em `api/security/api_key.py` como `minha_chave_api`.

## Rodar a API

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Endpoints

- `GET /health` → health check
- `GET /autorizacao` → lista todas as autorizações
- `POST /autorizacao/query` → filtra com payload

Exemplo de payload:

```json
{
  "fields": ["id", "protocolo", "atividade"],
  "filters": {"municipio": "Curitiba"},
  "order_by": "id",
  "order_dir": "asc",
  "limit": 50,
  "offset": 0
}
```

## Rodar o scraper

```bash
python scraper/sia_scraper.py
```

Logs são gravados em `scraper/logs/scraper.log` e também no console.

## Banco de dados e migrations

O Alembic lê `DATABASE_URL` do `api/.env` (se existir). Para rodar migrations:

```bash
alembic -c api/alembic.ini upgrade head
```
