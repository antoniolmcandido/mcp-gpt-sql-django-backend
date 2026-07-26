import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .services.alunos import (AlunoNaoEncontrado, atualizar_idade_dados,
                              cadastrar_aluno_dados, listar_alunos_dados,
                              remover_aluno_dados)
from .services.chat import responder_com_mcp

# Função auxiliar para analisar o corpo JSON da requisição.
def _parse_json_body(request):
    if not request.body:
        return {}

    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("Corpo JSON inválido.") from exc


def _erro(mensagem, status=400):
    return JsonResponse({"error": mensagem}, status=status)

# Endpoint para verificar se a API está funcionando.
@require_http_methods(["GET"])
def health_check(request):
    return JsonResponse({"status": "ok"})

# Endpoint para listar a coleção de alunos ou cadastrar um novo.
@csrf_exempt
@require_http_methods(["GET", "POST"])
def alunos_collection(request):
    if request.method == "GET":
        return JsonResponse({"alunos": listar_alunos_dados()})

    try:
        payload = _parse_json_body(request)
        nome = str(payload.get("nome", "")).strip()
        idade = int(payload.get("idade"))
        if not nome:
            return _erro("Informe o nome do aluno.")

        aluno = cadastrar_aluno_dados(nome, idade)
        return JsonResponse({"message": "Aluno cadastrado com sucesso.", "aluno": aluno}, status=201)
    except (TypeError, ValueError):
        return _erro("Informe nome e idade válidos.")

# Endpoint para atualizar a idade de um aluno ou remover um aluno existente.
@csrf_exempt
@require_http_methods(["PATCH", "PUT", "DELETE"])
def aluno_detail(request, nome):
    try:
        if request.method in {"PATCH", "PUT"}:
            payload = _parse_json_body(request)
            idade = int(payload.get("idade"))
            aluno = atualizar_idade_dados(nome, idade)
            return JsonResponse({"message": "Idade atualizada.", "aluno": aluno})

        remover_aluno_dados(nome)
        return JsonResponse({"message": "Aluno removido."})
    except (TypeError, ValueError):
        return _erro("Informe uma idade válida.")
    except AlunoNaoEncontrado as exc:
        return _erro(str(exc), status=404)

# Endpoint para interagir com o chat.
@csrf_exempt
@require_http_methods(["POST"])
def chat_endpoint(request):
    try:
        payload = _parse_json_body(request)
        instruction = str(payload.get("message", "")).strip()

        if not instruction:
            return _erro("Envie uma mensagem para o chat.")

        response = responder_com_mcp(instruction)
        return JsonResponse(response)
    except RuntimeError as exc:
        return _erro(str(exc), status=500)
    except ValueError as exc:
        return _erro(str(exc))
