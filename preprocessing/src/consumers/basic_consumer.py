from kafka import KafkaConsumer
import json
import abc
import logging

from src.config_reader import config


class BasicConsumer:
    def __init__(self, topic_name):
        self.consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=config["kafka"]["bootstrap_servers"],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='group2',
            value_deserializer=self.json_deserializer)
        self.topic_name = topic_name

    @staticmethod
    def json_deserializer(m):
        try:
            return json.loads(m.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            logging.error(f"Wrong format passed to consumer: {m}. Expecting JSON format.")
            return m

    @abc.abstractmethod
    def consume(self):
        pass
