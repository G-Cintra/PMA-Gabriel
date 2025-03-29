import requests
import pandas as pd
from datetime import datetime
import logging
import json

def load_bcb_series_metadata(json_path: str = "../data/metadata/bcb_series.json") -> pd.DataFrame:
    """
    Loads BCB series metadata from a JSON file and returns it as a DataFrame.

    Parameters:
        json_path (str): Relative or absolute path to the JSON metadata file.

    Returns:
        pd.DataFrame: A DataFrame with columns ['name', 'Descrição', 'code'].
    """
    logger = logging.getLogger()

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)

    logger.info(f"Loaded BCB Metadata from file: {json_path}")

    return df.set_index("name")

def fetch_bcb_series(series_code, start_date, end_date=None):
    """
    Fetches a time series from the Central Bank of Brazil (BCB) SGS API.

    Args:
        series_code (int): The SGS series code.
        start_date (str): Start date in DD/MM/YYYY format.
        end_date (str, optional): End date in DD/MM/YYYY format (default: today).

    Returns:
        pd.DataFrame: A DataFrame with columns ['data', 'valor'], or empty on failure.
    """
    logger = logging.getLogger()

    if end_date is None:
        end_date = datetime.today().strftime('%d/%m/%Y')

    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{series_code}/dados"
    params = {"formato": "json", "dataInicial": start_date, "dataFinal": end_date}

    logger.info(f"Requesting BCB series {series_code} from {start_date} to {end_date}")
    logger.debug(f"URL: {url}")
    logger.debug(f"Parameters: {params}")

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        df = pd.DataFrame(data)
        df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
        df['valor'] = pd.to_numeric(df['valor'], errors='coerce')

        logger.info(f"Successfully fetched {len(df)} rows for series {series_code}")
        return df

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error while fetching series {series_code}: {e}")
        try:
            error_json = response.json()
            logger.error("API error details:")
            for key, value in error_json.items():
                logger.error(f"{key}: {value}")
        except Exception:
            logger.warning("Failed to parse error response as JSON.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for series {series_code}: {e}")
    except ValueError as e:
        logger.error(f"Data parsing error for series {series_code}: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error while fetching series {series_code}: {e}")

    return pd.DataFrame()
