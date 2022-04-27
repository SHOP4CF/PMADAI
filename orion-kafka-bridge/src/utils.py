import logging
from src.config_reader import config


def set_up_logger():
    logger = logging.getLogger()

    # Get handlers
    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler('logfile.log')

    # Log formatting
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    # Set logging level
    if config["general"]["logging-level"] == 'DEBUG':
        logger.setLevel(logging.DEBUG)
        logging.getLogger('werkzeug').setLevel(logging.DEBUG)
    elif config["general"]["logging-level"] == 'WARNING':
        logger.setLevel(logging.WARNING)
        logging.getLogger('werkzeug').setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.INFO)
        logging.getLogger('werkzeug').setLevel(logging.INFO)