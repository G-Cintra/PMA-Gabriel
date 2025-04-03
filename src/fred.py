import requests
import json
import logging
import hashlib

def save_fred(name, url, filename, filetype):
    """
    Fetch data from a FRED-like API and save as JSON or XML.
    
    Args:
        name (str): Descriptive name for logging.
        url (str): Full API endpoint URL.
        filename (str): Output file name (without extension).
        filetype (str): File type to save, either 'json' or 'xml'.
    """
    logger = logging.getLogger()

    try:
        logger.info(f"Requesting data for: {name}")
        logger.debug(f"URL: {url}")

        # Request data
        response = requests.get(url)
        response.raise_for_status()

        # Handle JSON
        if filetype.lower() == 'json':
            data = response.json()
            json_filename = f"{filename}.json"
            with open(json_filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"JSON file saved: {json_filename}")

            with open(json_filename, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            logger.debug(f"SHA-256 hash of saved JSON file: {file_hash}")

        # Handle XML
        elif filetype.lower() == 'xml':
            xml_filename = f"{filename}.xml"
            with open(xml_filename, "wb") as f:
                f.write(response.content)
            logger.info(f"XML file saved: {xml_filename}")

            with open(xml_filename, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            logger.debug(f"SHA-256 hash of saved XML file: {file_hash}")

        else:
            logger.error(f"Unsupported filetype '{filetype}'. Must be 'json' or 'xml'.")

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error for {name}: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for {name}: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error for {name}: {e}")