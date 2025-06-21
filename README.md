# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="[Image of FIAP Logo]" border="0" width=40% height=40%></a>
</p>

<br>

# FarmTech Solutions - Sistema de Monitoramento Agrícola Inteligente

## Nome do grupo

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/arthur-alentejo/">Arthur Alentejo</a>
- <a href="https://www.linkedin.com/in/michaelrodriguess/">Michael Rodrigues</a>
- <a href="https://www.linkedin.com/in/nathalia-vasconcelos-18a390292/">Nathalia Vasconcelos</a> 


## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/company/inova-fusca">Lucas Moreira</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/company/inova-fusca">Andre Godoi</a>


## 📜 Descrição Geral do Projeto

Este projeto, **FarmTech Solutions**, visa otimizar a agricultura através de um sistema de monitoramento e irrigação inteligente. Iniciado com uma simulação de sensores agrícolas e acionamento de bomba de irrigação (via relé e LED) em resposta à baixa umidade do solo, montado na plataforma Wokwi.com.

Para a simulação de sensores, utilizamos:
* **Botões:** Para simular a presença de Potássio e Fósforo no solo.
* **Sensor LDR:** Usado para simulação de pH do solo (normalmente utilizado para luminosidade).
* **Sensor DHT22:** Para simulação de umidade e temperatura do solo/ambiente.

O controle geral do sistema é feito por um microcontrolador **ESP32**.

Na **Fase 4**, levamos o projeto a um novo nível de sofisticação, incorporando:
* **Inteligência com Scikit-learn:** Modelos preditivos para otimizar decisões de irrigação.
* **Dashboard Interativo com Streamlit:** Interface web para visualização de dados em tempo real e insights.
* **Banco de Dados MySQL:** Para persistência robusta dos dados coletados.
* **Otimizações no ESP32:** Melhorias de performance e uso de memória no firmware.

## 🎯 Desafios e Requisitos da FASE 4:

* **Incorporar Scikit-learn:** Utilizar a biblioteca Scikit-learn para aprimorar a inteligência do sistema de irrigação automatizado, criando um modelo preditivo que sugira ações futuras de irrigação (e.g., previsão da necessidade de irrigação com base no histórico de umidade).
* **Implementar Streamlit:** Aprimorar o dashboard do projeto utilizando Streamlit, criando uma interface interativa para visualização em tempo real de dados (gráficos de umidade, níveis de nutrientes) e insights gerados pelo Machine Learning.
* **Adicionar display LCD no Wokwi:** Usar um display LCD conectado ao ESP32 no Wokwi (barramento I2C - pinos SDA e SCL) para mostrar métricas principais (umidade, níveis de nutrientes, status da irrigação) diretamente no sistema físico simulado.
* **Monitoramento com Serial Plotter:** Implementar o uso do Serial Plotter para monitorar variáveis do projeto (e.g., umidade), apresentando mudanças em tempo real para análise visual.
* **Otimização de Memória no ESP32:** Revisar e otimizar o uso das variáveis no código C/C++ do ESP32, realizando otimizações com tipos de dados inteiros, floats e chars para economizar memória e garantir eficiência, com comentários no código justificando as escolhas.

## ✨ Novas Funcionalidades Implementadas na Fase 4

### 1. **Dashboard Interativo com Streamlit e Scikit-learn**

Uma interface web amigável e moderna para monitorar e analisar os dados da plantação.

* **Visualização em Tempo Real:** Métricas atualizadas da última leitura de umidade e pH.
* **Histórico de Leituras:** Gráficos de linha que mostram a variação dos parâmetros coletados ao longo do tempo.
* **Previsão de Umidade:** Um modelo de **Regressão Linear** do Scikit-learn prevê a umidade futura (por exemplo, para a próxima hora) com base no histórico de dados, auxiliando significativamente na decisão de irrigação e otimização do uso da água.

![Dashboard FarmTech](assets/imagem_dashboard.png)

### 2. **Banco de Dados MySQL Persistente e Modularizado**

Os dados dos sensores e das plantações são agora armazenados em um banco de dados MySQL, gerenciado via Docker, garantindo persistência, integridade e acessibilidade para o dashboard.

