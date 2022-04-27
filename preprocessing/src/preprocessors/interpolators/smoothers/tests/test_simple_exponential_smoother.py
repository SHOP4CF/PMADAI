import numpy as np

from src.preprocessors.interpolators.smoothers.simple_exponential_smoother import SimpleExponentialSmoother
from src.preprocessors.interpolators.smoothers.simple_exponential_smoother_config import SimpleExponentialSmootherConfig


def test_simple_exponential_smoother():
    data = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    smoother_config = SimpleExponentialSmootherConfig()
    smoother_config.smoothing_level = 0.0

    smoother = SimpleExponentialSmoother(smoother_config)
    results = smoother.smooth_out(data)

    # smoothing level equals 0 so results should be an average of input array.
    expected_results = np.array([np.mean(data)] * data.shape[0])

    assert (results == expected_results).all()
    assert results.shape == data.shape
