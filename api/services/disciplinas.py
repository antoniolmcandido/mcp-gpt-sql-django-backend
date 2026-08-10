from .mysql import conectar

class DisciplinaNaoEncontrada(Exception):
    # Excecao usada quando uma operacao tenta acessar uma disciplina inexistente.
    pass

def listar_disciplinas_dados():
    # Consulta todas as disciplinas e devolve a resposta em formato simples para a API.
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, descricao FROM disciplinas ORDER BY nome")
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return [{"nome": nome, "descricao": descricao} for nome, descricao in dados]

def cadastrar_disciplina_dados(nome: str, descricao: str):
    # Insere uma nova disciplina no banco e devolve os dados cadastrados.
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO disciplinas(nome, descricao) VALUES(%s, %s)",
        (nome, descricao),
    )
    conexao.commit()
    cursor.close()
    conexao.close()
    return {"nome": nome, "descricao": descricao}