* **Estrutura de Dados Aprimorada:** O modelo de banco de dados foi revisado para melhor representar as entidades de plantações, sensores e suas leituras.
* **População de Dados Modular:** Introduzimos um script separado (`populate_db.py`) que utiliza um dataset mockado (`dataset_mock.py`) para popular o banco de dados com dados de teste de forma organizada, facilitando o desenvolvimento e a demonstração.

### 3. **Monitoramento Avançado no Hardware (Wokwi - ESP32)**

* **Display LCD (I2C):** Integrado ao ESP32 no Wokwi, o display LCD 16x2 exibe as principais métricas (umidade, temperatura, pH, status de nutrientes) em tempo real, fornecendo informações críticas diretamente no "campo".
* **Serial Plotter:** A umidade do solo é monitorada continuamente e visualizada em tempo real através do Serial Plotter do Wokwi. Este recurso é fundamental para depuração e análise visual do comportamento do sensor e da lógica de irrigação.

![Wokwi LCD e Serial Plotter](assets/imagem_wokwi.png)

### 4. **Otimização de Memória no ESP32**

O código C/C++ (`src/prog1.ino`) foi meticulosamente revisado para otimizar o uso de memória. Isso incluiu a análise e adequação de tipos de dados (e.g., `uint8_t` para variáveis que armazenam valores pequenos, minimizando o uso de `float` onde a precisão não é crítica para economia de RAM), garantindo que o sistema rode de maneira mais eficiente e estável em um ambiente embarcado. As modificações e as justificativas para as escolhas de otimização estão devidamente comentadas diretamente no código-fonte.

## 📁 Estrutura de Pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

-   **`.github`**: Nesta pasta ficarão os arquivos de configuração específicos do GitHub que ajudam a gerenciar e automatizar processos no repositório.
-   **`assets`**: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens (incluindo as capturas de tela do dashboard e Wokwi).
-   **`config`**: Posicione aqui arquivos de configuração que são usados para definir parâmetros e ajustes do projeto.
-   **`document`**: aqui estão todos os documentos do projeto que as atividades poderão pedir. Na subpasta "other", adicione documentos complementares e menos importantes.
-   **`scripts`**: Posicione aqui scripts auxiliares para tarefas específicas do seu projeto. Exemplo: deploy, migrações de banco de dados, backups.
-   **`src`**: Todo o código fonte criado para o desenvolvimento do projeto ao longo das 7 fases.
    * `src/prog1.ino`: Código C/C++ para ESP32 (sensores, LCD, lógica de relé).
    * `src/banco_dados.py`: Script Python para operações CRUD manuais no MySQL (cria tabelas).
    * `src/dataset_mock.py`: **(NOVO)** Definições dos dados de teste (mockados) para população do banco.
    * `src/populate_db.py`: **(NOVO)** Script Python para popular o MySQL com dados de teste.
    * `src/dashboard.py`: Aplicação Streamlit (dashboard web com ML e Pandas).
-   **`docker-compose.yml`**: Configuração para orquestrar o serviço MySQL e a aplicação Python.
-   **`Dockerfile`**: Instruções para construir a imagem Docker da aplicação Python.
-   **`requirements.txt`**: Dependências Python (Streamlit, Pandas, Scikit-learn, mysql-connector).
-   **`diagram.json`**: Configuração da simulação do hardware no Wokwi.
-   **`README.md`**: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

## 🚀 Como Rodar o Projeto (Ambiente Docker)

Para configurar e executar a aplicação FarmTech Solutions em seu ambiente local usando Docker, siga os passos abaixo:

