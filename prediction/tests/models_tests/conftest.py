import pytest
import os
from importlib import reload

from src.models.models_handlers import multiple_types_models_handler, single_type_models_handler
from src.models.models_handlers import setup_config
from src.detection_results import detection_result


class ModelConfig:
    def __init__(self,
                 scaler_var=0.0,
                 scaler_mean=1.0,
                 result_var=0.0,
                 result_mean=1.0,
                 std_multiplication=1,
                 result_upper_bound=10):
        self.scaler_var = scaler_var
        self.scaler_mean = scaler_mean
        self.result_var = result_var
        self.result_mean = result_mean
        self.std_multiplication = std_multiplication
        self.result_upper_bound = result_upper_bound


@pytest.fixture
def model_configuration(request):
    try:
        config = ModelConfig(**request.param)
    except:
        config = ModelConfig()
    return config


@pytest.fixture(params=['Autoencoder', 'Isolationforest'])
def single_models_handler(request, setup_config_model_type):
    setup_config_model_type(request.param)

    reload(single_type_models_handler)
    reload(setup_config)

    setup_config.SetupConfig.root_path = os.path.join(os.getcwd(), 'models_data', '{}')
    return single_type_models_handler.SingleTypeModelsHandler()


@pytest.fixture(params=['Autoencoder,Isolationforest'])
def multiple_models_handler(request, setup_config_model_type):
    setup_config_model_type(request.param)

    reload(detection_result)
    reload(multiple_types_models_handler)
    reload(setup_config)

    setup_config.SetupConfig.root_path = os.path.join(os.getcwd(), 'models_data', '{}')
    return multiple_types_models_handler.MultipleTypesModelsHandler()
