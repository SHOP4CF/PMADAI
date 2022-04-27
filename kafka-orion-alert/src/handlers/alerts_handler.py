import requests
import logging
import cx_Oracle
from src.domain.alert_types import BasicAlert
from src.consumers.alert_consumer import AlertConsumer
from src.db.relational_repository import RelationalRepository
from src.config_reader import config
from typing import List
from datetime import datetime
import simplejson as json


class Alert:
    """
    This is a data structure class. Contains information required for construction alert in orion-alert style.
    Information is extracted from raw alerts retrieved from the kafka topic.

    Attributes
    ----------
    id : str
        Unique id number taken from oracle sequence. Initially equal to None and setting up after querying the sequence.
    orion_id_template : str
        Template of unique id in orion alert. Supplemented with the id value.
    type : str
        Value represents the type of alert.
    category : str
        Value represents the category of alert.
    sub_category : str
        Value represents the subcategory of alert.
    description : str
        Value represents the detailed description of the anomaly.
    human_verified : str
         Value indicating whether it has been verified by a human.
    date_issued : str
        Value that indicates the date when the anomaly occurred. Date format: %Y-%m-%d %H:%M:%S
    date_modified : str
        Value that specifies the modification date of the anomaly information. Initially equal to the date the event occurred. Date format: %Y-%m-%d %H:%M:%S
    alert_source : str
        Value represents the exact source of alert. In this case it is an unique car body id which cause the problem.
    source : str
        Value represents the global source of alert.
    valid_from : str
        A value that indicates the date from which the instance is valid. Initially equal to the date the event occurred. Date format: %Y-%m-%d %H:%M:%S
    see_also : str
        An encoded url referring to where the anomaly can be seen.
    severity : str
        A value that indicates the severity of the alert.
    """

    def __init__(self, raw_alert: BasicAlert):
        """
        Parameters
        ----------
        raw_alert
            raw alert which was inserted into kafka topic in case of anomaly detection by other modules.
        """
        self.id = None
        self.orion_id_template = 'urn:ngsi-ld:Alert:Volkswagen:pred-maint-{}'
        self.type = 'Alert'
        self.category = "predictiveMaintenance"
        self.sub_category = raw_alert.name
        self.description = str(raw_alert.description)
        self.human_verified = str(raw_alert.human_verified)
        self.date_issued = self.convert_to_valid_date(raw_alert.date_issued)
        self.date_modified = self.convert_to_valid_date(raw_alert.date_modified)
        self.alert_source = "urn:ngsi-ld:Asset:Volkswagen:skid-{}".format(str(raw_alert.metadata['carBodyId']))
        self.source = 'PMADAI'
        self.valid_from = self.convert_to_valid_date(raw_alert.date_issued)
        self.see_also = raw_alert.url
        self.severity = 'high'

    @property
    def orion_body(self):
        """
        str : an alert body containing all the data written in the manner adopted by orion.
        """
        assert self.id, 'ID is not set.'
        return {
            "id": self.orion_id_template.format(self.id),
            "type": self.type,
            "category": {
                "type": "Property",
                "value": self.category
            },
            "subCategory": {
                "type": "Property",
                "value": self.sub_category
            },
            "description": {
                "type": "Property",
                "value": self.description
            },
            "humanVerified": {
                "type": "Property",
                "value": self.human_verified
            },
            "dateIssued": {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.date_issued
                }
            },
            "dateModified": {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.date_modified
                }
            },
            "alertSource": {
                "type": "Relationship",
                "object": self.alert_source
            },
            "source": {
                "type": "Property",
                "value": self.source
            },
            "validFrom": {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value":  self.valid_from
                }
            },
            "seeAlso": {
                "type": "Property",
                "value": [
                    self.see_also
                ]
            },
            "severity": {
                "type": "Property",
                "value": self.severity
            },
            "@context": [
                "https://smartdatamodels.org/context.jsonld",
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
            ]
        }

    @property
    def datetime_format(self):
        return '%Y-%m-%dT%H:%M:%S.%fZ'

    def convert_to_valid_date(self, date: str) -> str:
        """
        This method converts the obtained date to a form acceptable by orion.
        """
        return datetime.fromisoformat(date).strftime(self.datetime_format)

    def __str__(self):
        return str({
            "id": self.id,
            "orion_id_template": self.orion_id_template,
            "type": self.type,
            "category": self.category,
            "sub_category": self.sub_category,
            "description": self.description,
            "human_verified": self.human_verified,
            "date_issued": self.date_issued,
            "date_modified": self.date_modified,
            "alert_source": self.alert_source,
            "source": self.source,
            "valid_from": self.valid_from,
            "see_also": self.see_also,
            "severity": self.severity
        })


class AlertsHandler:
    """
    This class is responsible for managing alerts. It reads alerts from the kafka topic and
    sends them to the orion server after saving the alert to the database.
    """

    def __init__(self, *, alert_consumer: AlertConsumer, database: RelationalRepository, alert_types: List):
        """
        Parameters
        ----------
        alert_consumer
            Object responsible for reading data from a kafka topic.
        database
            Object responsible for reading the unique id from the sequence and writing data to the oracle database.
        alert_types
            List with all supported alert types.
        """
        self.alert_consumer = alert_consumer
        self.database = database
        self.alert_types = alert_types

    def start_processing_alerts(self):
        """
        This method is responsible for processing alerts which occur in kafka topic.
        Here the alert body is constructed. A unique id is retrieved and a database entry is called.
        At the end of processing, the alert with the unified id is sent to the orion server.
        """
        raw_alert: BasicAlert
        for raw_alert in self.alert_consumer.consume():
            logging.info("Received Alert notification")
            logging.debug(f"Alert notification: {raw_alert}")
            if raw_alert.name in self.alert_types:
                orion_alert = Alert(raw_alert)
                unique_id = self.database.get_unique_id()
                orion_alert.id = unique_id
                try:
                    self.database.insert_alert(orion_alert)
                except cx_Oracle.DatabaseError as err:
                    logging.error(f"Could not store Alert in database: {err}")
                self.send_alert_to_orion(orion_alert)
            else:
                logging.info(f"Other possibility occur - unhandled. Data: {raw_alert}")

    def send_alert_to_orion(self, orion_alert: Alert):
        """
        This method sends the alert with unique id to orion server. The alert is sent in the form required by the server.
        """
        logging.info("Sending entity")
        logging.debug(f"Sending entity body: {orion_alert.orion_body}")
        response = requests.post(f"{config['general']['orion-server']}/ngsi-ld/v1/entities",
                                 data=json.dumps(orion_alert.orion_body),
                                 headers={'Content-type': 'application/ld+json'})
        logging.debug(response)
