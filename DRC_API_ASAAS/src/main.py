from modules.extrac_data import extract_data
from modules.process_data import process_payments_data, process_customers_data
from modules.database import update_db_data
from modules.logger import get_logger
from datetime import datetime

# Configuração de logging
logger = get_logger()

def run_pipeline(endpoint, table, function, start_date=None, end_date=None):
    """
    Executa os scripts de extração, processamento e atualização dos dados no banco de dados.

    :param endpoint: endpoint da API a ser acessado para extrair dados.
    :param table: nome da tabela do banco onde os dados serão inseridos.
    :param function: Função especifica de tratamento de dados para o endpoint.
    :param start_date: Data de início para a extração de dados (no formato 'AAAA-MM-DD').
    :param end_date: Data de término para a extração de dados (a data atual)
    """
    try:
        # extraindo dados da API
        logger.info(f"Iniciando a extração dos dados do endpoint '{endpoint}'! Por favor aguarde...")
        raw_data = extract_data(endpoint, start_date=start_date, end_date=end_date)

        # Processando dados extraídos
        logger.info("Processando os dados extraídos...")
        processed_data = function(raw_data)

        # Atualizando banco de dados
        logger.info(f"Iniciando atualização dos dados na tabela '{table}'...")
        update_db_data(processed_data, table)

        logger.info("Pipeline concluído com sucesso!")

    except Exception as e:
        logger.error(f"Ocorreu um erro inesperado: {e}")

def main():
    # Datas para os endpoints
    start_date = "2023-01-01"
    end_date = datetime.now().strftime("%Y-%m-%d")

    # Configurações para os endpoints e tabelas
    pipelines = [
        {"endpoint": "payments", "table": "DADOS_API_ASAAS_PAYMENTS", "process_function": process_payments_data},
        {"endpoint": "customers", "table": "DADOS_API_ASAAS_CUSTOMERS", "process_function": process_customers_data}
    ]

    # Executando o pipeline para cada configuração
    for pipeline in pipelines:
        try:
            run_pipeline(
                pipeline["endpoint"], 
                pipeline["table"], 
                pipeline["process_function"], 
                start_date, 
                end_date
            )

        except Exception as e:
            logger.error(f"Falha ao executar pipeline para o endpoint '{pipeline['endpoint']}': {e}")
            continue 

if __name__ == "__main__":
    main()
