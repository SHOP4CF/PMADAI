from enum import Enum
from typing import Mapping
import numpy as np
import pandas as pd
from src.domain.waveform import Waveform


class PreprocessingStatus(Enum):
    """
    The processing ends with one of the 4 statuses:\n
    - CORRECT -> The preprocessing  was completed without problems
    - CAGE -> Some of the data considers painting of so called 'cages'. Those shapes should be treated separately because they are inherently different from rest of the data.
    - GAP_IN_READINGS -> There was a gap in readings on any of the buses. There is no data to apply preprocessing to.
    - BAD_EXTRACTION -> The preprocessing could not be completed from unpredictable reasons.
    """
    CORRECT = "CORRECT"
    CAGE = "CAGE"
    GAP_IN_READINGS = "GAP_IN_READINGS"
    BAD_EXTRACTION = "BAD_EXTRACTION"


class RawData:
    """
    A class containing data which was extracted by waveform extractor from each bus.
    """
    def __init__(self, waveforms: Mapping[str, Waveform] = None):
        self.values, self.times, self.max_values, self.min_values, self.max_times, self.min_times = {}, {}, {}, {}, {}, {}
        if waveforms:  # Waveforms is optional: in case a shape is filtered, we don't do waveform extraction
            self.values = {k: list(w.values) for k, w in waveforms.items()}
            self.times = {k: list(pd.to_datetime(w.timestamps).strftime('%Y-%m-%d %H:%M:%S')) for k, w in waveforms.items()}
            for k, w in waveforms.items():
                if w.values.size:  # values may be empty, looking for max inside such array is nonsense and gives error
                    self.max_values[k] = float(max(w.values))
                    self.min_values[k] = float(min(w.values))
                    self.max_times[k] = self.np_dt64_to_str(w.timestamps[np.argmax(w.values)])
                    self.min_times[k] = self.np_dt64_to_str(w.timestamps[np.argmin(w.values)])

    def to_dict(self):
        return {
            "values": self.values,
            "times": self.times,
            "maxValues": self.max_values,
            "minValues": self.min_values,
            "maxTimes": self.max_times,
            "minTimes": self.min_times
        }

    @staticmethod
    def np_dt64_to_str(np_dt):
        return pd.to_datetime(str(np_dt)).strftime('%Y-%m-%d %H:%M:%S')


class PreprocessingPayload:
    """
    Features extracted from the payload about the painting: \n
    - metadata
    - histograms
    - tsfresh_features
    - custom_features
    - interpolation_features
    """
    def __init__(self, metadata, histograms=None, tsfresh_features=None, custom_features=None, interpolation_features=None):
        self.metadata = metadata
        self.histograms = histograms
        self.tsfresh_features = tsfresh_features
        self.custom_features = custom_features
        self.interpolation_features = interpolation_features

    def to_dict(self):
        return {
            "metadata": self.metadata.to_dict(),
            "histograms": self.histograms if self.histograms else [],
            "tsfreshFeatures": self.tsfresh_features if self.tsfresh_features else [],
            "customFeatures": self.custom_features if self.custom_features else [],
            "interpolationFeatures": self.interpolation_features if self.interpolation_features else [],
        }


class PreprocessingResult:
    """
    A class which represents the preprocessing result. The preprocessing results is comprised of:\n
    - status - a preprocessing status assigned to the preprocessing process performed over the data
    - payload - a preprocessing payload, i.e. the actual result of preprocessor applied on data
    - raw_data - raw data to which the preprocessing was applied
    """
    def __init__(self, preprocessing_status: PreprocessingStatus, payload: PreprocessingPayload, raw_data: RawData):
        self.status: PreprocessingStatus = preprocessing_status
        self.payload: PreprocessingPayload = payload
        self.raw_data: RawData = raw_data

    def to_dict(self) -> dict:
        result = {
            "status": self.status.value,
            "payload": self.payload.to_dict(),
            "rawData": self.raw_data.to_dict()
        }
        return result


