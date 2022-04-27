from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from src.config_reader import config
from src.db.ts_repository import TimeSeriesRepository
import logging


class InfluxDbRepository(TimeSeriesRepository):
    def __init__(self):
        self.influx_client = InfluxDBClient(url=config["influx"]["url"], token=config["influx"]["token"], org=config["influx"]["org"])
        self.write_api = self.influx_client.write_api(write_options=SYNCHRONOUS)

    def save_measurement(self, measurement, trend_name, timestamp, value):
        measurements = [
            {
                "measurement": measurement,
                "tags": {
                    "trend_name": trend_name
                },
                "time": timestamp,
                "fields": {
                    "value": float(value)
                }
            }
        ]
        logging.debug(f"Saving trends:  {measurements}")
        self.write_api.write(config["influx"]["bucket"], config["influx"]["org"], measurements)