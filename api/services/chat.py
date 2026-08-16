import json

from django.conf import settings
from openai import OpenAI

from .graficos import gerar_grafico
from .mcp_client import execute_tool

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "criar_tabelas",
            "description": "Cria tabelas no banco de dados.",
            "parameters": {
                "type": "object",
                "properties": {"query_criacao": {"type": "string"}},
                "required": ["query_criacao"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "listar_disciplinas",
            "description": "Lista todas as disciplinas cadastradas.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cadastrar_disciplina",
            "description": "Cadastra uma nova disciplina.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string"},
                    "descricao": {"type": "string"},
                },
                "required": ["nome", "descricao"],
            },
        },
    },
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
    {
        "type": "function",
        "function": {
            "name": "gerar_grafico",
            "description": "SEMPRE use esta função quando o usuário pedir para gerar, criar, mostrar ou visualizar um gráfico. Gera uma imagem PNG do gráfico com os dados fornecidos. Use OBRIGATORIAMENTE quando o usuário mencionar: 'gráfico', 'grafico', 'chart', 'visualizar', 'plotar', 'mostrar gráfico'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dados_json": {
                        "type": "string",
                        "description": 'Dados em formato JSON. Para gráfico de barras/pizza use {"labels": ["A", "B", "C"], "values": [10, 20, 30]}. Para gráfico de linha/dispersão use {"x": [1, 2, 3], "y": [10, 20, 30]}'
                    },
                    "tipo_grafico": {
                        "type": "string",
                        "enum": ["barras", "linha", "pizza", "dispersao"],
                        "description": "Tipo do gráfico: barras, linha, pizza ou dispersao"
                    },
                    "titulo": {
                        "type": "string",
                        "description": "Título do gráfico"
                    },
                    "xlabel": {
                        "type": "string",
                        "description": "Rótulo do eixo X"
                    },
                    "ylabel": {
                        "type": "string",
                        "description": "Rótulo do eixo Y"
                    }
                },
                "required": ["dados_json", "tipo_grafico", "titulo"],
            },
        },
    },
]


def get_client():
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY não configurada no backend.")

    return OpenAI(api_key=settings.OPENAI_API_KEY)


def responder_com_mcp(instruction: str):
    client = get_client()

    # Detectar se o usuário está pedindo um gráfico
    palavras_grafico = ["gráfico", "grafico", "chart",
                        "plotar", "plot", "visualizar", "mostrar gráfico"]
    solicita_grafico = any(palavra in instruction.lower()
                           for palavra in palavras_grafico)

    messages = [
        {
            "role": "system",
            "content": "Você é um assistente especializado em dados e gráficos. Você TEM uma função 'gerar_grafico' disponível. SEMPRE que o usuário mencionar 'gráfico', 'grafico', 'chart' ou pedir para visualizar dados, você DEVE usar a função 'gerar_grafico' para criar a imagem do gráfico. NUNCA apenas descreva o gráfico em texto - sempre EXECUTE a função para gerar a imagem visual real."
        },
        {
            "role": "user",
            "content": instruction
        }
    ]
    tool_events = []
    chart = None  # Armazenar gráfico gerado (base64)

    for i in range(5):  # Aumentei para 5 iterações
        # Se solicita gráfico e ainda não foi gerado, força o uso da ferramenta
        if solicita_grafico and chart is None and i == 0:
            tool_choice = {"type": "function",
                           "function": {"name": "gerar_grafico"}}
        else:
            tool_choice = "auto"

        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice=tool_choice,
        )

        assistant_message = response.choices[0].message

        # Se não há tool calls, retorna a resposta final
        if not assistant_message.tool_calls:
            result = {
                "reply": assistant_message.content or "",
                "tool_events": tool_events,
            }
            if chart:
                result["chart"] = chart
                print(
                    f"[DEBUG] Retornando com chart! Tamanho: {len(chart)} chars")
            else:
                print("[DEBUG] Retornando SEM chart")
            return result

        # Processar tool calls
        mensagens_tool_calls = []
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments or "{}")

            try:
                # Verificar se é uma chamada para gerar gráfico
                if function_name == "gerar_grafico":
                    result = gerar_grafico(**function_args)

                    # Log dos primeiros 50 chars
                    print(f"[DEBUG] Resultado gerar_grafico: {result[:50]}...")

                    # Se o resultado não começa com "Erro", é uma imagem base64
                    if not result.startswith("Erro"):
                        chart = result  # Armazenar o base64 diretamente
                        print(
                            f"[DEBUG] Chart armazenado! Tamanho: {len(chart)} chars")
                        result = f"Gráfico '{function_args.get('titulo', 'Gráfico')}' gerado com sucesso."
                else:
                    # Executar outras tools normalmente via MCP
                    result = execute_tool(function_name, function_args)
            except Exception as e:
                result = f"Erro ao executar {function_name}: {str(e)}"
                print(f"[DEBUG] Erro: {e}")

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

        # Adicionar mensagem do assistente e respostas das tools
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

    result = {
        "reply": "Não consegui concluir a ação solicitada.",
        "tool_events": tool_events,
    }
    if chart:
        result["chart"] = chart
        print(
            f"[DEBUG] Retornando (fim loop) com chart! Tamanho: {len(chart)} chars")
    else:
        print("[DEBUG] Retornando (fim loop) SEM chart")
    return result
