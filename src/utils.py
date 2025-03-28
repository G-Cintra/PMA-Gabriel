from datetime import datetime

def make_file_name(base_name: str = "IBGE_DATA", extension: str = "log") -> str:
    """
    Generates a timestamped session name with the format: YYYYMMDD_HHMMSS_basename.extension

    Parameters:
        base_name (str): The base name of the log file (e.g., 'IBGE_DATA')
        extension (str): File extension (default: 'log')

    Returns:
        str: A filename like '20250328_141230_dados_alterados.log'
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{timestamp}_{base_name}.{extension}"