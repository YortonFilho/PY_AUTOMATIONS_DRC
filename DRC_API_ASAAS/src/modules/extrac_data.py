import requests
from datetime import datetime
from modules.config import API_KEY, API_URL
from modules.logger import get_logger

# Função para gerar logs
logger = get_logger()

def extract_data(endpoint: str, start_date: str = None, end_date:str = None) -> list:
    """
    Função para fazer requisições GET à API. A função utiliza a mesma chave de API, URL base e 
    intervalo de datas para todas as requisições. 

    :param endpoint: O ponto de extremidade da API a ser acessado, por exemplo: 'payments',
    'clients','subscriptions'.
    """

    # Lista vazia para inserir os dados
    data_list = []

    # Variáveis para o sistema de paginação
    offset = 0
    limit = 100

    # Laço de repetição para percorrer todas páginas
    while True:
        url = (
            f"{API_URL}{endpoint}?limit={limit}&offset={offset}&"
            f"dateCreated[ge]={start_date}&dateCreated[le]={end_date}"
        )

        headers = {
            "Content-Type" : "application/json",
            "access_token" : API_KEY
        }

        response = requests.get(url, headers=headers)

        # Verificação do código de resposta
        if response.status_code == 200:
            response_data = response.json()

            # Extrai a lista de dados da chave 'data'
            data = response_data.get("data", [])

            # Quando não tiver mais dados, encerra o laço de repetição.
            if not data:
                break

            data_list.extend(data)
            offset += limit
            
        elif response.status_code == 401:
            logger.error("Falha na autenticação: verifique sua chave de API.")
            raise
        elif response.status_code == 404:
            logger.error(f"Endpoint '{endpoint}' não encontrado.")
            raise
        else:
            logger.error(
                f"Erro ao fazer requisição para API no offset {offset}" 
                f"no endpoint '{endpoint}': Status {response.status_code}"
                )
            raise

    logger.info("Requisição para API realizada com sucesso!")
    return data_list 
