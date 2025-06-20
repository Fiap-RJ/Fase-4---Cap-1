import mysql.connector
from mysql.connector import errorcode
import datetime

DB_CONFIG = {
    'user': 'farmtech_user',
    'password': 'password',
    'host': 'db',  #'db' é o nome do serviço no docker-compose.yml
    'database': 'farmtech_db',
    'port': 3306
}

def criar_conexao():
    """Cria e retorna uma conexão com o banco de dados MySQL."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("Conexão com o banco de dados estabelecida.")
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro de acesso: verifique usuário e senha.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("O banco de dados não existe.")
        else:
            print(f"Erro ao conectar ao banco de dados: {err}")
        return None

def criar_tabelas(conn):
    """Cria as tabelas no banco de dados se não existirem."""
    cursor = conn.cursor()
    
    tabelas = {
        'Plantacao': (
            "CREATE TABLE IF NOT EXISTS `Plantacao` ("
            "  `id` INT AUTO_INCREMENT PRIMARY KEY,"
            "  `nome` VARCHAR(255) NOT NULL,"
            "  `localizacao` VARCHAR(255) NOT NULL,"
            "  `umidade_ideal` FLOAT DEFAULT 60.0,"
            "  `ph_ideal_min` FLOAT DEFAULT 6.0,"
            "  `ph_ideal_max` FLOAT DEFAULT 7.0"
            ") ENGINE=InnoDB"
        ),
        'Sensor': (
            "CREATE TABLE IF NOT EXISTS `Sensor` ("
            "  `id` INT AUTO_INCREMENT PRIMARY KEY,"
            "  `tipo` VARCHAR(50) NOT NULL,"
            "  `id_plantacao` INT NOT NULL,"
            "  FOREIGN KEY (`id_plantacao`) REFERENCES `Plantacao`(`id`) ON DELETE CASCADE"
            ") ENGINE=InnoDB"
        ),
        'Leitura': (
            "CREATE TABLE IF NOT EXISTS `Leitura` ("
            "  `id` INT AUTO_INCREMENT PRIMARY KEY,"
            "  `id_sensor` INT NOT NULL,"
            "  `tipo_sensor` VARCHAR(50) NOT NULL,"
            "  `data_hora` DATETIME NOT NULL,"
            "  `valor` FLOAT NOT NULL,"
            "  FOREIGN KEY (`id_sensor`) REFERENCES `Sensor`(`id`) ON DELETE CASCADE"
            ") ENGINE=InnoDB"
        )
    }
    
    for nome_tabela, ddl in tabelas.items():
        try:
            print(f"Criando tabela {nome_tabela}...", end='')
            cursor.execute(ddl)
            print(" OK")
        except mysql.connector.Error as err:
            print(f"Erro ao criar tabela {nome_tabela}: {err.msg}")
            
    cursor.close()

def inserir_plantacao():
    conn = criar_conexao()
    if not conn: return
    cursor = conn.cursor()
    
    try:
        nome = input("Nome da plantação: ")
        local = input("Localização: ")
        umidade = float(input("Umidade ideal (%): "))
        ph_min = float(input("pH ideal (mínimo): "))
        ph_max = float(input("pH ideal (máximo): "))
        
        query = """
            INSERT INTO Plantacao (nome, localizacao, umidade_ideal, ph_ideal_min, ph_ideal_max) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (nome, local, umidade, ph_min, ph_max))
        conn.commit()
        print("🌱 Plantação cadastrada com sucesso!")
    except ValueError:
        print("⚠️ Entrada inválida. Certifique-se de inserir números para umidade e pH.")
    except mysql.connector.Error as err:
        print(f"Erro ao inserir plantação: {err}")
    finally:
        cursor.close()
        conn.close()

