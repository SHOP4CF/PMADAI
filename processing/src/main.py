import logging

import requests
import simplejson as json
from src.consumers.preprocessing_result_consumer import PreprocessingResultConsumer
from src.utils import set_up_logger
from src.config_reader import config

JWT = None


def post_to_backend():
    """
    This function is responsible for posting data to the backend module, including the login token.
    If such a token does not exist or has expired, it is re-logged in using the login data appropriate for this module.
    """
    global JWT
    backend_response = requests.post(f"{config['general']['backend-api-url']}/api/painting-predictions",
                                     data=json.dumps(painting_prediction),
                                     headers={'Content-type': 'application/json',
                                              'Accept': 'text/plain',
                                              'Authorization': f'Bearer {JWT}'})
    logging.debug(backend_response.text)
    if backend_response.status_code == 401 or not JWT:  # Authenticate and re-post
        logging.debug(f"Authenticating")

        auth_response = requests.post(f"{config['general']['backend-api-url']}/auth/login",
                                      data={'username': config['general']['backend_auth']['username'],
                                            'password': config['general']['backend_auth']['password']},
                                      headers={'Content-type': 'application/x-www-form-urlencoded',
                                               'Accept': 'text/plain'})

        logging.debug(f"{auth_response.text}")

        JWT = auth_response.json()["accessToken"]

        backend_response = requests.post(f"{config['general']['backend-api-url']}/api/painting-predictions",
                                         data=json.dumps(painting_prediction),
                                         headers={'Content-type': 'application/json',
                                                  'Accept': 'text/plain',
                                                  'Authorization': f'Bearer {JWT}'})
    return backend_response


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

        # BACKEND. Lines below should be uncommented if backend module is available.
        # logging.info(f"Posting to backend module.")
        # logging.debug(f"Posting message: {painting_prediction}")

        # backend_response = post_to_backend()

        # logging.debug(f"Backend response: {backend_response.json()}")
