from datetime import datetime
from typing import Mapping, List

from src.domain.metadata import Metadata
from src.preprocessors.interpolators.shape_interpolator import ShapeInterpolator
from src.preprocessors.interpolators.time_aware_shape_interpolator_config import TimeAwareShapeInterpolatorConfig
from src.preprocessors.interpolators.smoothers.basic_smoother import BasicSmoother
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


class TimeAwareShapeInterpolator(ShapeInterpolator):
    def __init__(self, config: TimeAwareShapeInterpolatorConfig, smoother: BasicSmoother):
        super().__init__(config=config)
        self.config = config
        self.smoother = smoother

    def interpolate(self, bus_to_extracted_waveform: Mapping, metadata: Metadata) -> List:
        """
        Time-aware shape interpolation. Fills the gaps from left, right and in the middle, because is aware of proper
        time bounds of each waveform. Should be used only in combination with TimeBasedPreprocessor.

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

        dt = datetime.strptime(metadata.time_of_event, "%Y-%m-%d %H:%M:%S.%f")
        ktl_entry_time = np.datetime64(dt)

        for bus in self.config.shifts:
            # Cut to fit within bounds if necessary
            w = bus_to_extracted_waveform[bus]

            cutoff_start = ktl_entry_time + self.config.shifts[bus][0]
            cutoff_end = ktl_entry_time + self.config.shifts[bus][1]

            expanded_vals = np.append(np.insert(w.values, 0, w.values[0]), [w.values[-1]])
            expanded_timestamps = np.append(np.insert(w.timestamps, 0, cutoff_start), [cutoff_end])
            ts = pd.Series(expanded_vals, index=expanded_timestamps)

            # First interpolation (with a specified frequency of 1s, to fill all the gaps)
            beg = ts.index[0]
            end = ts.index[-1]
            xnew = pd.date_range(beg, end, freq='1s')
            f = interp1d(ts.index.view(int), ts.values, kind='previous')
            ynew = f(xnew.view(int))

            if self.smoother:
                data_for_smoothing = pd.Series(ynew, xnew)
                smoothed_data = self.smoother.smooth_out(data_for_smoothing)
                xnew, ynew = smoothed_data.index, smoothed_data.values

            # Second interpolation (with a specified number of interpolation points), performed evenly on filled signal
            interpolated = self.interpolate_simple(ynew, self.config.no_interp_points[bus])[1]
            interpolated_row.append(interpolated.tolist())
        return interpolated_row
