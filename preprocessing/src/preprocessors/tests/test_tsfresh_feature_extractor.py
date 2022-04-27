import numpy as np

from src.domain.waveform import Waveform
from src.preprocessors.features_extractors.tsfresh_feature_extractor import TsfreshFeatureExtractor, TsfreshConfig
from datetime import datetime


def test_tsfresh_feature_extractor_response_shape_ok():
    # Change in shape would require changes in the rest of the pipeline. Therefore we should prioritize checking shape.

    def s_to_dt(s):
        dformat = "%Y-%m-%d %H:%M:%S.%f"
        return np.datetime64(datetime.strptime(f'2020-01-01 00:00:0{s}.00000', dformat))

    bus_to_extracted_waveforms = {
        "K1": Waveform("K1", np.array([1, 2, 3, 4]), [s_to_dt(1), s_to_dt(2), s_to_dt(3), s_to_dt(4)]),
        "K2": Waveform("K2", np.array([1, 2]), [s_to_dt(2), s_to_dt(3)]),
        "K3": Waveform("K3", np.array([1, 2, 3]), [s_to_dt(4), s_to_dt(5), s_to_dt(6)]),
        "K4": Waveform("K4", np.array([1, 2, 3]), [s_to_dt(4), s_to_dt(6), s_to_dt(7)]),
    }

    tsfresh_features = TsfreshFeatureExtractor(TsfreshConfig()).extract_features(bus_to_extracted_waveforms)

    assert len(tsfresh_features) == 4
    assert all(len(bus_features) == 26 for bus_features in tsfresh_features)