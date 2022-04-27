import logging

from flask import Flask, request

from src.models.models_handlers.single_type_models_handler import SingleTypeModelsHandler
from src.models.models_handlers.multiple_types_models_handler import MultipleTypesModelsHandler
from src.utils import set_up_logger, check_if_ensemble
from src.config_reader import config

app = Flask(__name__)

# Models
models = None


@app.route('/predict', methods=['POST'])
def predict():
    global json_id
    global models
    # May be useful: https://stackoverflow.com/questions/53548127/post-numpy-array-with-json-to-flask-app-with-requests
    data = request.json
    logging.info("In /predict endpoint")
    logging.debug(f"Data: {data}")

    # querying the model on the metadata payload
    results = models(data['payload'])
    logging.debug(f"Results: {results.to_dict()}")

    return results.to_dict(), 200


def init_app():
    """
    Initialization of component needed in this module.
    This function is needed to run the application in the development and production environment.
    Gunicorn will directly reference this function, while the development environment will run this function from main.
    """
    global models
    # Set up logger
    set_up_logger()
    logging.info("Container started.")
    # Setup models handler
    try:
        if check_if_ensemble(config):
            models = MultipleTypesModelsHandler()
        else:
            models = SingleTypeModelsHandler()
    except FileNotFoundError as err:
        logging.exception(err)
        exit()

    return app


if __name__ == "__main__":
    app = init_app()
    app.run(debug=True, host='0.0.0.0', port=config['flask']['port'])
