from .mysql import conectar

def obter_tabela(nome_tabela):
    pass

def criar_tabela_dados(query_criacao):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(query_criacao)
    conexao.commit()
    cursor.close()
    conexao.close()
    return 'Tabela criada com sucesso.'