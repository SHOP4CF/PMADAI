import abc
from typing import Mapping, List, Tuple

import numpy as np
from scipy.interpolate import interp1d

from src.domain.metadata import Metadata
from src.domain.waveform import Waveform
from src.preprocessors.interpolators.shape_interpolator_config import ShapeInterpolatorConfig


class ShapeInterpolator:
    """
    The main purpose of this class is to interpolate extracted shapes. Subclasses should implement the 'interpolate'
     method.

    """

    def __init__(self, config: ShapeInterpolatorConfig):
        self.config = config

    @abc.abstractmethod
    def interpolate(self, bus_to_extracted_waveform: Mapping[str, Waveform], metadata: Metadata) -> List:
        """
        The method interpolates extracted shapes. The shapes are provided in the `bus_to_extracted_waveform` dictionary.

        Parameters
        ----------
        bus_to_extracted_waveform
            Dictionary of string->waveform. The string is one of "K1", "K2", "K3", "K4".
        metadata
            Metadata describing extracted shapes.
        Returns
        -------
        List of interpolated shapes on each bus.
        """
        pass

    @staticmethod
    def interpolate_simple(shape: np.ndarray, no_interp_points: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Simple interpolation function which doesn't take into account changing probing frequency. Just accepts nummpy array
        and implicitly assumes that probing frequency is constant across all observations.

        Parameters
        ----------
        shape
            current waveform single curve
        no_interp_points
            number of points tu perform interpolation for

        Returns
        -------
        Tuple
            Tuple: new x and y values in a form of numpy arrays.
        """
        if type(shape) != np.ndarray:
            raise TypeError
        f = interp1d(np.arange(shape.size), shape)
        xnew = np.linspace(0, shape.size - 1, no_interp_points)
        ynew = f(xnew)
        return xnew, ynew
