import numpy as np
from typing import List


class PredictionData:
    def __init__(self, car_body_type: str, voltage_program_type: str):
        self.car_body_type = car_body_type
        self.voltage_program_type = voltage_program_type


class NestedPredictionData(PredictionData):
    """
    This class stores the data for each bus needed to query the prediction model.
    It also facilitates iteration over the data elements required for prediction
    (each bus has its own separate data set passed to the model)

    Attributes
    ----------
    painting_process_data : numpy array
        Metadata for each bus on which model compute decision/result.
    car_body_type : str
        Car body type if a dedicated model exists, otherwise the name of the general model.
    voltage_program_type
        Voltage program type if a dedicated model exists, otherwise the name of the general model.
    """

    def __init__(self, painting_process_data: List[List], car_body_type: str, voltage_program_type: str):
        super().__init__(car_body_type=car_body_type, voltage_program_type=voltage_program_type)
        self.painting_process_data = np.array(painting_process_data)

    def __iter__(self):
        for single_bus_painting_process_data in self.painting_process_data:
            yield SingleBusPredictionData(
                painting_process_data=single_bus_painting_process_data,
                car_body_type=self.car_body_type,
                voltage_program_type=self.voltage_program_type
            )


class SingleBusPredictionData(PredictionData):
    """
    This class stores the data for single bus needed to query the prediction model.

    Attributes
    ----------
    painting_process_data : numpy array
        Metadata for single bus on which model compute decision/result.
    car_body_type : str
        Car body type if a dedicated model exists, otherwise the name of the general model.
    voltage_program_type
        Voltage program type if a dedicated model exists, otherwise the name of the general model.
    """

    def __init__(self, painting_process_data: np.ndarray, car_body_type: str, voltage_program_type: str):
        super().__init__(car_body_type=car_body_type, voltage_program_type=voltage_program_type)
        self.painting_process_data = np.array(painting_process_data).astype(np.float)

    @property
    def encoding_pair(self) -> str:
        """
        Return concatenated pair.
        """
        return self.car_body_type + self.voltage_program_type
