import os
from dotenv import load_dotenv
from modules.logger import get_logger

# Logging function
logger = get_logger()

def check_env_var(var_name: str) -> str:
    """
    Function to check if an environment variable exists and is not empty.

    :param var_name: Name of the environment variable
    """
    value = os.getenv(var_name)
    
    if not value or not value.strip():
        error = f"A variável de ambiente {var_name} não foi encontrada no arquivo .env!"
        logger.error(error)
        raise ValueError(error)
    return value
         
# Loads environment variables from the .env file
load_dotenv()

# Verifies the environment variables for Zimbra email
ZIMBRA_EMAIL = check_env_var("ZIMBRA_EMAIL")
ZIMBRA_EMAIL_PASSWORD = check_env_var("ZIMBRA_EMAIL_PASSWORD")
SMTP_SERVER = check_env_var("SMTP_SERVER")
SMTP_PORT = check_env_var("SMTP_PORT")

# Verifies the environment variables for database connection
DB_NAME = check_env_var("DB_NAME")
DB_USER = check_env_var("DB_USER")
DB_PASSWORD = check_env_var("DB_PASSWORD")
