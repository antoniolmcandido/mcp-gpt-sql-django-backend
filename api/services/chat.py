import json

from django.conf import settings
from openai import OpenAI

from .mcp_client import execute_tool

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "cadastrar_aluno",
            "description": "Cadastra um novo aluno.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string"},
                    "idade": {"type": "integer"},
                },
                "required": ["nome", "idade"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "atualizar_idade",
            "description": "Atualiza a idade de um aluno.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string"},
                    "idade": {"type": "integer"},
                },
                "required": ["nome", "idade"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "remover_aluno",
            "description": "Remove um aluno pelo nome.",
            "parameters": {
                "type": "object",
                "properties": {"nome": {"type": "string"}},
                "required": ["nome"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "listar_alunos",
            "description": "Lista todos os alunos cadastrados.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


def get_client():
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY não configurada no backend.")

    return OpenAI(api_key=settings.OPENAI_API_KEY)


def responder_com_mcp(instruction: str):
    client = get_client()
    messages = [{"role": "user", "content": instruction}]
    tool_events = []

    for _ in range(3):
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        assistant_message = response.choices[0].message
        if not assistant_message.tool_calls:
            return {
                "reply": assistant_message.content or "",
                "tool_events": tool_events,
            }

        mensagens_tool_calls = []
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments or "{}")
            result = execute_tool(function_name, function_args)

            tool_events.append(
                {
                    "name": function_name,
                    "arguments": function_args,
                    "result": result,
                }
            )

            mensagens_tool_calls.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )

        messages.append(
            {
                "role": "assistant",
                "content": assistant_message.content,
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments,
                        },
                    }
                    for tool_call in assistant_message.tool_calls
                ],
            }
        )
        messages.extend(mensagens_tool_calls)

    return {
        "reply": "Não consegui concluir a ação solicitada.",
        "tool_events": tool_events,
    }
