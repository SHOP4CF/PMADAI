import sys
import pytest

config = None

module = type(sys)('test_config_reader')
module.config = config

sys.modules['src.config_reader'] = module


@pytest.fixture(autouse=True)
def setup_config_weights():
    def setup_config(a_w, i_w):
        module.config = {
            'models': {
                'aggregation_weights': {
                    'autoencoder': a_w,
                    'isolationforest': i_w
                }
            }
        }
        sys.modules['src.config_reader'] = module
    return setup_config


@pytest.fixture(autouse=True)
def setup_config_model_type():
    def setup_config(model):
        module.config = {
            'models': {
                'model-type': model,
                'scaling-std_multiplication': {
                    'autoencoder': 1,
                    'isolationforest': None
                },
                'aggregation_weights': {
                    'autoencoder': 0.5,
                    'isolationforest': 0.5
                }
            }
        }
        sys.modules['src.config_reader'] = module
    return setup_config
