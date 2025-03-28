import json
import pandas as pd

def load_bcb_series_metadata(json_path: str = "../data/metadata/bcb_series.json") -> pd.DataFrame:
    """
    Loads BCB series metadata from a JSON file and returns it as a DataFrame.

    Parameters:
        json_path (str): Relative or absolute path to the JSON metadata file.

    Returns:
        pd.DataFrame: A DataFrame with columns ['name', 'Descrição', 'code'].
    """
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    return df.set_index("name")
