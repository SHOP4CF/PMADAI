from joblib import load
import os
import numpy as np
from src.models.basic_model import Model
from src.models.model_config import ModelConfig

from src.domain.prediction_data import SingleBusPredictionData


class Isolationforest(Model):
    """
    This class manage single model for selected bus. This class support IsolationForest model implemented with
    'scikit-learn' library.

    Attributes
    ---------
    config : ModelConfig
        Configuration of particular model.
    model
        model which is queried and based on its result, a decision is made about an anomaly on the selected bus
    """

    def __init__(self, config: ModelConfig):
        super(Isolationforest, self).__init__(config)

    def load_model(self):
        """
        This method loads model to the memory.

        Returns
        -------
            returns loaded model.
        """
        model_path = os.path.join(self.config.models_dir, self.config.model_file_name)
        return load(model_path)

    def anomaly_score(self, data: SingleBusPredictionData) -> float:
        """
        This method compute the anomaly score. Proper shape of the data is checked and prediction data are scaled.
        The model is queried and next, response is computed to be in anomaly score form.

        Parameters
        ---------
        data
            SingleBusPredictionData container containing prediction data and
            additional information in case of general model usage.

        Returns
        -------
        Float
            Float: the result that is the calculated model response which is understood as anomaly score.
        """
        scaled_prediction_data = self.scale_input_data(data.painting_process_data)
        extended_data = self.extend_dimension(scaled_prediction_data)

        if self.body_voltage_pair_encoder is None:
            prediction_result = -self.model.score_samples(extended_data)[0]
        else:
            body_program_code = self.body_voltage_pair_encoder.transform(data.encoding_pair)
            concatenated_input_data = np.concatenate((extended_data, body_program_code), axis=1)
            prediction_result = -self.model.score_samples(concatenated_input_data)[0]
        return prediction_result
