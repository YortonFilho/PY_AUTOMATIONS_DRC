
# README

## Descrição

Automação em Python para extrair e tratar dados da API do ASAAS, e importa-los para o banco de dados Oracle SQL. Essa automação foi implementada no Jenkins, programada para rodar todos os dias.

Projeto feito usando módulos e funções, para facilitar tanto a manutenção quanto a implementação de novos endpoints no futuro.

## Estrutura do Projeto

A estrutura do projeto é dividida nos seguintes módulos:

### 1. **main.py**
Este é o arquivo principal que executa as principais funções. Ele integra a extração, processamento e atualização dos dados no banco de dados. O fluxo de execução ocorre da seguinte maneira:
- Extração de Dados: Dados são extraídos de um endpoint da API especificado.
- Processamento de Dados: Os dados extraídos são processados por uma função específica de tratamento.
- Atualização no Banco de Dados: Após o processamento, os dados são inseridos na tabela correspondente no banco de dados.

### 2. **modules/config.py**
Carrega e verifica as variáveis de ambiente necessárias para a execução do projeto.

### 3. **modules/database.py**
Este módulo contém funções para conectar ao banco de dados e atualizar as tabelas com os dados de um DataFrame. As principais funções são:
- `db_connection()`: Estabelece a conexão com o banco de dados utilizando as credenciais de configuração (nome do banco, usuário e senha).
- `update_db_data(df, table)`: Atualiza a tabela do banco de dados com os dados do DataFrame. Realiza uma exclusão dos dados existentes e insere os novos dados.

### 4. **modules/extract_data.py**
Este módulo contém funções para fazer requisições GET à API e extrair dados com base nos parâmetros de data. A função principal é:
- `extract_data(endpoint, start_date=None, end_date=None)`: Realiza requisições à API utilizando um intervalo de datas e um ponto de extremidade específico. A função gerencia a paginação dos resultados e retorna os dados extraídos.

### 5. **modules/process_data.py**
Este módulo contém funções para processar e formatar os dados extraídos da API, incluindo a conversão de colunas de data e a tradução de valores. As principais funções são:
- `normalize_columns(df)`: Expande colunas que contêm dados em formato JSON ou lista, transformando-os em colunas separadas no DataFrame.
- `process_payments_data(data)`: Processa dados do endpoint "payments", realizando operações como conversão de colunas de data para o formato `DD/MM/AAAA`, renomeação de colunas e tradução de valores de status e métodos de pagamento.
- `process_customers_data(data)`: Processa dados do endpoint "customers", incluindo a conversão de datas e renomeação de colunas, bem como a tradução de alguns campos.

### 6. **modules/logger.py**
Gerencia a geração de logs para monitoramento e diagnóstico. Utiliza o módulo `logging` para registrar mensagens de erro, aviso e informações.

Cada módulo é projetado para ser independente, permitindo fácil manutenção e adição de novos recursos.

## Variáveis de Ambiente

- `DB_NAME`=nome-do-banco
- `DB_USER`=usuario-do-banco
- `DB_PASSWORD`=senha-do-banco
- `API_URL`=url-base-api.
- `API_KEY`=token-api.
