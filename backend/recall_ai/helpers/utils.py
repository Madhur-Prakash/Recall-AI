import logging
import requests
import os
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