1.  **Pré-requisitos:**
    * Certifique-se de ter o [Docker Desktop](https://www.docker.com/products/docker-desktop/) (ou Docker Engine e Docker Compose) instalado e em execução em sua máquina.

2.  **Navegue até o diretório raiz do projeto:**
    * Abra o terminal e vá para a pasta onde estão os arquivos `docker-compose.yml`, `Dockerfile`, etc.:
        ```bash
        cd /caminho/para/o/repositorio/Fase-4---Cap-1
        ```

3.  **Inicie os serviços Docker (MySQL e Streamlit App):**
    * Este comando derrubará quaisquer contêineres anteriores do projeto, removerá volumes de dados (garantindo um banco de dados limpo para teste) e, em seguida, construirá a imagem da sua aplicação Python e iniciará os contêineres do MySQL (`db`) e do Streamlit (`app`) em segundo plano.
        ```bash
        docker compose down --volumes && docker compose up --build -d
        ```
    * Aguarde alguns segundos para que ambos os serviços (`db` e `app`) estejam totalmente `Up`. Você pode verificar o status com `docker compose ps`.

4.  **Criar as Tabelas no Banco de Dados:**
    * Mesmo após a inicialização do MySQL, as tabelas ainda precisam ser criadas. Acesse o contêiner `app` e execute o script `banco_dados.py` que se conecta ao MySQL e cria as tabelas se elas não existirem:
        ```bash
        docker compose exec app python -m src.banco_dados
        ```
    * Você verá mensagens como "Criando tabela Plantacao... OK". Quando o "MENU FARMTECH" aparecer, digite `0` e pressione `Enter` para sair.

5.  **Popular o Banco de Dados com Dados de Teste (Mockados):**
    * Para que o dashboard tenha dados para exibir (plantas, sensores, leituras), execute o script de população de dados mockados:
        ```bash
        docker compose exec app python -m src.populate_db
        ```
    * Observe a saída no terminal. Ele deve indicar que as plantações, sensores e leituras de teste estão sendo inseridos. Este script também remove dados mockados antigos antes de inserir novos, garantindo que o dashboard sempre carregue dados consistentes.

6.  **Reiniciar o Contêiner do Streamlit (Importante para Recarregar Cache):**
    * O Streamlit usa cache para otimizar o desempenho. Para garantir que ele carregue os dados recém-inseridos, reinicie apenas o contêiner da sua aplicação:
        ```bash
        docker compose restart app
        ```

7.  **Acesse o Dashboard Streamlit:**
    * Após o contêiner `app` reiniciar (geralmente em poucos segundos), abra seu navegador e visite:
        ```
        http://localhost:8501
        ```
    * O dashboard FarmTech Solutions estará disponível, exibindo os dados das plantações de teste na barra lateral e os gráficos/previsões ao selecioná-las.

## 🌐 Simulação do Hardware (Wokwi)

Para ver a parte do ESP32 (sensores, LCD e Serial Plotter) em ação, que funciona de forma independente do ambiente Docker neste momento:

1.  Acesse seu projeto no Wokwi através do link fornecido: `https://wokwi.com/projects/SEU_ID_DO_PROJETO_WOKWI_AQUI`.
2.  Inicie a simulação clicando no botão `▶` (Play).
3.  Observe o **display LCD** para as métricas em tempo real (umidade, temperatura, pH, status de nutrientes).
4.  Abra o **Serial Plotter** no ambiente Wokwi para monitorar visualmente a variação da umidade ao longo do tempo.

## 📺 Demonstração em Vídeo

Assista a uma demonstração completa do sistema em funcionamento, cobrindo tanto a simulação de hardware quanto o dashboard web:

**[LINK PARA SEU VÍDEO NO YOUTUBE AQUI]**
*(Certifique-se de que o vídeo esteja "Não Listado" ou "Unlisted" para que apenas quem tem o link possa vê-lo.)*

## 🗃 Histórico de lançamentos

* 0.4.0 - 20/06/2025
    * **Fase 4:** Integração de Scikit-learn para previsão de umidade, dashboard Streamlit interativo, banco de dados MySQL, display LCD no Wokwi, Serial Plotter e otimizações de memória no ESP32.
* 0.3.0 - XX/XX/2024
    * **Fase 3:** Início da simulação de sensores, lógica de irrigação, controle com ESP32, prototipagem inicial.
* 0.2.0 - XX/XX/2024
    * **Fase 2:**
* 0.1.0 - 12/06/2025
    * **Fase 1:**


## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>