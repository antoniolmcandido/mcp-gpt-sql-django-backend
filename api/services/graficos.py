import base64
import io
import json
from typing import Literal

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

# Configurar matplotlib para usar o backend "Agg" 
# para renderização de gráficos sem exibição
matplotlib.use("Agg") 

def gerar_grafico(
    dados_json: str,
    tipo_grafico: Literal["barras", "linha", "pizza", "dispersao"] = "barras",
    titulo: str = "Gráfico",
    xlabel: str = "X",
    ylabel: str = "Y"
) -> str:
    """
    Gera um gráfico a partir de dados JSON e retorna a imagem em base64.
    
    Args:
        dados_json: JSON com os dados. Formato esperado:
                   {"labels": ["A", "B", "C"], "values": [10, 20, 30]}
                   ou {"x": [1, 2, 3], "y": [10, 20, 30]}
        tipo_grafico: Tipo do gráfico (barras, linha, pizza, dispersao)
        titulo: Título do gráfico
        xlabel: Rótulo do eixo X
        ylabel: Rótulo do eixo Y
    
    Returns:
        String base64 da imagem PNG
    """
    try:
        dados = json.loads(dados_json)
    except json.JSONDecodeError:
        return "Erro: dados_json inválido"

    # Criar figura
    plt.figure(figsize=(10, 6))

    try:
        if tipo_grafico == "barras":
            labels = dados.get("labels", dados.get("x", []))
            values = dados.get("values", dados.get("y", []))
            plt.bar(labels, values)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)

        elif tipo_grafico == "linha":
            x = dados.get("x", dados.get("labels", []))
            y = dados.get("y", dados.get("values", []))
            plt.plot(x, y, marker='o')
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.grid(True, alpha=0.3)

        elif tipo_grafico == "pizza":
            labels = dados.get("labels", [])
            values = dados.get("values", [])
            plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')

        elif tipo_grafico == "dispersao":
            x = dados.get("x", [])
            y = dados.get("y", [])
            plt.scatter(x, y)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.grid(True, alpha=0.3)

        plt.title(titulo)
        plt.tight_layout()

        # Converter para base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close()

        return image_base64

    except Exception as e:
        plt.close()
        return f"Erro ao gerar gráfico: {str(e)}"


def gerar_grafico_sql(
    resultados_sql: str,
    tipo_grafico: Literal["barras", "linha", "pizza", "dispersao"] = "barras",
    coluna_x: str = "",
    coluna_y: str = "",
    titulo: str = "Gráfico",
    xlabel: str = "X",
    ylabel: str = "Y"
) -> str:
    """
    Gera um gráfico a partir de resultados de consulta SQL.
    
    Args:
        resultados_sql: String JSON com resultados SQL (lista de dicts)
        tipo_grafico: Tipo do gráfico
        coluna_x: Nome da coluna para eixo X
        coluna_y: Nome da coluna para eixo Y
        titulo: Título do gráfico
        xlabel: Rótulo do eixo X
        ylabel: Rótulo do eixo Y
    
    Returns:
        String base64 da imagem PNG
    """
    try:
        dados = json.loads(resultados_sql)

        if not dados or not isinstance(dados, list):
            return "Erro: resultados SQL vazios ou formato inválido"

        # Converter para formato esperado pela função gerar_grafico
        if coluna_x and coluna_y:
            dados_formatados = {
                "x": [item.get(coluna_x, "") for item in dados],
                "y": [item.get(coluna_y, 0) for item in dados]
            }
        else:
            # Tentar detectar automaticamente as colunas
            primeiro_item = dados[0]
            colunas = list(primeiro_item.keys())

            if len(colunas) >= 2:
                dados_formatados = {
                    "labels": [item.get(colunas[0], "") for item in dados],
                    "values": [item.get(colunas[1], 0) for item in dados]
                }
            else:
                return "Erro: não foi possível detectar colunas para o gráfico"

        return gerar_grafico(
            json.dumps(dados_formatados),
            tipo_grafico,
            titulo,
            xlabel,
            ylabel
        )

    except json.JSONDecodeError:
        return "Erro: resultados SQL em formato JSON inválido"
    except Exception as e:
        return f"Erro ao processar dados SQL: {str(e)}"
