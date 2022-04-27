import abc

from typing import Tuple
from src.models.model_config import ModelConfig
import numpy as np
from src.domain.prediction_data import SingleBusPredictionData
from src.models.encoders.encoder import Encoder
from src.models.encoders.encoder_config import EncoderConfig


class Model:
    """
    This class manage single model for selected bus. This class implements data-input scaling, model querying, result
    normalizing and anomaly checking. The subclass should implement 'load_model' and 'anomaly_score' methods.


    Attributes
    ---------
    config : ModelConfig
        Configuration of particular model.
    model
        model which is queried and based on its result, a decision is made about an anomaly on the selected bus
    body_voltage_pair_encoder
        If general model should be used, voltage program type and car body type are coded to provide additional information.
    """

    def __init__(self, config: ModelConfig):
        """
        Parameters
        ----------
        config : ModelConfig
            Configuration of particular model.
        """
        self.config = config
        self.model = self.load_model()
        self.body_voltage_pair_encoder = self.load_encoder_if_required()

    @abc.abstractmethod
    def load_model(self):
        """
        This method loads model to the memory.

        Returns
        -------
            returns loaded model.
        """
        pass

    def load_encoder_if_required(self):
        """
        This method loads encoder to the memory. if no encoder is required, 'none' is returned.

        Returns
        -------
            returns loaded encoder.
        """
        encoder = None
        if self.config.encoder_dir is not None and self.config.encoder_file_name is not None:
            encoder_config = EncoderConfig(
                encoder_dir=self.config.encoder_dir,
                encoder_file_name=self.config.encoder_file_name)
            encoder = Encoder(encoder_config)
        return encoder

    @abc.abstractmethod
    def anomaly_score(self, data: SingleBusPredictionData) -> float:
        """
        This method compute the anomaly score. Result depends on model type and its response.

        Parameters
        ---------
        data
            array with model response.

        Returns
        -------
        Float
            Float: the result that is the calculated model response which is understood as anomaly score.
        """
        pass

    def normalize_output_score(self, score_value: float) -> float:
        """
        This method is used to normalize the model response. If std_multiplication (value in config) has not been set,
        the result is returned unchanged.

        Parameters
        ---------
        score_value
            score which represent the model response.

        Returns
        -------
        Float
            Float which is the normalized response of the model.
        """
        if self.config.std_multiplication is None:
            return score_value
        result_value = min(score_value, self.config.result_upper_bound)
        result_value = ((result_value - self.config.result_mean) / (
                self.config.std_multiplication * np.sqrt(self.config.result_var)))
        result_value = 1 / (1 + np.power(np.e, -result_value))
        return float(result_value)

    @staticmethod
    def is_valid(data: np.ndarray) -> bool:
        """
        This method check if received data is valid. If data contain NaN values or infinity,
        the data are considered incorrect.

        Parameters
        ----------
        data
            data to check

        Returns
        -------
        Bool
            Bool: boolean value represents data correctness.
        """
        if None in data or np.isnan(data).any() or np.isinf(data).any():
            return False
        return True

    def __call__(self, data: SingleBusPredictionData) -> Tuple[float, float]:
        """
        Here the data flow is performed. Firstly, correctness of data is checking. If true, model is
        queried and the result is normalized.

        Parameters
        ----------
        data
            Input data on the basis of which the prediction is made.

        Returns
        -------
        Tuple
            Tuple: score and normalized score
        """
        if self.is_valid(data.painting_process_data):
            score = self.anomaly_score(data)
            normalized_score = self.normalize_output_score(score)
            return score, normalized_score
        else:
            return 1.0, 1.0

    def scale_input_data(self, data: np.ndarray) -> np.ndarray:
        """
        This function scale the input data. If it is not necessary, config default values allow
        the data to be left unchanged.

        Parameters
        ----------
        data
            Input data on the basis of which the prediction is made.
        """
        std = np.sqrt(self.config.scaler_var)
        return (data - self.config.scaler_mean) / std

    @staticmethod
    def extend_dimension(data: np.ndarray) -> np.ndarray:
        """
        This method extend the data (if necessary) dimension for model purpose.

        Parameters
        ----------
        data
            the model input data.

        Returns
        -------
        data with an increased number of dimensions (if an extension was necessary).
        """
        if len(data.shape) == 1:
            data = data[np.newaxis, ...]
        return data
