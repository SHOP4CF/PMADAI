from src.preprocessors.features_extractors.basic_feature_extractor_config import BasicFeatureConfig


class TsfreshConfig(BasicFeatureConfig):
    def __init__(self):
        super(TsfreshConfig, self).__init__()
        self.settings = {
            "mean": None,
            "standard_deviation": None,
            "minimum": None,
            "maximum": None,
            "kurtosis": None,
            "large_standard_deviation": [{"r": 0.05}, {"r": 0.1}],
            "sum_values": None,
            "abs_energy": None,
            "cid_ce": [{"normalize": False}, {"normalize": True}],
            "mean_abs_change": None,
            "mean_change": None,
            "mean_second_derivative_central": None,
            "skewness": None,
            "median": None,
            "longest_strike_below_mean": None,
            "longest_strike_above_mean": None,
            "fft_coefficient": [{"coeff": 1, "attr": "real"}],
            "fft_aggregated": [{"aggtype": "centroid"}, {"aggtype": "variance"}, {"aggtype": "skew"}],
            "number_peaks": [{"n": 10}],
            "benford_correlation": None,
            "fourier_entropy": [{"bins": 30}],
            "sample_entropy": None
        }