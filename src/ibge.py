import logging
import json
import pandas as pd
import requests
import hashlib

def load_ibge_series_metadata(json_path: str = "../data/metadata/ibge_series.json") -> pd.DataFrame:
    """
    Loads IBGE series metadata from a JSON file and returns it as a DataFrame.

    Parameters:
        json_path (str): Relative or absolute path to the JSON metadata file.

    Returns:
        pd.DataFrame: A DataFrame with columns ['name', 'Descrição', 'code'].
    """
    logger = logging.getLogger()

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)

    logger.info(f"Loaded IBGE Metadata from file: {json_path}")

    return df.set_index("name")

def name_to_details(name,df_ibge_series_metadata):
    # Get Series Metadata
    row = df_ibge_series_metadata.loc[name]

    #Build URL
    if pd.notna(row["category"]):
            category = f"c11255/{row['category']:.0f}"
    else:
            category = ""

    table=row["table"]
    variable=row["variable"]

    return table,variable,category


def build_URL(table,variable,category,sidra):

    # Select Base URL
    if sidra:
        base_url = f"https://apisidra.ibge.gov.br/values/t/{table}/v/{variable}/p/all/N1/1/{category}"
    else:
        base_url = f"https://servicodados.ibge.gov.br/api/v3/agregados/{table}/periodos/all/variaveis/{variable}?localidades=N1[all]{category}"

    url = base_url.format(
        table=table,
        variable=variable,
        category=category
    )

    return url


def fetch_and_save(url, name, filename):
    logger = logging.getLogger()

    try:
        logger.info(f"Requesting data for: {name}")
        logger.debug(f"URL: {url}")

        # Request Data from API
        response = requests.get(url)
        response.raise_for_status()

        # Get JSON
        data = response.json()

        # Salve JSON file
        json_filename = f"{filename}.json"
        with open(json_filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"JSON file saved: {json_filename}")

        # Calculate SHA-256 for JSON file
        with open(json_filename, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        
        logger.debug(f"SSHA-256 hash of saved JSON file: {file_hash}")

        # Create dataframe
        df = pd.DataFrame(data[1:]) 
        df['data'] = pd.to_datetime(df['D2C'].str[:4] + '-' + (df['D2C'].str[4:].astype(int) * 3 - 2).astype(str), format='%Y-%m')    
        df['valor'] = pd.to_numeric(df['V'], errors='coerce')
        df = df[['data', 'valor']]

        # Save DataFrame to CSV without the index
        csv_filename = f"{filename}.csv"
        df.to_csv(csv_filename , index=False)
        logger.info(f"CSV file saved: {csv_filename }")

        # Compute SHA-256 hash of the saved file
        with open(csv_filename, "rb") as f:
            file_bytes = f.read()
            file_hash = hashlib.sha256(file_bytes).hexdigest()

        # Log the hash for traceability
        logger.debug(f"SHA-256 hash of saved CSV file: {file_hash}")       

        return df

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error for {name}: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for {name}: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error for {name}: {e}")
    
    return None