from envyaml import EnvYAML

from src.consumers.table_consumer import TableConsumer
from src.consumers.trend_consumer import TrendConsumer
from multiprocessing import Process
import logging
from src.utils import set_up_logger
from src.config_reader import config


class DataCollector:
    """
    Main DataCollector class which consumes data from kafka and saves it to influx and oracle.
    """

    def __init__(self):
        self.consumers = []

    def create_consumers(self):
        """
        Creates consumers that consume data from kafka. There are two types of consumers: trend consumers and table consumers.
        The trend consumers consume trend data (current, voltage etc.). They save the data in time series repository
        (e.g., Influx). Table consumers on the other hand, consume data that should be saved in relational repository
        (e.g., Oracle) like Metadata or SkidManagementTool (SMT) entries.
        Returns
        -------

        """
        topics = config["kafka"]["topics"]
        for t in topics:
            consumer = None
            if t.endswith("Trends"):
                consumer = TrendConsumer(t)
            else:
                consumer = TableConsumer(t)
            self.consumers.append(consumer)

    def run_consumers(self):
        """
        Runs consumers as many processes at once.

        Returns
        -------

        """
        processes = []
        for consumer in self.consumers:
            proc = Process(target=consumer.consume)
            processes.append(proc)

        for proc in processes:
            proc.start()


if __name__ == '__main__':
    # Set up logger
    set_up_logger()
    logging.info("Container started.")

    # Start data collection
    dc = DataCollector()
    dc.create_consumers()
    dc.run_consumers()
