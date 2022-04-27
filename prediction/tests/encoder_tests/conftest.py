import os

import pytest

from src.models.encoders.encoder import Encoder
from src.models.encoders.encoder_config import EncoderConfig


def get_encoder_config(model_name):
    encoder_dir = os.path.join('models_data', model_name, 'general', 'body_voltage_pair_encoder')
    encoder_file_name = 'general_encoder'
    return EncoderConfig(encoder_dir=encoder_dir, encoder_file_name=encoder_file_name)


@pytest.fixture
def encoder_ae():
    return Encoder(get_encoder_config('autoencoder'))


@pytest.fixture
def encoder_if():
    return Encoder(get_encoder_config('isolationforest'))
