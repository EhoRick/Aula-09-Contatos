import sqlite3
def conexao_banco():
   conexao = sqlite3.connect("contatos.db")

   cursor = conexao.cursor()
 
   sql = '''
             CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL
        )'''
   cursor.execute(sql)
   conexao.commit()  
   return conexao



def adicionar_contato(nome, telefone, email):
    conexao = conexao_banco()
    cursor = conexao.cursor()
    sql = '''
    INSERT INTO contatos (nome, telefone, email)
    VALUES (?, ?, ?)'''
    cursor.execute(sql, (nome, telefone, email))
    conexao.commit()
    conexao.close()

def listar_contatos():
    conexao = conexao_banco()
    cursor = conexao.cursor()
    sql = '''
    SELECT * FROM contatos'''
    cursor.execute(sql)
    contatos = cursor.fetchall()
    if len(contatos) == 0:
        print("Nenhum contato encontrado.")
    else:
       print("Lista de contatos:")
       print("-" * 80)
       print(f" | {'ID':<5} | {'Nome':<20} | {'Telefone':<15} | {'Email':<30} | ")
       print("-" * 80)
    for contato in contatos:
        print(f" | {contato[0]:<5} | {contato[1]:<20} | {contato[2]:<15} | {contato[3]:<30} | ")
        print("-" * 80)
    conexao.close()

def buscar_contato():
    nome = input("Digite o nome do contato que deseja buscar: ")
    conexao = conexao_banco()
    cursor = conexao.cursor()
    sql = '''
    SELECT * FROM contatos WHERE nome LIKE ?'''
    cursor.execute(sql, ('%' + nome + '%',))
    contatos = cursor.fetchall()
    if len(contatos) == 0:
        print("Nenhum contato encontrado com esse nome.")
    else:
        print("Contatos encontrados:")
        print("-" * 80)
        print(f" | {'ID':<5} | {'Nome':<20} | {'Telefone':<15} | {'Email':<30} | ")
        print("-" * 80)
        for contato in contatos:
            print(f" | {contato[0]:<5} | {contato[1]:<20} | {contato[2]:<15} | {contato[3]:<30} | ")
            print("-" * 80)
    conexao.close()

def editar_contato():
    nome = input("Digite o nome do contato que deseja editar: ")
    numero = input("Digite o número do contato que deseja editar: ")
    email = input("Digite o email do contato que deseja editar: ")
    novo_nome = input("Digite o novo nome do contato: ")
    novo_numero = input("Digite o novo número do contato: ")
    novo_email = input("Digite o novo email do contato: ")
    conexao = conexao_banco()
    cursor = conexao.cursor()
    sql = '''
    UPDATE contatos SET nome = ?, telefone = ?, email = ? WHERE nome = ?'''
    cursor.execute(sql, (novo_nome, novo_numero, novo_email, nome))
    conexao.commit()
    if cursor.rowcount == 0:
        print("Nenhum contato encontrado com esse nome.")
    else:
        print("Contato atualizado com sucesso!")
        print("-" * 80)
        print(f" | {'ID':<5} | {'Nome':<20} | {'Telefone':<15} | {'Email':<30} | ")
        print("-" * 80)
        for contato in cursor.execute("SELECT * FROM contatos WHERE nome = ?", (nome,)):
            print(f" | {contato[0]:<5} | {contato[1]:<20} | {contato[2]:<15} | {contato[3]:<30} | ")
            print("-" * 80)
    conexao.close()
    

def excluir_contato():
    termo_busca = input("Digite o nome (ou parte dele) do contato que deseja excluir: ")
    
    conexao = conexao_banco()
    cursor = conexao.cursor()
    
    
    sql_busca = "SELECT * FROM contatos WHERE nome LIKE ?"
    cursor.execute(sql_busca, ('%' + termo_busca + '%',))
    contatos_encontrados = cursor.fetchall()
    
    if not contatos_encontrados:
        print("Nenhum contato encontrado com esse termo.")
    else:
        print("\nContatos encontrados:")
        print("-" * 80)
        print(f" | {'ID':<5} | {'Nome':<20} | {'Telefone':<15} | {'Email':<30} | ")
        print("-" * 80)
        for contato in contatos_encontrados:
            print(f" | {contato[0]:<5} | {contato[1]:<20} | {contato[2]:<15} | {contato[3]:<30} | ")
        print("-" * 80)

        id_escolhido = input("Digite o **ID** do contato que deseja realmente excluir (ou Enter para cancelar): ")
        
        if id_escolhido.strip(): 
            sql_delete = "DELETE FROM contatos WHERE id = ?"
            cursor.execute(sql_delete, (id_escolhido,))
            conexao.commit()
            print("Contato excluído com sucesso!")
        else:
            print("Operação cancelada.")
            
    conexao.close()


def restaurar_contato():
    nome = input("Digite o nome do contato que deseja restaurar: ")
    numero = input("Digite o número do contato que deseja restaurar: ")
    email = input("Digite o email do contato que deseja restaurar: ")
    conexao = conexao_banco()
    cursor = conexao.cursor()
    sql = '''
    INSERT INTO contatos (nome, telefone, email)
    VALUES (?, ?, ?)'''
    cursor.execute(sql, (nome, numero, email))
    conexao.commit()
    print("Contato restaurado com sucesso!")    
    conexao.close()

def menu ():
    while True:
     print("### Contatos ###")
     print("1 - Adicionar contato")
     print("2 - Listar contatos")
     print("3 - Buscar contato pelo  nome")
     print("4 - Editar contato")
     print("5 - Excluir contato")
     print("0 - Sair")

     opcao = input("Escolha uma opção: ")

     if opcao == "1":
        nome = input("Nome: ")
        telefone = input("Telefone: ")
        email = input("Email: ")
        adicionar_contato(nome, telefone, email)
        print("Contato adicionado com sucesso!")

     elif opcao == "2":
        listar_contatos()
     elif opcao == "3":
        buscar_contato()
     elif opcao == "4":
        editar_contato()
     elif opcao == "5":
        excluir_contato()
     elif opcao == "0":
        print("Saindo do programa...")
        break
     else:
        print("Opção inválida. Tente novamente.")

        
menu()