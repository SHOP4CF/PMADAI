from time import sleep

import requests

from src.utils.trend_reader import TrendReader
from src.config_reader import config
import logging
import simplejson as json


class TrendProducer:
    def __init__(self, trend_id, trend_name):
        self.trend_id = trend_id
        self.trend_name = trend_name
        self.trend_values_df = TrendReader.read("../trends", trend_name)

        entity_creation_body = {
            "id": f"urn:ngsi-ld:Device:company-xyz:trends",
            "type": "Device",
            "source": {"type": "Relationship",
                       "object": f"urn:ngsi-ld:Device:company-xyz:busbar-{trend_id[-1]}"},
            "category": {"type": "Property",
                         "value": ["sensor"]},
            "controlledProperty": {"type": "Property",
                                   "value": ["electricCharge", "electricCurrent"]},
            "value": {"type": "Property",
                      "value": [self.trend_values_df.iloc[0]['value'],
                                self.trend_values_df.iloc[0]['value']],
                      "observedAt": self.trend_values_df.iloc[0]['dt'].strftime("%Y-%m-%dT%H:%M:%S.%fZ")},
            "@context": ["https://smartdatamodels.org/context.jsonld",
                         "https://raw.githubusercontent.com/shop4cf/data-models/master/docs/shop4cfcontext.jsonld"]
        }

        logging.debug("Creating trend entity")
        response = requests.post(f"{config['general']['orion-server']}/ngsi-ld/v1/entities",
                                 data=json.dumps(entity_creation_body),
                                 headers={'Content-type': 'application/ld+json'})

    def produce(self):
        for row in self.trend_values_df.iloc[1:].iterrows():
            sleep(config['general']['trends-sleep-time'])
            entity_update_body = {
                "source": {"type": "Relationship",
                           "object": f"urn:ngsi-ld:Device:company-xyz:busbar-{self.trend_id[-1]}"},
                "value": {"type": "Property",
                          "value": [row[1]['value'], row[1]['value']],
                          "observedAt": row[1]['dt'].strftime("%Y-%m-%dT%H:%M:%S.%fZ")},
                "@context": ["https://smartdatamodels.org/context.jsonld",
                             "https://raw.githubusercontent.com/shop4cf/data-models/master/docs/shop4cfcontext.jsonld"]
            }

            logging.debug(f"Updating trend entity: {self.trend_id}")
            response = requests.post(f"{config['general']['orion-server']}/ngsi-ld/v1/entities/urn:ngsi-ld:Device:company-xyz:trends/attrs",
                                     data=json.dumps(entity_update_body),
                                     headers={'Content-type': 'application/ld+json'})