def inserir_sensor():
    conn = criar_conexao()
    if not conn: return
    cursor = conn.cursor()

    try:
        listar_plantacoes_simples() # Lista as plantações sem abrir nova conexão
        id_plantacao = int(input("ID da plantação à qual o sensor pertence: "))
        tipo = input("Tipo do sensor (ex: Umidade, pH, Temperatura): ")
        
        # Verificar se a plantação existe
        cursor.execute("SELECT id FROM Plantacao WHERE id = %s", (id_plantacao,))
        if not cursor.fetchone():
            print("⚠️ Plantação não encontrada!")
            return

        query = """
            INSERT INTO Sensor (tipo, id_plantacao) 
            VALUES (%s, %s)
        """
        cursor.execute(query, (tipo, id_plantacao))
        conn.commit()
        print("📡 Sensor cadastrado com sucesso!")
    except ValueError:
        print("⚠️ Entrada inválida. Certifique-se de inserir um número para o ID da plantação.")
    except mysql.connector.Error as err:
        print(f"Erro ao inserir sensor: {err}")
    finally:
        cursor.close()
        conn.close()

def inserir_leitura():
    conn = criar_conexao()
    if not conn: return
    cursor = conn.cursor()

    try:
        listar_sensores_simples() # Lista os sensores sem abrir nova conexão
        id_sensor = int(input("ID do sensor: "))
        
        cursor.execute('SELECT tipo FROM Sensor WHERE id = %s', (id_sensor,))
        resultado = cursor.fetchone()
        if not resultado:
            print("⚠️ Sensor não encontrado!")
            return
        tipo_sensor = resultado[0]

        valor = float(input(f"Valor da leitura para o sensor de '{tipo_sensor}': "))
        data_hora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        query = """
            INSERT INTO Leitura (id_sensor, tipo_sensor, data_hora, valor) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (id_sensor, tipo_sensor, data_hora, valor))
        conn.commit()
        print("📊 Leitura registrada com sucesso!")
    except ValueError:
        print("⚠️ Entrada inválida. Certifique-se de inserir números para o ID do sensor e o valor da leitura.")
    except mysql.connector.Error as err:
        print(f"Erro ao inserir leitura: {err}")
    finally:
        cursor.close()
        conn.close()

def listar_plantacoes():
    conn = criar_conexao()
    if not conn: return
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, nome, localizacao, umidade_ideal, ph_ideal_min, ph_ideal_max FROM Plantacao")
        plantacoes = cursor.fetchall()
        
        if not plantacoes:
            print("Nenhuma plantação cadastrada.")
            return

        print("\n--- Lista de Plantações ---")
        for p in plantacoes:
            print(f"ID: {p[0]}, Nome: {p[1]}, Localização: {p[2]}, Umidade Ideal: {p[3]}%, pH Ideal: {p[4]}-{p[5]}")
        print("--------------------------")
    except mysql.connector.Error as err:
        print(f"Erro ao listar plantações: {err}")
    finally:
        cursor.close()
        conn.close()

def listar_plantacoes_simples():
    """Lista as plantações sem abrir e fechar conexão, útil para ser chamada dentro de outras funções."""
    conn = criar_conexao()
    if not conn: return
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, nome FROM Plantacao")
        plantacoes = cursor.fetchall()
        
        if not plantacoes:
            print("Nenhuma plantação cadastrada.")
            return

        print("\n--- Plantações Disponíveis ---")
        for p in plantacoes:
            print(f"ID: {p[0]}, Nome: {p[1]}")
        print("--------------------------")
    except mysql.connector.Error as err:
        print(f"Erro ao listar plantações (simples): {err}")
    finally:
        cursor.close()
        conn.close()

def listar_sensores():
    conn = criar_conexao()
    if not conn: return
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT s.id, s.tipo, p.nome AS plantacao_nome 
            FROM Sensor s
            JOIN Plantacao p ON s.id_plantacao = p.id
        """)
        sensores = cursor.fetchall()
        
        if not sensores:
            print("Nenhum sensor cadastrado.")
            return

        print("\n--- Lista de Sensores ---")
        for s in sensores:
            print(f"ID: {s[0]}, Tipo: {s[1]}, Plantação: {s[2]}")
        print("------------------------")
    except mysql.connector.Error as err:
        print(f"Erro ao listar sensores: {err}")
    finally:
        cursor.close()
        conn.close()

