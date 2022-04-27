from typing import Mapping, List
from influxdb_client import InfluxDBClient
from src.db.influxdb_schema import schema
from collections import defaultdict
import logging
import pandas as pd

from src.config_reader import config
from src.db.ts_repository import TimeSeriesRepository


class InfluxDbRepository(TimeSeriesRepository):
    def __init__(self):
        self.influx_client = InfluxDBClient(url=config["influx"]["url"], token=config["influx"]["token"], org=config["influx"]["org"])
        self.query_api = self.influx_client.query_api()

    def get_trends_values(self, time_from, time_to) -> Mapping[str, Mapping[str, pd.DataFrame]]:
        result = {}
        for measurement, trend_names in schema.items():
            sub_res = {}
            for trend_name in trend_names:
                query = 'from(bucket: "'+config["influx"]["bucket"]+'")' \
                        '|> range(start: '+time_from.strftime("%Y-%m-%dT%H:%M:%SZ")+', stop: '+time_to.strftime("%Y-%m-%dT%H:%M:%SZ")+')' \
                        '|> filter(fn: (r) => r["_measurement"] == "'+measurement+'")' \
                        '|> filter(fn: (r) => r["trend_name"] == "'+trend_name+'")' \
                        '|> filter(fn: (r) => r["_field"] == "value")'

                logging.debug(f"Query: {query}")
                influx_result_tables = self.query_api.query(org=config["influx"]["org"], query=query)

                df = self.tables_to_df(influx_result_tables)
                sub_res[trend_name] = df
            result[measurement] = sub_res

        return result

    @staticmethod
    def tables_to_df(result) -> pd.DataFrame:
        """
        Converts InfluxDB tables result to pandas Dataframe.
        Parameters
        ----------
        result
            A dictionary of dictionaries (measurement -> dictionary).
            Each child dictionary contains values of specific trend names of a given measurement.

            Example: {
                "PositionTrends" {
                    "position_of_car_body_on_busbar_1": pd.Dataframe (with position readings),
                    ...
                    },
                ...
                }

        Returns
        -------
        pd.Dataframe
            Pandas Dataframe with the readings
        """
        res = {
            "dt": [],
            "value": []
        }
        for table in result:
            for record in table.records:
                res["dt"].append(record.get_time())
                res["value"].append(record.get_value())
        result_df = pd.DataFrame.from_dict(res)
        if 'dt' in result_df:  # Some rows WERE extracted from Influx
            return result_df.set_index('dt').sort_index()
        else:  # No rows extracted from Influx -> return empty Dataframe.
            return result_df

