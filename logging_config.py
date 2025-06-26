# logging_config.py
import logging
import sys
import os

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)

        # Enhanced formatter with more detail for debugging user issues
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.propagate = False  # Avoid duplicate logs if root logger also logs
    return logger

def setup_file_logger(name: str, log_file: str = "logs/article_extractor.log") -> logging.Logger:
    """
    Set up a file logger for persistent logging to file.
    This is useful for tracking user issues over time.
    """
    logger = logging.getLogger(f"{name}_file")
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        # Ensure logs directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        # Enhanced formatter with more detail for file logs
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.propagate = False
    return logger