class ShapeInterpolatorConfig:
    """
    Base configuration class for the shape interpolator
    """

    def __init__(self, no_interp_points):
        """

        Parameters
        ----------
        no_interp_points
            Dictionary containing number of points in which current waveforms will be interpolated by ShapeInterpolator
        """
        self.no_interp_points = no_interp_points
