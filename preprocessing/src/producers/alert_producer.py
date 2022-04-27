from src.domain.preprocessing_result import PreprocessingResult, PreprocessingStatus
from src.producers.basic_producer import BasicProducer
from src.config_reader import config
from typing import Dict
from datetime import datetime
from typing import Mapping


class AlertProducer(BasicProducer):
    def __init__(self):
        super().__init__(config["kafka"]["alerts-topic"])

    @property
    def alerts_trigger_list(self):
        return [PreprocessingStatus.GAP_IN_READINGS, PreprocessingStatus.BAD_EXTRACTION, PreprocessingStatus.CAGE]

    @staticmethod
    def extract_relevant_information(preprocessing_result: PreprocessingResult) -> Mapping:
        return {
            "source": preprocessing_result.status.value,
            'metadata': preprocessing_result.payload.metadata.to_dict(),
            'date_issued': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        }

    def produce(self, preprocessing_result: PreprocessingResult):
        prepared_alert = self.extract_relevant_information(preprocessing_result)
        self.producer.send(self.topic_name, prepared_alert)