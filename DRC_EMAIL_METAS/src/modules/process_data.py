from modules.logger import get_logger
import pandas as pd

# Logger configuration
logger = get_logger()

def process_data(data):
    """
    Function to process and handle the data collected from the Oracle SQL database.

    :data: Data extracted from the database.
    """
    try:
        # Columns name
        columns = ['ID',
                'DATA',
                'NOME_VENDEDOR',
                'EMAIL_VENDEDOR',
                'CPF_VENDEDOR',
                'VALOR',
                'PLANO',
                'CPF_CLIENTE',
                'VENDAS',
                'VALOR_META',
                'VALOR_META_FINAL',
                'LIDER']

        # Creating a dataframe from the extracted data
        df = pd.DataFrame(data, columns=columns)

        # Grouping the sales by affiliate to calculate the total commission
        df_grouped = df.groupby(['CPF_VENDEDOR'], as_index=False)['VALOR_META_FINAL'].sum()

        # Select relevant columns for sales
        df_sales = df[[
            'CPF_VENDEDOR', 
            'DATA', 
            'CPF_CLIENTE', 
            'VALOR', 
            'PLANO', 
            'VALOR_META', 
            'VALOR_META_FINAL', 
            'VENDAS'
            ]]

        # Initialize an empty dictionary to store affiliate data
        affiliate_data = {}

        # Iterating through the affiliates
        for _, row in df_grouped.iterrows():
            # Using CPF to find the corresponding sales
            cpf = row['CPF_VENDEDOR'] 
            # Filtering the sales for this affiliate
            sales = df_sales[df_sales['CPF_VENDEDOR'] == cpf] 
            affiliate = df[df['CPF_VENDEDOR'] == cpf]

            # Converting DataFrames to dictionaries for easier manipulation
            affiliate_dict = affiliate.to_dict(orient='records')[0]

            sales_dict = sales[[
                'DATA', 
                'CPF_CLIENTE', 
                'VALOR', 
                'PLANO', 
                'VALOR_META', 
                'VALOR_META_FINAL', 
                'VENDAS'
                ]].to_dict(orient='records')

            # Storing the affiliate data, including sales and commissions, in the dictionary
            affiliate_data[cpf] = {
                'VENDEDOR': affiliate_dict,  # Affiliate information as a dictionary
                'VENDAS': sales_dict,  # Sales as a list of dictionaries
                'COMISSAO': row['VALOR_META_FINAL'] # Commission for the affiliate
            }

        return affiliate_data

    except Exception as e:
        error = f"Erro ao tratar dados! {e}"
        logger.error(error)
        raise ValueError(error)
    
