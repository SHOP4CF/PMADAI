from src.domain.preprocessing_result import PreprocessingResult
from src.producers.basic_producer import BasicProducer
from src.config_reader import config


class PreprocessingResultProducer(BasicProducer):
    def __init__(self):
        super().__init__(config["kafka"]["preprocessing-results-topic"])

    def produce(self, preprocessing_result: PreprocessingResult):
        self.producer.send(self.topic_name, preprocessing_result.to_dict())