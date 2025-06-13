import sqlite3
import csv
import os
import random
from datetime import datetime, timedelta

# --- CONFIGURAÇÃO INICIAL ---
DB_FILE = "agritech.db"
CSV_FILES = {
    "produtores.csv": [
        ["ID_Produtor", "Nome", "CPF_CNPJ", "Email"],
        [1, "João da Silva", "111.222.333-44", "joao.silva@email.com"],
        [2, "Maria Oliveira", "555.666.777-88", "maria.oliveira@email.com"],
        [3, "Pedro Souza", "999.888.777-66", "pedro.souza@email.com"],
    ],
    "areas.csv": [
        ["ID_Area", "ID_Produtor", "Nome_Identificador", "Localizacao_Geografica", "Tamanho_Hectares"],
        [101, 1, "Talhão Norte", "-23.5505,-46.6333", 50.5],
        [102, 1, "Talhão Sul", "-23.5612,-46.6411", 75.0],
        [103, 2, "Setor A", "-22.9068,-43.1729", 120.2],
    ],
    "culturas.csv": [
        ["ID_Cultura", "Nome_Popular", "Nome_Cientifico", "PH_Ideal_Min", "PH_Ideal_Max", "Umidade_Ideal_Min", "Umidade_Ideal_Max"],
        [1, "Soja", "Glycine max", 6.0, 7.0, 60, 75],
        [2, "Milho", "Zea mays", 5.8, 6.8, 55, 70],
        [3, "Algodão", "Gossypium hirsutum", 6.0, 6.5, 50, 65],
    ],
    "sensores.csv": [
        ["ID_Sensor", "ID_Area", "Tipo_Sensor", "Data_Instalacao", "Status"],
        [1001, 101, "Umidade", "2023-01-15", "Ativo"],
        [1002, 101, "pH", "2023-01-15", "Ativo"],
        [1003, 101, "Nutrientes", "2023-01-16", "Ativo"],
        [2001, 103, "Umidade", "2023-02-20", "Manutenção"],
    ]
}

# --- FUNÇÕES DE SETUP DO BANCO DE DADOS ---

def criar_arquivos_csv():
    """Cria os arquivos CSV de exemplo se eles não existirem."""
    print("Verificando arquivos CSV...")
    for filename, data in CSV_FILES.items():
        if not os.path.exists(filename):
            print(f"Criando arquivo de exemplo: {filename}")
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerows(data)
            except IOError as e:
                print(f"Erro ao criar {filename}: {e}")
                
def conectar_bd():
    """Conecta ao banco de dados SQLite e retorna a conexão."""
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.execute("PRAGMA foreign_keys = ON;") # Habilita o suporte a chaves estrangeiras
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def criar_tabelas(conn):
    """Cria as tabelas do banco de dados com base no MER."""
    cursor = conn.cursor()
    
    # Dicionário com todos os comandos CREATE TABLE
    comandos_sql = {
        "PRODUTOR": """
            CREATE TABLE IF NOT EXISTS PRODUTOR (
                ID_Produtor INTEGER PRIMARY KEY,
                Nome TEXT NOT NULL,
                CPF_CNPJ TEXT NOT NULL UNIQUE,
                Email TEXT UNIQUE
            );
        """,
        "AREA_PLANTIO": """
            CREATE TABLE IF NOT EXISTS AREA_PLANTIO (
                ID_Area INTEGER PRIMARY KEY,
                ID_Produtor INTEGER,
                Nome_Identificador TEXT,
                Localizacao_Geografica TEXT,
                Tamanho_Hectares REAL,
                FOREIGN KEY (ID_Produtor) REFERENCES PRODUTOR (ID_Produtor) ON DELETE CASCADE
            );
        """,
        "CULTURA": """
            CREATE TABLE IF NOT EXISTS CULTURA (
                ID_Cultura INTEGER PRIMARY KEY,
                Nome_Popular TEXT NOT NULL UNIQUE,
                Nome_Cientifico TEXT,
                PH_Ideal_Min REAL,
                PH_Ideal_Max REAL,
                Umidade_Ideal_Min REAL,
                Umidade_Ideal_Max REAL
            );
        """,
        "PLANTIO": """
            CREATE TABLE IF NOT EXISTS PLANTIO (
                ID_Plantio INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_Area INTEGER,
                ID_Cultura INTEGER,
                Data_Inicio_Plantio DATE NOT NULL,
                Data_Fim_Colheita DATE,
                FOREIGN KEY (ID_Area) REFERENCES AREA_PLANTIO (ID_Area) ON DELETE CASCADE,
                FOREIGN KEY (ID_Cultura) REFERENCES CULTURA (ID_Cultura)
            );
        """,
        "SENSOR": """
            CREATE TABLE IF NOT EXISTS SENSOR (
                ID_Sensor INTEGER PRIMARY KEY,
                ID_Area INTEGER,
                Tipo_Sensor TEXT NOT NULL,
                Data_Instalacao DATE,
                Status TEXT,
                FOREIGN KEY (ID_Area) REFERENCES AREA_PLANTIO (ID_Area) ON DELETE CASCADE
            );
        """,
        "LEITURA_SENSOR": """
            CREATE TABLE IF NOT EXISTS LEITURA_SENSOR (
                ID_Leitura INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_Sensor INTEGER,
                Data_Hora_Leitura TIMESTAMP NOT NULL,
                Valor_Umidade REAL,
                Valor_pH REAL,
                Valor_Fosforo_P REAL,
                Valor_Potassio_K REAL,
                FOREIGN KEY (ID_Sensor) REFERENCES SENSOR (ID_Sensor) ON DELETE CASCADE
            );
        """,
        "ACAO_SISTEMA": """
            CREATE TABLE IF NOT EXISTS ACAO_SISTEMA (
                ID_Acao INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_Area INTEGER,
                Data_Hora_Recomendacao TIMESTAMP NOT NULL,
                Tipo_Acao TEXT,
                Quantidade_Recomendada REAL,
                Unidade_Medida TEXT,
                Status_Acao TEXT,
                FOREIGN KEY (ID_Area) REFERENCES AREA_PLANTIO (ID_Area) ON DELETE CASCADE
            );
        """
    }

    print("Criando tabelas...")
    for nome_tabela, sql in comandos_sql.items():
        try:
            cursor.execute(sql)
            # print(f"Tabela {nome_tabela} criada com sucesso ou já existente.")
        except sqlite3.Error as e:
            print(f"Erro ao criar tabela {nome_tabela}: {e}")

    conn.commit()


