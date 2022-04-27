from typing import Dict
from src.models.models_handlers.basic_models_handler import BasicModelsHandler
from src.detection_results import DetectionResult


class SingleTypeModelsHandler(BasicModelsHandler):
    """
    This class is used when only one model type (e.g. autoencoder) is used.
    Thanks to this, calling individual instances of models and creating a detection result is greatly simplified.

    Attributes
    ----------
    model_class_name
        String: Name of handled model (e.g. 'Autoencoder')
    models
        GeneralModelsDict: Dictionary containing all required models for decision making.
    """

    def __init__(self):
        super().__init__()
        self.model_class_name: str = self.setup_config.model_types[0]

    def __call__(self, data: Dict) -> DetectionResult:
        """
        This method compute result. Here the model is selected based on constructed key and together with data is
        passing to parent class where the response is constructed. Finally the result is aggregated and stored in
        'DetectionResult' class.

        Parameters
        ----------
        data
            Dictionary containing data waveforms.

        Returns
        -------
        detection_result
            Result of detection stored in 'DetectionResult' class.
        """
        specified_models_type = self.get_specified_models_for_received_data(data=data, model_type=self.model_class_name)
        prediction_data = self.construct_prediction_data_for_models(data=data, models=specified_models_type)
        buses_result = self.compute_results(data=prediction_data, models=specified_models_type)
        detection_result = DetectionResult.single_model_result(buses_result)
        return detection_result
