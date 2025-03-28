import logging
import os

def start_logger(logger_name: str, log_file_path: str) -> logging.Logger:
    """
    Starts or resets a logger with the specified name and log file path.

    Parameters:
        logger_name (str): Name of the logger.
        log_file_path (str): Path to the log file.

    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Remove any existing handlers
    if logger.hasHandlers():
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

    # Clear the log file
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    with open(log_file_path, "w", encoding="utf-8") as f:
        f.write("")

    # Formatter used by both handlers
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Create and add file handler
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Stream handler (outputs to notebook)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    logger.info("Logger started.")
    return logger


def shutdown_logger(logger: logging.Logger):
    """
    Shuts down the logger and closes all its handlers.

    Parameters:
        logger (logging.Logger): The logger to shut down.
    """
    logger.info("Logger shutting down.")
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)
