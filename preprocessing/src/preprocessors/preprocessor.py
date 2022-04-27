import abc
import logging
from typing import Mapping

from src.domain.metadata import Metadata
from src.domain.preprocessing_result import PreprocessingResult, PreprocessingPayload
from src.domain.waveform import Waveform
from src.preprocessors.histograms_calculators.histograms_calculator import HistogramsCalculatorConfig, \
    HistogramsCalculator
from src.preprocessors.interpolators.time_aware_shape_interpolator import TimeAwareShapeInterpolator
from src.preprocessors.interpolators.time_aware_shape_interpolator_config import TimeAwareShapeInterpolatorConfig
from src.preprocessors.features_extractors.tsfresh_feature_extractor import TsfreshFeatureExtractor, TsfreshConfig
from src.preprocessors.interpolators.smoothers.simple_exponential_smoother import SimpleExponentialSmoother
from src.preprocessors.interpolators.smoothers.simple_exponential_smoother_config import SimpleExponentialSmootherConfig
from src.config_reader import config


class Preprocessor:
    """
    Preprocessor class: takes metadata and trends associated with a painting and preprocesses it.
    Features needed for prediction are additionally calculated after performing the preprocessing of data.
    """
    @abc.abstractmethod
    def preprocess(self, metadata: Metadata, trends: Mapping) -> PreprocessingResult:
        pass

    def construct_payload(self, metadata: Metadata,
                          bus_to_extracted_waveform: Mapping[str, Waveform]) -> PreprocessingPayload:
        """
        Constructs PreprocessingPayload from preprocessed data.
        Parameters
        ----------
        metadata
            Metadata which describes a painting.
        bus_to_extracted_waveform
            Dictionary with extracted waveforms.

        Returns
        -------
        PreprocessingPayload
            PreprocessingPayload with prediction features.
        """
        logging.info("Interpolating shapes.")
        interpolator_config = TimeAwareShapeInterpolatorConfig.equal_number_of_interpolation_points(
            no_interp_points=config['general']['interpolation-points'])
        smoother = self.get_smoother_if_required()
        interpolator = TimeAwareShapeInterpolator(interpolator_config, smoother=smoother)
        interpolation_features = interpolator.interpolate(bus_to_extracted_waveform, metadata)
        logging.info("Calculating histograms.")
        histogram_features = HistogramsCalculator(HistogramsCalculatorConfig()).calculate_histograms(
            bus_to_extracted_waveform)
        logging.info("Calculating tsfresh features.")
        tsfresh_features = TsfreshFeatureExtractor(TsfreshConfig()).extract_features(bus_to_extracted_waveform)
        custom_features = []
        return PreprocessingPayload(metadata,
                                    histogram_features,
                                    tsfresh_features,
                                    custom_features,
                                    interpolation_features)

    @staticmethod
    def get_smoother_if_required():
        smoother = None
        if config['general']['smoother'] == 'SimpleExponentialSmoothing':
            smoother = SimpleExponentialSmoother(SimpleExponentialSmootherConfig())
        return smoother
