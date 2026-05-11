import logging
import os

LOG_DIR = "logs"
LOG_FILE = "app.log"

def get_logger(name:str):

    # Create logs directory if missing
    os.makedirs(LOG_DIR, exist_ok=True)
    
    # Create Logger
    logger = logging.getLogger(name)

    # Set minimum logging level
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
     # Log format
    formatter = logging.Formatter(
         "%(asctime)s | %(levelname)s | %(message)s"
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    #File handler

    file_handler = logging.FileHandler(
        "logs/app.log",
        mode = "a"
    )

    file_handler.setFormatter(formatter)

    # Attach handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger