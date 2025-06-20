import streamlit as st
import pandas as pd
import mysql.connector
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(
    page_title="FarmTech Dashboard",
    page_icon="🌱",
    layout="wide"
)

# --- Conexão com o Banco de Dados MySQL ---
# st.cache_resource: Cacheia a conexão para não reabrir a cada interação
@st.cache_resource
def get_db_connection():
    """
    Cria e retorna uma conexão com o banco de dados MySQL.
    As credenciais são as mesmas configuradas no seu docker-compose.yml.
    """
    try:
        conn = mysql.connector.connect(
            host='db', #'db' é o nome do serviço do MySQL no docker-compose.yml
            user='farmtech_user',
            password='password',
            database='farmtech_db',
            port=3306
        )
        # st.success("Conectado ao banco de dados MySQL com sucesso!")
        return conn
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            st.error("Erro de acesso ao MySQL: verifique usuário e senha.")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            st.error("O banco de dados 'farmtech_db' não existe.")
        else:
            st.error(f"Erro ao conectar ao banco de dados MySQL: {err}")
        return None


@st.cache_data
def carregar_plantacoes():
    """
    Carrega todas as plantações do banco de dados MySQL.
    """
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        df = pd.read_sql_query("SELECT * FROM Plantacao", conn)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar plantações: {e}")
        return pd.DataFrame()
    finally:
        # Não fechamos a conexão aqui porque ela é gerenciada pelo st.cache_resource
        pass 

@st.cache_data
def carregar_leituras(id_plantacao):
    """
    Carrega as leituras de sensores para uma plantação específica do banco de dados MySQL.
    Utiliza %s como placeholder para o parâmetro id_plantacao.
    """
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()

    query = """
    SELECT L.data_hora, L.valor, L.tipo_sensor
    FROM Leitura L
    JOIN Sensor S ON L.id_sensor = S.id
    WHERE S.id_plantacao = %s
    ORDER BY L.data_hora
    """
    try:
        df = pd.read_sql_query(query, conn, params=(id_plantacao,))
        if not df.empty:
            df['data_hora'] = pd.to_datetime(df['data_hora'])
        return df
    except Exception as e:
        st.error(f"Erro ao carregar leituras para a plantação ID {id_plantacao}: {e}")
        return pd.DataFrame()
    finally:
        # Não fechamos a conexão aqui porque ela é gerenciada pelo st.cache_resource
        pass

st.title("🌱 FarmTech Solutions - Dashboard de Monitoramento")
st.markdown("Visualize dados em tempo real e previsões para otimizar sua plantação.")

st.sidebar.header("Filtros")
plantacoes_df = carregar_plantacoes()

if plantacoes_df.empty:
    st.warning("Nenhuma plantação cadastrada ou erro de conexão com o banco de dados. Por favor, certifique-se de que o MySQL está rodando no Docker e que o script `banco_dados.py` foi executado para adicionar dados.")
    st.stop()

lista_plantacoes = ["Visão Geral"] + plantacoes_df['nome'].tolist()
plantacao_selecionada_nome = st.sidebar.selectbox("Selecione uma Plantação", lista_plantacoes)

if plantacao_selecionada_nome == "Visão Geral":
    st.header("🌾 Visão Geral de Todas as Plantações")
    st.dataframe(plantacoes_df, use_container_width=True)
    st.markdown("""
    Esta seção apresenta uma visão consolidada de todas as plantações cadastradas.
    Para análises detalhadas e previsões, selecione uma plantação específica no menu lateral.
    """)

