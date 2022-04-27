from collections import defaultdict
from typing import Tuple
import os
from src.domain.specific_painting_type_dict import SpecificPaintingTypeKey
from src.utils import check_if_ensemble
from src.config_reader import config


class SetupConfig:
    """
    This class is responsible for providing the correct paths and variable values for all required data.

    Attributes
    ----------
    model_types
            List of models that the user wants to use.
    models_paths
        Dictionary containing paths for specific models, body types and currents.
    features_paths
        Dictionary containing paths for specific features, body types and currents.
    body_voltage_pair_encoder_paths
         Dictionary containing paths for encoder which transform voltage program type and car body type
         to provide additional information.
    std_multiplications
        Dictionary containing std_multiplication values for each model separately
    root_path
        main root of the data.
    general_models
        Name of subdirectory with the general-purpose model. Every model has its own general directory.
    """
    root_path = '../models_data/{}'
    general_models = 'general'

    def __init__(self):
        self.model_types = list()
        self.models_paths = defaultdict(str)
        self.features_paths = defaultdict(str)
        self.body_voltage_pair_encoder_paths = defaultdict(lambda: None)
        self.std_multiplications = defaultdict(float)
        self.initialize_paths()

    def initialize_paths(self) -> None:
        """
        This method load all paths and data to dictionary.
        """

        def update_models_info():
            self.model_types.append(model_type.capitalize())
            for painting_key, path in self.get_paths_from_directory_structure(model_type):
                if painting_key.source == 'models':
                    self.models_paths[painting_key] = path
                elif painting_key.source == 'features':
                    self.features_paths[painting_key] = path
                elif painting_key.source == 'body_voltage_pair_encoder':
                    self.body_voltage_pair_encoder_paths[painting_key] = path

        if check_if_ensemble(config):
            config_model_type = config["models"]["model-type"].split(',')
            for model_type in config_model_type:
                std = config["models"]["scaling-std_multiplication"][model_type.lower()]
                std_key = model_type.strip().capitalize()
                self.std_multiplications[std_key] = std
                update_models_info()
        else:
            model_type = config["models"]["model-type"]
            self.std_multiplications[model_type.capitalize()] = config["models"]["scaling-std_multiplication"][
                model_type.lower()]
            update_models_info()

    @staticmethod
    def get_paths_from_directory_structure(model_type: str) -> Tuple[SpecificPaintingTypeKey, str]:
        """
        This method yield dictionary key and value. Key is constructed using 'SpecificPaintingTypeKeys' class.
        All information is extracted thanks to the analysis of the structure of the root directory containing the necessary data

        Parameters
        ----------
        model_type
            type of the model.

        Yields
        -------
        Tuple
            Tuple: Key represented as 'SpecificPaintingTypeKeys' class, data path.
        """
        root_path = SetupConfig.root_path.format(model_type.lower())
        for path, directories, _ in os.walk(root_path):
            if not directories:
                split_path = path.split(os.path.sep)
                voltage_program_type = split_path[-2]
                car_body_type = split_path[-2] if voltage_program_type == 'general' else split_path[-3]
                painting_key = SpecificPaintingTypeKey(
                    model_type=model_type,
                    car_body_type=car_body_type,
                    voltage_program_type=voltage_program_type,
                    source=split_path[-1]
                )
                yield painting_key, path