def popular_tabelas(conn):
    """Popula as tabelas a partir dos arquivos CSV."""
    cursor = conn.cursor()

    # Mapeamento de arquivos para tabelas e colunas
    mapa_populacao = {
        "produtores.csv": ("PRODUTOR", ["ID_Produtor", "Nome", "CPF_CNPJ", "Email"]),
        "areas.csv": ("AREA_PLANTIO", ["ID_Area", "ID_Produtor", "Nome_Identificador", "Localizacao_Geografica", "Tamanho_Hectares"]),
        "culturas.csv": ("CULTURA", ["ID_Cultura", "Nome_Popular", "Nome_Cientifico", "PH_Ideal_Min", "PH_Ideal_Max", "Umidade_Ideal_Min", "Umidade_Ideal_Max"]),
        "sensores.csv": ("SENSOR", ["ID_Sensor", "ID_Area", "Tipo_Sensor", "Data_Instalacao", "Status"]),
    }

    print("Populando tabelas com dados iniciais...")
    for filename, (tabela, colunas) in mapa_populacao.items():
        try:
            # Verifica se a tabela já tem dados
            cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
            if cursor.fetchone()[0] > 0:
                # print(f"Tabela {tabela} já populada. Pulando.")
                continue

            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Pula o cabeçalho
                for linha in reader:
                    placeholders = ', '.join(['?'] * len(colunas))
                    sql = f"INSERT INTO {tabela} ({', '.join(colunas)}) VALUES ({placeholders})"
                    cursor.execute(sql, linha)
            # print(f"Dados de {filename} inseridos em {tabela}.")
        except FileNotFoundError:
            print(f"Erro: Arquivo {filename} não encontrado.")
        except sqlite3.IntegrityError as e:
            print(f"Erro de integridade ao inserir em {tabela} (dados duplicados?): {e}")
        except sqlite3.Error as e:
            print(f"Erro de SQL ao popular tabela {tabela}: {e}")

    conn.commit()


# --- FUNÇÕES CRUD (CRIAR, LER, ATUALIZAR, DELETAR) ---

