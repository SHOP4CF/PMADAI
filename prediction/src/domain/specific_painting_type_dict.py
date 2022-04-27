from collections import defaultdict
import logging


class SpecificPaintingTypeKey:
    """
    This class is used as the key to the dictionary. Allows you to maintain a consistent and legible way of building the key.

    """
    def __init__(self, model_type: str, car_body_type: str, voltage_program_type: str, source: str = 'models'):
        """
        Parameters
        ----------
        model_type
            The type of model used.
         car_body_type
            Car body type.
        voltage_program_type
             Voltage program type.
        source : default 'models'
            The source of data. In particular to choose from "models" and "features".
        """
        self.model_type = model_type.capitalize()
        self.car_body_type = car_body_type.upper()
        self.voltage_program_type = voltage_program_type.upper()
        self.source = source

    def __hash__(self):
        """
        Hash method which allows you to create a key based on selected attributes.

        Returns
        -------
            Hashed class based on selected attributes.
        """
        return hash((self.model_type, self.car_body_type, self.voltage_program_type))

    def __eq__(self, other):
        """
        Method used to compare keys.
        """
        return (self.model_type, self.car_body_type, self.voltage_program_type) == (
            other.model_type, other.car_body_type, other.voltage_program_type)

    def __ne__(self, other):
        """
        Method used to compare keys.
        """
        return not (self == other)

    def __str__(self):
        """
        String representation od class.
        """
        return f'{self.model_type}&{self.car_body_type}&{self.voltage_program_type}'

    def __repr__(self):
        return self.__str__()


class GeneralModelsDict(defaultdict):
    """
    This class inherits from 'defaultdict'. It allows to store multiple models and retrieve them by key.
    The main idea behind the class is to return the model that matches the given key, but if the key is not in the
    dictionary, it returns a general-purpose model. This allows you to easily get models without worrying about
    whether they are in the dictionary.
    Main key of dictionary is "SpecificPaintingTypeKey" class.
    """
    def __init__(self, general_type):
        """
        Parameters
        ----------
        general_type
            The name on the basis of which the general-purpose model is saved.
        """
        super().__init__(None)
        self.general_type = general_type

    def __missing__(self, key: SpecificPaintingTypeKey):
        """
        If key is missing (not in dictionary), the general-purpose model is returned.

        Parameters
        ----------
        key : SpecificPaintingTypeKey
            The missing key from which an attempt was made to provide the dictionary value and from which
            the general-purpose model is retrieved.

        Returns
        -------
            general-purpose model.
        """
        logging.info(
            f'Received unsupported painting types: {key.car_body_type}, {key.voltage_program_type}. Using general model.')
        general_key = SpecificPaintingTypeKey(
            model_type=key.model_type,
            car_body_type=self.general_type,
            voltage_program_type=self.general_type)

        return super(defaultdict, self).__getitem__(general_key)
