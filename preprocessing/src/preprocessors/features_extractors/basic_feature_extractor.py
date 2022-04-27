from typing import List, Mapping
from abc import abstractmethod

from src.domain.waveform import Waveform
from src.preprocessors.features_extractors.basic_feature_extractor_config import BasicFeatureConfig


class BasicFeatureExtractor:
    def __init__(self, config: BasicFeatureConfig):
        self.config = config

    @abstractmethod
    def extract_features(self, bus_to_extracted_waveform: Mapping[str, Waveform]) -> List:
        pass
