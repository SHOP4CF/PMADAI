from src.consumers.basic_consumer import BasicConsumer
import logging

from src.db.influxdb_repository import InfluxDbRepository


class TrendConsumer(BasicConsumer):
    def __init__(self, topic_name):
        super().__init__(topic_name)
        self.ts_repository = InfluxDbRepository()

    def consume(self):
        i = 0 # going from 0 to 1000
        for message in self.consumer:
            i = (i + 1) % 10**3
            if i % 300 == 0:
                logging.info(f"{self.topic_name}: writing {message.value}")
            logging.debug(f"{self.topic_name}: writing {message.value}")

            try:
                trend_name = [k for k in message.value.keys() if k != "timestamp"][0]

                self.ts_repository.save_measurement(measurement=self.topic_name,
                                                    trend_name=trend_name,
                                                    timestamp=message.value["timestamp"],
                                                    value=message.value[trend_name])
            except TypeError as te:
                logging.error(f"{self.topic_name} consumer: could not save measurement. Message: {message}. Error: {te}")
