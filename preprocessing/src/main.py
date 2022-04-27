import logging
import pandas as pd

from src.consumers.metadata_consumer import MetadataConsumer
from src.db.influxdb_repository import InfluxDbRepository
from src.filters.cage_filter import CageFilter
from src.preprocessors.preprocessor import Preprocessor
from src.preprocessors.time_based_preprocessor import TimeBasedPreprocessor
from src.utils import set_up_logger
from src.single_row_metadata_processor import SingleRowMetadataProcessorConfig, SingleRowMetadataProcessor
from src.config_reader import config
from multiprocessing import Process

APPLY_METADATA_TIME_SHIFT = True
winter_times = [(pd.to_datetime("2020-10-25 02:00"), pd.to_datetime("2021-03-28 02:00"))]


def manage_processing_metadata_rows():
    """
    This function starts the process processing metadata (one process for each new car body in the paint bath).
    This is because there can be more than one car body in the paint bath at the same time.
    They have to be considered separately and it takes some time to drive through the bathtub.
    """
    for metadata in metadata_consumer.consume():
        if metadata.in_out == "IN":  # Preconditions
            Process(target=metadata_row_processor.produce_processed_metadata_row, args=(metadata,)).start()


if __name__ == '__main__':

    # Set up logger
    set_up_logger()
    logging.info("Container started.")

    # Initialize time series repo
    ts_repo = InfluxDbRepository()

    # Init preprocessor
    preprocessor: Preprocessor = TimeBasedPreprocessor()

    # Connect to topic
    metadata_consumer = MetadataConsumer(topic_name=config["kafka"]["metadata-topic"])

    # Define Metadata filters
    metadata_filters = [
        CageFilter()
    ]

    # Define metadata row processor
    m_processor_cfg = SingleRowMetadataProcessorConfig(metadata_filters=metadata_filters,
                                                       apply_metadata_time_shift=APPLY_METADATA_TIME_SHIFT,
                                                       winter_times=winter_times)

    metadata_row_processor = SingleRowMetadataProcessor(config=m_processor_cfg,
                                                        preprocessor=preprocessor,
                                                        ts_repo=ts_repo)

    manage_processing_metadata_rows()
