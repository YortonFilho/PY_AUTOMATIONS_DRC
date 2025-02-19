import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Função para utilizar os logging
def get_logger():
    return logging.getLogger()