def listar_sensores_simples():
    """Lista os sensores sem abrir e fechar conexão, útil para ser chamada dentro de outras funções."""
    conn = criar_conexao()
    if not conn: return
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, tipo FROM Sensor")
        sensores = cursor.fetchall()
        
        if not sensores:
            print("Nenhum sensor cadastrado.")
            return

        print("\n--- Sensores Disponíveis ---")
        for s in sensores:
            print(f"ID: {s[0]}, Tipo: {s[1]}")
        print("--------------------------")
    except mysql.connector.Error as err:
        print(f"Erro ao listar sensores (simples): {err}")
    finally:
        cursor.close()
        conn.close()

def listar_leituras():
    conn = criar_conexao()
    if not conn: return
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT l.id, l.id_sensor, l.tipo_sensor, l.data_hora, l.valor, p.nome AS plantacao_nome
            FROM Leitura l
            JOIN Sensor s ON l.id_sensor = s.id
            JOIN Plantacao p ON s.id_plantacao = p.id
            ORDER BY l.data_hora DESC
        """)
        leituras = cursor.fetchall()
        
        if not leituras:
            print("Nenhuma leitura registrada.")
            return

        print("\n--- Histórico de Leituras ---")
        for l in leituras:
            print(f"ID: {l[0]}, Sensor ID: {l[1]} ({l[2]}), Plantação: {l[5]}, Data/Hora: {l[3]}, Valor: {l[4]}")
        print("----------------------------")
    except mysql.connector.Error as err:
        print(f"Erro ao listar leituras: {err}")
    finally:
        cursor.close()
        conn.close()

def atualizar_plantacao():
    conn = criar_conexao()
    if not conn: return
    cursor = conn.cursor()

    try:
        listar_plantacoes_simples()
        idp = int(input("ID da plantação a atualizar: "))
        
        # Verificar se a plantação existe
        cursor.execute("SELECT id FROM Plantacao WHERE id = %s", (idp,))
        if not cursor.fetchone():
            print("⚠️ Plantação não encontrada!")
            return

        nome = input("Novo nome (deixe em branco para não alterar): ")
        local = input("Nova localização (deixe em branco para não alterar): ")
        umidade_str = input("Nova Umidade ideal (%) (deixe em branco para não alterar): ")
        ph_min_str = input("Novo pH ideal (mínimo) (deixe em branco para não alterar): ")
        ph_max_str = input("Novo pH ideal (máximo) (deixe em branco para não alterar): ")

        updates = []
        params = []

        if nome:
            updates.append("nome=%s")
            params.append(nome)
        if local:
            updates.append("localizacao=%s")
            params.append(local)
        if umidade_str:
            try:
                umidade = float(umidade_str)
                updates.append("umidade_ideal=%s")
                params.append(umidade)
            except ValueError:
                print("⚠️ Umidade ideal inválida. Manter valor existente.")
        if ph_min_str:
            try:
                ph_min = float(ph_min_str)
                updates.append("ph_ideal_min=%s")
                params.append(ph_min)
            except ValueError:
                print("⚠️ pH mínimo ideal inválido. Manter valor existente.")
        if ph_max_str:
            try:
                ph_max = float(ph_max_str)
                updates.append("ph_ideal_max=%s")
                params.append(ph_max)
            except ValueError:
                print("⚠️ pH máximo ideal inválido. Manter valor existente.")
        
        if not updates:
            print("Nenhuma alteração a ser feita.")
            return

        query = f"UPDATE Plantacao SET {', '.join(updates)} WHERE id=%s"
        params.append(idp)
        
        cursor.execute(query, tuple(params))
        conn.commit()
        if cursor.rowcount > 0:
            print("✅ Plantação atualizada com sucesso!")
        else:
            print("Nenhuma alteração foi aplicada (talvez o ID não exista).")
    except ValueError:
        print("⚠️ Entrada inválida. Certifique-se de inserir um número para o ID.")
    except mysql.connector.Error as err:
        print(f"Erro ao atualizar plantação: {err}")
    finally:
        cursor.close()
        conn.close()

def remover_plantacao():
    conn = criar_conexao()
    if not conn: return
    cursor = conn.cursor()

    try:
        listar_plantacoes_simples()
        idp = int(input("ID da plantação a remover: "))
        
        # Verificar se a plantação existe antes de tentar remover
        cursor.execute("SELECT id FROM Plantacao WHERE id = %s", (idp,))
        if not cursor.fetchone():
            print("⚠️ Plantação não encontrada!")
            return

        cursor.execute('DELETE FROM Plantacao WHERE id=%s', (idp,))
        conn.commit()
        if cursor.rowcount > 0:
            print("🗑️ Plantação removida com sucesso!")
        else:
            print("Nenhuma plantação foi removida (ID não encontrado).")
    except ValueError:
        print("⚠️ Entrada inválida. Certifique-se de inserir um número para o ID.")
    except mysql.connector.Error as err:
        print(f"Erro ao remover plantação: {err}")
    finally:
        cursor.close()
        conn.close()

def remover_sensor():
    conn = criar_conexao()
    if not conn: return
    cursor = conn.cursor()

    try:
        listar_sensores_simples()
        ids = int(input("ID do sensor a remover: "))
        
        # Verificar se o sensor existe
        cursor.execute("SELECT id FROM Sensor WHERE id = %s", (ids,))
        if not cursor.fetchone():
            print("⚠️ Sensor não encontrado!")
            return

        cursor.execute('DELETE FROM Sensor WHERE id=%s', (ids,))
        conn.commit()
        if cursor.rowcount > 0:
            print("🗑️ Sensor removido com sucesso!")
        else:
            print("Nenhum sensor foi removido (ID não encontrado).")
    except ValueError:
        print("⚠️ Entrada inválida. Certifique-se de inserir um número para o ID.")
    except mysql.connector.Error as err:
        print(f"Erro ao remover sensor: {err}")
    finally:
        cursor.close()
        conn.close()

def remover_leitura():
    conn = criar_conexao()
    if not conn: return
    cursor = conn.cursor()

    try:
        listar_leituras()
        idl = int(input("ID da leitura a remover: "))
        
        # Verificar se a leitura existe
        cursor.execute("SELECT id FROM Leitura WHERE id = %s", (idl,))
        if not cursor.fetchone():
            print("⚠️ Leitura não encontrada!")
            return

        cursor.execute('DELETE FROM Leitura WHERE id=%s', (idl,))
        conn.commit()
        if cursor.rowcount > 0:
            print("🗑️ Leitura removida com sucesso!")
        else:
            print("Nenhuma leitura foi removida (ID não encontrado).")
    except ValueError:
        print("⚠️ Entrada inválida. Certifique-se de inserir um número para o ID.")
    except mysql.connector.Error as err:
        print(f"Erro ao remover leitura: {err}")
    finally:
        cursor.close()
        conn.close()

def menu():
    conn_init = criar_conexao()
    if conn_init:
        criar_tabelas(conn_init)
        conn_init.close()
    else:
        print("Não foi possível conectar ao banco de dados na inicialização. Algumas funcionalidades podem não estar disponíveis.")

    while True:
        print("""
======== 🌱 MENU FARMTECH 🌱 ========
1. Inserir Plantação
2. Inserir Sensor
3. Inserir Leitura

4. Listar Plantações
5. Listar Sensores
6. Listar Leituras

7. Atualizar Plantação

8. Remover Plantação
9. Remover Sensor
10. Remover Leitura

0. Sair
""")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            inserir_plantacao()
        elif opcao == '2':
            inserir_sensor()
        elif opcao == '3':
            inserir_leitura()
        elif opcao == '4':
            listar_plantacoes()
        elif opcao == '5':
            listar_sensores()
        elif opcao == '6':
            listar_leituras()
        elif opcao == '7':
            atualizar_plantacao()
        elif opcao == '8':
            remover_plantacao()
        elif opcao == '9':
            remover_sensor()
        elif opcao == '10':
            remover_leitura()
        elif opcao == '0':
            print("🌾 Encerrando o programa.")
            break
        else:
            print("⚠️ Opção inválida!")

if __name__ == '__main__':
    menu()
