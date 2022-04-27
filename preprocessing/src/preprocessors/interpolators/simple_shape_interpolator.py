from typing import Mapping, List

from src.domain.metadata import Metadata
from src.preprocessors.interpolators.shape_interpolator import ShapeInterpolator
from src.preprocessors.interpolators.simple_shape_interpolator_config import SimpleShapeInterpolatorConfig
import numpy as np

class SimpleShapeInterpolator(ShapeInterpolator):
    def __init__(self, config: SimpleShapeInterpolatorConfig):
        super().__init__(config)
        self.config = config

    def interpolate(self, bus_to_extracted_waveform: Mapping, metadata: Metadata) -> List:
        """
        Interpolates waveforms, cuts them if they are too long and right-pad them if they're too short.

        Parameters
        ----------
        bus_to_extracted_waveform
            Dictionary with extracted waveforms on each bus.
        metadata
            Metadata associated with the shapes.
        Returns
        -------
        List of interpolated shapes on each bus.
        """
        interpolated_row = []
        for k in self.config.bnd:
            # Cut to fit within bounds if necessary
            w = bus_to_extracted_waveform[k]
            lower_bound, upper_bound = self.config.bnd[k]
            w_values_tmp = w.values
            if len(w_values_tmp) > upper_bound:
                w_values_tmp = w.values[:upper_bound]

            # Add padding
            interpolated_values = np.pad(w_values_tmp,
                              (0, upper_bound - w_values_tmp.size),
                              'constant',
                              constant_values=(self.config.padding_val, self.config.padding_val))

            # Interpolate simple
            interpolated = self.interpolate_simple(interpolated_values, self.config.no_interp_points[k])[1]
            interpolated_row.append(interpolated.tolist())
        return interpolated_row