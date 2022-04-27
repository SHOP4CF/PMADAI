from typing import Dict, Mapping
import joblib
import os
from src.detection_results import BusDetectionResult
from src.models.models_handlers.setup_config import SetupConfig
from src.domain.specific_painting_type_dict import SpecificPaintingTypeKey, GeneralModelsDict
from src.models.model_config import ModelConfig
import src.models.models_instances as models_instances
from src.domain.prediction_data import NestedPredictionData


class BasicModelsHandler:
    """
    This class is responsible for managing all basic models (for example auotoencoder).
    It enables easy use and obtaining results from all models.

    Attributes
    ---------
    buses
        List of all buses under analysis
    setup_config
        information about config
    """

    def __init__(self):
        self.buses = ['K1', 'K2', 'K3', 'K4']
        self.setup_config = SetupConfig()
        self.models: GeneralModelsDict = self.initialize_models()

    def initialize_models(self) -> GeneralModelsDict:
        """
        This method is required for models initialization. Model for each specific bus is initialize
        with specific configuration and store in dictionary.

        Returns
        -------
        models
        Dictionary containing all loaded and configured models. Keys are stored as 'SpecificPaintingTypeKeys'.
        """
        models = GeneralModelsDict(general_type=SetupConfig.general_models)
        for painting_type, path in self.setup_config.models_paths.items():
            models[painting_type] = dict()
            for features_dict, bus in self.get_bus_specific_model_building_features(painting_type):
                model_config = ModelConfig(**features_dict)
                model_instance = getattr(models_instances, painting_type.model_type)(model_config)
                models[painting_type][bus] = model_instance
        return models

    def get_bus_specific_model_building_features(self, painting_type: SpecificPaintingTypeKey):
        """
        This method yield an extended features dictionary required for proper model configuration.
        This method extends information about the bus, std_multiplication and the exact path to the model.
        All this information are needed to read a specific model and its correct configuration.

        Parameters
        ----------
        painting_type
            Keys to dictionary with information to extend configuration, stored as 'SpecificPaintingTypeKeys'.

        Yields
        -------
        features_dict
            Dictionary containing model configuration.
        bus
            String: information about bus name
        """
        features_paths = self.setup_config.features_paths
        features_dict = self.read_specific_painting_type_features(features_paths[painting_type])
        for bus in self.buses:
            models_dir = self.setup_config.models_paths[painting_type]
            encoder_dir = self.setup_config.body_voltage_pair_encoder_paths[painting_type]
            std_multiplication = self.setup_config.std_multiplications[painting_type.model_type]
            features_dict[bus]['bus'] = bus
            features_dict[bus]['std_multiplication'] = std_multiplication
            features_dict[bus]['models_dir'] = models_dir
            features_dict[bus]['encoder_dir'] = encoder_dir
            yield features_dict[bus], bus

    @staticmethod
    def read_specific_painting_type_features(features_path: str) -> Dict:
        """
        This method is loading features stored in file which the received path leads to.

        Parameters
        ----------
        features_path
            String: path that goes to the data file.

        Returns
        -------
            Dictionary containing features.
        """
        features_full_path = os.path.join(features_path, 'models_features')
        return joblib.load(features_full_path)

    def get_specified_models_for_received_data(self, data: Dict, model_type: str) -> Dict:
        """
        This method load model based on data information.

        Parameters
        ----------
        data : Dict
            Dictionary containing data waveforms.
        model_type : str
            Model name used.
        Returns
        -------
        loaded model for prediction making
        """
        metadata = data['metadata']
        model_key = SpecificPaintingTypeKey(model_type=model_type,
                                            car_body_type=metadata['carBodyType'],
                                            voltage_program_type=metadata['voltageProgramType'])
        return self.models[model_key]

    def construct_prediction_data_for_models(self, data: Dict, models: Dict) -> NestedPredictionData:
        """
        This method construct container containing data.

        Parameters
        ----------
        data : Dict
            Dictionary containing data waveforms.
        models
            List of specified models for each bus (only one type of model).

        Returns
        -------
        PredictionData containing data for model prediction.
        """
        data_working_name = models[self.buses[0]].config.payload_field_name_for_prediction_making
        metadata = data['metadata']
        return NestedPredictionData(painting_process_data=data[data_working_name],
                                    car_body_type=metadata['carBodyType'],
                                    voltage_program_type=metadata['voltageProgramType'])

    def compute_results(self, data: NestedPredictionData, models: dict) -> Mapping[str, BusDetectionResult]:
        """
        This method computes results for each bus. Every bus has its own model to obtain the result.
        Result is stored  in the 'BusDetectionResult' class
        which store all information needed to represent the detection result.

        Parameters
        ----------
        data
            PredictionData container with data containing all information about waveforms and used model.
            Based on selected information the result is computed.
        models
            Dictionary of models for every buses. Only one model type.

        Returns
        -------
        buses_detection
            Dictionary of 'BusDetectionResult' for each bus.
        """
        buses_detection = dict()
        data_iterator = iter(data)
        for bus, single_bus_data in zip(self.buses, data_iterator):
            not_normalized_score, normalized_score = models[bus](single_bus_data)
            normalized_threshold = models[bus].config.normalized_threshold
            threshold = models[bus].config.threshold
            key = f'{bus.lower()}_result'
            buses_detection[key] = BusDetectionResult(
                not_normalized_score=not_normalized_score,
                normalized_score=normalized_score,
                threshold=threshold,
                normalized_threshold=normalized_threshold)
        return buses_detection
