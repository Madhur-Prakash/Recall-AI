from datetime import timedelta
import logging
import os
import time
from concurrent_log_handler import ConcurrentRotatingFileHandler

def setup_logging():
    logger = logging.getLogger("recallAi")
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)

        file_handler = ConcurrentRotatingFileHandler(
            os.path.join(log_dir, "recallAi.log"),
            maxBytes=10000,
            backupCount=500
        )
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s - %(filename)s - %(lineno)d",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger


def get_file_creation_age(file_path):
    if not os.path.exists(file_path):
        return None
    creation_time = os.path.getctime(file_path)  # Get creation time in seconds since epoch
    current_time = time.time() # Get current time in seconds since epoch
    age_seconds = current_time - creation_time # Calculate age in seconds
    return timedelta(seconds=age_seconds)

