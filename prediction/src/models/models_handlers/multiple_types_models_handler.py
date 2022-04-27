from typing import Dict
from src.models.models_handlers.basic_models_handler import BasicModelsHandler
from src.detection_results import DetectionResult


class MultipleTypesModelsHandler(BasicModelsHandler):
    """
        This class is used when more than one model is used and the results aggregation is needed.
        Thanks to this, calling every individual instances of every model types and creating a detected result is greatly simplified.

        Attributes
        ----------
        models
            GeneralModelsDict: Dictionary containing all required models for decision making.
        """

    def __init__(self):
        super().__init__()

    def __call__(self, data: Dict) -> DetectionResult:
        """
        This method compute result. Here for every selected model types the model instance is picked based on constructed key
        and together with data is passing to parent class where the response is constructed.
        Finally the result is aggregated and stored in 'DetectionResult' class.

        Parameters
        ----------
        data
            Dictionary containing data waveforms.

        Returns
        -------
        detection_result
            Result of detection stored in 'DetectionResult' class.
        """
        results = dict()
        for model_type in self.setup_config.model_types:
            specified_models_type = self.get_specified_models_for_received_data(data=data, model_type=model_type)
            prediction_data = self.construct_prediction_data_for_models(data=data, models=specified_models_type)
            results[model_type] = self.compute_results(data=prediction_data, models=specified_models_type)
        detection_result = DetectionResult.multiple_models_result(results)
        return detection_result
