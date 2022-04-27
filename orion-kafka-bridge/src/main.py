from flask import Flask, request, Response
from src.utils import set_up_logger
from src.config_reader import config
import logging
from kafka import KafkaProducer
from json import dumps
from datetime import datetime
from src.subscriptions_setter import SubscriptionsSetter
from src.device_controlled_properties_states import electric_current_state

app = Flask(__name__)

controlled_property_to_topic_name = {
    'electricCurrent': 'CurrentTrends'
}

TRENDS_TYPE = "Device"
METADATA_TYPE = "Task"
SMT_TYPE = "SMT"


@app.route('/notify', methods=['POST'])
def produce_received_data():
    logging.debug(f"Request: {request}")
    logging.debug(f"JSON: {request.json}")
    for entity in request.json['data']:
        if entity['type'] == TRENDS_TYPE:
            produce_trend_row(entity)
        elif entity['type'] == METADATA_TYPE:
            produce_metadata_row(entity)
        elif entity['type'] == SMT_TYPE:
            produce_smt_row(entity)
        else:
            logging.info(f"Unknown type of entity received: {entity['type']}")
    return Response(status=200)


def produce_trend_row(entity):
    timestamp = datetime.strptime(entity["value"]["observedAt"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime(
        '%Y-%m-%d %H:%M:%S.%f')
    busbar_number = entity["source"]["object"][entity["source"]["object"].rfind(":") + 1:][-1]
    trend_name = f"current_on_busbar_{busbar_number}"

    controlled_property = entity["controlledProperty"]["value"]
    for index, c_property in enumerate(controlled_property):

        if property_is_not_handled(c_property):
            continue

        topic_name = controlled_property_to_topic_name[c_property]
        value = entity["value"]["value"][index]

        if electric_current_state.is_updated(value=value):
            producer.send(topic=topic_name, value={
                "timestamp": timestamp,
                trend_name: value
            })


def property_is_not_handled(c_property: str) -> bool:
    return c_property not in controlled_property_to_topic_name.keys()


def produce_metadata_row(entity):
    def int_like(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    start_idx: int = entity["isDefinedBy"]["object"].rfind(":") + 1
    skid_len: int = len('skid-')
    if entity["isDefinedBy"]["object"][start_idx:start_idx + skid_len] == "skid-":
        producer.send(topic="Metadata", value={
            "timeOfEvent": datetime.strptime(entity['status']["observedAt"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime(
                '%Y-%m-%d %H:%M:%S.%f'),
            "inOut": "IN" if entity["status"]['value'] == "inProgress" else "OUT",
            "carBodyId": entity['workParameters']['value']["carBodyId"],
            "carBodyType": entity['workParameters']['value']["carBodyType"],
            "voltageProgramType": entity['workParameters']['value']["voltageProgramType"],
            "skidId": entity['workParameters']['value']["skidId"],
            "pendulumId": int(entity['workParameters']['value']["pendulumId"]) if int_like(
                entity['workParameters']['value']["pendulumId"]) else -1
        })


def produce_smt_row(entity):
    producer.send(topic="SMT", value={
        "timestamp": entity["timestamp"]["value"],
        "skidId": entity["skidId"]["value"],
        "typeOfSmtEvent": entity["typeOfSmtEvent"]["value"],
    })


def init_app():
    """
    Initialization of component needed in this module.
    This function is needed to run the application in the development and production environment.
    Gunicorn will directly reference this function, while the development environment will run this function from main.
    """
    global producer
    set_up_logger()
    producer = KafkaProducer(bootstrap_servers=config["kafka"]["bootstrap_servers"],
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
    # async
    SubscriptionsSetter().set_up_subscriptions()
    return app


if __name__ == "__main__":
    app = init_app()
    app.run(debug=True, host='0.0.0.0', port=config['flask']['port'])
