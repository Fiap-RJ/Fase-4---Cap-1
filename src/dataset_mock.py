import datetime

# Dados Mockados para Plantações
plantacoes_mock = [
    {
        "nome": "Fazenda Teste Mockada",
        "localizacao": "Setor A",
        "umidade_ideal": 65.0,
        "ph_ideal_min": 6.2,
        "ph_ideal_max": 6.8
    },
    {
        "nome": "Horta do Quintal",
        "localizacao": "Jardim",
        "umidade_ideal": 55.0,
        "ph_ideal_min": 5.8,
        "ph_ideal_max": 6.5
    }
]

# Dados Mockados para Sensores
sensores_mock_template = [
    {"tipo": "umidade"},
    {"tipo": "ph"},
    {"tipo": "temperatura"},
    {"tipo": "umidade"} # Mais um sensor de umidade para Horta do Quintal
]

# Dados Mockados para Leituras

def gerar_leituras_mock(sensor_id_umidade, sensor_id_ph, sensor_id_temperatura, num_leituras=48):
    """
    Gera uma lista de leituras mockadas para os sensores fornecidos.
    num_leituras = 48 -> 2 leituras por hora por 24 horas.
    """
    leituras = []
    agora = datetime.datetime.now()
    intervalo_segundos = 3600 / (num_leituras / 24) # Ex: 30 minutos

    for i in range(num_leituras):
        # Gera datas retroativas para simular histórico
        delta = datetime.timedelta(seconds=(num_leituras - 1 - i) * intervalo_segundos)
        data_hora_leitura = agora - delta
        data_hora_str = data_hora_leitura.strftime('%Y-%m-%d %H:%M:%S')

        # Valores simulados (com alguma variação)
        umidade_valor = round(50 + (i % 10) * 1.5 + (i % 5) * 0.5 + (i / num_leituras) * 10, 2)
        ph_valor = round(6.0 + (i % 7) * 0.1 + (i / num_leituras) * 0.5, 2)
        temperatura_valor = round(20 + (i % 8) * 0.3 + (i / num_leituras) * 5, 2)

        leituras.append({
            "id_sensor": sensor_id_umidade,
            "tipo_sensor": "umidade",
            "data_hora": data_hora_str,
            "valor": umidade_valor
        })
        leituras.append({
            "id_sensor": sensor_id_ph,
            "tipo_sensor": "ph",
            "data_hora": data_hora_str,
            "valor": ph_valor
        })
        leituras.append({
            "id_sensor": sensor_id_temperatura,
            "tipo_sensor": "temperatura",
            "data_hora": data_hora_str,
            "valor": temperatura_valor
        })
    return leituras
