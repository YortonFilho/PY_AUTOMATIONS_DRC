import pandas as pd
from modules.logger import get_logger
from typing import Dict, List

# função para gerar logs
logger = get_logger()

def is_dict_or_list(x) -> bool:
    return isinstance(x, dict) or isinstance(x, list)

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Função para expandir JSONs ou arrays dentro das colunas.
    
    :param df: DataFrame com o as colunas que devem ser 'normalizadas'.
    """
    while True:
        columns_to_expand = [col for col in df.columns if df[col].apply(is_dict_or_list).any()]
        if not columns_to_expand:
            break
        for column in columns_to_expand:
            if df[column].apply(lambda x: isinstance(x, dict)).any():
                json_df = pd.json_normalize(df[column])
                json_df.columns = [f"{column}_{subcol}" for subcol in json_df.columns]
                df = pd.concat([df.drop(columns=[column]), json_df], axis=1)
            elif df[column].apply(lambda x: isinstance(x, list)).any():
                array_df = df[column].apply(lambda x: pd.Series(x) if isinstance(x, list) else pd.Series([x]))
                array_df.columns = [f"{column}_{i}" for i in array_df.columns]
                df = pd.concat([df.drop(columns=[column]), array_df], axis=1)
    return df

def process_payments_data(data: list) -> pd.DataFrame:
    """
    Processa e formata dados do endpoint "payments", incluindo conversões de colunas de data e 
    tradução de valores de status, gerando um dataFrame.

    :param data: Dados brutos extraídos da API.
    """
    try:
        df = pd.DataFrame(data)
        df = normalize_columns(df)

        # Traduzindo os nomes das colunas desejadas
        columns_mapping = {
            'id': 'ID',
            'dateCreated': 'DATA_CRIACAO',
            'customer': 'ID_CLIENTE',
            'paymentLink': 'LINK_PAGAMENTO',
            'value': 'VALOR',
            'netValue': 'VALOR_LIQUIDO',
            'description': 'DESCRICAO',
            'billingType': 'METODO_PAGAMENTO',
            'pixTransaction': 'TRANSACAO_PIX',
            'status': 'STATUS',
            'dueDate': 'DATA_VENCIMENTO',
            'clientPaymentDate': 'DATA_PAGAMENTO_CLIENTE',
            'installmentNumber': 'NUMERO_PARCELA',
            'invoiceUrl': 'URL_FATURA',
            'invoiceNumber': 'NUMERO_FATURA',
            'externalReference': 'REFERENCIA_EXTERNA',
            'creditDate': 'DATA_CREDITO',
            'creditCard_creditCardBrand': 'BANDEIRA_CARTAO'
        }

        # Seleciona e renomeia as colunas
        df_filtered = df[columns_mapping.keys()].rename(columns=columns_mapping)

        # conversão de colunas de data para o formato 'DD/MM/AAAA'
        date_columns = ['DATA_CRIACAO', 'DATA_VENCIMENTO', 'DATA_PAGAMENTO_CLIENTE', 'DATA_CREDITO']
        for col in date_columns:
            df_filtered[col] = pd.to_datetime(df_filtered[col], errors='coerce').dt.strftime('%d/%m/%Y')

        # traduzindo campos necessários
        status_translation = {
            'CONFIRMED': 'CONFIRMADO',
            'REFUNDED': 'REEMBOLSADO',
            'RECEIVED': 'RECEBIDO',
            'OVERDUE': 'VENCIDO',
            'PENDING': 'PENDENTE',
            'CHARGEBACK_DISPUTE': 'DISPUTA DE ESTORNO',
            'CHARGEBACK_REQUESTED': 'SOLICITAÇÃO DE ESTORNO'
        }
        df_filtered['STATUS'] = df_filtered['STATUS'].replace(status_translation)

        billing_type_translation = {
            'CREDIT_CARD': 'CARTAO DE CREDITO'
        }
        df_filtered['METODO_PAGAMENTO'] = df_filtered['METODO_PAGAMENTO'].replace(billing_type_translation)
        
        logger.info("Dados processados com sucesso!")
        return df_filtered
    
    except Exception as e:
        logger.error(f"Erro ao tratar dados! {e}")
        raise e

def process_customers_data(data: list) -> pd.DataFrame:
    """
    Processa e formata dados do endpoint "customers", incluindo conversões de colunas de data 
    e tradução de valores gerando um dataFrame.

    :param data: Dados brutos extraídos da API.
    """
    try:
        df = pd.DataFrame(data)
        df = normalize_columns(df)

        # Traduzindo os nomes das colunas desejadas
        columns_mapping = {
            "id": "ID",
            "dateCreated": "DATA_CRIACAO",
            "name": "NOME",
            "email": "EMAIL",
            "phone": "TELEFONE",
            "mobilePhone": "CELULAR",
            "address": "ENDERECO",
            "addressNumber": "NUMERO_ENDERECO",
            "complement": "COMPLEMENTO",
            "province": "PROVINCIA",
            "postalCode": "CEP",
            "cpfCnpj": "CPF_CNPJ",
            "externalReference": "REFERENCIA_EXTERNA",
            "city": "ID_CIDADE",
            "cityName": "NOME_CIDADE",
            "state": "ESTADO",
            "country": "PAIS"
        }

        # Seleciona e renomeia as colunas
        df_filtered = df[columns_mapping.keys()].rename(columns=columns_mapping)

        # convertendo data para o formato 'DD/MM/AAAA'
        df_filtered['DATA_CRIACAO'] = pd.to_datetime(df_filtered['DATA_CRIACAO']).dt.strftime('%d/%m/%Y')

        logger.info("Dados processados com sucesso!")
        return df_filtered

    except Exception as e:
        logger.error(f"Erro ao tratar dados! {e}")
        raise e
        