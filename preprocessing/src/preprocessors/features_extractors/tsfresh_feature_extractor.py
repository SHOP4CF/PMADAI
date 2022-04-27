from typing import List, Mapping

import pandas as pd
from tsfresh import extract_features

from src.domain.waveform import Waveform
from src.preprocessors.features_extractors.tsfresh_feature_extractor_config import TsfreshConfig
from src.preprocessors.features_extractors.basic_feature_extractor import BasicFeatureExtractor


class TsfreshFeatureExtractor(BasicFeatureExtractor):
    """
    Feature extraction with the use of `tsfresh` library.
    """

    def __init__(self, config: TsfreshConfig):
        super(TsfreshFeatureExtractor, self).__init__(config=config)

    def extract_features(self, bus_to_extracted_waveform: Mapping[str, Waveform]) -> List:
        result = []

        for bus, waveform in bus_to_extracted_waveform.items():
            tsfresh_input = {
                "id": [0] * waveform.values.size,
                "time": list(waveform.timestamps),
                f"{bus}_value": list(waveform.values)
            }

            in_df = pd.DataFrame.from_dict(tsfresh_input)

            # Extract features using tsfresh
            extracted_features = extract_features(in_df,
                                                  column_id="id",
                                                  column_sort="time",
                                                  default_fc_parameters=self.config.settings,
                                                  disable_progressbar=True)

            result.append(extracted_features.to_numpy().tolist()[0])
        return result
