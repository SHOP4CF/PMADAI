from src.consumers.basic_consumer import BasicConsumer
from src.domain.alert_types import IncorrectPaintingProcess, IncorrectPaintingData, UnhandledAlert
from src.domain.preprocessing_status import PreprocessingStatus
import logging


class AlertConsumer(BasicConsumer):
    def __init__(self, topic_name):
        super().__init__(topic_name)

    @property
    def alerts_trigger_list(self):
        return [PreprocessingStatus.GAP_IN_READINGS.value, PreprocessingStatus.BAD_EXTRACTION.value, PreprocessingStatus.CAGE.value]

    def consume(self):
        for message in self.consumer:
            logging.debug(f"{self.topic_name}: received {message.value}")
            try:
                if message.value['source'] == 'ANOMALY' or message.value['source'] == 'HUMAN_REPORTED':
                    data = IncorrectPaintingProcess(alert_data=message.value)
                elif message.value['source'] in self.alerts_trigger_list:
                    data = IncorrectPaintingData(alert_data=message.value)
                else:
                    data = UnhandledAlert()
                yield data
            except TypeError as te:
                logging.error(f"Could not construct object from message: {message}. Error: {te}")
