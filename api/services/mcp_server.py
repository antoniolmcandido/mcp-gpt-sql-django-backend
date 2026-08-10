from mcp.server.fastmcp import FastMCP

from .tabelas import criar_tabela_dados
from .disciplinas import (DisciplinaNaoEncontrada, cadastrar_disciplina_dados,
                          listar_disciplinas_dados)
from .alunos import (AlunoNaoEncontrado, atualizar_idade_dados,
                     cadastrar_aluno_dados, listar_alunos_dados,
                     remover_aluno_dados)

# Instancia o servidor MCP que publica as funcoes de alunos como ferramentas.
mcp = FastMCP("Escola Backend")

@mcp.tool()
def criar_tabelas(query_criacao: str):
    # Cria tabela no banco de dados.
    criar_tabela_dados(query_criacao)
    return "Tabela criada com sucesso."

@mcp.tool()
def listar_disciplinas():
    # Recupera as disciplinas do banco e devolve em formato legivel.
    disciplinas = listar_disciplinas_dados()
    if not disciplinas:
        return "Nenhuma disciplina cadastrada."

    return "\n".join(f"{disciplina['nome']}: {disciplina['descricao']}" for disciplina in disciplinas)

@mcp.tool()
def cadastrar_disciplina(nome: str, descricao: str):
    # Cadastra uma nova disciplina e devolve a confirmacao.
    try:
        disciplina = cadastrar_disciplina_dados(nome, descricao)
    except DisciplinaNaoEncontrada as e:
        return f"Erro ao cadastrar disciplina: {e}"
    return f"Disciplina cadastrada com sucesso: {disciplina['nome']} - {disciplina['descricao']}."

@mcp.tool()
def listar_alunos():
    # Recupera os alunos do banco e converte a resposta em texto legivel.
    alunos = listar_alunos_dados()
    if not alunos:
        return "Nenhum aluno cadastrado."

    return "\n".join(f"{aluno['nome']} ({aluno['idade']} anos)" for aluno in alunos)

@mcp.tool()
def cadastrar_aluno(nome: str, idade: int):
    # Executa o cadastro e devolve uma mensagem de confirmacao.
    aluno = cadastrar_aluno_dados(nome, idade)
    return f"Aluno cadastrado com sucesso: {aluno['nome']} ({aluno['idade']} anos)."


@mcp.tool()
def atualizar_idade(nome: str, idade: int):
    # Atualiza a idade de um aluno e devolve o resultado da operacao.
    aluno = atualizar_idade_dados(nome, idade)
    return f"Idade atualizada para {aluno['nome']}: {aluno['idade']} anos."


@mcp.tool()
def remover_aluno(nome: str):
    # Remove o aluno selecionado e devolve a confirmacao da exclusao.
    aluno = remover_aluno_dados(nome)
    return f"Aluno removido: {aluno['nome']}."


if __name__ == "__main__":
    # Permite executar este modulo diretamente como servidor MCP.
    mcp.run()
