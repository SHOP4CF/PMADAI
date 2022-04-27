import simplejson as json
from time import sleep
import requests
from multiprocessing import Process
import logging
from src.config_reader import config


class SubscriptionsSetter:
    def __init__(self):
        self.watched_entities_to_params = {
            "urn:ngsi-ld:Task:Volkswagen:metadata": {"entity_type": "Task",
                                                      "attribs": ["workParameters", "status", "isDefinedBy"]},
            f"urn:ngsi-ld:Device:Volkswagen:trends": {"entity_type": "Device",
                                                       "attribs": ["value", "controlledProperty", "source"]}
        }

    def set_up_subscriptions(self):
        for entity_id, params in self.watched_entities_to_params.items():
            Process(target=SingleSubscriptionSetter(entity_id, params).set_subscription).start()


class SingleSubscriptionSetter:
    def __init__(self, entity_id, params):
        self.entity_id = entity_id
        self.params = params

    def set_subscription(self):
        while True:
            # Sleep one sec
            sleep(1)
            if self.entity_exists():
                if not self.subscription_exists():
                    logging.info(f"Creating subscription for {self.entity_id}")
                    self.create_subscription(**self.params)
                break

    def subscription_exists(self):
        response = requests.get(f"{config['general']['orion-server']}/ngsi-ld/v1/subscriptions/{self.entity_id}",
                                headers={'Accept': 'application/ld+json'})
        return response.status_code == 200

    def entity_exists(self):
        response = requests.get(
            f"{config['general']['orion-server']}/ngsi-ld/v1/entities/?type={self.params['entity_type']}",
            headers={'Accept': 'application/ld+json'})
        return response.status_code == 200

    def create_subscription(self, entity_type, attribs):
        logging.debug("Creating subscription")
        subscription_body = {
            "id": f"{self.entity_id}",
            "description": f"A subscription to get info about entity: {entity_type}",
            "type": "Subscription",
            "entities": [{"type": entity_type}],
            "watchedAttributes": attribs,
            "notification": {
                "attributes": attribs,
                "format": "normalized",
                "endpoint": {
                    "uri": config['general']['orion-kafka-bridge'],
                    "accept": "application/ld+json"
                }
            },
            "expires": "2040-01-01T14:00:00.00Z",
            "throttling": 0,
            "@context": ["https://smartdatamodels.org/context.jsonld",
                         "https://raw.githubusercontent.com/shop4cf/data-models/master/docs/shop4cfcontext.jsonld",
                         {
                             "source": {
                                 "@id": "https://smart-data-models.github.io/data-models/terms.jsonld#/definitions/source",
                                 "@type": "ngsi-ld:Relationship"
                             }
                         },
                         {
                             "isDefinedBy": {
                                 "@id": "https://smart-data-models.github.io/data-models/terms.jsonld#/definitions/isDefinedBy",
                                 "@type": "ngsi-ld:Relationship"
                             }
                         }
                         ]
        }
        response = requests.post(f"{config['general']['orion-server']}/ngsi-ld/v1/subscriptions",
                                 data=json.dumps(subscription_body),
                                 headers={'Content-type': 'application/ld+json'})
