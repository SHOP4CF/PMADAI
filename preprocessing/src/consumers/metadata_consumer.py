from src.consumers.basic_consumer import BasicConsumer
import logging

from src.domain.metadata import Metadata


class MetadataConsumer(BasicConsumer):
    def __init__(self, topic_name):
        super().__init__(topic_name)

    def consume(self):
        for message in self.consumer:
            logging.info(f"{self.topic_name}: received {message.value}")
            try:
                metadata = Metadata(metadata_json_dict=message.value)
                yield metadata
            except TypeError as te:
                logging.error(f"Could not construct Metadata object from message: {message}. Error: {te}")