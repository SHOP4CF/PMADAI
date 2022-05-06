import logging

from src.producers.basic_producer import BasicProducer
from src.domain.painting_prediction import PaintingPrediction
from src.config_reader import config
from typing import Dict


class AnomalyAlertProducer(BasicProducer):
    def __init__(self):
        super().__init__(config["kafka"]["alerts-topic"])

    def produce(self, pp: PaintingPrediction):
        prepared_alert = self.extract_relevant_information(pp)
        self.producer.send(self.topic_name, prepared_alert)
        logging.info(prepared_alert)

    def extract_relevant_information(self, pp: PaintingPrediction) -> Dict:
        metadata = {
            'timeOfEvent': pp.time_of_event,
            'inOut': pp.in_out,
            'carBodyId': pp.car_body_id,
            'carBodyType': pp.car_body_type,
            'voltageProgramType': pp.voltage_program_type,
            'skidId': pp.skid_id,
            'pendulumId': pp.pendulum_id
        }

        return self.construct_kafka_data_to_produce(pp, metadata)

    @staticmethod
    def construct_kafka_data_to_produce(pp: PaintingPrediction, metadata: Dict) -> Dict:
        return {
                "source": 'ANOMALY',
                'metadata': metadata,
                'prediction_result': pp.prediction_result,
                'human_result': pp.human_result,
                'date_issued': str(pp.date_modified),
                'date_modified': str(pp.date_modified),
                'human_verified': pp.human_verified
            }


alert_producer = AnomalyAlertProducer()