from src.utils import set_up_logger
from src.consumers.alert_consumer import AlertConsumer
from src.handlers.alerts_handler import AlertsHandler
from src.db.oracle_repository import OracleRepository
import logging

from src.config_reader import config

alert_types = ['incorrectPaintingProcessInKTL', 'incorrectPaintingData']

if __name__ == "__main__":
    # Set up logger
    set_up_logger()
    logging.info("Container started.")

    # Connect to topic
    alert_consumer = AlertConsumer(topic_name=config['kafka']['alerts-topic'])

    # Database
    database = OracleRepository()
    database.create_schema()

    # Create alerts handler
    alerts_handler = AlertsHandler(alert_consumer=alert_consumer,
                                   database=database,
                                   alert_types=alert_types)

    alerts_handler.start_processing_alerts()
