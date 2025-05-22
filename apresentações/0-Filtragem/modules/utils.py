from datetime import datetime
import pandas as pd
import requests

# Função para buscar dados da API do Banco Central
def fetch_bcb_series(series_code, start_date, end_date=None):
    """
    Busca uma série do Banco Central do Brasil usando a API SGS.
    
    Args:
        series_code (int): Código da série.
        start_date (str): Data de início no formato DD/MM/AAAA.
        end_date (str): Data de fim no formato DD/MM/AAAA (default: hoje).
    
    Returns:
        pd.DataFrame: DataFrame com as datas e valores da série.
    """
    if end_date is None:
        end_date = datetime.today().strftime('%d/%m/%Y')
    
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{series_code}/dados"
    params = {"formato": "json", "dataInicial": start_date, "dataFinal": end_date}
    print(url)
    print(params)
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()
    df = pd.DataFrame(data)
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
    return df

def fetch_ibge_series(parametros,printu=False):
    """
    Busca dados do IBGE usando a API SIDRA.
    
    Args:
        table_id (int): Código da tabela no SIDRA.
        variable_id (int): Código da variável na tabela.
        period (str): Período de busca (default: "all").
    
    Returns:
        pd.DataFrame: DataFrame com os dados da série.
    """                                         
    url = f"https://apisidra.ibge.gov.br/values/{parametros}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    if printu: print(url)
    
    # Converter JSON para DataFrame
    df = pd.DataFrame(data[1:])  # Ignora o cabeçalho
    df['data'] = pd.to_datetime(df['D2C'].str[:4] + '-' + (df['D2C'].str[4:].astype(int) * 3 - 2).astype(str), format='%Y-%m')
    df['valor'] = pd.to_numeric(df['V'], errors='coerce')
    return df[['data', 'valor']]