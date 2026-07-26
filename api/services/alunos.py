from .mysql import conectar


class AlunoNaoEncontrado(Exception):
    # Excecao usada quando uma operacao tenta acessar um aluno inexistente.
    pass


def listar_alunos_dados():
    # Consulta todos os alunos e devolve a resposta em formato simples para a API.
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, idade FROM alunos ORDER BY nome")
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return [{"nome": nome, "idade": idade} for nome, idade in dados]


def cadastrar_aluno_dados(nome: str, idade: int):
    # Insere um novo aluno no banco e devolve os dados cadastrados.
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO alunos(nome, idade) VALUES(%s, %s)",
        (nome, idade),
    )
    conexao.commit()
    cursor.close()
    conexao.close()
    return {"nome": nome, "idade": idade}


def atualizar_idade_dados(nome: str, idade: int):
    # Atualiza a idade de um aluno existente e valida se houve alteracao.
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
        UPDATE alunos
        SET idade=%s
        WHERE nome=%s
        """,
        (idade, nome),
    )
    if cursor.rowcount == 0:
        cursor.close()
        conexao.close()
        raise AlunoNaoEncontrado(f"Aluno '{nome}' não encontrado.")
    conexao.commit()
    cursor.close()
    conexao.close()
    return {"nome": nome, "idade": idade}


def remover_aluno_dados(nome: str):
    # Remove um aluno pelo nome e aponta erro se nenhum registro for encontrado.
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM alunos WHERE nome=%s", (nome,))
    if cursor.rowcount == 0:
        cursor.close()
        conexao.close()
        raise AlunoNaoEncontrado(f"Aluno '{nome}' não encontrado.")
    conexao.commit()
    cursor.close()
    conexao.close()
    return {"nome": nome}
