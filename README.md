# Projeto Django com backend MCP

Este repositório contém:

- `backend`: API que interpreta comandos em linguagem natural, aciona o MCP e altera o MySQL.

## Estrutura

- `backend/`
    - `api/`
    - `config/`

## Como executar

1. Crie os ambientes virtuais:

```powershell
python -m venv backend/.venv
```

2. Instale as dependências de cada projeto:

```powershell
backend/.venv/Scripts/python -m pip install -r backend/requirements.txt
```

3. Configure as variáveis de ambiente a partir dos arquivos `.env.example`.

4. Inicie o backend na porta `8000`.

## Observações

- O backend usa MySQL via `mysql-connector-python` para o banco `escola`.
- Em desenvolvimento, o backend permite CORS para o frontend local.
