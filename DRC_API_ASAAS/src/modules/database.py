from modules.config import DB_NAME, DB_PASSWORD, DB_USER
from modules.logger import get_logger
import pyodbc
import pandas as pd

# Função de logging
logger = get_logger()

def db_connection() -> pyodbc.Connection:
    connection_data = f"DSN={DB_NAME};UID={DB_USER};PWD={DB_PASSWORD}"

    try:
        connection = pyodbc.connect(connection_data)
        logger.info("Banco de dados conectado com sucesso!")
        return connection  
    except pyodbc.Error as e:
          logger.error(f"Erro ao conectar com banco de dados! {e}")
          raise 

def update_db_data(df: pd.DataFrame, table: str) -> None:
    """
    Atualiza a tabela do banco de dados com os dados do DataFrame.
    Realiza uma exclusão total dos dados existentes e insere os novos dados.

    :param df: DataFrame contendo os dados a serem inseridos.
    :param table: Nome da tabela no banco de dados.
    """
    try:
        # Conectando com banco de dados
        with db_connection() as connection:
            with connection.cursor() as cursor:
                
                # Obtem a estrutura da tabela
                cursor.execute(f"SELECT COLUMN_NAME FROM ALL_TAB_COLUMNS WHERE TABLE_NAME = '{table}'")
                columns = [row[0] for row in cursor.fetchall()]
                num_columns = len(columns)

                # Reordena as colunas do DataFrame para corresponder a ordem da tabela
                df_filtered = df[columns] 

                # Verifica se o número de colunas na tabela corresponde ao número de colunas no DataFrame
                if len(df_filtered.columns) != num_columns:
                    logger.error(
                        f"Número de colunas no DataFrame ({len(df_filtered.columns)})" 
                        f"não corresponde ao número de colunas na tabela Oracle ({num_columns})."
                        )
                    return

                # Prepara a query para inserção dos dados
                placeholders = ', '.join(['?' for _ in range(num_columns)])
                insert_command = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"

                try:
                    # Excluir dados existentes
                    cursor.execute(f"DELETE FROM {table}")
                    logger.info(f"Dados da tabela deletados com sucesso!")

                    # Inserir novos dados
                    for index, row in df_filtered.iterrows():
                        values = row.tolist()
                        values = [None if v == '' or pd.isna(v) else v for v in values]

                        try:
                            cursor.execute(insert_command, values)                          
                        except pyodbc.Error as e:
                            logger.error(f"Erro ao inserir os seguintes dados: {values} ERRO: {e})")
                            connection.rollback() 
                            raise

                    connection.commit()
                    logger.info(f"Todos os dados foram inseridos na tabela '{table}'!")

                except pyodbc.Error as e:   
                    logger.error(f"Erro ao deletar dados da tabela {table}: {e}")
                    connection.rollback()
                    raise

    except pyodbc.Error as e:
        logger.error(f'Erro ao se conectar com banco de dados! {e}')
        raise
