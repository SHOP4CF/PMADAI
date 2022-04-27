import logging
from time import sleep
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Mapping, Optional

from src.domain.metadata import Metadata
from src.filters.metadata_filter import MetadataFilter
from src.domain.preprocessing_result import PreprocessingResult, PreprocessingPayload, RawData
from src.preprocessors.preprocessor import Preprocessor
from src.db.influxdb_repository import InfluxDbRepository
from src.producers.alert_producer import AlertProducer
from src.producers.preprocessing_result_producer import PreprocessingResultProducer
from src.domain.preprocessing_result import PreprocessingResult, PreprocessingStatus
from src.config_reader import config as module_config


class SingleRowMetadataProcessorConfig:
    def __init__(self, metadata_filters: List, apply_metadata_time_shift: bool,
                 winter_times: List):
        self.metadata_filters = metadata_filters
        self.apply_metadata_time_shift = apply_metadata_time_shift
        self.winter_times = winter_times
        self.metadata_filters_statuses = [m_filter.status for m_filter in metadata_filters]


class SingleRowMetadataProcessor:
    def __init__(self, config: SingleRowMetadataProcessorConfig, preprocessor: Preprocessor,
                 ts_repo: InfluxDbRepository):
        self.config = config
        self.preprocessor = preprocessor
        self.ts_repo = ts_repo
        self.pr_producer: Optional[PreprocessingResultProducer] = None
        self.alert_producer: Optional[AlertProducer] = None

    def produce_processed_metadata_row(self, metadata: Metadata):
        # Required for using kafka in multiprocessing
        self.create_producers()
        self.add_winter_time_shift_if_required(metadata)
        self.wait_till_data_save_in_influxd()

        # Apply filters based on type of painting (e.g. cage)
        filtering_results = [filter.apply(metadata) for filter in self.config.metadata_filters]

        if self.any_filter_is_fired(filtering_results):
            first_fired_filter = self.get_first_fired_up_filter(filtering_results)
            pr_result = self.construct_raw_preprocessing_result(metadata, first_fired_filter.status)
            logging.info(f"Sending filtered PR result: {pr_result.to_dict()}")

        else:  # If none of the pre-filters fired up -> run preprocessing
            trends_dict = self.get_trends_based_on_received_metadata(metadata)
            # Prepare batch
            logging.info("Preparing batch")
            pr_result = self.preprocessor.preprocess(metadata, trends_dict)
            # Check preprocessing quality with some post-processing filters?
            # Skip for now
            logging.info(f"Sending preprocessing result.")
            logging.debug(f"PreprocessingResult: {pr_result.to_dict()}")

        self.pr_producer.produce(pr_result)
        self.produce_alert_if_required(pr_result)
        # Required for using kafka in multiprocessing
        self.close_producers()

    def create_producers(self):
        self.pr_producer = PreprocessingResultProducer()
        self.alert_producer = AlertProducer()

    def add_winter_time_shift_if_required(self, metadata: Metadata):
        """
        Value 6985 is needed for good waveform mapping.
        It is equal 2 hours (2*60*60) - winter/summer time mapping (3600 seconds are responsible for controlling this time)
        minus
        4*60 = 240 seconds - time after which (from the moment of entry) the painting process begins
        plus
        25 seconds - experimentally selected value.

        This mapping is it is caused most probably by unsynchronized times of the measuring machines.
        """
        if self.config.apply_metadata_time_shift:
            metadata.time_of_event = pd.to_datetime(metadata.time_of_event)
            if any([start < metadata.time_of_event < end for start, end in self.config.winter_times]):
                metadata.time_of_event = (metadata.time_of_event - np.timedelta64(6985 - 3600, 's')).strftime(
                    "%Y-%m-%d %H:%M:%S.%f")
            else:
                metadata.time_of_event = (metadata.time_of_event - np.timedelta64(6985, 's')).strftime(
                    "%Y-%m-%d %H:%M:%S.%f")

    def wait_till_data_save_in_influxd(self):
        logging.info("Received metadata, starting to sleep.")
        sleep(module_config["general"]["sleep-time"])

    def get_first_fired_up_filter(self, filtering_results: List) -> MetadataFilter:
        return self.config.metadata_filters[np.argwhere(filtering_results)[0]]

    @staticmethod
    def any_filter_is_fired(filtering_results: List) -> bool:
        return any(filtering_results)

    @staticmethod
    def construct_raw_preprocessing_result(metadata: Metadata, status: PreprocessingStatus) -> PreprocessingResult:
        raw_data = RawData()
        return PreprocessingResult(preprocessing_status=status,
                                   payload=PreprocessingPayload(metadata),
                                   raw_data=raw_data)

    def get_trends_based_on_received_metadata(self, metadata: Metadata) -> Mapping[str, Mapping[str, pd.DataFrame]]:
        logging.info("Querying influx.")
        time_from = datetime.strptime(metadata.time_of_event, "%Y-%m-%d %H:%M:%S.%f")
        time_to = datetime.strptime(metadata.time_of_event, "%Y-%m-%d %H:%M:%S.%f") + timedelta(minutes=10)
        return self.ts_repo.get_trends_values(time_from, time_to)

    def produce_alert_if_required(self, pr_result: PreprocessingResult):
        if pr_result.status in self.alert_producer.alerts_trigger_list:
            self.alert_producer.produce(pr_result)

    def close_producers(self):
        self.pr_producer.close()
        self.alert_producer.close()
