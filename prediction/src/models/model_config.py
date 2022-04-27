import numpy as np
from functools import cached_property


class ModelConfig:
    """
    This class contains information about model directory and name. Deals with data scaling, model result normalization etc.

    Attributes
    ----------
    bus : str
        Informs which bus is supported by the given model
    threshold : float
        Contains the threshold based on which the decision about the anomaly is made.
    model_file_name : str
        It is a name of model attendant a specific bus - same as one from 'models' directory.
    models_dir : str
        Includes a link to the model catalog.
    payload_field_name_for_prediction_making : str
        Name of payload field (preprocessing result on raw waveform) on the basis of which the prediction is made.
    encoder_file_name : str
        It is a name of encoder attendant a specific bus.
    encoder_dir : str
        Includes a link to the encoder catalog. If encoder is not needed, than 'None' value is set.
        If general model should be used, voltage program type and car body type are coded to provide additional information.
        Coder must be provided when a general purpose model is used and put into 'body_voltage_pair_transformer' directory.
    scaler_mean : float, default: 0.0
        Mean of training data. Filled if data should be scaled before feeding the model.
    scaler_var : float, default: 1.0
        Variation of training data. Filled if data should be scaled before feeding the model.
    result_mean : float, default: 0.0
        Mean of output result in training phase. Filled if model result should be normalized.
    result_var : float, default: 1.0
        Variation of output result in training phase. Filled if model result should be normalized.
    result_upper_bound : float, default: 1000.0
        If result has no upper-bound, this will be used to normalize the output.
    std_multiplication : float, default: 1.0
        Standard multiplication value. Used when the result needs to be normalized by dividing by a value that is a
        multiple of this variable
    normalized_threshold : float
        Normalized threshold calculated from the variables.
    """

    def __init__(self,
                 bus,
                 threshold,
                 model_file_name,
                 models_dir,
                 payload_field_name_for_prediction_making,
                 encoder_file_name=None,
                 encoder_dir=None,
                 scaler_mean=0.0,
                 scaler_var=1.0,
                 result_mean=0.0,
                 result_var=1.0,
                 result_upper_bound=1000.0,
                 std_multiplication=1.0):
        self.bus = bus
        self.threshold = threshold
        self.model_file_name = model_file_name
        self.models_dir = models_dir
        self.payload_field_name_for_prediction_making = payload_field_name_for_prediction_making
        self.encoder_file_name = encoder_file_name
        self.encoder_dir = encoder_dir
        self.scaler_mean = scaler_mean
        self.scaler_var = scaler_var
        self.result_mean = result_mean
        self.result_var = result_var
        self.result_upper_bound = result_upper_bound
        self.std_multiplication = std_multiplication

    @cached_property
    def normalized_threshold(self) -> float:
        """
        Normalized threshold calculated from the variables.
        """
        normalized_threshold = self.threshold
        if self.std_multiplication is not None:
            value = (self.threshold - self.result_mean) / (self.std_multiplication * np.sqrt(self.result_var))
            normalized_threshold = float(1 / (1 + np.power(np.e, -value)))
        return normalized_threshold
