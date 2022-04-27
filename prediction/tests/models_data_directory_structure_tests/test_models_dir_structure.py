import pytest
import os


@pytest.mark.directory_structure
def test_directory_structure(list_of_existing_paths, valid_data_paths):
    number_of_general_models = 0
    for path in list_of_existing_paths:
        splitted_path = path.split(os.path.sep)
        if len(splitted_path) == 4:
            path = path.replace(splitted_path[1], 'car_body_type')
            path = path.replace(splitted_path[2], 'voltage_program_type')
        assert path in valid_data_paths
        if splitted_path[1] == 'general' and splitted_path[-1] == 'models':
            number_of_general_models += 1

    # two models (autoencoder, isolationforest) and each of model has 3 catalogs (features, encoders and models)
    assert number_of_general_models == 2
