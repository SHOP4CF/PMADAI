from src.domain.waveform import Waveform
from src.preprocessors.histograms_calculators.histograms_calculator import HistogramsCalculator, HistogramsCalculatorConfig
import numpy as np


def test_histograms_calculator():
    bus_to_extracted_waveforms = {
        "K1": Waveform("K1", np.array([0.1, 1.1, 2.1, 3.1, 4.1]), []),  # should be 0.2, 0.2, 0.2, 0.2, 0.2
        "K2": Waveform("K2", np.array([1, 2, 3, 4, 5]), []),  # should 0, 0.2, 0.2, 0.2, 0.4
        "K3": Waveform("K3", np.array([0.5]), []),  # should be 1, 0, 0, 0, 0
        "K4": Waveform("K4", np.array([0.5, 1]), []),  # should be 0.5, 0.5, 0, 0, 0
    }

    hist_calc_config = HistogramsCalculatorConfig(bins_no={
            "K1": 5,
            "K2": 5,
            "K3": 5,
            "K4": 5
        }, bus_to_min_max = {
            "K1": (0, 5),
            "K2": (0, 5),
            "K3": (0, 5),
            "K4": (0, 5)
        })

    histogram_features = HistogramsCalculator(hist_calc_config)\
        .calculate_histograms(bus_to_extracted_waveforms)

    expected_histograms = [
        [0.2, 0.2, 0.2, 0.2, 0.2],
        [0.0, 0.2, 0.2, 0.2, 0.4],
        [1.0, 0.0, 0.0, 0.0, 0.0],
        [0.5, 0.5, 0.0, 0.0, 0.0]
    ]

    assert np.allclose(np.array(expected_histograms), np.array(histogram_features))
