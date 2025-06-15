import sqlite3
import datetime

# Conectar ao banco (arquivo local SQLite)
conn = sqlite3.connect('farmtech.db')
cursor = conn.cursor()

# Criação das tabelas
cursor.execute('''
CREATE TABLE IF NOT EXISTS Plantacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    localizacao TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Sensor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    id_plantacao INTEGER NOT NULL,
    FOREIGN KEY (id_plantacao) REFERENCES Plantacao(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Leitura (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_sensor INTEGER NOT NULL,
    data_hora TEXT NOT NULL,
    valor REAL NOT NULL,
    FOREIGN KEY (id_sensor) REFERENCES Sensor(id)
)
''')

conn.commit()

# Funções CRUD
def inserir_plantacao():
    nome = input("Nome da plantação: ")
    local = input("Localização: ")
    cursor.execute('INSERT INTO Plantacao (nome, localizacao) VALUES (?, ?)', (nome, local))
    conn.commit()
    print("🌱 Plantação cadastrada com sucesso!")

def inserir_sensor():
    tipo = input("Tipo de sensor (umidade, pH, nutrientes): ")
    listar_plantacoes()
    id_plantacao = int(input("ID da plantação: "))
    cursor.execute('INSERT INTO Sensor (tipo, id_plantacao) VALUES (?, ?)', (tipo, id_plantacao))
    conn.commit()
    print("🛰️ Sensor cadastrado com sucesso!")

def inserir_leitura():
    listar_sensores()
    id_sensor = int(input("ID do sensor: "))
    valor = float(input("Valor da leitura: "))
    data_hora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO Leitura (id_sensor, data_hora, valor) VALUES (?, ?, ?)', (id_sensor, data_hora, valor))
    conn.commit()
    print("📊 Leitura registrada com sucesso!")

def listar_plantacoes():
    cursor.execute('SELECT * FROM Plantacao')
    plantacoes = cursor.fetchall()
    print("\n🌾 Plantações:")
    for p in plantacoes:
        print(p)

def listar_sensores():
    cursor.execute('SELECT * FROM Sensor')
    sensores = cursor.fetchall()
    print("\n🛰️ Sensores:")
    for s in sensores:
        print(s)

def listar_leituras():
    cursor.execute('SELECT * FROM Leitura')
    leituras = cursor.fetchall()
    print("\n📊 Leituras:")
    for l in leituras:
        print(l)

def atualizar_plantacao():
    listar_plantacoes()
    idp = int(input("ID da plantação a atualizar: "))
    nome = input("Novo nome: ")
    local = input("Nova localização: ")
    cursor.execute('UPDATE Plantacao SET nome=?, localizacao=? WHERE id=?', (nome, local, idp))
    conn.commit()
    print("✅ Plantação atualizada!")

def remover_plantacao():
    listar_plantacoes()
    idp = int(input("ID da plantação a remover: "))
    cursor.execute('DELETE FROM Plantacao WHERE id=?', (idp,))
    conn.commit()
    print("🗑️ Plantação removida!")

def remover_sensor():
    listar_sensores()
    ids = int(input("ID do sensor a remover: "))
    cursor.execute('DELETE FROM Sensor WHERE id=?', (ids,))
    conn.commit()
    print("🗑️ Sensor removido!")

def remover_leitura():
    listar_leituras()
    idl = int(input("ID da leitura a remover: "))
    cursor.execute('DELETE FROM Leitura WHERE id=?', (idl,))
    conn.commit()
    print("🗑️ Leitura removida!")

# Menu principal
def menu():
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

# Executa o menu
menu()

# Fecha conexão no final
conn.close()
