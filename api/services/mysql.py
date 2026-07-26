import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

# Caminho base do projeto para localizar o arquivo .env.
BASE_DIR = Path(__file__).resolve().parents[3]
# Carrega as variaveis de ambiente antes de abrir a conexao.
load_dotenv(BASE_DIR / ".env")


def conectar():
    # Cria uma conexao nova com o MySQL usando os dados do arquivo .env.
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "1234"),
        database=os.getenv("MYSQL_DATABASE", "escola"),
    )
