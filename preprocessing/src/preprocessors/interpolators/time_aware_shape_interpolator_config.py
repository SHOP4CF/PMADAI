import numpy as np

from src.preprocessors.interpolators.shape_interpolator_config import ShapeInterpolatorConfig


class TimeAwareShapeInterpolatorConfig(ShapeInterpolatorConfig):
    def __init__(self, no_interp_points, shifts):
        super().__init__(no_interp_points=no_interp_points)
        self.shifts = shifts if shifts else {
            "K1": (np.timedelta64(5, 's'), np.timedelta64(2 * 60 + 46, 's')),
            "K2": (np.timedelta64(2 * 60 + 29, 's'), np.timedelta64(5 * 60 + 5, 's')),
            "K3": (np.timedelta64(4 * 60 + 46, 's'), np.timedelta64(7 * 60 + 30, 's')),
            "K4": (np.timedelta64(6 * 60 + 52, 's'), np.timedelta64(9 * 60 + 18, 's'))
        }

    @classmethod
    def equal_number_of_interpolation_points(cls, no_interp_points, shifts=None):
        no_interp_points_dict = {
            "K1": no_interp_points,
            "K2": no_interp_points,
            "K3": no_interp_points,
            "K4": no_interp_points
        }
        return cls(
            no_interp_points=no_interp_points_dict,
            shifts=shifts
        )

    @classmethod
    def specific_dictionary_of_interpolation_points(cls, no_interp_points, shifts=None):
        return cls(
            no_interp_points=no_interp_points,
            shifts=shifts
        )
