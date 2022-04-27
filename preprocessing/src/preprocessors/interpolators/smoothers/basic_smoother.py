from abc import abstractmethod
from numpy import ndarray

from src.preprocessors.interpolators.smoothers.basic_smoother_config import BasicSmootherConfig


class BasicSmoother:
    def __init__(self, smoother_config: BasicSmootherConfig):
        self.smoother_config = smoother_config

    @abstractmethod
    def smooth_out(self, data: ndarray) -> ndarray:
        pass