else:
    id_plantacao_selecionada = int(plantacoes_df[plantacoes_df['nome'] == plantacao_selecionada_nome]['id'].iloc[0])
    info_plantacao = plantacoes_df[plantacoes_df['id'] == id_plantacao_selecionada].iloc[0]

    st.header(f"📍 Plantação: {info_plantacao['nome']}")
    st.write(f"**Localização:** {info_plantacao['localizacao']}")
    st.markdown(f"**Umidade Ideal:** `{info_plantacao['umidade_ideal']:.1f}%`")
    st.markdown(f"**pH Ideal do Solo:** `{info_plantacao['ph_ideal_min']:.1f}` a `{info_plantacao['ph_ideal_max']:.1f}`")
    
    leituras_df = carregar_leituras(id_plantacao_selecionada)

    if leituras_df.empty:
        st.info("Ainda não há leituras para esta plantação. Por favor, adicione leituras usando o script de gerenciamento do banco de dados.")
        st.stop()

    st.subheader("📊 Métricas em Tempo Real (Última Leitura)")
    col1, col2, col3 = st.columns(3)

    # Filtrar e obter a última leitura para Umidade e pH
    df_umidade_sensor = leituras_df[leituras_df['tipo_sensor'] == 'umidade']
    df_ph_sensor = leituras_df[leituras_df['tipo_sensor'] == 'ph']
    
    ultima_umidade = df_umidade_sensor['valor'].iloc[-1] if not df_umidade_sensor.empty else "N/A"
    ultima_ph = df_ph_sensor['valor'].iloc[-1] if not df_ph_sensor.empty else "N/A"
    
    col1.metric(
        "Umidade Atual",
        f"{ultima_umidade} %",
        f"Ideal: {info_plantacao['umidade_ideal']:.1f}%"
    )
    col2.metric(
        "pH do Solo Atual",
        f"{ultima_ph}",
        f"Ideal: {info_plantacao['ph_ideal_min']:.1f}-{info_plantacao['ph_ideal_max']:.1f}"
    )
    col3.metric(
        "Total de Leituras Registradas",
        f"{len(leituras_df)}"
    )

    st.subheader("📈 Histórico de Leituras - Gráficos de Linha")
    
    if not df_umidade_sensor.empty:
        st.write("#### Variação da Umidade do Solo ao Longo do Tempo")
        st.line_chart(df_umidade_sensor.set_index('data_hora')['valor'], use_container_width=True)
        st.caption("Este gráfico mostra a variação da umidade do solo (%) ao longo do tempo para esta plantação.")
    else:
        st.info("Nenhum dado de umidade disponível para exibir gráfico.")

    if not df_ph_sensor.empty:
        st.write("#### Variação do pH do Solo ao Longo do Tempo")
        st.line_chart(df_ph_sensor.set_index('data_hora')['valor'], use_container_width=True, color="#FFA500") # Exemplo de cor
        st.caption("Este gráfico mostra a variação do pH do solo ao longo do tempo para esta plantação.")
    else:
        st.info("Nenhum dado de pH disponível para exibir gráfico.")

    # Predição com Scikit-learn
    st.subheader("🤖 Previsão de Umidade com Machine Learning")

    if len(df_umidade_sensor) < 2:
        st.warning("É necessário ter pelo menos 2 leituras de umidade para esta plantação para fazer uma previsão. Adicione mais dados para ativar a previsão.")
    else:
        # Preparando os dados para o modelo de Regressão Linear
        # Convertendo datetime para timestamp (número de segundos desde a Época)
        df_modelo = df_umidade_sensor.copy()
        df_modelo['timestamp'] = df_modelo['data_hora'].apply(lambda x: x.timestamp())
        
        X = df_modelo[['timestamp']] # Feature: o tempo em timestamp
        y = df_modelo['valor']      # Target: o valor da umidade

        # Treinando o modelo de Regressão Linear
        modelo = LinearRegression()
        modelo.fit(X, y)

        # Fazer a previsão para 1 hora no futuro (3600 segundos)
        ultimo_timestamp = X['timestamp'].iloc[-1]
        proximo_timestamp = ultimo_timestamp + 3600
        
        # A previsão precisa de um array 2D, por isso np.array([[...]])
        previsao = modelo.predict(np.array([[proximo_timestamp]]))
        
        st.success(f"**Previsão de umidade para a próxima hora: {previsao[0]:.2f} %**")
        st.markdown("""
        Este modelo de **Regressão Linear** simples usa o histórico de tempo e umidade para prever a tendência futura. 
        Com mais dados e uma frequência de leituras maior, o modelo tende a se tornar mais preciso e pode ajudar a 
        antecipar necessidades de irrigação, otimizando o uso da água e a saúde da plantação.
        """)
