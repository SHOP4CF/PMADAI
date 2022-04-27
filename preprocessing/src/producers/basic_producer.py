import abc
from json import dumps
from src.config_reader import config

from kafka import KafkaProducer


class BasicProducer:
    def __init__(self, topic_name):
        self.producer = KafkaProducer(bootstrap_servers=config["kafka"]["bootstrap_servers"],
                                      value_serializer=lambda x:
                                      dumps(x).encode('utf-8'))
        self.topic_name = topic_name

    def close(self):
        self.producer.close()

    @abc.abstractmethod
    def produce(self, message):
        pass
