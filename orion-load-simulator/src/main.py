from multiprocessing import Process

from src.producers.metadata_producer import MetadataProducer
from src.producers.trend_producer import TrendProducer
from src.config_reader import config
import logging


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
    elif config["general"]["logging-level"] == 'WARNING':
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.INFO)


if __name__ == '__main__':
    # Set up logger
    set_up_logger()
    logging.info("Container started.")

    procs = []
    for i in range(1, 5):
        logging.info(f"Creating trend producer number: {i}")
        tp = TrendProducer(trend_id=f"current_on_busbar_{i}",
                           trend_name=f"L1VGL1.C811KS_1HS_K{i}.AA.R2323_AVCuB")

        procs.append(Process(target=tp.produce))

    mp = MetadataProducer()
    procs.append(Process(target=mp.produce))

    for proc in procs:
        proc.start()
