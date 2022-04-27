from time import sleep

import requests
import pandas as pd
import logging
import numpy as np
import simplejson as json
import random

from src.config_reader import config


class MetadataProducer:
    def __init__(self):
        self.metadata_df = pd.read_excel("Metadata.xlsx", sheet_name="Arkusz1", engine="openpyxl")
        self.metadata_df['Punkt czasu'] = pd.to_datetime(self.metadata_df['Punkt czasu'])
        self.metadata_df = self.metadata_df.sort_values('Punkt czasu')
        self.timedelta = 0
        self.entity_id = "urn:ngsi-ld:Task:company-xyz:metadata:"


    def produce(self):
        # Sleep one minute after reading all the data (wait till trends are read)
        sleep(config['general']['metadata-start-sleep-time'])

        for row in self.metadata_df.iloc[1:].iterrows():
            sleep(config['general']['metadata-sleep-time'])
            logging.debug(f"Generating metadata: {(row[1]['Punkt czasu'] - np.timedelta64(self.timedelta, 's')).strftime('%Y-%m-%d %H:%M:%S.%f')}")

            entity_creation_body = {
                "id": self.entity_id + str(random.randint(1, 100000000)),
                "type": "Task",
                "isDefinedBy": {"type": "Relationship",
                                "object": "urn:ngsi-ld:TaskDefinition:company-xyz:skid-in-the-pool"},
                "workParameters": {"type": "Property",
                                   "value": {"carBodyId": str(row[1]["Numer Karoserii"]),
                                             "carBodyType": row[1]["Typ podstawowy"],
                                             "voltageProgramType":  str(row[1]["Rodzaj programu napiecia KTL"]),
                                             "skidId": int(row[1]["ID Skida"]),
                                             "pendulumId":  int(row[1]["Numer wahadla"]) if self.int_like(row[1]["Numer wahadla"]) else -1
                                             }
                                   },
                "status": {"type": "Property",
                           "value": "inProgress" if row[1]["IN/OUT"] == "IN" else "completed",
                           "observedAt": (row[1]["Punkt czasu"] - np.timedelta64(self.timedelta, 's')).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                           },
                "@context": ["https://smartdatamodels.org/context.jsonld",
                             "https://raw.githubusercontent.com/shop4cf/data-models/master/docs/shop4cfcontext.jsonld"]
            }

            logging.debug(entity_creation_body)
            response = requests.post(f"{config['general']['orion-server']}/ngsi-ld/v1/entities",
                                     data=json.dumps(entity_creation_body),
                                     headers={'Content-type': 'application/ld+json'})

    def int_like(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False