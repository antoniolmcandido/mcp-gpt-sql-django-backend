import os
from pathlib import Path

from dotenv import load_dotenv

# Base do projeto usada para localizar o arquivo .env do backend.
BASE_DIR = Path(__file__).resolve().parent.parent
# Carrega as variaveis locais antes de montar as configuracoes do Django.
load_dotenv(BASE_DIR / ".env")


def env_bool(name: str, default: str = "false") -> bool:
    # Converte uma variavel textual em valor booleano.
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


def env_list(name: str, default: str = "") -> list[str]:
    # Transforma uma string separada por virgulas em lista Python.
    return [item.strip() for item in os.getenv(name, default).split(",") if item.strip()]


# Chave secreta do Django usada em assinaturas internas e protecoes do framework.
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-backend-dev-key")
# Liga ou desliga o modo de depuracao.
DEBUG = env_bool("DJANGO_DEBUG", "true")
# Lista de hosts autorizados a acessar o projeto.
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS",
                         "127.0.0.1,localhost") or ["*"]

# Aplicacoes carregadas pelo backend.
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "api",
]

# Middlewares executados em cada requisicao HTTP.
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Raiz das rotas do projeto backend.
ROOT_URLCONF = "config.urls"

# Configuracao padrao de templates do Django.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

# Ponto de entrada WSGI.
WSGI_APPLICATION = "config.wsgi.application"

# Banco local do Django. O acesso ao MySQL ocorre nas funcoes de dominio.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Validadores de senha nao sao usados neste exemplo.
AUTH_PASSWORD_VALIDATORS = []

# Parametros de idioma e fuso horario.
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# Pasta publica para arquivos estaticos.
STATIC_URL = "static/"
# Tipo padrao de chave primaria para modelos.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Habilita consumo local da API pelo frontend durante o desenvolvimento.
CORS_ALLOW_ALL_ORIGINS = env_bool("CORS_ALLOW_ALL_ORIGINS", "true")

# Configuracoes da integracao com o modelo OpenAI.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-nano")
