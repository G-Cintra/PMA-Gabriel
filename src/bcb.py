from datetime import datetime
import requests
import pandas as pd

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