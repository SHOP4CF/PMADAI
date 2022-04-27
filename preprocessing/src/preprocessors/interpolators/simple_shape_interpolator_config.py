from src.preprocessors.interpolators.shape_interpolator_config import ShapeInterpolatorConfig


class SimpleShapeInterpolatorConfig(ShapeInterpolatorConfig):
    def __init__(self, no_interp_points, bnd: dict, padding_val: int):
        """

        Parameters
        ----------
        no_interp_points
            Dictionary containing number of points in which current waveforms will be interpolated by ShapeInterpolator
        bnd
            Boundaries describing min and max length of current waveforms on each of the buses. Depending on the length
            we'll want to right-pad the shape or trim it
        padding_val
            The value which will be used to right-pad current waveforms
        """
        super().__init__(no_interp_points=no_interp_points)
        self.bnd = bnd if bnd else {
            "K1": (30, 150),
            "K2": (50, 170),
            "K3": (50, 170),
            "K4": (50, 150)
        }
        self.padding_val = padding_val

    @classmethod
    def equal_number_of_interpolation_points(cls, no_interp_points, bnd: dict = None, padding_val: int = 10):
        no_interp_points_dict = {
            "K1": no_interp_points,
            "K2": no_interp_points,
            "K3": no_interp_points,
            "K4": no_interp_points
        }
        return cls(
            no_interp_points=no_interp_points_dict,
            bnd=bnd,
            padding_val=padding_val
        )

    @classmethod
    def specific_dictionary_of_interpolation_points(cls, no_interp_points, bnd: dict = None, padding_val: int = 10):
        return cls(
            no_interp_points=no_interp_points,
            bnd=bnd,
            padding_val=padding_val
        )