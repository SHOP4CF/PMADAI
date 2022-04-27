from src.models.encoders.encoder_config import EncoderConfig
from joblib import load
import numpy as np
import logging
import os


class Encoder:
    """
    Class responsible for encoding the categorical data (car body type, voltage program type) into a representation
    acceptable by the model. While the received item to be encoded has not previously been seen in the fitting phase -
    an out of bucket (OOB) item is used (In this case, the most frequent item in the data for the general purpose model).

    Attributes
    ---------
    encoder_config
        Configuration of an encoder.
    encoder
        encoder to encode the value
    """

    OOB = 'CG322000'

    def __init__(self, encoder_config: EncoderConfig):
        self.encoder_config = encoder_config
        self.encoder = self.load_encoder()

    def load_encoder(self):
        """
        This method will load the encoder based on the appropriate paths.
        """
        encoder_path = os.path.join(self.encoder_config.encoder_dir,
                                    self.encoder_config.encoder_file_name)
        return load(encoder_path)

    def transform(self, data: str) -> np.ndarray:
        """
        This method encodes the received data.
        If the data to be encoded is not in the encoder dictionary, the string stored in the OOB class variable is used.
        data:
            data to encode - in string. This is concatenation of car_body_type, voltage_program_type.
        """
        if self.is_valid_pair(data):
            transformed_data = self.encoder.transform([data])
        else:
            logging.info(f'Data contains previously unseen pair: {data}')
            transformed_data = self.encoder.transform([Encoder.OOB])
        return transformed_data

    def is_valid_pair(self, pair: str) -> bool:
        """
        This method checks if the received data to be encoded is in the encoder dictionary.
        pair:
            data to encode
        """
        return pair in self.encoder.classes_
