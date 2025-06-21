import mysql.connector
from mysql.connector import errorcode
import datetime
from src.dataset_mock import plantacoes_mock, sensores_mock_template, gerar_leituras_mock
from src.banco_dados import DB_CONFIG # Importa a configuração do DB do banco_dados.py

def criar_conexao():
    """Cria e retorna uma conexão com o banco de dados MySQL."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("Conexão com o banco de dados estabelecida para população.")
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro de acesso: verifique usuário e senha.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("O banco de dados não existe.")
        else:
            print(f"Erro ao conectar ao banco de dados para população: {err}")
        return None

def limpar_dados_mockados(conn):
    """
    Remove plantações e dados associados que correspondem aos nomes mockados,
    garantindo um estado limpo para a repopulação.
    """
    cursor = conn.cursor()
    try:
        for plantacao in plantacoes_mock:
            nome_plantacao = plantacao["nome"]
            cursor.execute("SELECT id FROM Plantacao WHERE nome = %s", (nome_plantacao,))
            plantacao_existente = cursor.fetchone()
            if plantacao_existente:
                plantacao_id = plantacao_existente[0]
                print(f"ℹ️ Removendo dados antigos para a plantação '{nome_plantacao}' (ID: {plantacao_id})...")
                cursor.execute("DELETE FROM Plantacao WHERE id = %s", (plantacao_id,))
                conn.commit()
                print(f"Dados antigos de '{nome_plantacao}' removidos.")
    except mysql.connector.Error as err:
        print(f"Erro ao limpar dados mockados: {err}")
        conn.rollback()
    finally:
        cursor.close()

def popular_banco_de_dados_com_mocks():
    """
    Popula o banco de dados com os dados mockados definidos em dataset_mock.py.
    """
    conn = criar_conexao()
    if not conn:
        print("Não foi possível conectar ao banco de dados. Abortando população de mocks.")
        return
    
    cursor = conn.cursor()

    try:
        limpar_dados_mockados(conn)

        print("--- Iniciando População com Dados Mockados ---")

        # 1. Inserir Plantações
        plantacao_ids = {} # Para armazenar os IDs das plantações inseridas
        for plantacao_data in plantacoes_mock:
            print(f"🌱 Inserindo plantação: '{plantacao_data['nome']}'...")
            query_plantacao = """
                INSERT INTO Plantacao (nome, localizacao, umidade_ideal, ph_ideal_min, ph_ideal_max) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query_plantacao, (
                plantacao_data['nome'],
                plantacao_data['localizacao'],
                plantacao_data['umidade_ideal'],
                plantacao_data['ph_ideal_min'],
                plantacao_data['ph_ideal_max']
            ))
            conn.commit()
            plantacao_ids[plantacao_data['nome']] = cursor.lastrowid
            print(f"Plantação '{plantacao_data['nome']}' (ID: {cursor.lastrowid}) inserida.")

        # 2. Inserir Sensores para cada plantação
        sensor_ids_por_tipo_e_plantacao = {} # {plantacao_nome: {tipo_sensor: id_sensor}}
        for plantacao_nome, p_id in plantacao_ids.items():
            sensor_ids_por_tipo_e_plantacao[plantacao_nome] = {}
            print(f"📡 Inserindo sensores para a plantação '{plantacao_nome}'...")
            for sensor_template in sensores_mock_template:
                tipo_sensor = sensor_template['tipo']
                query_sensor = "INSERT INTO Sensor (tipo, id_plantacao) VALUES (%s, %s)"
                cursor.execute(query_sensor, (tipo_sensor, p_id))
                conn.commit()
                sensor_ids_por_tipo_e_plantacao[plantacao_nome][tipo_sensor] = cursor.lastrowid
                print(f"Sensor '{tipo_sensor}' (ID: {cursor.lastrowid}) inserido para '{plantacao_nome}'.")

        # 3. Inserir Leituras Mockadas
        print("\n📊 Inserindo leituras mockadas para todas as plantações e sensores...")
        query_leitura = """
            INSERT INTO Leitura (id_sensor, tipo_sensor, data_hora, valor) 
            VALUES (%s, %s, %s, %s)
        """
        for plantacao_nome, p_id in plantacao_ids.items():
            if plantacao_nome == "Fazenda Teste Mockada":
                # Usar os IDs de sensores da "Fazenda Teste Mockada"
                umidade_sensor_id = sensor_ids_por_tipo_e_plantacao[plantacao_nome].get('umidade')
                ph_sensor_id = sensor_ids_por_tipo_e_plantacao[plantacao_nome].get('ph')
                temperatura_sensor_id = sensor_ids_por_tipo_e_plantacao[plantacao_nome].get('temperatura')

                if umidade_sensor_id and ph_sensor_id and temperatura_sensor_id:
                    leituras = gerar_leituras_mock(umidade_sensor_id, ph_sensor_id, temperatura_sensor_id)
                    for leitura_data in leituras:
                        cursor.execute(query_leitura, (
                            leitura_data['id_sensor'],
                            leitura_data['tipo_sensor'],
                            leitura_data['data_hora'],
                            leitura_data['valor']
                        ))
                    conn.commit()
                    print(f"Leituras para '{plantacao_nome}' inseridas.")
                else:
                    print(f"Aviso: Sensores para '{plantacao_nome}' não encontrados, leituras não inseridas.")
            elif plantacao_nome == "Horta do Quintal":
                umidade_sensor_id = sensor_ids_por_tipo_e_plantacao[plantacao_nome].get('umidade')
                ph_sensor_id = sensor_ids_por_tipo_e_plantacao[plantacao_nome].get('ph')
                
                if umidade_sensor_id and ph_sensor_id:
                    leituras = gerar_leituras_mock(umidade_sensor_id, ph_sensor_id, umidade_sensor_id)
                    
                    for leitura_data in leituras:
                        if leitura_data['tipo_sensor'] == 'temperatura':
                            continue 
                        
                        cursor.execute(query_leitura, (
                            leitura_data['id_sensor'],
                            leitura_data['tipo_sensor'],
                            leitura_data['data_hora'],
                            leitura_data['valor']
                        ))
                    conn.commit()
                    print(f"Leituras para '{plantacao_nome}' inseridas.")
                else:
                    print(f"Aviso: Sensores para '{plantacao_nome}' não encontrados, leituras não inseridas.")


        print("\n🎉 Banco de dados populado com dados de exemplo!")

    except mysql.connector.Error as err:
        print(f"Erro geral ao popular dados mockados: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    popular_banco_de_dados_com_mocks()
