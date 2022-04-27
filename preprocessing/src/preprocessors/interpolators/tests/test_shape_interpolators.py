from datetime import datetime

import numpy as np

from src.domain.metadata import Metadata
from src.domain.waveform import Waveform
from src.preprocessors.interpolators.simple_shape_interpolator import SimpleShapeInterpolator
from src.preprocessors.interpolators.simple_shape_interpolator_config import SimpleShapeInterpolatorConfig
from src.preprocessors.interpolators.time_aware_shape_interpolator import TimeAwareShapeInterpolator
from src.preprocessors.interpolators.time_aware_shape_interpolator_config import TimeAwareShapeInterpolatorConfig


def test_simple_shape_interpolator():
    interp_config = SimpleShapeInterpolatorConfig(
        no_interp_points={"K1": 4, "K2": 4, "K3": 4, "K4": 4},
        bnd={"K1": (0, 4), "K2": (0, 4), "K3": (0, 4), "K4": (0, 4)},
        padding_val=10
    )

    interpolator = SimpleShapeInterpolator(interp_config)

    bus_to_extracted_waveforms = {
        "K1": Waveform("K1", np.array([1, 2, 3, 4]), []),  # should be left as is
        "K2": Waveform("K2", np.array([1, 2]), []),  # should be right-padded with `padding_val`
        "K3": Waveform("K3", np.array([1, 2, 3]), []),  # should be right-padded with `padding_val`
        "K4": Waveform("K4", np.array([1, 1, 1, 1, 1]), []),  # should be cut from right to contain only 4 values
    }

    metadata = Metadata({
        'timeOfEvent': None, 'inOut': None, 'carBodyId': None, 'carBodyType': None, 'voltageProgramType': None,
        'skidId': None, 'pendulumId': None, 'paintingCyclesCount': None, 'servicesCount': None
    })

    interpolated = interpolator.interpolate(bus_to_extracted_waveforms, metadata)

    expected_interpolated = [
        [1, 2, 3, 4],
        [1, 2, 10, 10],
        [1, 2, 3, 10],
        [1, 1, 1, 1]
    ]
    assert np.allclose(np.array(interpolated), np.array(expected_interpolated))


def test_time_aware_shape_interpolator():
    interp_config = TimeAwareShapeInterpolatorConfig(
        no_interp_points={"K1": 4, "K2": 4, "K3": 4, "K4": 4},
        shifts={"K1": (np.timedelta64(1, 's'), np.timedelta64(4, 's')),
                "K2": (np.timedelta64(2, 's'), np.timedelta64(5, 's')),
                "K3": (np.timedelta64(3, 's'), np.timedelta64(6, 's')),
                "K4": (np.timedelta64(4, 's'), np.timedelta64(7, 's'))},
    )

    interpolator = TimeAwareShapeInterpolator(interp_config, smoother=None)

    def s_to_dt(s):
        dformat = "%Y-%m-%d %H:%M:%S.%f"
        return np.datetime64(datetime.strptime(f'2020-01-01 00:00:0{s}.00000', dformat))

    bus_to_extracted_waveforms = {
        "K1": Waveform("K1", np.array([1, 2, 3, 4]),  # should be left as is
                       [s_to_dt(1), s_to_dt(2), s_to_dt(3), s_to_dt(4)]),
        "K2": Waveform("K2", np.array([1, 2]),  # should be right-padded with 2
                       [s_to_dt(2), s_to_dt(3)]),
        "K3": Waveform("K3", np.array([1, 2, 3]),  # should be lef-padded with 1
                       [s_to_dt(4), s_to_dt(5), s_to_dt(6)]),
        "K4": Waveform("K4", np.array([1, 2, 3]),  # should be filled by 'previous' values when missing
                       [s_to_dt(4), s_to_dt(6),s_to_dt(7)]),
    }

    metadata = Metadata({
        'timeOfEvent': '2020-01-01 00:00:00.00000', 'inOut': None, 'carBodyId': None, 'carBodyType': None, 'voltageProgramType': None,
        'skidId': None, 'pendulumId': None, 'paintingCyclesCount': None, 'servicesCount': None
    })

    interpolated = interpolator.interpolate(bus_to_extracted_waveforms, metadata)

    expected_interpolated = [
        [1, 2, 3, 4],
        [1, 2, 2, 2],
        [1, 1, 2, 3],
        [1, 1, 2, 3]
    ]
    assert np.allclose(np.array(interpolated), np.array(expected_interpolated))