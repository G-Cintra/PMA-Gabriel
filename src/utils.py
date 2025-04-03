import hashlib

def compute_file_hash(filepath):
    """Returns the SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_api_key(file_path='../secrets/fred_api_key.txt'):
    """
    Load the API key from a file, or ask the user to input and save it.
    
    Args:
        file_path (str): Path to the file storing the API key.
        
    Returns:
        str: The API key.
    """
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return f.read().strip()
    else:
        api_key = input("Enter your API key: ").strip()
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(api_key)
        print(f"API key saved to {file_path}. Make sure it's in .gitignore!")
        return api_key


import os
import re

def delete_old_raw_versions(raw_data_dir="../data/raw/"):
    """
    Deletes older versions of CSV and JSON files in the raw data folder,
    keeping only the latest version per (source, table, variable, extension).
    
    Parameters:
        raw_data_dir (str): Path to the raw data directory.
    
    Returns:
        List[str]: List of deleted file names.
    """
    filename_pattern = re.compile(
        r"(?P<source>IBGE|BCB)_(?P<session>\d{8}_\d{6})_T(?P<table>\d+)-V(?P<variable>\d+)_(?P<filetime>\d{6})\.(csv|json)"
    )

    files_by_key = {}

    for fname in os.listdir(raw_data_dir):
        match = filename_pattern.match(fname)
        if match:
            info = match.groupdict()
            key = (info["source"], info["table"], info["variable"])
            file_record = {
                "filename": fname,
                "full_path": os.path.join(raw_data_dir, fname),
                "session": info["session"],
                "filetime": info["filetime"],
                "ext": fname.split(".")[-1]
            }
            files_by_key.setdefault(key, []).append(file_record)

    deleted_files = []

    for key, versions in files_by_key.items():
        # Group by file extension (csv/json)
        grouped = {}
        for v in versions:
            ext = v["ext"]
            existing = grouped.get(ext)
            if existing is None or (v["session"], v["filetime"]) > (existing["session"], existing["filetime"]):
                grouped[ext] = v

        # Delete non-latest
        keep_set = {v["filename"] for v in grouped.values()}
        for v in versions:
            if v["filename"] not in keep_set:
                os.remove(v["full_path"])
                deleted_files.append(v["filename"])

    return deleted_files
