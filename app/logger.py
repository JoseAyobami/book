# import os
# import logging


# logging.basicConfig(
#     format="%(filename)s - %(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
# )
# if os.environ.get("ENV") == "production":
#     logging.getLogger().setLevel(logging.INFO)
# else:
#     logging.getLogger().setLevel(logging.DEBUG)


# def get_logger(filename: str) -> logging.Logger:
#     return logging.getLogger(filename)


import os
import logging

def setup_logging():
    log_level = logging.INFO
 
    if os.environ.get("ENV") == "production":
        log_level = logging.INFO
    
    else: 
        log_level = logging.DEBUG

    # Clear existing handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        level=log_level,
        format="%(filename)s - %(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )

def get_logger(name: str):
    return logging.getLogger(name)

# Initialize logging configuration
setup_logging()




