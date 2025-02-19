from modules.config import DB_NAME, DB_PASSWORD, DB_USER
from modules.logger import get_logger
import oracledb
import os

# Function to generate logs
logger = get_logger()

class Oracle:
    def __init__(self) -> None:
        """ 
        Function Initializes the Oracle client 
        and connect to the database
        """
        client_path = r"C:\instantclient_19_21"

        try:
            os.environ["PATH"] = client_path + ";" + os.environ.get("PATH", "")
            oracledb.init_oracle_client(lib_dir=client_path)
            logger.info(f"Cliente Oracle inicializado com sucesso usando o caminho: {client_path}")

        except Exception as e:
            logger.error(f"Erro ao inicializar o cliente Oracle: {e}")
            raise e

        try:
            self.connection = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_NAME)
            self.cursor = self.connection.cursor()
            logger.info("Banco de dados conectado com sucesso!")
                    
        except oracledb.Error as e:
            error = f"Erro ao se conectar ao bando de dados: {e}"
            logger.error(error)
            raise ValueError(error)
        
    def extract_data(self, sql: str, params: dict = None) -> list:
        """
        Function to execute sql queries

        :param sql: SQL command to be executed
        :param params: Parameters to be used with the SQL command
        """
        try:
            self.cursor.execute(sql, params)
            data =  self.cursor.fetchall()
            logger.info("Dados coletados com sucesso!")
            return data
        
        except oracledb.Error as e:
            error = f"Erro ao executar consulta SQL! {e}"
            logger.error(error)
            raise ValueError(error)

    def close(self) -> None:
        """
        Function to close the database connection
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("Conexão fechada!")
    