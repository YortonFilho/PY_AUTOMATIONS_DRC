from modules.email_functions import send_emails_to_users
from modules.process_data import process_data
from modules.logger import get_logger
from modules.database import Database

# Logger configuration
logger = get_logger()

# Main function
def main() -> None:
    """
    Function to execute main functions
    """
    try:
        # Initialize database connection
        database = Database()
        
        # Extrating data
        logger.info("Extraindo dados...")
        data = database.extract_data("SELECT * FROM VIEW_DRC_METAS WHERE VENDAS IS NOT NULL")

        # processing data
        logger.info("Processando dados...")
        affiliate_data = process_data(data)
        
        # List of bcc
        bcc_emails = ['yorton.filho@centraldeconsultas.med.br']

        # Send emails
        logger.info("Enviando emails...")
        send_emails_to_users(affiliate_data=affiliate_data, bcc_emails=bcc_emails)

        # Close connection to the database
        database.close()
        logger.info("Conexão com banco de dados encerrada!")

    except Exception as e:
        logger.error(f"Erro ao executar scrip principal! {e}")

if __name__ == "__main__":
    main()