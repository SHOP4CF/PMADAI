import logging

import requests
import simplejson as json
from src.consumers.preprocessing_result_consumer import PreprocessingResultConsumer
from src.utils import set_up_logger
from src.config_reader import config
from src.domain.painting_prediction import PaintingPrediction
from src.producers.anomaly_alert_producer import alert_producer

JWT = None


def get_prediction():
    """
    This function is responsible for passing correctly processed data (CORRECT status) to the prediction module,
    and the obtained prediction results are returned.
    """
    prediction_response = None
    if pr_result_json.value['status'] == 'CORRECT':
        logging.info("Sending preprocessing result to Prediction Api")
        prediction_response = requests.post(f"{config['general']['prediction-api-url']}/predict",
                                            data=json.dumps(pr_result_json.value),
                                            headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
        logging.debug(f"Prediction API response text: {prediction_response.text}")
        logging.debug(f"Prediction API response json: {prediction_response.json()}")

    return prediction_response


def construct_painting_prediction():
    """
    This function is responsible for the preparation of complete data in order to transfer them to the backend module,
    where they are then saved to the database and any anomalies are handled.
    In addition to basic information, the data is extended with information that can only be changed by human-expert
    interference on the frontend side - here they are treated as fixed constants.
    """
    painting_prediction = dict()
    prediction_result = prediction_response.json() if prediction_response else {}
    painting_prediction['predictionResult'] = prediction_result
    painting_prediction['preprocessingResult'] = pr_result_json.value
    painting_prediction['humanResult'] = {}
    painting_prediction['problematicPainting'] = prediction_result['anomaly'] if prediction_response else True
    painting_prediction['humanVerified'] = False
    time_of_event = pr_result_json.value['payload']['metadata']['timeOfEvent']
    painting_prediction['dateModified'] = time_of_event
    return painting_prediction


def raise_alert_if_problematic_painting():
    """
    This method is checking the necessity of raising an alert and if true, alarm about painting incorrectness is sending.
    """
    pp = PaintingPrediction.from_painting_prediction(painting_prediction)
    # processing status is necessary for no-duplicate alerts inserting.
    # (Other status has been reported in preprocessing module.)
    if pp.preprocessing_status == 'CORRECT' and pp.problematic_painting:
        alert_producer.produce(pp)


if __name__ == '__main__':
    # Set up logger
    set_up_logger()
    logging.info("Container started.")

    # Connect to topic
    pr_consumer = PreprocessingResultConsumer(topic_name=config['kafka']['preprocessing-results-topic'])

    for pr_result_json in pr_consumer.consume():
        logging.info("Received Preprocessing Result")
        logging.debug(f"Preprocessing result: {pr_result_json}")

        # POST preprocessing result to prediction module and get the score (if preprocessing status isCORRECT)
        prediction_response = get_prediction()

        painting_prediction = construct_painting_prediction()
        raise_alert_if_problematic_painting()
