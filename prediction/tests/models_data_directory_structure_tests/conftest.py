import pytest
import os


@pytest.fixture
def base_path():
    return 'models_data'


@pytest.fixture
def list_of_existing_paths(base_path):
    list_of_paths = list()
    for path, dirs, files in os.walk(base_path):
        if not dirs:
            splitted_path = path.split(os.path.sep)[1:]  # take only subdir of base dir
            list_of_paths.append(f'{os.path.sep}'.join(splitted_path))
    return list_of_paths


@pytest.fixture
def valid_data_paths():
    """
    create all paths with pattern:
    - {autoencoder, isolationforest}/car_body_type/voltage_program_type/{models, features}
    and
    - {autoencoder, isolationforest}/general/{models, features, body_voltage_pair_encoder}
    """
    valid_data_paths = list()
    for model in ['autoencoder', 'isolationforest']:
        for name in ['models', 'features', 'body_voltage_pair_encoder']:
            if name != 'body_voltage_pair_encoder':
                path = os.path.join(model, 'car_body_type', 'voltage_program_type', name)
                valid_data_paths.append(path)
            path = os.path.join(model, 'general', name)
            valid_data_paths.append(path)
    return valid_data_paths