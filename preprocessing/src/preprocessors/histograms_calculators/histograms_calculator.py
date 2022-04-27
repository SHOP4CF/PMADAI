from typing import List, Mapping

import numpy as np

from src.domain.waveform import Waveform
from src.preprocessors.histograms_calculators.histograms_calculator_config import HistogramsCalculatorConfig


class HistogramsCalculator:
    def __init__(self, config: HistogramsCalculatorConfig):
        self.config = config

    def calculate_histograms(self, bus_to_extracted_waveform: Mapping[str, Waveform]) -> List:
        """
        Calculates a histogram for each shape in the `bus_to_extracted_waveform` dict.

        Parameters
        ----------
        bus_to_extracted_waveform
            Dictionary with extracted waveforms on each bus.

        Returns
        -------
        result
            List of lists. In each list there are values of the histogram calculated per shape with the np.histogram function.
        """
        result = []
        for bus in [f"K{i}" for i in range(1, 5)]:
            w = bus_to_extracted_waveform[bus]
            h = np.histogram(w.values, bins=self.config.bins_no[bus], range=self.config.bus_to_min_max[bus], density=True)[0]
            result.append(h.tolist())
        return result