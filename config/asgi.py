import os

from django.core.asgi import get_asgi_application

# Define o modulo de configuracao usado pelo servidor ASGI.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Ponto de entrada ASGI do backend.
application = get_asgi_application()