def adicionar_leitura_sensor():
    """Adiciona uma nova leitura de sensor simulada."""
    conn = conectar_bd()
    if not conn: return
    
    id_sensor = input("Digite o ID do sensor para adicionar a leitura: ")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT Tipo_Sensor FROM SENSOR WHERE ID_Sensor = ?", (id_sensor,))
        resultado = cursor.fetchone()
        if not resultado:
            print(f"Erro: Sensor com ID {id_sensor} não encontrado.")
            return

        tipo_sensor = resultado[0]
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        valores = {'Valor_Umidade': None, 'Valor_pH': None, 'Valor_Fosforo_P': None, 'Valor_Potassio_K': None}

        if tipo_sensor == 'Umidade':
            valores['Valor_Umidade'] = round(random.uniform(40, 90), 2)
        elif tipo_sensor == 'pH':
            valores['Valor_pH'] = round(random.uniform(5.0, 8.0), 2)
        elif tipo_sensor == 'Nutrientes':
            valores['Valor_Fosforo_P'] = round(random.uniform(10, 50), 2)
            valores['Valor_Potassio_K'] = round(random.uniform(20, 80), 2)

        sql = """
            INSERT INTO LEITURA_SENSOR (ID_Sensor, Data_Hora_Leitura, Valor_Umidade, Valor_pH, Valor_Fosforo_P, Valor_Potassio_K)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (id_sensor, data_hora, valores['Valor_Umidade'], valores['Valor_pH'], valores['Valor_Fosforo_P'], valores['Valor_Potassio_K']))
        conn.commit()
        print(f"Leitura para o sensor {id_sensor} adicionada com sucesso!")

    except sqlite3.Error as e:
        print(f"Erro ao adicionar leitura: {e}")
    finally:
        conn.close()

def consultar_dados(query, params=()):
    """Função genérica para realizar consultas SELECT e exibir os resultados."""
    conn = conectar_bd()
    if not conn: return

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        
        if not resultados:
            print("Nenhum resultado encontrado.")
            return

        # Pega os nomes das colunas
        nomes_colunas = [description[0] for description in cursor.description]
        print("\n--- RESULTADO DA CONSULTA ---")
        print(" | ".join(nomes_colunas))
        print("-" * (sum(len(col) for col in nomes_colunas) + 3 * len(nomes_colunas)))
        
        for linha in resultados:
            print(" | ".join(map(str, linha)))
        print("---------------------------\n")

    except sqlite3.Error as e:
        print(f"Erro na consulta: {e}")
    finally:
        conn.close()

def manipular_dados(query, params=()):
    """Função genérica para operações INSERT, UPDATE, DELETE."""
    conn = conectar_bd()
    if not conn: return False

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        print("Operação realizada com sucesso!")
        return True
    except sqlite3.IntegrityError as e:
        print(f"Erro de integridade: {e}. (Possível chave estrangeira não existente ou valor único duplicado).")
        return False
    except sqlite3.Error as e:
        print(f"Erro na operação: {e}")
        return False
    finally:
        conn.close()

def atualizar_status_sensor():
    """Atualiza o status de um sensor específico."""
    id_sensor = input("Digite o ID do sensor que deseja atualizar: ")
    novo_status = input("Digite o novo status (Ex: Ativo, Inativo, Manutenção): ")
    
    query = "UPDATE SENSOR SET Status = ? WHERE ID_Sensor = ?"
    manipular_dados(query, (novo_status, id_sensor))

def remover_sensor():
    """Remove um sensor e suas leituras associadas (via ON DELETE CASCADE)."""
    try:
        id_sensor = int(input("Digite o ID do sensor que deseja remover: "))
        confirmacao = input(f"Tem certeza que deseja remover o sensor {id_sensor} e todas as suas leituras? (s/n): ")
        if confirmacao.lower() == 's':
            query = "DELETE FROM SENSOR WHERE ID_Sensor = ?"
            manipular_dados(query, (id_sensor,))
        else:
            print("Operação cancelada.")
    except ValueError:
        print("ID inválido. Por favor, digite um número.")


# --- FUNÇÕES DE MENU ---

def menu_consultas():
    print("\n--- MENU DE CONSULTAS ---")
    print("1. Listar todos os produtores")
    print("2. Listar todas as áreas de plantio de um produtor")
    print("3. Listar todos os sensores de uma área")
    print("4. Ver leituras de um sensor específico")
    print("0. Voltar ao menu principal")
    
    escolha = input("Escolha uma opção: ")
    return escolha

def menu_principal():
    print("\n===== SIMULADOR DE BANCO DE DADOS AGRITECH =====")
    print("1. Consultar dados")
    print("2. Adicionar leitura de sensor (simulado)")
    print("3. Atualizar status de um sensor")
    print("4. Remover um sensor")
    print("0. Sair")
    
    escolha = input("Escolha uma opção: ")
    return escolha


# --- LÓGICA PRINCIPAL ---

def main():
    """Função principal que executa o programa."""
    criar_arquivos_csv()
    conn = conectar_bd()
    if conn:
        criar_tabelas(conn)
        popular_tabelas(conn)
        conn.close()
    else:
        print("Não foi possível inicializar o banco de dados. Encerrando.")
        return

    while True:
        escolha = menu_principal()
        if escolha == '1':
            while True:
                sub_escolha = menu_consultas()
                if sub_escolha == '1':
                    consultar_dados("SELECT * FROM PRODUTOR;")
                elif sub_escolha == '2':
                    id_produtor = input("Digite o ID do produtor: ")
                    consultar_dados("SELECT ID_Area, Nome_Identificador, Tamanho_Hectares FROM AREA_PLANTIO WHERE ID_Produtor = ?", (id_produtor,))
                elif sub_escolha == '3':
                    id_area = input("Digite o ID da área: ")
                    consultar_dados("SELECT ID_Sensor, Tipo_Sensor, Status FROM SENSOR WHERE ID_Area = ?", (id_area,))
                elif sub_escolha == '4':
                    id_sensor = input("Digite o ID do sensor: ")
                    consultar_dados("SELECT Data_Hora_Leitura, Valor_Umidade, Valor_pH, Valor_Fosforo_P, Valor_Potassio_K FROM LEITURA_SENSOR WHERE ID_Sensor = ? ORDER BY Data_Hora_Leitura DESC LIMIT 10", (id_sensor,))
                elif sub_escolha == '0':
                    break
                else:
                    print("Opção inválida.")
        elif escolha == '2':
            adicionar_leitura_sensor()
        elif escolha == '3':
            atualizar_status_sensor()
        elif escolha == '4':
            remover_sensor()
        elif escolha == '0':
            print("Encerrando o programa. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")
