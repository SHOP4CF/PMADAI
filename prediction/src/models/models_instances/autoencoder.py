from tensorflow.keras.models import load_model

import os
import numpy as np

from src.models.basic_model import Model
from src.models.model_config import ModelConfig

from src.domain.prediction_data import SingleBusPredictionData


class Autoencoder(Model):
    """
    This class manage single model for selected bus. This class support Autoencoder model implemented with
    'tensorflow' package.

    Attributes
    ---------
    config : ModelConfig
        Configuration of particular model.
    model
        model which is queried and based on its result, a decision is made about an anomaly on the selected bus
    """

    def __init__(self, config: ModelConfig):
        super(Autoencoder, self).__init__(config)

    def load_model(self):
        """
        This method loads model to the memory.

        Returns
        -------
            returns loaded model.
        """
        model_path = os.path.join(self.config.models_dir, self.config.model_file_name)
        return load_model(model_path)

    @staticmethod
    def reconstruction_score(true_value: np.ndarray, predicted_value: np.ndarray) -> float:
        """
        This method computes the autoencoder reconstruction score. The function used is Mean squared error.

        Parameters
        ----------
        true_value
            real value of data
        predicted_value
            predicted/reconstructed value

        Returns
        -------
        Float
            Float: Mean squared error between true and predicted values.
        """
        result_diff = true_value - predicted_value
        score = (np.power(result_diff, 2)).mean(axis=1)
        return float(np.squeeze(score))

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
            prediction_result = self.model(extended_data)
        else:
            body_program_code = self.body_voltage_pair_encoder.transform(data.encoding_pair)
            prediction_result = self.model((extended_data, body_program_code))
        return self.reconstruction_score(extended_data, prediction_result)
