import pytest
from src.domain.specific_painting_type_dict import SpecificPaintingTypeKey, GeneralModelsDict


@pytest.fixture
def key_1():
    model_type = 'auoteoncoder'
    car_body_type = 'CG33'
    voltage_program_type = '2000'
    source = 'models'
    return SpecificPaintingTypeKey(
        model_type=model_type,
        car_body_type=car_body_type,
        voltage_program_type=voltage_program_type,
        source=source
    )


@pytest.fixture
def key_2():
    model_type = 'isolationforest'
    car_body_type = 'CG44'
    voltage_program_type = '4000'
    source = 'features'
    return SpecificPaintingTypeKey(
        model_type=model_type,
        car_body_type=car_body_type,
        voltage_program_type=voltage_program_type,
        source=source
    )


@pytest.fixture
def not_existing_key():
    model_type = 'general_model'
    car_body_type = 'not_existing_car_body_type'
    voltage_program_type = 'not_existing_voltage_program_type'
    source = 'not_existing_source'
    return SpecificPaintingTypeKey(
        model_type=model_type,
        car_body_type=car_body_type,
        voltage_program_type=voltage_program_type,
        source=source
    )


@pytest.fixture
def general_key():
    model_type = 'general_model'
    car_body_type = 'general_model'
    voltage_program_type = 'general_model'
    source = 'general_source'
    return SpecificPaintingTypeKey(
        model_type=model_type,
        car_body_type=car_body_type,
        voltage_program_type=voltage_program_type,
        source=source
    )


@pytest.fixture
def general_dict(key_1, key_2, general_key):
    general_dict = GeneralModelsDict(general_type='general_model')
    general_dict[key_1] = 'key_1'
    general_dict[key_2] = 'key_2'
    general_dict[general_key] = 'general_model'
    return general_dict