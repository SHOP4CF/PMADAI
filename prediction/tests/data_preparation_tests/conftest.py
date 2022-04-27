import pytest
import os
import json

from src.domain.prediction_data import NestedPredictionData


@pytest.fixture
def cg33_2000_correct_data():
    path = os.path.join('tests', 'test_data', 'CG33_2000_correct_all_buses')
    with open(path, 'r') as j:
        data = json.loads(j.read())
    return data['payload']['interpolationFeatures']


@pytest.fixture
def nested_data(cg33_2000_correct_data):
    return NestedPredictionData(painting_process_data=cg33_2000_correct_data,
                                car_body_type='CG33',
                                voltage_program_type='2000')
